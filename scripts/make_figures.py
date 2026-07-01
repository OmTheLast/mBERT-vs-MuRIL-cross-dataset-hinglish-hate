#!/usr/bin/env python3
"""Generate paper-facing figures from saved experiment outputs."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FIGURES = RESULTS / "figures"


DATASET_LABELS = {
    "kaggle_hinglish_hate": "Kaggle\nHinglish Hate",
    "cm_splits_codemixed": "CM\nCode-mixed",
    "thar_religion": "THAR\nReligion",
    "existing_79_row_benchmark": "79-row\nBenchmark",
}


MODEL_LABELS = {
    "tfidf_logistic_regression": "TF-IDF LR",
    "tfidf_linear_svm": "TF-IDF SVM",
    "mbert": "mBERT",
    "muril": "MuRIL",
}


PALETTE = {
    "blue": "#2f6f9f",
    "green": "#3f8f6b",
    "red": "#b55252",
    "gold": "#b8872f",
    "gray": "#5f6670",
    "light_gray": "#e8eaed",
}


def setup_style() -> None:
    plt.rcParams.update(
        {
            "figure.dpi": 140,
            "savefig.dpi": 300,
            "font.family": "DejaVu Sans",
            "font.size": 10,
            "axes.titlesize": 12,
            "axes.labelsize": 10,
            "xtick.labelsize": 9,
            "ytick.labelsize": 9,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.grid": False,
        }
    )


def save_figure(fig: plt.Figure, name: str) -> None:
    FIGURES.mkdir(parents=True, exist_ok=True)
    png = FIGURES / f"{name}.png"
    svg = FIGURES / f"{name}.svg"
    fig.savefig(png, bbox_inches="tight", facecolor="white")
    fig.savefig(svg, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Saved {png}")
    print(f"Saved {svg}")


def add_value_labels(ax: plt.Axes, values: list[int], x_positions: np.ndarray, offset: int = 40) -> None:
    for x, value in zip(x_positions, values):
        ax.text(x, value + offset, f"{value:,}", ha="center", va="bottom", fontsize=8, color=PALETTE["gray"])


def dataset_inventory_figure() -> None:
    datasets = ["kaggle_hinglish_hate", "cm_splits_codemixed", "thar_religion"]
    label_0 = [2914, 2455, 6095]
    label_1 = [1866, 1445, 5454]
    labels = [DATASET_LABELS[name] for name in datasets]
    x = np.arange(len(datasets))

    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.bar(x, label_0, label="Label 0", color=PALETTE["blue"])
    ax.bar(x, label_1, bottom=label_0, label="Label 1", color=PALETTE["red"])
    totals = [a + b for a, b in zip(label_0, label_1)]
    add_value_labels(ax, totals, x, offset=90)
    ax.set_title("Dataset Size And Label Balance")
    ax.set_ylabel("Rows")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend(frameon=False, loc="upper left")
    ax.set_ylim(0, max(totals) * 1.18)
    save_figure(fig, "dataset_size_label_balance")


def heatmap_from_matrix(
    matrix: pd.DataFrame,
    title: str,
    filename: str,
    metric_label: str = "Macro F1",
    vmin: float = 0.0,
    vmax: float = 0.8,
) -> None:
    fig, ax = plt.subplots(figsize=(7.0, 5.2))
    values = matrix.to_numpy(dtype=float)
    image = ax.imshow(values, cmap="YlGnBu", vmin=vmin, vmax=vmax)

    ax.set_title(title)
    ax.set_xlabel("Test dataset")
    ax.set_ylabel("Train dataset")
    ax.set_xticks(np.arange(matrix.shape[1]))
    ax.set_yticks(np.arange(matrix.shape[0]))
    ax.set_xticklabels([DATASET_LABELS.get(col, col) for col in matrix.columns])
    ax.set_yticklabels([DATASET_LABELS.get(idx, idx) for idx in matrix.index])

    for row in range(matrix.shape[0]):
        for col in range(matrix.shape[1]):
            value = values[row, col]
            color = "white" if value >= 0.55 else "#1b1f23"
            ax.text(col, row, f"{value * 100:.1f}", ha="center", va="center", color=color, fontsize=9)

    cbar = fig.colorbar(image, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label(f"{metric_label} (%)")
    cbar.set_ticks([0.0, 0.2, 0.4, 0.6, 0.8])
    cbar.set_ticklabels(["0", "20", "40", "60", "80"])
    save_figure(fig, filename)


def baseline_heatmap() -> None:
    frame = pd.read_csv(RESULTS / "cross_dataset_baseline_summary.csv")
    usable = frame[frame["test_dataset"].isin(["kaggle_hinglish_hate", "cm_splits_codemixed", "thar_religion"])]
    best = (
        usable.sort_values(["train_dataset", "test_dataset", "f1_macro"], ascending=[True, True, False])
        .groupby(["train_dataset", "test_dataset"], as_index=False)
        .head(1)
    )
    matrix = best.pivot(index="train_dataset", columns="test_dataset", values="f1_macro")
    matrix = matrix.loc[["kaggle_hinglish_hate", "cm_splits_codemixed", "thar_religion"], ["kaggle_hinglish_hate", "cm_splits_codemixed", "thar_religion"]]
    heatmap_from_matrix(matrix, "Best TF-IDF Baseline Macro F1", "baseline_cross_dataset_macro_f1")


def ordered_available(values: set[str], preferred: list[str]) -> list[str]:
    return [value for value in preferred if value in values]


def transformer_heatmap() -> None:
    frame = pd.read_csv(RESULTS / "transformer_cross_dataset_summary.csv")
    usable = frame[frame["test_dataset"].isin(["kaggle_hinglish_hate", "cm_splits_codemixed", "thar_religion"])]
    best = (
        usable.sort_values(["train_dataset", "test_dataset", "f1_macro"], ascending=[True, True, False])
        .groupby(["train_dataset", "test_dataset"], as_index=False)
        .head(1)
    )
    matrix = best.pivot(index="train_dataset", columns="test_dataset", values="f1_macro")
    train_order = ordered_available(set(matrix.index), ["kaggle_hinglish_hate", "cm_splits_codemixed", "thar_religion"])
    test_order = ordered_available(set(matrix.columns), ["kaggle_hinglish_hate", "cm_splits_codemixed", "thar_religion"])
    matrix = matrix.loc[train_order, test_order]
    heatmap_from_matrix(matrix, "Best Transformer Macro F1", "transformer_cross_dataset_macro_f1")


def transformer_recall_heatmap() -> None:
    frame = pd.read_csv(RESULTS / "transformer_cross_dataset_summary.csv")
    usable = frame[frame["test_dataset"].isin(["kaggle_hinglish_hate", "cm_splits_codemixed", "thar_religion"])]
    best = (
        usable.sort_values(["train_dataset", "test_dataset", "recall_positive"], ascending=[True, True, False])
        .groupby(["train_dataset", "test_dataset"], as_index=False)
        .head(1)
    )
    matrix = best.pivot(index="train_dataset", columns="test_dataset", values="recall_positive")
    train_order = ordered_available(set(matrix.index), ["kaggle_hinglish_hate", "cm_splits_codemixed", "thar_religion"])
    test_order = ordered_available(set(matrix.columns), ["kaggle_hinglish_hate", "cm_splits_codemixed", "thar_religion"])
    matrix = matrix.loc[train_order, test_order]
    heatmap_from_matrix(
        matrix,
        "Best Transformer Positive Recall",
        "transformer_cross_dataset_positive_recall",
        metric_label="Positive recall",
        vmax=0.8,
    )


def transformer_vs_baseline() -> None:
    baseline = pd.read_csv(RESULTS / "cross_dataset_baseline_summary.csv")
    transformer = pd.read_csv(RESULTS / "transformer_cross_dataset_summary.csv")
    tests = ["kaggle_hinglish_hate", "cm_splits_codemixed", "thar_religion", "existing_79_row_benchmark"]

    baseline_best = (
        baseline[(baseline["train_dataset"] == "kaggle_hinglish_hate") & (baseline["test_dataset"].isin(tests))]
        .sort_values(["test_dataset", "f1_macro"], ascending=[True, False])
        .groupby("test_dataset", as_index=False)
        .head(1)
        .set_index("test_dataset")
    )
    transformer_best = (
        transformer[(transformer["train_dataset"] == "kaggle_hinglish_hate") & (transformer["test_dataset"].isin(tests))]
        .sort_values(["test_dataset", "f1_macro"], ascending=[True, False])
        .groupby("test_dataset", as_index=False)
        .head(1)
        .set_index("test_dataset")
    )

    x = np.arange(len(tests))
    width = 0.36
    fig, ax = plt.subplots(figsize=(8.2, 4.4))
    ax.bar(x - width / 2, [baseline_best.loc[t, "f1_macro"] * 100 for t in tests], width, label="Best TF-IDF", color=PALETTE["green"])
    ax.bar(x + width / 2, [transformer_best.loc[t, "f1_macro"] * 100 for t in tests], width, label="Best Transformer", color=PALETTE["blue"])
    ax.set_title("Kaggle-Hinglish-Hate Training: Baseline Vs Transformer")
    ax.set_ylabel("Macro F1 (%)")
    ax.set_xticks(x)
    ax.set_xticklabels([DATASET_LABELS[t] for t in tests])
    ax.set_ylim(0, 80)
    ax.legend(frameon=False, loc="upper right")
    ax.axhline(50, color=PALETTE["light_gray"], linewidth=1)
    save_figure(fig, "kaggle_hinglish_hate_baseline_vs_transformer")


def best_transformer_by_test() -> None:
    transformer = pd.read_csv(RESULTS / "transformer_cross_dataset_summary.csv")
    tests = ["kaggle_hinglish_hate", "cm_splits_codemixed", "thar_religion", "existing_79_row_benchmark"]
    usable = transformer[transformer["test_dataset"].isin(tests)].copy()
    usable["model_train"] = usable["model"] + "\ntrain=" + usable["train_dataset"].map(DATASET_LABELS).str.replace("\n", " ", regex=False)
    best = (
        usable.sort_values(["test_dataset", "f1_macro"], ascending=[True, False])
        .groupby("test_dataset", as_index=False)
        .head(1)
    )
    best = best.set_index("test_dataset").loc[tests].reset_index()

    x = np.arange(len(best))
    fig, ax = plt.subplots(figsize=(9.2, 4.8))
    bars = ax.bar(x, best["f1_macro"] * 100, color=PALETTE["blue"])
    ax.set_title("Best Transformer Condition By Test Dataset")
    ax.set_ylabel("Macro F1 (%)")
    ax.set_xticks(x)
    ax.set_xticklabels([DATASET_LABELS[test] for test in best["test_dataset"]])
    ax.set_ylim(0, 85)
    ax.axhline(50, color=PALETTE["light_gray"], linewidth=1)
    for bar, label in zip(bars, best["model_train"]):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 1.5,
            label,
            ha="center",
            va="bottom",
            fontsize=7,
            color=PALETTE["gray"],
        )
    save_figure(fig, "best_transformer_condition_by_test_dataset")


def positive_recall_comparison() -> None:
    transformer = pd.read_csv(RESULTS / "transformer_cross_dataset_summary.csv")
    frame = transformer[transformer["train_dataset"] == "kaggle_hinglish_hate"].copy()
    tests = ["kaggle_hinglish_hate", "cm_splits_codemixed", "thar_religion", "existing_79_row_benchmark"]
    x = np.arange(len(tests))
    width = 0.36

    fig, ax = plt.subplots(figsize=(8.2, 4.4))
    for offset, model, color in [(-width / 2, "mbert", PALETTE["blue"]), (width / 2, "muril", PALETTE["gold"])]:
        values = [
            frame[(frame["model"] == model) & (frame["test_dataset"] == test)]["recall_positive"].iloc[0] * 100
            for test in tests
        ]
        ax.bar(x + offset, values, width, label=MODEL_LABELS[model], color=color)

    ax.set_title("Transformer Positive Recall After Kaggle-Hinglish-Hate Training")
    ax.set_ylabel("Positive recall (%)")
    ax.set_xticks(x)
    ax.set_xticklabels([DATASET_LABELS[t] for t in tests])
    ax.set_ylim(0, 75)
    ax.legend(frameon=False, loc="upper right")
    ax.axhline(50, color=PALETTE["light_gray"], linewidth=1)
    save_figure(fig, "transformer_positive_recall_kaggle_hinglish_hate")


def write_index() -> None:
    content = """# Figures

