#!/usr/bin/env python3
"""Evaluate local transformer checkpoints across registered processed datasets."""

from __future__ import annotations

import argparse
import re
import time
from dataclasses import dataclass
from pathlib import Path

import pandas as pd
import torch
from sklearn.metrics import accuracy_score, confusion_matrix, precision_recall_fscore_support
from sklearn.model_selection import train_test_split
from tabulate import tabulate
from transformers import AutoModelForSequenceClassification, AutoTokenizer


ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class DatasetSpec:
    name: str
    path: Path
    task_category: str
    label_meaning: str
    situation: str
    has_split: bool = False


@dataclass(frozen=True)
class CheckpointSpec:
    model: str
    checkpoint_path: Path
    train_dataset: str
    condition: str


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


DEFAULT_CHECKPOINTS = [
    CheckpointSpec(
        model="mbert",
        checkpoint_path=ROOT / "Models" / "mbert__train-kaggle_hinglish_hate__seed42__e2",
        train_dataset="kaggle_hinglish_hate",
        condition="transformer_trained_on_kaggle_hinglish_hate",
    ),
    CheckpointSpec(
        model="muril",
        checkpoint_path=ROOT / "Models" / "muril__train-kaggle_hinglish_hate__seed42__e2",
        train_dataset="kaggle_hinglish_hate",
        condition="transformer_trained_on_kaggle_hinglish_hate",
    ),
]


