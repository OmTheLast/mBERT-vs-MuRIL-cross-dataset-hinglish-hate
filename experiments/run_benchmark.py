#!/usr/bin/env python3
"""Batch benchmark local mBERT and MuRIL checkpoints on a labeled CSV file."""

from __future__ import annotations

import argparse
import time
from pathlib import Path

import pandas as pd
import torch
from sklearn.metrics import accuracy_score, confusion_matrix, precision_recall_fscore_support
from tabulate import tabulate
from transformers import AutoModelForSequenceClassification, AutoTokenizer


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MODELS = {
    "mbert": ROOT / "Models" / "mbert_model",
    "muril": ROOT / "Models" / "muril_model",
}


class BatchedClassifier:
    def __init__(self, name: str, path: Path, max_length: int) -> None:
        self.name = name
        self.path = path
        self.max_length = max_length
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = AutoTokenizer.from_pretrained(path)
        self.model = AutoModelForSequenceClassification.from_pretrained(path).to(self.device)
        self.model.eval()

    def predict(self, texts: list[str], batch_size: int) -> tuple[list[int], list[float], float]:
        predictions: list[int] = []
        confidences: list[float] = []
        start = time.perf_counter()

        for offset in range(0, len(texts), batch_size):
            batch = texts[offset : offset + batch_size]
            inputs = self.tokenizer(
                batch,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=self.max_length,
            ).to(self.device)

            with torch.no_grad():
                logits = self.model(**inputs).logits
                probs = torch.nn.functional.softmax(logits, dim=-1)
                batch_predictions = probs.argmax(dim=-1)
                batch_confidences = probs.max(dim=-1).values

            predictions.extend(batch_predictions.cpu().tolist())
            confidences.extend(batch_confidences.cpu().tolist())

        latency_ms = (time.perf_counter() - start) * 1000
        return predictions, confidences, latency_ms / max(len(texts), 1)


def binary_metrics(labels: list[int], predictions: list[int]) -> dict[str, float | int]:
    precision, recall, f1, _ = precision_recall_fscore_support(
        labels,
        predictions,
        average="binary",
        zero_division=0,
    )
    macro_precision, macro_recall, macro_f1, _ = precision_recall_fscore_support(
        labels,
        predictions,
        average="macro",
        zero_division=0,
    )
    tn, fp, fn, tp = confusion_matrix(labels, predictions, labels=[0, 1]).ravel()
    return {
        "accuracy": accuracy_score(labels, predictions),
        "precision_hate": precision,
        "recall_hate": recall,
        "f1_hate": f1,
        "precision_macro": macro_precision,
        "recall_macro": macro_recall,
        "f1_macro": macro_f1,
        "tn": int(tn),
        "fp": int(fp),
        "fn": int(fn),
        "tp": int(tp),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Benchmark local checkpoints on a binary hate-speech CSV.")
    parser.add_argument("--input", type=Path, default=ROOT / "benchmark_test.csv")
    parser.add_argument("--output", type=Path, default=ROOT / "results" / "ad_hoc_benchmark_detailed.csv")
    parser.add_argument("--summary-output", type=Path, default=ROOT / "results" / "ad_hoc_benchmark_summary.csv")
    parser.add_argument("--text-column", default="text")
    parser.add_argument("--label-column", default="label")
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--max-length", type=int, default=128)
    parser.add_argument("--mbert-path", type=Path, default=DEFAULT_MODELS["mbert"])
    parser.add_argument("--muril-path", type=Path, default=DEFAULT_MODELS["muril"])
    parser.add_argument("--evaluation-name", default=None, help="Human-readable evaluation label saved in the summary.")
    parser.add_argument("--dataset-name", default=None, help="Dataset/test-set label saved in the summary.")
    parser.add_argument("--condition", default=None, help="Model/checkpoint condition, e.g. pre_cleanup or hinglish_retrained.")
    args = parser.parse_args()

    data = pd.read_csv(args.input)
    texts = data[args.text_column].fillna("").astype(str).tolist()
    labels = data[args.label_column].astype(int).tolist()
    evaluation_name = args.evaluation_name or args.input.stem
    dataset_name = args.dataset_name or args.input.stem
    condition = args.condition or "unspecified"

    args.output.parent.mkdir(parents=True, exist_ok=True)
    models = {
        "mbert": BatchedClassifier("mBERT", args.mbert_path, args.max_length),
        "muril": BatchedClassifier("MuRIL", args.muril_path, args.max_length),
    }

    summary_rows: list[dict[str, float | int | str]] = []
    detailed = pd.DataFrame({"text": texts, "true_label": labels})

    for key, classifier in models.items():
        predictions, confidences, latency = classifier.predict(texts, args.batch_size)
        detailed[f"{key}_prediction"] = predictions
        detailed[f"{key}_confidence"] = confidences
        detailed[f"{key}_avg_latency_ms"] = latency

        row = {
            "evaluation": evaluation_name,
            "dataset": dataset_name,
            "condition": condition,
            "model": key,
            "checkpoint_path": str(classifier.path),
            "avg_latency_ms": latency,
        }
        row.update(binary_metrics(labels, predictions))
        summary_rows.append(row)

    detailed.to_csv(args.output, index=False)
    summary = pd.DataFrame(summary_rows)
    summary.to_csv(args.summary_output, index=False)
    display = summary[
        [
            "evaluation",
            "condition",
            "model",
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

    print("\nBenchmark Results")
    print(tabulate(display, headers="keys", tablefmt="github", showindex=False))
    print(f"Saved detailed predictions to {args.output}")
    print(f"Saved summary metrics to {args.summary_output}")


if __name__ == "__main__":
    main()
