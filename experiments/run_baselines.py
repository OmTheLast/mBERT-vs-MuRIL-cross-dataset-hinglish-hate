#!/usr/bin/env python3
"""Run TF-IDF baselines for the Hinglish hate speech project."""

from __future__ import annotations

import argparse
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


def metrics(labels, predictions) -> dict[str, float | int]:
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
        "precision_hate": precision_hate,
        "recall_hate": recall_hate,
        "f1_hate": f1_hate,
        "precision_macro": precision_macro,
        "recall_macro": recall_macro,
        "f1_macro": f1_macro,
        "tn": int(tn),
        "fp": int(fp),
        "fn": int(fn),
        "tp": int(tp),
    }


def make_models() -> dict[str, Pipeline]:
    vectorizer = TfidfVectorizer(
        analyzer="word",
        ngram_range=(1, 2),
        min_df=2,
        max_features=50000,
        sublinear_tf=True,
    )
    return {
        "tfidf_logistic_regression": Pipeline(
            [
                ("tfidf", vectorizer),
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


def main() -> None:
    parser = argparse.ArgumentParser(description="Run simple TF-IDF baselines.")
    parser.add_argument("--train-csv", type=Path, default=ROOT / "data" / "processed" / "kaggle_hinglish_hate.csv")
    parser.add_argument("--benchmark-csv", type=Path, default=ROOT / "benchmark_test.csv")
    parser.add_argument("--text-column", default="text")
    parser.add_argument("--label-column", default="label")
    parser.add_argument("--output", type=Path, default=ROOT / "results" / "baseline_summary.csv")
    parser.add_argument("--detailed-output", type=Path, default=ROOT / "results" / "baseline_benchmark_detailed.csv")
    parser.add_argument("--test-size", type=float, default=0.2)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--train-dataset-name", default="kaggle_hinglish_hate")
    parser.add_argument("--benchmark-name", default="benchmark_test_79")
    args = parser.parse_args()

    frame = pd.read_csv(args.train_csv)
    frame = frame[[args.text_column, args.label_column]].dropna()
    frame[args.text_column] = frame[args.text_column].astype(str)
    frame[args.label_column] = frame[args.label_column].astype(int)

    train_frame, eval_frame = train_test_split(
        frame,
        test_size=args.test_size,
        random_state=args.seed,
        stratify=frame[args.label_column],
    )

    benchmark = pd.read_csv(args.benchmark_csv)
    benchmark_texts = benchmark[args.text_column].fillna("").astype(str)
    benchmark_labels = benchmark[args.label_column].astype(int)

    summary_rows: list[dict[str, float | int | str]] = []
    detailed = benchmark[[args.text_column, args.label_column]].rename(columns={args.label_column: "true_label"})

    for model_name, pipeline in make_models().items():
        pipeline.fit(train_frame[args.text_column], train_frame[args.label_column])

        eval_predictions = pipeline.predict(eval_frame[args.text_column])
        eval_row = {
            "model": model_name,
            "evaluation": f"{args.train_dataset_name}_validation",
            "train_dataset": args.train_dataset_name,
            "test_dataset": f"{args.train_dataset_name}_validation_split",
            "condition": "tfidf_baseline_80_20_stratified",
        }
        eval_row.update(metrics(eval_frame[args.label_column], eval_predictions))
        summary_rows.append(eval_row)

        benchmark_predictions = pipeline.predict(benchmark_texts)
        benchmark_row = {
            "model": model_name,
            "evaluation": args.benchmark_name,
            "train_dataset": args.train_dataset_name,
            "test_dataset": args.benchmark_name,
            "condition": "tfidf_baseline_train_kaggle_hinglish_hate_test_benchmark",
        }
        benchmark_row.update(metrics(benchmark_labels, benchmark_predictions))
        summary_rows.append(benchmark_row)
        detailed[f"{model_name}_prediction"] = benchmark_predictions

    args.output.parent.mkdir(parents=True, exist_ok=True)
    summary = pd.DataFrame(summary_rows)
    summary.to_csv(args.output, index=False)
    detailed.to_csv(args.detailed_output, index=False)

    display = summary[
        [
            "model",
            "evaluation",
            "condition",
            "accuracy",
            "precision_hate",
            "recall_hate",
            "f1_hate",
            "f1_macro",
            "tn",
            "fp",
            "fn",
            "tp",
        ]
    ].copy()
    for col in ["accuracy", "precision_hate", "recall_hate", "f1_hate", "f1_macro"]:
        display[col] = display[col].map(lambda value: f"{value * 100:.1f}%")

    print("\nTF-IDF Baseline Results")
    print(tabulate(display, headers="keys", tablefmt="github", showindex=False))
    print(f"Saved baseline summary to {args.output}")
    print(f"Saved baseline benchmark predictions to {args.detailed_output}")


if __name__ == "__main__":
    main()
