#!/usr/bin/env python3
"""Analyze transformer error patterns across primary dataset conditions."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
PREDICTIONS = ROOT / "results" / "transformer_cross_dataset_predictions.csv"
OUT = ROOT / "results" / "error_analysis"
DOC = ROOT / "docs" / "error_analysis_report.md"

PRIMARY_DATASETS = ["kaggle_hinglish_hate", "cm_splits_codemixed", "thar_religion"]
MODEL_ORDER = ["mbert", "muril"]

RELIGION_TERMS = {
    "hindu",
    "hinduism",
    "muslim",
    "musalman",
    "islam",
    "christian",
    "christianity",
    "religion",
    "dharam",
    "dharm",
    "maulana",
    "molana",
    "mulla",
    "mullo",
    "jihad",
    "halala",
    "talaq",
    "allah",
    "bhagwan",
    "mandir",
    "masjid",
    "मुसलमान",
    "इस्लाम",
    "हिंदू",
    "हिन्दू",
    "ईसाई",
}

POLITICAL_TERMS = {
    "bjp",
    "congress",
    "rss",
    "modi",
    "gandhi",
    "savarkar",
    "golwalkar",
    "chidambaram",
    "rbi",
    "demonetisation",
    "india",
    "pakistan",
    "kashmir",
    "election",
    "politics",
    "rajneeti",
}

ABUSE_TERMS = {
    "rape",
    "kutta",
    "kuttay",
    "bhadwa",
    "bhadwe",
    "madarchod",
    "madharchod",
    "chutiya",
    "harami",
    "gandu",
    "hate",
    "nafrat",
    "kill",
    "mar",
    "maar",
    "murder",
    "terrorist",
    "aatankwadi",
}

STOPWORDS = {
    "the",
    "and",
    "for",
    "hai",
    "hain",
    "tha",
    "thi",
    "this",
    "that",
    "with",
    "you",
    "your",
    "user",
    "url",
    "are",
    "was",
    "were",
    "not",
    "but",
    "all",
    "have",
    "from",
    "they",
    "will",
    "kar",
    "kya",
    "aur",
    "hai",
    "ke",
    "ki",
    "ka",
    "ko",
    "se",
    "to",
    "me",
    "mein",
}


def normalize(text: object) -> str:
    text = str(text).lower()
    text = re.sub(r"http\S+|www\S+|https\S+", " url ", text)
    text = re.sub(r"@\w+", " user ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def tokens(text: object) -> list[str]:
    return re.findall(r"[a-zA-Z\u0900-\u097F]+", normalize(text))


def script_bucket(text: object) -> str:
    text = str(text)
    has_latin = bool(re.search(r"[A-Za-z]", text))
    has_devanagari = bool(re.search(r"[\u0900-\u097F]", text))
    if has_latin and has_devanagari:
        return "mixed_latin_devanagari"
    if has_devanagari:
        return "devanagari_only"
    if has_latin:
        return "latin_only"
    return "other_or_symbolic"


def feature_flags(text: object) -> dict[str, int | str]:
    toks = set(tokens(text))
    raw = str(text)
    return {
        "script_bucket": script_bucket(text),
        "word_count": len(tokens(text)),
        "has_religion_terms": int(bool(toks & RELIGION_TERMS)),
        "has_political_terms": int(bool(toks & POLITICAL_TERMS)),
        "has_abuse_terms": int(bool(toks & ABUSE_TERMS)),
        "has_mention": int(bool(re.search(r"@\w+", raw))),
        "has_hashtag": int(bool(re.search(r"#\w+", raw))),
        "has_url": int(bool(re.search(r"http\S+|www\S+|https\S+| URL ", raw, flags=re.I))),
    }


def pct(value: float) -> str:
    return f"{value * 100:.1f}%"


def md_table(frame: pd.DataFrame, columns: list[str]) -> str:
    visible = frame[columns].copy()
    for col in visible.columns:
        if col.endswith("_rate") or col in {
            "mbert_accuracy",
            "muril_accuracy",
            "mbert_false_negative_rate",
            "muril_false_negative_rate",
            "mbert_false_positive_rate",
            "muril_false_positive_rate",
            "mbert_error_rate",
            "muril_error_rate",
            "share",
        }:
            visible[col] = visible[col].map(lambda value: pct(float(value)))
        elif pd.api.types.is_float_dtype(visible[col]):
            visible[col] = visible[col].map(lambda value: f"{float(value):.3f}")
        elif not pd.api.types.is_numeric_dtype(visible[col]):
            visible[col] = visible[col].map(
                lambda value: re.sub(r"\s+", " ", str(value)).strip()[:180]
                + ("..." if len(re.sub(r"\s+", " ", str(value)).strip()) > 180 else "")
            )
    return visible.to_markdown(index=False)


def write_csv(frame: pd.DataFrame, name: str) -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / name
    frame.to_csv(path, index=False)
    return path


def load_paired_predictions() -> pd.DataFrame:
    frame = pd.read_csv(PREDICTIONS)
    frame = frame[
        frame["train_dataset"].isin(PRIMARY_DATASETS)
        & frame["test_dataset"].isin(PRIMARY_DATASETS)
        & frame["model"].isin(MODEL_ORDER)
    ].copy()
    frame["example_index"] = frame.groupby(["model", "train_dataset", "test_dataset"]).cumcount()
    pair = frame.pivot_table(
        index=["train_dataset", "test_dataset", "example_index", "text", "true_label"],
        columns="model",
        values=["prediction", "confidence"],
        aggfunc="first",
    )
    pair.columns = [f"{model}_{kind}" for kind, model in pair.columns]
    pair = pair.reset_index()
    pair = pair.rename(
        columns={
            "mbert_prediction": "mbert_pred",
            "muril_prediction": "muril_pred",
            "mbert_confidence": "mbert_confidence",
            "muril_confidence": "muril_confidence",
        }
    )
    for col in ["mbert_pred", "muril_pred", "true_label"]:
        pair[col] = pair[col].astype(int)
    pair["mbert_correct"] = pair["mbert_pred"] == pair["true_label"]
    pair["muril_correct"] = pair["muril_pred"] == pair["true_label"]
    pair["mbert_error_type"] = pair.apply(lambda row: error_type(row["true_label"], row["mbert_pred"]), axis=1)
    pair["muril_error_type"] = pair.apply(lambda row: error_type(row["true_label"], row["muril_pred"]), axis=1)
    pair["outcome"] = pair.apply(outcome_label, axis=1)
    pair["prediction_pattern"] = pair.apply(lambda row: f"true={row['true_label']};mbert={row['mbert_pred']};muril={row['muril_pred']}", axis=1)
    features = pd.DataFrame([feature_flags(text) for text in pair["text"]])
    pair = pd.concat([pair, features], axis=1)
    return pair


def error_type(true_label: int, pred: int) -> str:
    if true_label == pred:
        return "correct"
    if true_label == 1 and pred == 0:
        return "false_negative"
    if true_label == 0 and pred == 1:
        return "false_positive"
    return "other_error"


def outcome_label(row: pd.Series) -> str:
    if row["mbert_correct"] and row["muril_correct"]:
        return "both_correct"
    if row["mbert_correct"] and not row["muril_correct"]:
        return "mbert_only_correct"
    if row["muril_correct"] and not row["mbert_correct"]:
        return "muril_only_correct"
    if row["mbert_pred"] == row["muril_pred"]:
        return "both_wrong_same_prediction"
    return "both_wrong_different_prediction"


def outcome_summary(pair: pd.DataFrame) -> pd.DataFrame:
    rows = []
    total_by_pair = pair.groupby(["train_dataset", "test_dataset"]).size().to_dict()
    counts = pair.groupby(["train_dataset", "test_dataset", "outcome"]).size().reset_index(name="rows")
    for _, row in counts.iterrows():
        total = total_by_pair[(row["train_dataset"], row["test_dataset"])]
        rows.append({**row.to_dict(), "share": row["rows"] / total})
    return pd.DataFrame(rows)


def error_rate_summary(pair: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (train_dataset, test_dataset), group in pair.groupby(["train_dataset", "test_dataset"]):
        positives = group[group["true_label"] == 1]
        negatives = group[group["true_label"] == 0]
        rows.append(
            {
                "train_dataset": train_dataset,
                "test_dataset": test_dataset,
                "rows": len(group),
                "positive_rows": len(positives),
                "negative_rows": len(negatives),
                "mbert_accuracy": group["mbert_correct"].mean(),
                "muril_accuracy": group["muril_correct"].mean(),
                "mbert_false_negative_rate": (positives["mbert_pred"] == 0).mean() if len(positives) else 0,
                "muril_false_negative_rate": (positives["muril_pred"] == 0).mean() if len(positives) else 0,
                "mbert_false_positive_rate": (negatives["mbert_pred"] == 1).mean() if len(negatives) else 0,
                "muril_false_positive_rate": (negatives["muril_pred"] == 1).mean() if len(negatives) else 0,
                "mbert_error_rate": (~group["mbert_correct"]).mean(),
                "muril_error_rate": (~group["muril_correct"]).mean(),
            }
        )
    return pd.DataFrame(rows)


def feature_error_summary(pair: pd.DataFrame) -> pd.DataFrame:
    rows = []
    feature_cols = [
        "script_bucket",
        "has_religion_terms",
        "has_political_terms",
        "has_abuse_terms",
        "has_mention",
        "has_hashtag",
        "has_url",
    ]
    for feature in feature_cols:
        for value, group in pair.groupby(feature):
            positives = group[group["true_label"] == 1]
            rows.append(
                {
                    "feature": feature,
                    "value": value,
                    "rows": len(group),
                    "positive_rows": len(positives),
                    "mbert_error_rate": (~group["mbert_correct"]).mean(),
                    "muril_error_rate": (~group["muril_correct"]).mean(),
                    "mbert_false_negative_rate": (positives["mbert_pred"] == 0).mean() if len(positives) else 0,
                    "muril_false_negative_rate": (positives["muril_pred"] == 0).mean() if len(positives) else 0,
                }
            )
    return pd.DataFrame(rows).sort_values(["feature", "rows"], ascending=[True, False])


def sample_errors(pair: pd.DataFrame, per_group: int = 8) -> pd.DataFrame:
    samples = []
    sample_outcomes = [
        "mbert_only_correct",
        "muril_only_correct",
        "both_wrong_same_prediction",
        "both_wrong_different_prediction",
    ]
    for keys, group in pair[pair["outcome"].isin(sample_outcomes)].groupby(["train_dataset", "test_dataset", "outcome"]):
        group = group.copy()
        group["max_confidence"] = group[["mbert_confidence", "muril_confidence"]].max(axis=1)
        chosen = group.sort_values("max_confidence", ascending=False).head(per_group)
        samples.append(chosen)
    if not samples:
        return pd.DataFrame()
    return pd.concat(samples, ignore_index=True)[
        [
            "train_dataset",
            "test_dataset",
            "outcome",
            "prediction_pattern",
            "mbert_confidence",
            "muril_confidence",
            "script_bucket",
            "has_religion_terms",
            "has_political_terms",
            "has_abuse_terms",
            "text",
        ]
    ]


def hard_false_negative_samples(pair: pd.DataFrame, per_group: int = 12) -> pd.DataFrame:
    hard = pair[(pair["true_label"] == 1) & (pair["mbert_pred"] == 0) & (pair["muril_pred"] == 0)].copy()
    if hard.empty:
        return hard
    hard["mean_confidence"] = hard[["mbert_confidence", "muril_confidence"]].mean(axis=1)
    samples = []
    for _, group in hard.groupby(["train_dataset", "test_dataset"]):
        samples.append(group.sort_values("mean_confidence", ascending=False).head(per_group))
    return pd.concat(samples, ignore_index=True)[
        [
            "train_dataset",
            "test_dataset",
            "prediction_pattern",
            "mbert_confidence",
            "muril_confidence",
            "script_bucket",
            "has_religion_terms",
            "has_political_terms",
            "has_abuse_terms",
            "text",
        ]
    ]


def top_error_terms(pair: pd.DataFrame, top_n: int = 20) -> pd.DataFrame:
    rows = []
    for model in MODEL_ORDER:
        pred_col = f"{model}_pred"
        for (train_dataset, test_dataset), group in pair.groupby(["train_dataset", "test_dataset"]):
            for kind, subset in {
                "false_negative": group[(group["true_label"] == 1) & (group[pred_col] == 0)],
                "false_positive": group[(group["true_label"] == 0) & (group[pred_col] == 1)],
            }.items():
                counter: Counter[str] = Counter()
                for text in subset["text"]:
                    counter.update(token for token in tokens(text) if len(token) >= 3 and token not in STOPWORDS)
                for rank, (token, count) in enumerate(counter.most_common(top_n), start=1):
                    rows.append(
                        {
                            "model": model,
                            "train_dataset": train_dataset,
                            "test_dataset": test_dataset,
                            "error_type": kind,
                            "rank": rank,
                            "token": token,
                            "count": count,
                        }
                    )
    return pd.DataFrame(rows)


def manual_annotation_template(samples: pd.DataFrame, hard_fns: pd.DataFrame) -> pd.DataFrame:
    combined = pd.concat(
        [
            samples.assign(sample_source="disagreement_or_error_sample"),
            hard_fns.assign(outcome="hard_false_negative", sample_source="hard_false_negative"),
        ],
        ignore_index=True,
        sort=False,
    )
    if combined.empty:
        return combined
    combined = combined.drop_duplicates(subset=["train_dataset", "test_dataset", "prediction_pattern", "text"]).copy()
    combined["manual_reason"] = ""
    combined["label_quality_note"] = ""
    combined["paper_relevance"] = ""
    keep = [
        "sample_source",
        "train_dataset",
        "test_dataset",
        "outcome",
        "prediction_pattern",
        "script_bucket",
        "has_religion_terms",
        "has_political_terms",
        "has_abuse_terms",
        "manual_reason",
        "label_quality_note",
        "paper_relevance",
        "text",
    ]
    return combined[[col for col in keep if col in combined.columns]]


def make_figures(error_rates: pd.DataFrame, outcomes: pd.DataFrame) -> list[Path]:
    OUT.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"figure.dpi": 140, "savefig.dpi": 300, "font.family": "DejaVu Sans"})
    paths: list[Path] = []

    display = error_rates.copy()
    display["pair"] = display["train_dataset"] + " -> " + display["test_dataset"]
    display = display.sort_values(["test_dataset", "train_dataset"])
    x = range(len(display))
    fig, ax = plt.subplots(figsize=(10, 4.8))
    width = 0.36
    ax.bar([i - width / 2 for i in x], display["mbert_false_negative_rate"] * 100, width, label="mBERT", color="#2f6f9f")
    ax.bar([i + width / 2 for i in x], display["muril_false_negative_rate"] * 100, width, label="MuRIL", color="#b8872f")
    ax.set_xticks(list(x))
    ax.set_xticklabels(display["pair"], rotation=35, ha="right", fontsize=8)
    ax.set_ylabel("False negative rate among positives (%)")
    ax.set_title("Positive Examples Missed By Model")
    ax.legend(frameon=False)
    fig.tight_layout()
    for ext in ("png", "svg"):
        path = OUT / f"false_negative_rates.{ext}"
        fig.savefig(path, facecolor="white")
        paths.append(path)
    plt.close(fig)

    disagreement = outcomes[outcomes["outcome"].isin(["mbert_only_correct", "muril_only_correct"])].copy()
    if not disagreement.empty:
        pivot = disagreement.pivot_table(index=["train_dataset", "test_dataset"], columns="outcome", values="share", fill_value=0)
        labels = [f"{idx[0]} -> {idx[1]}" for idx in pivot.index]
        fig, ax = plt.subplots(figsize=(10, 4.8))
        x = range(len(pivot))
        ax.bar([i - width / 2 for i in x], pivot.get("mbert_only_correct", pd.Series(0, index=pivot.index)) * 100, width, label="mBERT only correct", color="#2f6f9f")
        ax.bar([i + width / 2 for i in x], pivot.get("muril_only_correct", pd.Series(0, index=pivot.index)) * 100, width, label="MuRIL only correct", color="#b8872f")
        ax.set_xticks(list(x))
        ax.set_xticklabels(labels, rotation=35, ha="right", fontsize=8)
        ax.set_ylabel("Share of evaluated rows (%)")
        ax.set_title("Model Disagreement Advantage")
        ax.legend(frameon=False)
        fig.tight_layout()
        for ext in ("png", "svg"):
            path = OUT / f"model_disagreement_advantage.{ext}"
            fig.savefig(path, facecolor="white")
            paths.append(path)
        plt.close(fig)
    return paths


def build_report(
    error_rates: pd.DataFrame,
    outcomes: pd.DataFrame,
    feature_summary: pd.DataFrame,
    samples: pd.DataFrame,
    hard_fns: pd.DataFrame,
    terms: pd.DataFrame,
    figures: list[Path],
) -> None:
    sections = [
        "# Error Analysis Report",
        "",
        "Date: 2026-06-26",
        "",
        "This report analyzes transformer prediction errors on the three primary source-backed datasets. The 79-row diagnostic probe is excluded from this primary error analysis because its provenance is uncertain.",
        "",
        "## Error Rate Summary",
        "",
        md_table(
            error_rates.sort_values(["test_dataset", "train_dataset"]),
            [
                "train_dataset",
                "test_dataset",
                "rows",
                "positive_rows",
                "negative_rows",
                "mbert_accuracy",
                "muril_accuracy",
                "mbert_false_negative_rate",
                "muril_false_negative_rate",
                "mbert_false_positive_rate",
                "muril_false_positive_rate",
            ],
        ),
        "",
        "False negatives are especially important because they are hate/offensive examples predicted as non-hate/non-offensive. High false-negative rates indicate a conservative model under that dataset condition.",
        "",
        "## Outcome Summary",
        "",
        md_table(
            outcomes.sort_values(["train_dataset", "test_dataset", "outcome"]),
            ["train_dataset", "test_dataset", "outcome", "rows", "share"],
        ),
        "",
        "## Feature-Level Error Signals",
        "",
        md_table(
            feature_summary[
                (feature_summary["feature"].isin(["script_bucket", "has_religion_terms", "has_political_terms", "has_abuse_terms"]))
                & (feature_summary["rows"] >= 50)
            ].head(40),
            ["feature", "value", "rows", "positive_rows", "mbert_error_rate", "muril_error_rate", "mbert_false_negative_rate", "muril_false_negative_rate"],
        ),
        "",
        "These feature signals are heuristic, not final causal explanations. They tell us where to focus manual reading.",
        "",
        "## High-Confidence Disagreement And Error Samples",
        "",
        "Full sample table: `results/error_analysis/error_samples.csv`.",
        "",
        "Manual annotation template: `results/error_analysis/manual_error_annotation_template.csv`.",
        "",
        md_table(samples.head(30), ["train_dataset", "test_dataset", "outcome", "prediction_pattern", "script_bucket", "has_religion_terms", "has_political_terms", "has_abuse_terms", "text"]),
        "",
        "## Hard False Negatives",
        "",
        "Hard false negatives are positive examples that both mBERT and MuRIL predicted as negative for the same train/test condition. Full table: `results/error_analysis/hard_false_negative_samples.csv`.",
        "",
        md_table(hard_fns.head(30), ["train_dataset", "test_dataset", "prediction_pattern", "script_bucket", "has_religion_terms", "has_political_terms", "has_abuse_terms", "text"]),
        "",
        "## Top Error Terms",
        "",
        "Full term table: `results/error_analysis/top_error_terms.csv`.",
        "",
    ]
    for model in MODEL_ORDER:
        subset = terms[(terms["model"] == model) & (terms["error_type"] == "false_negative")].head(20)
        sections.extend(
            [
                f"### `{model}` False-Negative Terms",
                "",
                md_table(subset, ["train_dataset", "test_dataset", "rank", "token", "count"]),
                "",
            ]
        )

    sections.extend(
        [
            "## Figures",
            "",
            *[f"- `{path.relative_to(ROOT)}`" for path in figures],
            "",
            "## Initial Interpretation",
            "",
            "- Kaggle-trained models miss many positive examples on THAR, confirming that broad Hinglish hate training does not transfer cleanly to targeted religious hate.",
            "- THAR-trained models still miss many Kaggle positives, confirming that targeted religious hate training does not become a general Hinglish hate detector.",
            "- mBERT tends to have lower false-negative rates on matched Kaggle and CM conditions, while MuRIL has lower false-negative rates on matched THAR and THAR-to-CM transfer.",
            "- Disagreement rows are the most useful manual-reading set: they show where model pretraining and dataset situation produce different decisions on the same text.",
            "- The next manual step is to annotate sampled errors with human-readable reasons such as label ambiguity, target-group cue, political context, transliteration, Devanagari/script issue, generic profanity, or missing context.",
        ]
    )
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    pair = load_paired_predictions()
    outcomes = outcome_summary(pair)
    error_rates = error_rate_summary(pair)
    feature_summary = feature_error_summary(pair)
    samples = sample_errors(pair)
    hard_fns = hard_false_negative_samples(pair)
    terms = top_error_terms(pair)
    annotation_template = manual_annotation_template(samples, hard_fns)
    figures = make_figures(error_rates, outcomes)

    write_csv(pair, "paired_transformer_predictions_primary.csv")
    write_csv(outcomes, "error_outcome_summary.csv")
    write_csv(error_rates, "error_rate_summary.csv")
    write_csv(feature_summary, "feature_error_summary.csv")
    write_csv(samples, "error_samples.csv")
    write_csv(hard_fns, "hard_false_negative_samples.csv")
    write_csv(terms, "top_error_terms.csv")
    write_csv(annotation_template, "manual_error_annotation_template.csv")
    build_report(error_rates, outcomes, feature_summary, samples, hard_fns, terms, figures)

    print("\nError Rate Summary")
    print(
        md_table(
            error_rates.sort_values(["test_dataset", "train_dataset"]),
            [
                "train_dataset",
                "test_dataset",
                "rows",
                "mbert_accuracy",
                "muril_accuracy",
                "mbert_false_negative_rate",
                "muril_false_negative_rate",
                "mbert_false_positive_rate",
                "muril_false_positive_rate",
            ],
        )
    )
    print(f"\nSaved error analysis report to {DOC}")
    print(f"Saved CSV outputs and figures under {OUT}")


if __name__ == "__main__":
    main()