Generated by `scripts/make_figures.py`.

| Figure | Files | Use |
|---|---|---|
| Dataset size and label balance | `dataset_size_label_balance.png/.svg` | Dataset section |
| Best TF-IDF baseline macro F1 heatmap | `baseline_cross_dataset_macro_f1.png/.svg` | Baseline results |
| Best transformer macro F1 heatmap | `transformer_cross_dataset_macro_f1.png/.svg` | Transformer results |
| Best transformer positive recall heatmap | `transformer_cross_dataset_positive_recall.png/.svg` | Recall/error analysis |
| Best transformer condition by test dataset | `best_transformer_condition_by_test_dataset.png/.svg` | Results summary |
| Kaggle-Hinglish-Hate baseline vs transformer macro F1 | `kaggle_hinglish_hate_baseline_vs_transformer.png/.svg` | Discussion |
| Transformer positive recall after Kaggle-Hinglish-Hate training | `transformer_positive_recall_kaggle_hinglish_hate.png/.svg` | Error/limitations discussion |
"""
    (FIGURES / "README.md").write_text(content, encoding="utf-8")
    print(f"Saved {FIGURES / 'README.md'}")


def main() -> None:
    setup_style()
    dataset_inventory_figure()
    baseline_heatmap()
    transformer_heatmap()
    transformer_recall_heatmap()
    transformer_vs_baseline()
    best_transformer_by_test()
    positive_recall_comparison()
    write_index()


if __name__ == "__main__":
    main()
