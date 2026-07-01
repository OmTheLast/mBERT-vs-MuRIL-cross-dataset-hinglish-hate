#!/usr/bin/env python3
"""Run TF-IDF baselines across all locally usable processed datasets."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, precision_recall_fscore_support
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from tabulate import tabulate


ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class DatasetSpec:
    name: str
    path: Path
    task_category: str
    label_meaning: str
    situation: str
    has_split: bool = False


DATASETS = [
    DatasetSpec(
        name="kaggle_hinglish_hate",
        path=ROOT / "data" / "processed" / "kaggle_hinglish_hate.csv",
        task_category="hate",
        label_meaning="0 = non-hate, 1 = hate",
        situation="Kaggle Code-Mixed Hinglish Hate Speech Detection dataset by Shardul Dhekane",
    ),
    DatasetSpec(
        name="cm_splits_codemixed",
        path=ROOT / "data" / "processed" / "cm_splits_codemixed.csv",
        task_category="offensive/hate-adjacent",
        label_meaning="0 = not offensive, 1 = offensive",
        situation="Indian politics Hindi-English code-mixed Twitter/X data",
        has_split=True,
    ),
    DatasetSpec(
        name="thar_religion",
        path=ROOT / "data" / "processed" / "thar_religion.csv",
        task_category="targeted religious hate",
        label_meaning="0 = Non-AntiReligion, 1 = AntiReligion",
        situation="Hindi-English code-mixed YouTube comments about religious hate",
    ),
]


def make_models() -> dict[str, Pipeline]:
    return {
        "tfidf_logistic_regression": Pipeline(
            [
                (
                    "tfidf",
                    TfidfVectorizer(
                        analyzer="word",
                        ngram_range=(1, 2),
                        min_df=2,
                        max_features=50000,
                        sublinear_tf=True,
                    ),
                ),
                ("classifier", LogisticRegression(max_iter=2000, class_weight="balanced")),
            ]
        ),
        "tfidf_linear_svm": Pipeline(
            [
                (
                    "tfidf",
                    TfidfVectorizer(
                        analyzer="word",
                        ngram_range=(1, 2),
                        min_df=2,
                        max_features=50000,
                        sublinear_tf=True,
                    ),
                ),
                ("classifier", LinearSVC(class_weight="balanced")),
            ]
        ),
    }


def compute_metrics(labels: pd.Series, predictions: list[int]) -> dict[str, float | int]:
    precision_hate, recall_hate, f1_hate, _ = precision_recall_fscore_support(
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
        "precision_positive": precision_hate,
        "recall_positive": recall_hate,
        "f1_positive": f1_hate,
        "precision_macro": precision_macro,
        "recall_macro": recall_macro,
        "f1_macro": f1_macro,
        "tn": int(tn),
        "fp": int(fp),
        "fn": int(fn),
        "tp": int(tp),
    }


def normalized_frame(spec: DatasetSpec, text_column: str, label_column: str, deduplicate: bool) -> pd.DataFrame:
    frame = pd.read_csv(spec.path)
    keep_columns = [text_column, label_column]
    if spec.has_split and "split" in frame.columns:
        keep_columns.append("split")
    frame = frame[keep_columns].dropna(subset=[text_column, label_column]).copy()
    frame[text_column] = frame[text_column].astype(str)
    frame[label_column] = frame[label_column].astype(int)
    frame = frame.rename(columns={text_column: "text", label_column: "label"})
    frame["dataset"] = spec.name
    if "split" not in frame.columns:
        frame["split"] = ""
    if deduplicate:
        frame = frame.drop_duplicates(subset=["text"], keep="first")
    return frame.reset_index(drop=True)


def train_test_frames(
    spec: DatasetSpec,
    frame: pd.DataFrame,
    test_size: float,
    seed: int,
) -> tuple[pd.DataFrame, pd.DataFrame, str]:
    if spec.has_split and set(frame["split"]).intersection({"train", "val", "test"}):
        train_frame = frame[frame["split"].isin(["train", "val"])].copy()
        test_frame = frame[frame["split"] == "test"].copy()
        return train_frame, test_frame, "provided_train_val_vs_test_split"

    train_frame, test_frame = train_test_split(
        frame,
        test_size=test_size,
        random_state=seed,
        stratify=frame["label"],
    )
    return train_frame.copy(), test_frame.copy(), f"stratified_{int((1 - test_size) * 100)}_{int(test_size * 100)}_split_seed{seed}"


def add_benchmark_test(path: Path) -> pd.DataFrame:
    benchmark = pd.read_csv(path)
    return pd.DataFrame(
        {
            "text": benchmark["text"].fillna("").astype(str),
            "label": benchmark["label"].astype(int),
            "dataset": "existing_79_row_benchmark",
            "split": "benchmark",
        }
    )


def pct(value: float) -> str:
    return f"{value * 100:.1f}%"


def main() -> None:
    parser = argparse.ArgumentParser(description="Run TF-IDF baselines across local processed datasets.")
    parser.add_argument("--output", type=Path, default=ROOT / "results" / "cross_dataset_baseline_summary.csv")
    parser.add_argument("--detailed-output", type=Path, default=ROOT / "results" / "cross_dataset_baseline_predictions.csv")
    parser.add_argument("--benchmark-csv", type=Path, default=ROOT / "benchmark_test.csv")
    parser.add_argument("--text-column", default="text")
    parser.add_argument("--label-column", default="label")
    parser.add_argument("--test-size", type=float, default=0.2)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--no-deduplicate", action="store_true", help="Keep duplicate texts instead of dropping them.")
    args = parser.parse_args()

    deduplicate = not args.no_deduplicate
    specs_by_name = {spec.name: spec for spec in DATASETS}
    loaded = {
        spec.name: normalized_frame(spec, args.text_column, args.label_column, deduplicate)
        for spec in DATASETS
    }
    splits = {
        spec.name: train_test_frames(spec, loaded[spec.name], args.test_size, args.seed)
        for spec in DATASETS
    }
    tests = {name: test for name, (_, test, _) in splits.items()}
    if args.benchmark_csv.exists():
        tests["existing_79_row_benchmark"] = add_benchmark_test(args.benchmark_csv)

    summary_rows: list[dict[str, float | int | str]] = []
    prediction_frames: list[pd.DataFrame] = []

    for train_name, (train_frame, _, split_policy) in splits.items():
        train_spec = specs_by_name[train_name]
        for model_name, pipeline in make_models().items():
            pipeline.fit(train_frame["text"], train_frame["label"])
            for test_name, test_frame in tests.items():
                predictions = pipeline.predict(test_frame["text"])
                row = {
                    "model": model_name,
                    "train_dataset": train_name,
                    "test_dataset": test_name,
                    "condition": "tfidf_cross_dataset_baseline",
                    "split_policy": split_policy,
                    "train_rows": len(train_frame),
                    "test_rows": len(test_frame),
                    "train_task_category": train_spec.task_category,
                    "train_label_meaning": train_spec.label_meaning,
                    "train_dataset_situation": train_spec.situation,
                    "deduplicated_text": deduplicate,
                }
                row.update(compute_metrics(test_frame["label"], predictions))
                summary_rows.append(row)

                prediction_frames.append(
                    pd.DataFrame(
                        {
                            "model": model_name,
                            "train_dataset": train_name,
                            "test_dataset": test_name,
                            "text": test_frame["text"].to_numpy(),
                            "true_label": test_frame["label"].to_numpy(),
                            "prediction": predictions,
                        }
                    )
                )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    summary = pd.DataFrame(summary_rows)
    summary.to_csv(args.output, index=False)
    pd.concat(prediction_frames, ignore_index=True).to_csv(args.detailed_output, index=False)

    display = summary[
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
        ]
    ].copy()
    for col in ["accuracy", "recall_positive", "f1_positive", "f1_macro"]:
        display[col] = display[col].map(pct)

    print("\nCross-Dataset TF-IDF Baseline Results")
    print(tabulate(display, headers="keys", tablefmt="github", showindex=False))
    print(f"Saved summary metrics to {args.output}")
    print(f"Saved detailed predictions to {args.detailed_output}")


if __name__ == "__main__":
    main()
