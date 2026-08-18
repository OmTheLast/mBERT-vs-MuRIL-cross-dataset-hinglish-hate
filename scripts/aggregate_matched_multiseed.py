#!/usr/bin/env python3
"""Aggregate matched-dataset multi-seed transformer runs."""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from tabulate import tabulate


ROOT = Path(__file__).resolve().parents[1]
DATASET_LABELS = {
    "kaggle_hinglish_hate": "Kaggle Hinglish Hate",
    "cm_splits_codemixed": "CM Code-mixed",
    "thar_religion": "THAR Religion",
}
METRICS = [
    "accuracy",
    "precision_hate",
    "recall_hate",
    "f1_hate",
    "precision_macro",
    "recall_macro",
    "f1_macro",
]


def pct(value: float) -> str:
    return f"{value * 100:.1f}%"


def load_row(model: str, dataset: str, seed: int, epochs: int) -> dict[str, str | int | float]:
    checkpoint = ROOT / "Models" / f"{model}__train-{dataset}__seed{seed}__e{epochs}"
    metrics_path = checkpoint / "eval_metrics.json"
    metadata_path = checkpoint / "training_metadata.json"
    if not metrics_path.exists():
        raise FileNotFoundError(f"Missing metrics file: {metrics_path}")

    metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
    metadata = json.loads(metadata_path.read_text(encoding="utf-8")) if metadata_path.exists() else {}
    row: dict[str, str | int | float] = {
        "model": model,
        "train_dataset": dataset,
        "train_dataset_label": DATASET_LABELS.get(dataset, dataset),
        "seed": seed,
        "epochs": epochs,
        "checkpoint_path": str(checkpoint),
        "split_policy": metadata.get("split_policy", ""),
        "train_rows": metadata.get("train_rows", ""),
        "eval_rows": metadata.get("eval_rows", ""),
        "cleaning": metadata.get("cleaning", ""),
        "max_length": metadata.get("max_length", ""),
        "batch_size": metadata.get("batch_size", ""),
        "learning_rate": metadata.get("learning_rate", ""),
    }
    for metric in METRICS:
        row[metric] = float(metrics[f"eval_{metric}"])
    return row


def make_summary(per_seed: pd.DataFrame) -> pd.DataFrame:
    grouped = per_seed.groupby(["train_dataset", "train_dataset_label", "model"], as_index=False)
    summary = grouped.agg(
        seeds=("seed", lambda values: ",".join(str(int(value)) for value in sorted(values))),
        n_seeds=("seed", "nunique"),
        accuracy_mean=("accuracy", "mean"),
        accuracy_std=("accuracy", "std"),
        recall_hate_mean=("recall_hate", "mean"),
        recall_hate_std=("recall_hate", "std"),
        f1_hate_mean=("f1_hate", "mean"),
        f1_hate_std=("f1_hate", "std"),
        f1_macro_mean=("f1_macro", "mean"),
        f1_macro_std=("f1_macro", "std"),
    )
    return summary.fillna(0.0)


def write_report(per_seed: pd.DataFrame, summary: pd.DataFrame, output: Path) -> None:
    included_datasets = ", ".join(
        f"`{dataset}`" for dataset in sorted(per_seed["train_dataset"].unique())
    )
    included_seeds = ", ".join(
        f"`{int(seed)}`" for seed in sorted(per_seed["seed"].unique())
    )

    visible = summary.copy()
    for metric in [
        "accuracy_mean",
        "accuracy_std",
        "recall_hate_mean",
        "recall_hate_std",
        "f1_hate_mean",
        "f1_hate_std",
        "f1_macro_mean",
        "f1_macro_std",
    ]:
        visible[metric] = visible[metric].map(pct)

    per_seed_visible = per_seed[
        ["train_dataset", "model", "seed", "accuracy", "recall_hate", "f1_hate", "f1_macro", "split_policy"]
    ].copy()
    for metric in ["accuracy", "recall_hate", "f1_hate", "f1_macro"]:
        per_seed_visible[metric] = per_seed_visible[metric].map(pct)

    sections = [
        "# Matched Multi-Seed Transformer Results",
        "",
        f"Date: {date.today().isoformat()}",
        "",
        "Purpose: test whether the main matched-dataset mBERT vs MuRIL findings are stable when only the random seed changes.",
        "",
        f"Scope: matched conditions included in this aggregation: {included_datasets}. Each condition is trained/evaluated under its controlled matched split policy.",
        "",
        f"Seeds included: {included_seeds}.",
        "",
        "Primary metric: Macro F1. Positive-class recall and positive-class F1 are kept because false negatives matter in hate/offensive speech detection.",
        "",
        "## Mean And Standard Deviation",
        "",
        visible[
            [
                "train_dataset",
                "model",
                "seeds",
                "n_seeds",
                "accuracy_mean",
                "accuracy_std",
                "recall_hate_mean",
                "recall_hate_std",
                "f1_hate_mean",
                "f1_hate_std",
                "f1_macro_mean",
                "f1_macro_std",
            ]
        ].to_markdown(index=False),
        "",
        "## Per-Seed Results",
        "",
        per_seed_visible.to_markdown(index=False),
        "",
        "## Interpretation Notes",
        "",
        "- Multi-seed results are a stability check, not a new model architecture or new dataset.",
        "- If a model wins by less than the seed-to-seed standard deviation, the safer claim is that the models are close under that condition.",
        "- If one model has better Macro F1 but lower positive recall, the moderation interpretation should mention missed positive examples.",
        "- These matched results should be discussed separately from cross-dataset and mixed-training results because they answer a different question.",
        "",
    ]
    output.write_text("\n".join(sections), encoding="utf-8")


