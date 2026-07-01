#!/usr/bin/env python3
"""Create paper-friendly Markdown result tables from saved CSV/JSON outputs."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
from tabulate import tabulate


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"


def pct(value: float) -> str:
    return f"{value * 100:.1f}%"


def markdown_table(frame: pd.DataFrame, columns: list[str]) -> str:
    visible = frame[columns].copy()
    for col in visible.columns:
        if col not in {
            "model",
            "evaluation",
            "condition",
            "dataset",
            "train_dataset",
            "test_dataset",
            "split_policy",
            "train_task_category",
            "train_label_meaning",
            "train_dataset_situation",
            "deduplicated_text",
            "train_rows",
            "test_rows",
            "tn",
            "fp",
            "fn",
            "tp",
        }:
            visible[col] = visible[col].map(lambda value: pct(float(value)))
    return visible.to_markdown(index=False)


def terminal_table(frame: pd.DataFrame, columns: list[str]) -> str:
    visible = frame[columns].copy()
    for col in visible.columns:
        if col not in {
            "model",
            "evaluation",
            "condition",
            "dataset",
            "train_dataset",
            "test_dataset",
            "split_policy",
            "train_rows",
            "test_rows",
            "tn",
            "fp",
            "fn",
            "tp",
        }:
            visible[col] = visible[col].map(lambda value: pct(float(value)))
    return tabulate(visible, headers="keys", tablefmt="github", showindex=False)


def load_validation_metrics(model_name: str, path: Path) -> dict[str, str | float]:
    metrics = json.loads(path.read_text(encoding="utf-8"))
    return {
        "model": model_name,
        "accuracy": metrics["eval_accuracy"],
        "precision_hate": metrics["eval_precision_hate"],
        "recall_hate": metrics["eval_recall_hate"],
        "f1_hate": metrics["eval_f1_hate"],
        "f1_macro": metrics["eval_f1_macro"],
    }


def main() -> None:
    existing_checkpoint_benchmark = pd.read_csv(RESULTS / "current_saved_benchmark_summary.csv")
    retrained_benchmark = pd.read_csv(RESULTS / "hinglish_retrained_benchmark_summary.csv")

    validation_rows = [
        {
            **load_validation_metrics(
                "mbert",
                ROOT / "Models" / "mbert__train-kaggle_hinglish_hate__seed42__e2" / "eval_metrics.json",
            ),
            "train_dataset": "kaggle_hinglish_hate",
        },
        {
            **load_validation_metrics(
                "muril",
                ROOT / "Models" / "muril__train-kaggle_hinglish_hate__seed42__e2" / "eval_metrics.json",
            ),
            "train_dataset": "kaggle_hinglish_hate",
        },
        {
            **load_validation_metrics(
                "mbert",
                ROOT / "Models" / "mbert__train-cm_splits_codemixed__seed42__e2" / "eval_metrics.json",
            ),
            "train_dataset": "cm_splits_codemixed",
        },
        {
            **load_validation_metrics(
                "muril",
                ROOT / "Models" / "muril__train-cm_splits_codemixed__seed42__e2" / "eval_metrics.json",
            ),
            "train_dataset": "cm_splits_codemixed",
        },
        {
            **load_validation_metrics(
                "mbert",
                ROOT / "Models" / "mbert__train-thar_religion__seed42__e2" / "eval_metrics.json",
            ),
            "train_dataset": "thar_religion",
        },
        {
            **load_validation_metrics(
                "muril",
                ROOT / "Models" / "muril__train-thar_religion__seed42__e2" / "eval_metrics.json",
            ),
            "train_dataset": "thar_religion",
        },
    ]
    validation = pd.DataFrame(validation_rows)

    baseline_path = RESULTS / "baseline_summary.csv"
    baseline = pd.read_csv(baseline_path) if baseline_path.exists() else pd.DataFrame()
    cross_baseline_path = RESULTS / "cross_dataset_baseline_summary.csv"
    cross_baseline = pd.read_csv(cross_baseline_path) if cross_baseline_path.exists() else pd.DataFrame()
    transformer_cross_path = RESULTS / "transformer_cross_dataset_summary.csv"
    transformer_cross = pd.read_csv(transformer_cross_path) if transformer_cross_path.exists() else pd.DataFrame()

    output = RESULTS / "summary.md"
    sections = [
        "# Results Summary",
        "",
        "Generated from saved experiment outputs. These tables are intended for quick reference and later paper drafting.",
        "",
        "## Kaggle Hinglish Hate Dataset Context",
        "",
        "- `kaggle_hinglish_hate.csv`: 4,780 rows after de-duplication.",
        "- Label distribution: 2,914 non-hate and 1,866 hate.",
        "- Source attribution: Shardul Dhekane, `Code-Mixed Hinglish Hate Speech Detection Dataset`, Kaggle.",
        "",
        "## Transformer Validation Results",
        "",
        markdown_table(validation, ["model", "train_dataset", "accuracy", "precision_hate", "recall_hate", "f1_hate", "f1_macro"]),
        "",
        "## Existing Saved Checkpoints At Session Start On 79-Row Benchmark",
        "",
        "These results come from the checkpoints that already existed in the project before the code cleanup and retraining work. They are useful because they show the model behavior that motivated the current investigation.",
        "",
        markdown_table(
            existing_checkpoint_benchmark,
            ["model", "accuracy", "precision_hate", "recall_hate", "f1_hate", "f1_macro", "tn", "fp", "fn", "tp"],
        ),
        "",
        "## Retrained Hinglish Checkpoints On 79-Row Benchmark",
        "",
        markdown_table(
            retrained_benchmark,
            ["model", "accuracy", "precision_hate", "recall_hate", "f1_hate", "f1_macro", "tn", "fp", "fn", "tp"],
        ),
        "",
    ]

    if not baseline.empty:
        sections.extend(
            [
                "## Earlier TF-IDF Baseline Results",
                "",
                markdown_table(
                    baseline,
                    ["model", "evaluation", "accuracy", "precision_hate", "recall_hate", "f1_hate", "f1_macro", "tn", "fp", "fn", "tp"],
                ),
                "",
            ]
        )

    if not cross_baseline.empty:
        sections.extend(
            [
                "## Cross-Dataset TF-IDF Baseline Results",
                "",
                "These results train each baseline on one usable dataset and evaluate it across all usable test sets plus the 79-row sanity benchmark. The positive label means different things across datasets, so interpret these as dataset-situation results, not direct universal hate-speech scores.",
                "",
                markdown_table(
                    cross_baseline,
                    [
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
                    ],
                ),
                "",
            ]
        )

    if not transformer_cross.empty:
        sections.extend(
            [
                "## Transformer Cross-Dataset Evaluation",
                "",
                "These results evaluate local transformer checkpoints across the same dataset test conditions used by the cross-dataset baselines. Rows are labeled by the training dataset used to create each checkpoint.",
                "",
                markdown_table(
                    transformer_cross,
                    [
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
                    ],
                ),
                "",
            ]
        )

    sections.extend(
        [
            "## Initial Interpretation",
            "",
            "- The existing saved checkpoints at the start of this session were strongly biased toward predicting non-hate.",
            "- Retraining on `kaggle_hinglish_hate` restored hate detection, but hate recall remains a weakness.",
            "- mBERT is stronger than MuRIL on both matched `kaggle_hinglish_hate` and matched `cm_splits_codemixed` transformer test conditions.",
            "- MuRIL is stronger than mBERT on matched `thar_religion` transformer evaluation.",
            "- MuRIL remains stronger on the tiny 79-row benchmark when trained on `kaggle_hinglish_hate`, but CM-trained and THAR-trained transformers perform poorly there.",
            "- CM-trained transformers transfer better to `thar_religion` than Kaggle-Hinglish-Hate-trained transformers, especially MuRIL on positive-class recall/F1.",
            "- THAR-trained MuRIL transfers better to `cm_splits_codemixed` than THAR-trained mBERT, but both THAR-trained models transfer weakly to `kaggle_hinglish_hate`.",
            "- The 79-row benchmark is useful for sanity checks but too small and label-noisy for final conclusions.",
            "- The 79-row benchmark issue is paper-relevant: many positive labels are generic negative phrases rather than strict targeted hate, while both models still miss several targeted/religious examples.",
            "",
        ]
    )

    output.write_text("\n".join(sections), encoding="utf-8")
    print("\nTransformer Validation Results")
    print(terminal_table(validation, ["model", "train_dataset", "accuracy", "precision_hate", "recall_hate", "f1_hate", "f1_macro"]))
    print("\nExisting Saved Checkpoints At Session Start On 79-Row Benchmark")
    print(terminal_table(existing_checkpoint_benchmark, ["model", "accuracy", "precision_hate", "recall_hate", "f1_hate", "f1_macro", "tn", "fp", "fn", "tp"]))
    print("\nRetrained Hinglish Checkpoints On 79-Row Benchmark")
    print(terminal_table(retrained_benchmark, ["model", "accuracy", "precision_hate", "recall_hate", "f1_hate", "f1_macro", "tn", "fp", "fn", "tp"]))
    if not baseline.empty:
        print("\nTF-IDF Baseline Results")
        print(terminal_table(baseline, ["model", "evaluation", "accuracy", "precision_hate", "recall_hate", "f1_hate", "f1_macro", "tn", "fp", "fn", "tp"]))
    if not cross_baseline.empty:
        print("\nCross-Dataset TF-IDF Baseline Results")
        print(terminal_table(cross_baseline, ["model", "train_dataset", "test_dataset", "test_rows", "accuracy", "recall_positive", "f1_positive", "f1_macro", "tn", "fp", "fn", "tp"]))
    if not transformer_cross.empty:
        print("\nTransformer Cross-Dataset Evaluation")
        print(terminal_table(transformer_cross, ["model", "train_dataset", "test_dataset", "test_rows", "accuracy", "recall_positive", "f1_positive", "f1_macro", "tn", "fp", "fn", "tp"]))
    print(f"Saved Markdown summary to {output}")


if __name__ == "__main__":
    main()
