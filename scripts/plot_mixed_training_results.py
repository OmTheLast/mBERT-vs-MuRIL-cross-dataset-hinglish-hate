#!/usr/bin/env python3
"""Create mixed-training summary tables and figures."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
OUT = RESULTS / "result_analysis"

MIXED_SUMMARIES = [
    RESULTS / "mixed_kaggle_plus_cm_transformer_summary.csv",
    RESULTS / "mixed_cm_plus_thar_transformer_summary.csv",
    RESULTS / "mixed_kaggle_plus_thar_transformer_summary.csv",
    RESULTS / "mixed_all_three_transformer_summary.csv",
]

MODEL_LABELS = {
    "mbert": "mBERT",
    "muril": "MuRIL",
}

DATASET_LABELS = {
    "kaggle_hinglish_hate": "Kaggle",
    "cm_splits_codemixed": "CM",
    "thar_religion": "THAR",
}

TRAIN_LABELS = {
    "mixed_kaggle_plus_cm": "Kaggle+CM",
    "mixed_cm_plus_thar": "CM+THAR",
    "mixed_kaggle_plus_thar": "Kaggle+THAR",
    "mixed_all_three": "All three",
}


def load_mixed_results() -> pd.DataFrame:
    frames = []
    for path in MIXED_SUMMARIES:
        if path.exists():
            frames.append(pd.read_csv(path))
    if not frames:
        raise FileNotFoundError("No mixed transformer summary files found.")

    frame = pd.concat(frames, ignore_index=True)
    frame = frame[frame["test_dataset"].isin(DATASET_LABELS)].copy()
    frame["model_label"] = frame["model"].map(MODEL_LABELS)
    frame["test_label"] = frame["test_dataset"].map(DATASET_LABELS)
    frame["train_label"] = frame["train_dataset"].map(TRAIN_LABELS)
    return frame


def write_summary(frame: pd.DataFrame) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    columns = [
        "model",
        "train_dataset",
        "test_dataset",
        "test_rows",
        "accuracy",
        "recall_positive",
        "f1_positive",
        "f1_macro",
        "tn",
        "fp",
        "fn",
        "tp",
    ]
    frame[columns].to_csv(OUT / "mixed_training_macro_f1_summary.csv", index=False)


def plot_macro_f1_grid(frame: pd.DataFrame) -> None:
    order = list(TRAIN_LABELS.values())
    datasets = list(DATASET_LABELS.values())
    models = ["mBERT", "MuRIL"]
    colors = {"mBERT": "#356da8", "MuRIL": "#b65f2a"}

    fig, axes = plt.subplots(1, len(datasets), figsize=(13, 4.8), sharey=True)
    for ax, dataset in zip(axes, datasets):
        subset = frame[frame["test_label"] == dataset]
        x = range(len(order))
        width = 0.36

        for offset, model in [(-width / 2, "mBERT"), (width / 2, "MuRIL")]:
            values = []
            for train_label in order:
                row = subset[(subset["train_label"] == train_label) & (subset["model_label"] == model)]
                values.append(float(row["f1_macro"].iloc[0]) * 100 if not row.empty else 0.0)
            ax.bar([position + offset for position in x], values, width=width, label=model, color=colors[model])

        ax.set_title(dataset)
        ax.set_xticks(list(x))
        ax.set_xticklabels(order, rotation=25, ha="right")
        ax.set_ylim(0, 85)
        ax.grid(axis="y", alpha=0.25)
        ax.set_ylabel("Macro F1 (%)")

    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", ncols=2, frameon=False)
    fig.suptitle("Mixed-Training Cross-Dataset Macro F1", y=1.03)
    fig.tight_layout()

    for ext in ("png", "svg"):
        fig.savefig(OUT / f"mixed_training_macro_f1.{ext}", dpi=180, bbox_inches="tight")
    plt.close(fig)


def plot_model_gap(frame: pd.DataFrame) -> None:
    pivot = frame.pivot_table(
        index=["train_label", "test_label"],
        columns="model_label",
        values="f1_macro",
        aggfunc="first",
    ).reset_index()
    pivot["muril_minus_mbert_macro_f1"] = (pivot["MuRIL"] - pivot["mBERT"]) * 100
    pivot = pivot.sort_values(["train_label", "test_label"])
    pivot.to_csv(OUT / "mixed_training_muril_minus_mbert.csv", index=False)

    labels = [f"{row.train_label}\n{row.test_label}" for row in pivot.itertuples()]
    values = pivot["muril_minus_mbert_macro_f1"]
    colors = ["#b65f2a" if value >= 0 else "#356da8" for value in values]

    fig, ax = plt.subplots(figsize=(12, 5.2))
    ax.bar(range(len(values)), values, color=colors)
    ax.axhline(0, color="#333333", linewidth=1)
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=45, ha="right")
    ax.set_ylabel("MuRIL minus mBERT Macro F1 (points)")
    ax.set_title("Mixed-Training Model Gap By Test Dataset")
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()

    for ext in ("png", "svg"):
        fig.savefig(OUT / f"mixed_training_muril_minus_mbert.{ext}", dpi=180, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    frame = load_mixed_results()
    write_summary(frame)
    plot_macro_f1_grid(frame)
    plot_model_gap(frame)
    print(f"Saved mixed-training figures and summaries to {OUT}")


if __name__ == "__main__":
    main()
