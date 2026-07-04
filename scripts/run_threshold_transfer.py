#!/usr/bin/env python3
"""Apply validation-selected thresholds to held-out evaluation probability files."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import date
from pathlib import Path

import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix, precision_recall_fscore_support


ROOT = Path(__file__).resolve().parents[1]
PRIMARY_EVAL_SETS = ["kaggle_hinglish_hate", "cm_splits_codemixed", "thar_religion"]


@dataclass(frozen=True)
class ThresholdCondition:
    training_condition: str
    model: str
    prefix: str
    validation_set: str = "internal_validation"


CONDITIONS = [
    ThresholdCondition(
        training_condition="kaggle_hinglish_hate",
        model="mbert",
        prefix="calibration_kaggle_mbert",
    ),
    ThresholdCondition(
        training_condition="kaggle_hinglish_hate",
        model="muril",
        prefix="calibration_kaggle_muril",
    ),
    ThresholdCondition(
        training_condition="mixed_kaggle_plus_cm",
        model="mbert",
        prefix="calibration_mixed_kaggle_cm_mbert",
    ),
    ThresholdCondition(
        training_condition="mixed_kaggle_plus_cm",
        model="muril",
        prefix="calibration_mixed_kaggle_cm_muril",
    ),
    ThresholdCondition(
        training_condition="mixed_cm_plus_thar",
        model="mbert",
        prefix="calibration_mixed_cm_thar_mbert",
    ),
    ThresholdCondition(
        training_condition="mixed_cm_plus_thar",
        model="muril",
        prefix="calibration_mixed_cm_thar_muril",
    ),
    ThresholdCondition(
        training_condition="mixed_kaggle_plus_thar",
        model="mbert",
        prefix="calibration_mixed_kaggle_thar_mbert",
    ),
    ThresholdCondition(
        training_condition="mixed_kaggle_plus_thar",
        model="muril",
        prefix="calibration_mixed_kaggle_thar_muril",
    ),
]


def metric_row(labels: pd.Series, predictions: pd.Series) -> dict[str, float | int]:
    precision_pos, recall_pos, f1_pos, _ = precision_recall_fscore_support(
        labels,
        predictions,
        average="binary",
        zero_division=0,
    )
    precision_macro, recall_macro, f1_macro, _ = precision_recall_fscore_support(
        labels,
        predictions,
        average="macro",
        zero_division=0,
    )
    tn, fp, fn, tp = confusion_matrix(labels, predictions, labels=[0, 1]).ravel()
    return {
        "accuracy": accuracy_score(labels, predictions),
        "precision_positive": precision_pos,
        "recall_positive": recall_pos,
        "f1_positive": f1_pos,
        "precision_macro": precision_macro,
        "recall_macro": recall_macro,
        "f1_macro": f1_macro,
        "tn": int(tn),
        "fp": int(fp),
        "fn": int(fn),
        "tp": int(tp),
    }


def probability_path(output_dir: Path, prefix: str, eval_set: str) -> Path:
    return output_dir / f"{prefix}__{eval_set}__probabilities.csv"


def threshold_candidates(step: float) -> list[float]:
    values = []
    threshold = 0.0
    while threshold <= 1.000001:
        values.append(round(threshold, 10))
        threshold += step
    return values


def select_threshold(validation: pd.DataFrame, step: float) -> tuple[float, dict[str, float | int]]:
    best_threshold = 0.5
    best_metrics = metric_row(validation["label"], (validation["prob_positive"] >= 0.5).astype(int))
    for threshold in threshold_candidates(step):
        predictions = (validation["prob_positive"] >= threshold).astype(int)
        metrics = metric_row(validation["label"], predictions)
        if metrics["f1_macro"] > best_metrics["f1_macro"]:
            best_threshold = threshold
            best_metrics = metrics
    return best_threshold, best_metrics


def evaluate_threshold(frame: pd.DataFrame, threshold: float) -> dict[str, float | int]:
    return metric_row(frame["label"], (frame["prob_positive"] >= threshold).astype(int))


def report_markdown(summary: pd.DataFrame, path: Path, threshold_step: float) -> None:
    display = summary[
        [
            "training_condition",
            "model",
            "test_dataset",
            "selected_threshold",
            "default_f1_macro",
            "threshold_f1_macro",
            "macro_f1_delta",
            "default_recall_positive",
            "threshold_recall_positive",
            "positive_recall_delta",
            "default_f1_positive",
            "threshold_f1_positive",
            "leakage_caveat",
        ]
    ].copy()
    for column in [
        "selected_threshold",
        "default_f1_macro",
        "threshold_f1_macro",
        "macro_f1_delta",
        "default_recall_positive",
        "threshold_recall_positive",
        "positive_recall_delta",
        "default_f1_positive",
        "threshold_f1_positive",
    ]:
        display[column] = display[column].map(lambda value: f"{value:.3f}")

    lines = [
        "# Validation-Selected Threshold Transfer",
        "",
        f"Date: {date.today().isoformat()}",
        "",
        "This report applies thresholds selected on validation probability files to held-out evaluation sets.",
        "",
        f"Threshold search step: `{threshold_step}`",
        "",
        "## Important Caveat",
        "",
        "For the Kaggle-only checkpoints, the reconstructed internal validation split is the same split used as the Kaggle held-out evaluation in the earlier experiments. Therefore, the Kaggle matched rows for those two checkpoints are diagnostic rather than paper-safe. Their CM and THAR transfer rows remain independent of that Kaggle validation split.",
        "",
        "For the mixed Kaggle+CM checkpoints, the internal validation split comes from the mixed training CSV, while Kaggle, CM, and THAR evaluations are held-out source test sets. Those rows are the cleanest threshold-transfer evidence in this first pass.",
        "",
        "## Summary",
        "",
        display.to_markdown(index=False),
        "",
        "## Interpretation",
        "",
        "- If threshold tuning improves positive recall and Macro F1, the default `0.50` cutoff was hiding useful positive-class signal.",
        "- If threshold tuning improves recall but hurts Macro F1, the model may be trading too many false positives for recall.",
        "- These results should be interpreted alongside the default-threshold results, not as a replacement for model comparison.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run validation-selected threshold transfer.")
    parser.add_argument("--probability-dir", type=Path, default=ROOT / "results" / "collapse_diagnostics")
    parser.add_argument("--output", type=Path, default=ROOT / "results" / "collapse_diagnostics" / "threshold_transfer_summary.csv")
    parser.add_argument("--report", type=Path, default=ROOT / "docs" / "threshold_transfer_report.md")
    parser.add_argument("--threshold-step", type=float, default=0.01)
    args = parser.parse_args()

    rows = []
    for condition in CONDITIONS:
        validation_path = probability_path(args.probability_dir, condition.prefix, condition.validation_set)
        if not validation_path.exists():
            raise FileNotFoundError(f"Missing validation probability file: {validation_path}")
        validation = pd.read_csv(validation_path)
        selected_threshold, validation_metrics = select_threshold(validation, args.threshold_step)

        for eval_set in PRIMARY_EVAL_SETS:
            eval_path = probability_path(args.probability_dir, condition.prefix, eval_set)
            if not eval_path.exists():
                raise FileNotFoundError(f"Missing evaluation probability file: {eval_path}")
            frame = pd.read_csv(eval_path)
            default_metrics = evaluate_threshold(frame, 0.5)
            threshold_metrics = evaluate_threshold(frame, selected_threshold)
            leakage_caveat = (
                condition.training_condition == "kaggle_hinglish_hate"
                and eval_set == "kaggle_hinglish_hate"
            )
            row = {
                "training_condition": condition.training_condition,
                "model": condition.model,
                "threshold_source": condition.validation_set,
                "selected_threshold": selected_threshold,
                "validation_rows": len(validation),
                "validation_f1_macro": validation_metrics["f1_macro"],
                "validation_recall_positive": validation_metrics["recall_positive"],
                "test_dataset": eval_set,
                "test_rows": len(frame),
                "leakage_caveat": bool(leakage_caveat),
            }
            row.update({f"default_{key}": value for key, value in default_metrics.items()})
            row.update({f"threshold_{key}": value for key, value in threshold_metrics.items()})
            row["macro_f1_delta"] = row["threshold_f1_macro"] - row["default_f1_macro"]
            row["positive_recall_delta"] = row["threshold_recall_positive"] - row["default_recall_positive"]
            row["positive_f1_delta"] = row["threshold_f1_positive"] - row["default_f1_positive"]
            rows.append(row)

    summary = pd.DataFrame(rows)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(args.output, index=False)
    report_markdown(summary, args.report, args.threshold_step)

    print("Validation-Selected Threshold Transfer")
    print(
        summary[
            [
                "training_condition",
                "model",
                "test_dataset",
                "selected_threshold",
                "default_f1_macro",
                "threshold_f1_macro",
                "macro_f1_delta",
                "default_recall_positive",
                "threshold_recall_positive",
                "positive_recall_delta",
                "leakage_caveat",
            ]
        ].to_markdown(index=False, floatfmt=".4f")
    )
    print(f"\nSaved summary to {args.output}")
    print(f"Saved report to {args.report}")


if __name__ == "__main__":
    main()
