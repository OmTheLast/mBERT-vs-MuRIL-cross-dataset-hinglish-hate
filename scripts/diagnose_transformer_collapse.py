#!/usr/bin/env python3
"""Diagnose all-negative or all-positive transformer behavior.

The main evaluation script stores only the predicted label and max confidence.
For model-collapse debugging we need the positive-class probability distribution
and threshold sweeps.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path

import pandas as pd
import torch
from sklearn.metrics import accuracy_score, confusion_matrix, precision_recall_fscore_support
from sklearn.model_selection import train_test_split
from transformers import AutoModelForSequenceClassification, AutoTokenizer


ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class EvalSet:
    name: str
    frame: pd.DataFrame
    split_policy: str
    situation: str


def minimal_clean(text: object) -> str:
    text = str(text)
    text = re.sub(r"http\S+|www\S+|https\S+", " URL ", text)
    text = re.sub(r"@\w+", " USER ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def run_device() -> torch.device:
    if torch.cuda.is_available():
        return torch.device("cuda")
    if torch.backends.mps.is_available():
        return torch.device("mps")
    return torch.device("cpu")


def read_binary_csv(path: Path, text_column: str = "text", label_column: str = "label") -> pd.DataFrame:
    frame = pd.read_csv(path)
    frame = frame[[text_column, label_column] + (["split"] if "split" in frame.columns else [])].dropna()
    frame = frame.rename(columns={text_column: "text", label_column: "label"})
    frame["text"] = frame["text"].map(minimal_clean)
    frame["label"] = frame["label"].astype(int)
    frame = frame[frame["text"].str.len() > 0].drop_duplicates(subset=["text"], keep="first")
    return frame.reset_index(drop=True)


def external_eval_sets(seed: int, test_size: float) -> list[EvalSet]:
    specs = [
        (
            "kaggle_hinglish_hate",
            ROOT / "data" / "processed" / "kaggle_hinglish_hate.csv",
            "Kaggle held-out stratified test split",
            False,
        ),
        (
            "cm_splits_codemixed",
            ROOT / "data" / "processed" / "cm_splits_codemixed.csv",
            "CM source-provided test split",
            True,
        ),
        (
            "thar_religion",
            ROOT / "data" / "processed" / "thar_religion.csv",
            "THAR held-out stratified test split",
            False,
        ),
    ]
    eval_sets: list[EvalSet] = []
    for name, path, situation, has_split in specs:
        frame = read_binary_csv(path)
        if has_split and "split" in frame.columns:
            eval_frame = frame[frame["split"].astype(str) == "test"].copy()
            policy = "provided_test_split"
        else:
            _, eval_frame = train_test_split(
                frame,
                test_size=test_size,
                random_state=seed,
                stratify=frame["label"],
            )
            policy = f"stratified_{int((1 - test_size) * 100)}_{int(test_size * 100)}_split_seed{seed}"
        eval_sets.append(EvalSet(name, eval_frame.reset_index(drop=True), policy, situation))
    return eval_sets


def internal_eval_set(train_csv: Path, seed: int, test_size: float) -> EvalSet:
    frame = read_binary_csv(train_csv)
    _, eval_frame = train_test_split(
        frame,
        test_size=test_size,
        random_state=seed,
        stratify=frame["label"],
    )
    return EvalSet(
        "internal_mixed_validation",
        eval_frame.reset_index(drop=True),
        f"stratified_{int((1 - test_size) * 100)}_{int(test_size * 100)}_split_seed{seed}",
        "Validation split produced by the mixed training CSV",
    )


def predict_positive_probs(
    checkpoint: Path,
    frame: pd.DataFrame,
    batch_size: int,
    max_length: int,
    device: torch.device,
) -> pd.DataFrame:
    tokenizer = AutoTokenizer.from_pretrained(checkpoint)
    model = AutoModelForSequenceClassification.from_pretrained(checkpoint).to(device)
    model.eval()

    rows: list[pd.DataFrame] = []
    texts = frame["text"].tolist()
    for offset in range(0, len(texts), batch_size):
        batch_texts = texts[offset : offset + batch_size]
        inputs = tokenizer(
            batch_texts,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=max_length,
        ).to(device)
        with torch.no_grad():
            logits = model(**inputs).logits
            probs = torch.nn.functional.softmax(logits, dim=-1).detach().cpu()

        batch = frame.iloc[offset : offset + batch_size].copy()
        batch["prob_negative"] = probs[:, 0].tolist()
        batch["prob_positive"] = probs[:, 1].tolist()
        batch["prediction_0_50"] = (batch["prob_positive"] >= 0.5).astype(int)
        rows.append(batch)

    return pd.concat(rows, ignore_index=True)


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


def summarize_probabilities(predictions: pd.DataFrame, threshold_step: float) -> dict[str, float | int]:
    probs = predictions["prob_positive"]
    labels = predictions["label"]
    default_predictions = predictions["prediction_0_50"]
    summary: dict[str, float | int] = {
        "rows": len(predictions),
        "positive_rows": int(labels.sum()),
        "negative_rows": int((labels == 0).sum()),
        "predicted_positive_at_0_50": int(default_predictions.sum()),
        "prob_positive_min": probs.min(),
        "prob_positive_p01": probs.quantile(0.01),
        "prob_positive_p05": probs.quantile(0.05),
        "prob_positive_p25": probs.quantile(0.25),
        "prob_positive_median": probs.quantile(0.50),
        "prob_positive_p75": probs.quantile(0.75),
        "prob_positive_p95": probs.quantile(0.95),
        "prob_positive_p99": probs.quantile(0.99),
        "prob_positive_max": probs.max(),
        "mean_prob_true_negative": probs[labels == 0].mean(),
        "mean_prob_true_positive": probs[labels == 1].mean(),
    }
    summary.update({f"default_{key}": value for key, value in metric_row(labels, default_predictions).items()})

    best_threshold = 0.5
    best_metrics = metric_row(labels, default_predictions)
    threshold = 0.0
    while threshold <= 1.000001:
        threshold_predictions = (probs >= threshold).astype(int)
        metrics = metric_row(labels, threshold_predictions)
        if metrics["f1_macro"] > best_metrics["f1_macro"]:
            best_threshold = threshold
            best_metrics = metrics
        threshold += threshold_step

    summary["best_threshold_by_macro_f1"] = best_threshold
    summary.update({f"best_{key}": value for key, value in best_metrics.items()})
    return summary


def write_markdown_report(
    path: Path,
    checkpoint: Path,
    train_csv: Path,
    summary: pd.DataFrame,
    examples_path: Path,
) -> None:
    lines = [
        "# MuRIL Collapse Diagnostic Report",
        "",
        "Date: 2026-07-02",
        "",
        f"Checkpoint: `{checkpoint}`",
        f"Training CSV for internal validation reconstruction: `{train_csv}`",
        "",
        "## What This Checks",
        "",
        "This diagnostic checks whether the all-negative result is caused by the default 0.50 threshold, or whether the model assigns low positive probability to nearly every example.",
        "",
        "Important columns:",
        "",
        "- `predicted_positive_at_0_50`: how many examples the normal classifier marks positive.",
        "- `prob_positive_p95` and `prob_positive_max`: whether positive probabilities ever approach the decision threshold.",
        "- `best_threshold_by_macro_f1`: the threshold that would maximize Macro F1 on that evaluation set.",
        "- `best_f1_macro`: the best possible Macro F1 after threshold tuning on that same set.",
        "",
        "## Summary",
        "",
        summary.to_markdown(index=False, floatfmt=".4f"),
        "",
        "## Local Example File",
        "",
        f"Highest-positive-probability examples and strongest false negatives are saved at `{examples_path}`.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Diagnose transformer collapse with probability distributions.")
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--train-csv", type=Path, default=ROOT / "data" / "processed" / "mixed_train_kaggle_plus_cm__seed42.csv")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "results" / "collapse_diagnostics")
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--max-length", type=int, default=128)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--test-size", type=float, default=0.2)
    parser.add_argument("--threshold-step", type=float, default=0.01)
    parser.add_argument("--prefix", default="muril_mixed_kaggle_cm")
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    device = run_device()
    print(f"Using device: {device}")

    eval_sets = [internal_eval_set(args.train_csv, args.seed, args.test_size), *external_eval_sets(args.seed, args.test_size)]
    summaries = []
    examples = []
    for eval_set in eval_sets:
        print(f"Scoring {eval_set.name} ({len(eval_set.frame)} rows)")
        scored = predict_positive_probs(args.checkpoint, eval_set.frame, args.batch_size, args.max_length, device)
        scored["eval_set"] = eval_set.name
        scored["split_policy"] = eval_set.split_policy
        scored["situation"] = eval_set.situation
        scored_path = args.output_dir / f"{args.prefix}__{eval_set.name}__probabilities.csv"
        scored.to_csv(scored_path, index=False)

        row = summarize_probabilities(scored, args.threshold_step)
        row.update(
            {
                "eval_set": eval_set.name,
                "split_policy": eval_set.split_policy,
                "probabilities_file": str(scored_path),
            }
        )
        summaries.append(row)

        high_positive = scored.sort_values("prob_positive", ascending=False).head(10).copy()
        high_positive["example_group"] = "highest_positive_probability"
        false_negative = scored[(scored["label"] == 1) & (scored["prediction_0_50"] == 0)]
        false_negative = false_negative.sort_values("prob_positive", ascending=False).head(10).copy()
        false_negative["example_group"] = "strongest_false_negative_by_positive_probability"
        examples.extend([high_positive, false_negative])

    summary = pd.DataFrame(summaries)
    ordered_columns = [
        "eval_set",
        "rows",
        "positive_rows",
        "predicted_positive_at_0_50",
        "prob_positive_min",
        "prob_positive_p25",
        "prob_positive_median",
        "prob_positive_p75",
        "prob_positive_p95",
        "prob_positive_max",
        "mean_prob_true_negative",
        "mean_prob_true_positive",
        "default_f1_macro",
        "default_recall_positive",
        "default_f1_positive",
        "best_threshold_by_macro_f1",
        "best_f1_macro",
        "best_recall_positive",
        "best_f1_positive",
        "split_policy",
        "probabilities_file",
    ]
    summary = summary[[column for column in ordered_columns if column in summary.columns]]
    summary_path = args.output_dir / f"{args.prefix}__summary.csv"
    summary.to_csv(summary_path, index=False)

    examples_frame = pd.concat(examples, ignore_index=True)
    example_columns = [
        "eval_set",
        "example_group",
        "text",
        "label",
        "prediction_0_50",
        "prob_positive",
        "prob_negative",
    ]
    examples_path = args.output_dir / f"{args.prefix}__examples.csv"
    examples_frame[[column for column in example_columns if column in examples_frame.columns]].to_csv(
        examples_path,
        index=False,
    )

    report_path = ROOT / "docs" / "muril_collapse_diagnostic_report.md"
    write_markdown_report(report_path, args.checkpoint, args.train_csv, summary, examples_path)

    metadata_path = args.output_dir / f"{args.prefix}__metadata.json"
    metadata_path.write_text(
        json.dumps(
            {
                "checkpoint": str(args.checkpoint),
                "train_csv": str(args.train_csv),
                "summary": str(summary_path),
                "examples": str(examples_path),
                "report": str(report_path),
                "seed": args.seed,
                "test_size": args.test_size,
                "threshold_step": args.threshold_step,
                "device": str(device),
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )

    print("\nCollapse Diagnostic Summary")
    print(summary.to_markdown(index=False, floatfmt=".4f"))
    print(f"\nSaved summary to {summary_path}")
    print(f"Saved examples to {examples_path}")
    print(f"Saved report to {report_path}")


if __name__ == "__main__":
    main()