def make_macro_f1_figure(summary: pd.DataFrame, output: Path) -> None:
    present_datasets = set(summary["train_dataset"])
    datasets = [dataset for dataset in DATASET_LABELS if dataset in present_datasets]
    x_positions = range(len(datasets))
    width = 0.34
    colors = {"mbert": "#2f6f9f", "muril": "#b04d4d"}

    fig, ax = plt.subplots(figsize=(9, 5))
    for offset, model in [(-width / 2, "mbert"), (width / 2, "muril")]:
        values = []
        errors = []
        for dataset in datasets:
            row = summary[(summary["train_dataset"] == dataset) & (summary["model"] == model)]
            values.append(float(row["f1_macro_mean"].iloc[0]) * 100 if not row.empty else 0.0)
            errors.append(float(row["f1_macro_std"].iloc[0]) * 100 if not row.empty else 0.0)
        ax.bar(
            [position + offset for position in x_positions],
            values,
            width=width,
            yerr=errors,
            capsize=5,
            label=model.upper() if model == "muril" else "mBERT",
            color=colors[model],
            edgecolor="#1f1f1f",
            linewidth=0.5,
        )

    ax.set_ylabel("Macro F1 (%)")
    ax.set_title("Matched Dataset Macro F1 Across Seeds")
    ax.set_xticks(list(x_positions))
    ax.set_xticklabels([DATASET_LABELS[dataset] for dataset in datasets])
    ax.set_ylim(0, 100)
    ax.grid(axis="y", alpha=0.25)
    ax.legend(frameon=False)
    fig.tight_layout()
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=200)
    fig.savefig(output.with_suffix(".svg"))
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description="Aggregate matched multi-seed transformer runs.")
    parser.add_argument("--seeds", type=int, nargs="+", default=[42, 7, 13])
    parser.add_argument("--epochs", type=int, default=2)
    parser.add_argument(
        "--datasets",
        nargs="+",
        default=["kaggle_hinglish_hate", "cm_splits_codemixed", "thar_religion"],
    )
    parser.add_argument("--models", nargs="+", default=["mbert", "muril"])
    parser.add_argument("--output-dir", type=Path, default=ROOT / "results" / "multiseed")
    args = parser.parse_args()

    rows = []
    for dataset in args.datasets:
        for model in args.models:
            for seed in args.seeds:
                rows.append(load_row(model, dataset, seed, args.epochs))

    per_seed = pd.DataFrame(rows).sort_values(["train_dataset", "model", "seed"])
    summary = make_summary(per_seed).sort_values(["train_dataset", "model"])

    args.output_dir.mkdir(parents=True, exist_ok=True)
    per_seed_path = args.output_dir / "matched_multiseed_per_seed.csv"
    summary_path = args.output_dir / "matched_multiseed_summary.csv"
    report_path = ROOT / "docs" / "matched_multiseed_results.md"
    figure_path = ROOT / "results" / "result_analysis" / "matched_multiseed_macro_f1.png"

    per_seed.to_csv(per_seed_path, index=False)
    summary.to_csv(summary_path, index=False)
    write_report(per_seed, summary, report_path)
    make_macro_f1_figure(summary, figure_path)

    display = summary[
        [
            "train_dataset",
            "model",
            "seeds",
            "accuracy_mean",
            "accuracy_std",
            "recall_hate_mean",
            "recall_hate_std",
            "f1_hate_mean",
            "f1_hate_std",
            "f1_macro_mean",
            "f1_macro_std",
        ]
    ].copy()
    for column in display.columns:
        if column.endswith("_mean") or column.endswith("_std"):
            display[column] = display[column].map(pct)

    print("\nMatched Multi-Seed Summary")
    print(tabulate(display, headers="keys", tablefmt="github", showindex=False))
    print(f"\nSaved per-seed results to {per_seed_path}")
    print(f"Saved mean/std results to {summary_path}")
    print(f"Saved report to {report_path}")
    print(f"Saved figure to {figure_path}")


if __name__ == "__main__":
    main()