def minimal_clean(text: object) -> str:
    text = str(text)
    text = re.sub(r"http\S+|www\S+|https\S+", " URL ", text)
    text = re.sub(r"@\w+", " USER ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def aggressive_clean(text: object) -> str:
    text = minimal_clean(text).lower()
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def device() -> torch.device:
    if torch.cuda.is_available():
        return torch.device("cuda")
    if torch.backends.mps.is_available():
        return torch.device("mps")
    return torch.device("cpu")


def compute_metrics(labels: list[int], predictions: list[int]) -> dict[str, float | int]:
    precision_positive, recall_positive, f1_positive, _ = precision_recall_fscore_support(
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
        "precision_positive": precision_positive,
        "recall_positive": recall_positive,
        "f1_positive": f1_positive,
        "precision_macro": precision_macro,
        "recall_macro": recall_macro,
        "f1_macro": f1_macro,
        "tn": int(tn),
        "fp": int(fp),
        "fn": int(fn),
        "tp": int(tp),
    }


def normalized_frame(
    spec: DatasetSpec,
    text_column: str,
    label_column: str,
    cleaning: str,
    deduplicate: bool,
) -> pd.DataFrame:
    frame = pd.read_csv(spec.path)
    keep_columns = [text_column, label_column]
    if spec.has_split and "split" in frame.columns:
        keep_columns.append("split")
    frame = frame[keep_columns].dropna(subset=[text_column, label_column]).copy()
    frame = frame.rename(columns={text_column: "text", label_column: "label"})
    frame["label"] = frame["label"].astype(int)
    cleaner = minimal_clean if cleaning == "minimal" else aggressive_clean
    frame["text"] = frame["text"].map(cleaner)
    frame = frame[frame["text"].str.len() > 0]
    frame["dataset"] = spec.name
    if "split" not in frame.columns:
        frame["split"] = ""
    if deduplicate:
        frame = frame.drop_duplicates(subset=["text"], keep="first")
    return frame.reset_index(drop=True)


def evaluation_frame(
    spec: DatasetSpec,
    frame: pd.DataFrame,
    test_size: float,
    seed: int,
) -> tuple[pd.DataFrame, str]:
    if spec.has_split and set(frame["split"]).intersection({"train", "val", "test"}):
        return frame[frame["split"] == "test"].copy(), "provided_test_split"

    _, test_frame = train_test_split(
        frame,
        test_size=test_size,
        random_state=seed,
        stratify=frame["label"],
    )
    return test_frame.copy(), f"stratified_{int((1 - test_size) * 100)}_{int(test_size * 100)}_split_seed{seed}"


def benchmark_frame(path: Path, cleaning: str) -> pd.DataFrame:
    frame = pd.read_csv(path)
    cleaner = minimal_clean if cleaning == "minimal" else aggressive_clean
    return pd.DataFrame(
        {
            "text": frame["text"].fillna("").astype(str).map(cleaner),
            "label": frame["label"].astype(int),
            "dataset": "existing_79_row_benchmark",
            "split": "benchmark",
        }
    )


class BatchedTransformer:
    def __init__(self, checkpoint: CheckpointSpec, max_length: int, run_device: torch.device) -> None:
        self.checkpoint = checkpoint
        self.max_length = max_length
        self.device = run_device
        self.tokenizer = AutoTokenizer.from_pretrained(checkpoint.checkpoint_path)
        self.model = AutoModelForSequenceClassification.from_pretrained(checkpoint.checkpoint_path).to(self.device)
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
                probabilities = torch.nn.functional.softmax(logits, dim=-1)
                batch_predictions = probabilities.argmax(dim=-1)
                batch_confidences = probabilities.max(dim=-1).values

            predictions.extend(batch_predictions.cpu().tolist())
            confidences.extend(batch_confidences.cpu().tolist())

        avg_latency_ms = ((time.perf_counter() - start) * 1000) / max(len(texts), 1)
        return predictions, confidences, avg_latency_ms


def checkpoint_specs(args: argparse.Namespace) -> list[CheckpointSpec]:
    if args.checkpoint:
        specs: list[CheckpointSpec] = []
        for raw in args.checkpoint:
            parts = raw.split(":", 3)
            if len(parts) != 4:
                raise SystemExit("--checkpoint must be formatted as model:train_dataset:condition:path")
            model, train_dataset, condition, path = parts
            specs.append(
                CheckpointSpec(
                    model=model,
                    checkpoint_path=Path(path),
                    train_dataset=train_dataset,
                    condition=condition,
                )
            )
        return specs
    return DEFAULT_CHECKPOINTS


def pct(value: float) -> str:
    return f"{value * 100:.1f}%"


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate transformer checkpoints across local datasets.")
    parser.add_argument("--output", type=Path, default=ROOT / "results" / "transformer_cross_dataset_summary.csv")
    parser.add_argument("--detailed-output", type=Path, default=ROOT / "results" / "transformer_cross_dataset_predictions.csv")
    parser.add_argument("--benchmark-csv", type=Path, default=ROOT / "benchmark_test.csv")
    parser.add_argument("--text-column", default="text")
    parser.add_argument("--label-column", default="label")
    parser.add_argument("--cleaning", choices=("minimal", "aggressive"), default="minimal")
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--max-length", type=int, default=128)
    parser.add_argument("--test-size", type=float, default=0.2)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--no-deduplicate", action="store_true", help="Keep duplicate texts instead of dropping them.")
    parser.add_argument(
        "--checkpoint",
        action="append",
        help="Optional checkpoint spec formatted as model:train_dataset:condition:path. May be repeated.",
    )
    args = parser.parse_args()

    deduplicate = not args.no_deduplicate
    specs_by_name = {spec.name: spec for spec in DATASETS}
    tests: dict[str, tuple[pd.DataFrame, str]] = {}
    for spec in DATASETS:
        frame = normalized_frame(spec, args.text_column, args.label_column, args.cleaning, deduplicate)
        tests[spec.name] = evaluation_frame(spec, frame, args.test_size, args.seed)
    if args.benchmark_csv.exists():
        tests["existing_79_row_benchmark"] = (benchmark_frame(args.benchmark_csv, args.cleaning), "benchmark")

    run_device = device()
    checkpoints = checkpoint_specs(args)
    summary_rows: list[dict[str, float | int | str | bool]] = []
    detailed_rows: list[pd.DataFrame] = []

    print(f"Using device: {run_device}")
    for checkpoint in checkpoints:
        print(f"Loading {checkpoint.model} from {checkpoint.checkpoint_path}")
        classifier = BatchedTransformer(checkpoint, args.max_length, run_device)
        for test_dataset, (test_frame, split_policy) in tests.items():
            test_spec = specs_by_name.get(test_dataset)
            texts = test_frame["text"].fillna("").astype(str).tolist()
            labels = test_frame["label"].astype(int).tolist()
            predictions, confidences, avg_latency_ms = classifier.predict(texts, args.batch_size)

            row = {
                "model": checkpoint.model,
                "checkpoint_path": str(checkpoint.checkpoint_path),
                "train_dataset": checkpoint.train_dataset,
                "test_dataset": test_dataset,
                "condition": checkpoint.condition,
                "split_policy": split_policy,
                "test_rows": len(test_frame),
                "test_task_category": test_spec.task_category if test_spec else "hate/sanity-benchmark",
                "test_label_meaning": test_spec.label_meaning if test_spec else "0 = non-hate, 1 = hate",
                "test_dataset_situation": test_spec.situation if test_spec else "small 79-row sanity benchmark",
                "cleaning": args.cleaning,
                "deduplicated_text": deduplicate,
                "avg_latency_ms": avg_latency_ms,
            }
            row.update(compute_metrics(labels, predictions))
            summary_rows.append(row)

            detailed_rows.append(
                pd.DataFrame(
                    {
                        "model": checkpoint.model,
                        "checkpoint_path": str(checkpoint.checkpoint_path),
                        "train_dataset": checkpoint.train_dataset,
                        "test_dataset": test_dataset,
                        "text": texts,
                        "true_label": labels,
                        "prediction": predictions,
                        "confidence": confidences,
                    }
                )
            )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    summary = pd.DataFrame(summary_rows)
    summary.to_csv(args.output, index=False)
    pd.concat(detailed_rows, ignore_index=True).to_csv(args.detailed_output, index=False)

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

    print("\nTransformer Cross-Dataset Evaluation")
    print(tabulate(display, headers="keys", tablefmt="github", showindex=False))
    print(f"Saved summary metrics to {args.output}")
    print(f"Saved detailed predictions to {args.detailed_output}")


if __name__ == "__main__":
    main()
