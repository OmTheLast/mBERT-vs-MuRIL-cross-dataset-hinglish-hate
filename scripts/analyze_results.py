#!/usr/bin/env python3
"""Analyze saved model results for paper-facing interpretation."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
OUT = RESULTS / "result_analysis"
DOC = ROOT / "docs" / "result_analysis_report.md"

PRIMARY_DATASETS = ["kaggle_hinglish_hate", "cm_splits_codemixed", "thar_religion"]
DIAGNOSTIC_DATASETS = ["existing_79_row_benchmark"]

DATASET_LABELS = {
    "kaggle_hinglish_hate": "Kaggle Hinglish Hate",
    "cm_splits_codemixed": "CM Code-Mixed Offensive",
    "thar_religion": "THAR Religious Hate",
    "existing_79_row_benchmark": "79-row diagnostic probe",
}

MODEL_LABELS = {
    "mbert": "mBERT",
    "muril": "MuRIL",
    "tfidf_logistic_regression": "TF-IDF Logistic Regression",
    "tfidf_linear_svm": "TF-IDF Linear SVM",
}


def pct(value: float) -> str:
    return f"{value * 100:.1f}%"


def md_table(frame: pd.DataFrame, columns: list[str]) -> str:
    visible = frame[columns].copy()
    for col in visible.columns:
        if col in {
            "accuracy",
            "precision_positive",
            "recall_positive",
            "f1_positive",
            "f1_macro",
            "precision_macro",
            "recall_macro",
            "macro_f1_gap",
            "positive_f1_gap",
            "positive_recall_gap",
            "matched_f1_macro",
            "test_f1_macro",
            "generalization_gap",
            "transformer_f1_macro",
            "baseline_f1_macro",
            "transformer_minus_baseline",
        }:
            visible[col] = visible[col].map(lambda value: pct(float(value)))
        elif pd.api.types.is_float_dtype(visible[col]):
            visible[col] = visible[col].map(lambda value: f"{float(value):.3f}")
    return visible.to_markdown(index=False)


def write_csv(frame: pd.DataFrame, name: str) -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / name
    frame.to_csv(path, index=False)
    return path


def primary(frame: pd.DataFrame) -> pd.DataFrame:
    return frame[frame["test_dataset"].isin(PRIMARY_DATASETS)].copy()


def matched_rows(frame: pd.DataFrame) -> pd.DataFrame:
    return frame[(frame["train_dataset"] == frame["test_dataset"]) & frame["test_dataset"].isin(PRIMARY_DATASETS)].copy()


def pairwise_transformer_gaps(transformer: pd.DataFrame) -> pd.DataFrame:
    rows = []
    usable = primary(transformer)
    for train_dataset in PRIMARY_DATASETS:
        for test_dataset in PRIMARY_DATASETS:
            pair = usable[(usable["train_dataset"] == train_dataset) & (usable["test_dataset"] == test_dataset)]
            if set(pair["model"]) != {"mbert", "muril"}:
                continue
            mbert = pair[pair["model"] == "mbert"].iloc[0]
            muril = pair[pair["model"] == "muril"].iloc[0]
            rows.append(
                {
                    "train_dataset": train_dataset,
                    "test_dataset": test_dataset,
                    "winner_by_macro_f1": "mbert" if mbert["f1_macro"] > muril["f1_macro"] else "muril",
                    "macro_f1_gap": abs(mbert["f1_macro"] - muril["f1_macro"]),
                    "winner_by_positive_f1": "mbert" if mbert["f1_positive"] > muril["f1_positive"] else "muril",
                    "positive_f1_gap": abs(mbert["f1_positive"] - muril["f1_positive"]),
                    "winner_by_positive_recall": "mbert" if mbert["recall_positive"] > muril["recall_positive"] else "muril",
                    "positive_recall_gap": abs(mbert["recall_positive"] - muril["recall_positive"]),
                    "mbert_macro_f1": mbert["f1_macro"],
                    "muril_macro_f1": muril["f1_macro"],
                    "mbert_positive_f1": mbert["f1_positive"],
                    "muril_positive_f1": muril["f1_positive"],
                    "mbert_positive_recall": mbert["recall_positive"],
                    "muril_positive_recall": muril["recall_positive"],
                }
            )
    return pd.DataFrame(rows)


def best_by_test(transformer: pd.DataFrame) -> pd.DataFrame:
    usable = primary(transformer)
    best = (
        usable.sort_values(["test_dataset", "f1_macro"], ascending=[True, False])
        .groupby("test_dataset", as_index=False)
        .head(1)
        .copy()
    )
    return best[
        [
            "test_dataset",
            "model",
            "train_dataset",
            "accuracy",
            "recall_positive",
            "f1_positive",
            "f1_macro",
            "tn",
            "fp",
            "fn",
            "tp",
        ]
    ]


def generalization_gaps(transformer: pd.DataFrame) -> pd.DataFrame:
    rows = []
    usable = primary(transformer)
    for _, row in usable.iterrows():
        matched = usable[
            (usable["model"] == row["model"])
            & (usable["train_dataset"] == row["train_dataset"])
            & (usable["test_dataset"] == row["train_dataset"])
        ]
        if matched.empty:
            continue
        matched_macro = matched.iloc[0]["f1_macro"]
        rows.append(
            {
                "model": row["model"],
                "train_dataset": row["train_dataset"],
                "test_dataset": row["test_dataset"],
                "matched_f1_macro": matched_macro,
                "test_f1_macro": row["f1_macro"],
                "generalization_gap": matched_macro - row["f1_macro"],
                "recall_positive": row["recall_positive"],
                "f1_positive": row["f1_positive"],
            }
        )
    return pd.DataFrame(rows)


def best_baseline_vs_transformer(baseline: pd.DataFrame, transformer: pd.DataFrame) -> pd.DataFrame:
    base_primary = primary(baseline)
    trans_primary = primary(transformer)
    best_base = (
        base_primary.sort_values(["train_dataset", "test_dataset", "f1_macro"], ascending=[True, True, False])
        .groupby(["train_dataset", "test_dataset"], as_index=False)
        .head(1)
    )
    best_trans = (
        trans_primary.sort_values(["train_dataset", "test_dataset", "f1_macro"], ascending=[True, True, False])
        .groupby(["train_dataset", "test_dataset"], as_index=False)
        .head(1)
    )
    rows = []
    for _, trans in best_trans.iterrows():
        base = best_base[(best_base["train_dataset"] == trans["train_dataset"]) & (best_base["test_dataset"] == trans["test_dataset"])]
        if base.empty:
            continue
        base = base.iloc[0]
        rows.append(
            {
                "train_dataset": trans["train_dataset"],
                "test_dataset": trans["test_dataset"],
                "best_transformer": trans["model"],
                "transformer_f1_macro": trans["f1_macro"],
                "best_baseline": base["model"],
                "baseline_f1_macro": base["f1_macro"],
                "transformer_minus_baseline": trans["f1_macro"] - base["f1_macro"],
                "transformer_recall_positive": trans["recall_positive"],
                "baseline_recall_positive": base["recall_positive"],
            }
        )
    return pd.DataFrame(rows)


def diagnostic_probe(transformer: pd.DataFrame, baseline: pd.DataFrame) -> pd.DataFrame:
    trans = transformer[transformer["test_dataset"].isin(DIAGNOSTIC_DATASETS)].copy()
    trans["model_family"] = "transformer"
    base = baseline[baseline["test_dataset"].isin(DIAGNOSTIC_DATASETS)].copy()
    base["model_family"] = "tfidf_baseline"
    common_cols = [
        "model_family",
        "model",
        "train_dataset",
        "test_dataset",
        "accuracy",
        "recall_positive",
        "f1_positive",
        "f1_macro",
        "tn",
        "fp",
        "fn",
        "tp",
    ]
    return pd.concat([trans[common_cols], base[common_cols]], ignore_index=True)


def make_figures(transformer: pd.DataFrame, gaps: pd.DataFrame, comparison: pd.DataFrame) -> list[Path]:
    OUT.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"figure.dpi": 140, "savefig.dpi": 300, "font.family": "DejaVu Sans"})
    paths: list[Path] = []

    # Transformer macro F1 matrix with mBERT/MuRIL side-by-side per training dataset.
    usable = primary(transformer)
    labels = [DATASET_LABELS[d] for d in PRIMARY_DATASETS]
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.2), sharey=True)
    for ax, model in zip(axes, ["mbert", "muril"]):
        matrix = (
            usable[usable["model"] == model]
            .pivot(index="train_dataset", columns="test_dataset", values="f1_macro")
            .loc[PRIMARY_DATASETS, PRIMARY_DATASETS]
        )
        image = ax.imshow(matrix.values, vmin=0.35, vmax=0.80, cmap="YlGnBu")
        ax.set_title(MODEL_LABELS[model])
        ax.set_xticks(range(len(PRIMARY_DATASETS)))
        ax.set_xticklabels(labels, rotation=25, ha="right", fontsize=8)
        ax.set_yticks(range(len(PRIMARY_DATASETS)))
        ax.set_yticklabels(labels, fontsize=8)
        for row in range(matrix.shape[0]):
            for col in range(matrix.shape[1]):
                value = matrix.iloc[row, col]
                ax.text(col, row, f"{value * 100:.1f}", ha="center", va="center", fontsize=8)
    fig.suptitle("Transformer Macro F1 Across Primary Dataset Conditions")
    cbar = fig.colorbar(image, ax=axes.ravel().tolist(), fraction=0.03, pad=0.04)
    cbar.set_label("Macro F1")
    for ext in ("png", "svg"):
        path = OUT / f"transformer_primary_macro_f1_matrix.{ext}"
        fig.savefig(path, bbox_inches="tight", facecolor="white")
        paths.append(path)
    plt.close(fig)

    # Generalization gaps excluding matched rows.
    transfer = gaps[gaps["train_dataset"] != gaps["test_dataset"]].copy()
    transfer["label"] = transfer["model"] + ": " + transfer["train_dataset"] + " -> " + transfer["test_dataset"]
    transfer = transfer.sort_values("generalization_gap", ascending=False)
    fig, ax = plt.subplots(figsize=(9, 5.2))
    ax.barh(range(len(transfer)), transfer["generalization_gap"] * 100, color="#b55252")
    ax.set_yticks(range(len(transfer)))
    ax.set_yticklabels(transfer["label"], fontsize=7)
    ax.invert_yaxis()
    ax.set_xlabel("Macro F1 drop from matched test condition")
    ax.set_title("Cross-Dataset Generalization Gap")
    fig.tight_layout()
    for ext in ("png", "svg"):
        path = OUT / f"transformer_generalization_gaps.{ext}"
        fig.savefig(path, bbox_inches="tight", facecolor="white")
        paths.append(path)
    plt.close(fig)

    # Transformer vs baseline deltas.
    comp = comparison.copy()
    comp["label"] = comp["train_dataset"] + " -> " + comp["test_dataset"]
    comp = comp.sort_values("transformer_minus_baseline")
    fig, ax = plt.subplots(figsize=(9, 4.8))
    colors = ["#b55252" if value < 0 else "#3f8f6b" for value in comp["transformer_minus_baseline"]]
    ax.barh(range(len(comp)), comp["transformer_minus_baseline"] * 100, color=colors)
    ax.axvline(0, color="#5f6670", linewidth=1)
    ax.set_yticks(range(len(comp)))
    ax.set_yticklabels(comp["label"], fontsize=8)
    ax.set_xlabel("Best transformer macro F1 minus best TF-IDF macro F1")
    ax.set_title("Transformer Advantage Over TF-IDF Baselines")
    fig.tight_layout()
    for ext in ("png", "svg"):
        path = OUT / f"transformer_vs_tfidf_delta.{ext}"
        fig.savefig(path, bbox_inches="tight", facecolor="white")
        paths.append(path)
    plt.close(fig)
    return paths


def build_report(
    matched: pd.DataFrame,
    pairwise: pd.DataFrame,
    best: pd.DataFrame,
    gaps: pd.DataFrame,
    comparison: pd.DataFrame,
    diagnostic: pd.DataFrame,
    figures: list[Path],
) -> None:
    sections = [
        "# Result Analysis Report",
        "",
        "Date: 2026-06-25",
        "",
        "This report analyzes saved model outputs after separating primary datasets from the 79-row diagnostic probe. The primary analysis uses only registered source-backed datasets: `kaggle_hinglish_hate`, `cm_splits_codemixed`, and `thar_religion`.",
        "",
        "## Primary Matched Transformer Results",
        "",
        md_table(
            matched.sort_values(["test_dataset", "model"]),
            ["model", "train_dataset", "test_dataset", "accuracy", "recall_positive", "f1_positive", "f1_macro", "tn", "fp", "fn", "tp"],
        ),
        "",
        "Interpretation: mBERT is stronger on matched Kaggle Hinglish hate and matched CM offensive/code-mixed evaluation, while MuRIL is stronger on matched THAR targeted religious hate.",
        "",
        "## mBERT Versus MuRIL By Train/Test Situation",
        "",
        md_table(
            pairwise.sort_values(["train_dataset", "test_dataset"]),
            [
                "train_dataset",
                "test_dataset",
                "winner_by_macro_f1",
                "macro_f1_gap",
                "winner_by_positive_f1",
                "positive_f1_gap",
                "winner_by_positive_recall",
                "positive_recall_gap",
            ],
        ),
        "",
        "Interpretation: the winner changes by dataset situation. This is the central result: model choice cannot be separated from the training domain, target domain, script mix, and label definition.",
        "",
        "## Best Transformer For Each Primary Test Dataset",
        "",
        md_table(
            best.sort_values("test_dataset"),
            ["test_dataset", "model", "train_dataset", "accuracy", "recall_positive", "f1_positive", "f1_macro", "tn", "fp", "fn", "tp"],
        ),
        "",
        "Interpretation: each primary test dataset is best served by a model trained on the same dataset. This indicates strong in-domain specialization and weak universal transfer.",
        "",
        "## Cross-Dataset Generalization Gaps",
        "",
        md_table(
            gaps[gaps["train_dataset"] != gaps["test_dataset"]].sort_values("generalization_gap", ascending=False),
            ["model", "train_dataset", "test_dataset", "matched_f1_macro", "test_f1_macro", "generalization_gap", "recall_positive", "f1_positive"],
        ),
        "",
        "Interpretation: the largest drops occur when a model trained on one positive-label definition is evaluated against another. Kaggle-trained models are especially conservative on THAR, while THAR-trained models do not become general Hinglish hate detectors.",
        "",
        "## Best Transformer Versus Best TF-IDF Baseline",
        "",
        md_table(
            comparison.sort_values(["train_dataset", "test_dataset"]),
            [
                "train_dataset",
                "test_dataset",
                "best_transformer",
                "transformer_f1_macro",
                "best_baseline",
                "baseline_f1_macro",
                "transformer_minus_baseline",
                "transformer_recall_positive",
                "baseline_recall_positive",
            ],
        ),
        "",
        "Interpretation: transformers do not uniformly dominate TF-IDF. TF-IDF is competitive where lexical cues are strong or where cross-dataset transfer rewards broad keyword overlap. Transformers are strongest on matched dataset conditions.",
        "",
        "## 79-Row Diagnostic Probe",
        "",
        "The 79-row file is excluded from primary conclusions because it may be manually written or AI-generated, has no confirmed source provenance, contains duplicated rows, and has no text overlap with the registered datasets. It remains useful only as a diagnostic probe.",
        "",
        md_table(
            diagnostic.sort_values(["model_family", "train_dataset", "model"]),
            ["model_family", "model", "train_dataset", "accuracy", "recall_positive", "f1_positive", "f1_macro", "tn", "fp", "fn", "tp"],
        ),
        "",
        "Interpretation: results on this probe should not be used to claim model superiority. Its main value is methodological: it exposed how unstable conclusions become when evaluation provenance is unclear.",
        "",
        "## Figures",
        "",
        *[f"- `{path.relative_to(ROOT)}`" for path in figures],
        "",
        "## Paper-Level Takeaways",
        "",
        "- The cleanest paper claim is conditional, not absolute: mBERT wins some dataset situations and MuRIL wins others.",
        "- mBERT is stronger on matched Latin-script Kaggle Hinglish hate and CM offensive/code-mixed data.",
        "- MuRIL is stronger on matched THAR targeted religious hate and also improves THAR-to-CM transfer.",
        "- In-domain training is consistently stronger than cross-dataset transfer, showing that dataset definitions are not interchangeable.",
        "- TF-IDF baselines remain important because lexical cues are strong; any transformer claim should be compared against them.",
        "- The 79-row diagnostic probe should be excluded from primary tables and figures in the final paper.",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    transformer = pd.read_csv(RESULTS / "transformer_cross_dataset_summary.csv")
    baseline = pd.read_csv(RESULTS / "cross_dataset_baseline_summary.csv")

    matched = matched_rows(transformer)
    pairwise = pairwise_transformer_gaps(transformer)
    best = best_by_test(transformer)
    gaps = generalization_gaps(transformer)
    comparison = best_baseline_vs_transformer(baseline, transformer)
    diagnostic = diagnostic_probe(transformer, baseline)

    write_csv(matched, "primary_matched_transformer_results.csv")
    write_csv(pairwise, "mbert_vs_muril_pairwise_gaps.csv")
    write_csv(best, "best_transformer_by_primary_test_dataset.csv")
    write_csv(gaps, "transformer_generalization_gaps.csv")
    write_csv(comparison, "best_transformer_vs_best_tfidf.csv")
    write_csv(diagnostic, "diagnostic_79_row_probe_results.csv")
    figures = make_figures(transformer, gaps, comparison)
    build_report(matched, pairwise, best, gaps, comparison, diagnostic, figures)

    print("\nPrimary Matched Transformer Results")
    print(md_table(matched.sort_values(["test_dataset", "model"]), ["model", "train_dataset", "test_dataset", "recall_positive", "f1_positive", "f1_macro"]))
    print("\nBest Transformer For Each Primary Test Dataset")
    print(md_table(best.sort_values("test_dataset"), ["test_dataset", "model", "train_dataset", "recall_positive", "f1_positive", "f1_macro"]))
    print(f"\nSaved result analysis report to {DOC}")
    print(f"Saved CSV outputs and figures under {OUT}")


if __name__ == "__main__":
    main()
