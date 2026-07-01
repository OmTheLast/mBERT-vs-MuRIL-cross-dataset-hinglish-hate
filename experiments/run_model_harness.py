#!/usr/bin/env python3
"""Run registered mBERT/MuRIL checkpoints on CSV rows or ad-hoc text.

This is a lightweight harness for quick testing outside the full cross-dataset
matrix. Use it when you want one or more local transformer checkpoints to
predict on a new CSV, a benchmark file, or a few hand-written examples.
"""

from __future__ import annotations

import argparse
import re
import time
from dataclasses import dataclass
from pathlib import Path

import pandas as pd
import torch
from sklearn.metrics import accuracy_score, confusion_matrix, precision_recall_fscore_support
from tabulate import tabulate
from transformers import AutoModelForSequenceClassification, AutoTokenizer


ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class ModelSpec:
    key: str
    model_family: str
    train_dataset: str
    condition: str
    path: Path
    paper_use: str


MODEL_REGISTRY = {
    "mbert_kaggle_hinglish_hate": ModelSpec(
        key="mbert_kaggle_hinglish_hate",
        model_family="mbert",
        train_dataset="kaggle_hinglish_hate",
        condition="trained_on_kaggle_hinglish_hate",
        path=ROOT / "Models" / "mbert__train-kaggle_hinglish_hate__seed42__e2",
        paper_use="controlled result",
    ),
    "muril_kaggle_hinglish_hate": ModelSpec(
        key="muril_kaggle_hinglish_hate",
        model_family="muril",
        train_dataset="kaggle_hinglish_hate",
        condition="trained_on_kaggle_hinglish_hate",
        path=ROOT / "Models" / "muril__train-kaggle_hinglish_hate__seed42__e2",
        paper_use="controlled result",
    ),
    "mbert_cm_splits_codemixed": ModelSpec(
        key="mbert_cm_splits_codemixed",
        model_family="mbert",
        train_dataset="cm_splits_codemixed",
        condition="trained_on_cm_splits_codemixed",
        path=ROOT / "Models" / "mbert__train-cm_splits_codemixed__seed42__e2",
        paper_use="controlled result",
    ),
    "muril_cm_splits_codemixed": ModelSpec(
        key="muril_cm_splits_codemixed",
        model_family="muril",
        train_dataset="cm_splits_codemixed",
        condition="trained_on_cm_splits_codemixed",
        path=ROOT / "Models" / "muril__train-cm_splits_codemixed__seed42__e2",
        paper_use="controlled result",
    ),
    "mbert_thar_religion": ModelSpec(
        key="mbert_thar_religion",
        model_family="mbert",
        train_dataset="thar_religion",
        condition="trained_on_thar_religion",
        path=ROOT / "Models" / "mbert__train-thar_religion__seed42__e2",
        paper_use="controlled result",
    ),
    "muril_thar_religion": ModelSpec(
        key="muril_thar_religion",
        model_family="muril",
        train_dataset="thar_religion",
        condition="trained_on_thar_religion",
        path=ROOT / "Models" / "muril__train-thar_religion__seed42__e2",
        paper_use="controlled result",
    ),
    "mbert_session_start": ModelSpec(
        key="mbert_session_start",
        model_family="mbert",
        train_dataset="unknown_existing_checkpoint",
        condition="existing_checkpoint_at_session_start",
        path=ROOT / "Models" / "mbert_model",
        paper_use="historical/context only",
    ),
    "muril_session_start": ModelSpec(
        key="muril_session_start",
        model_family="muril",
        train_dataset="unknown_existing_checkpoint",
        condition="existing_checkpoint_at_session_start",
        path=ROOT / "Models" / "muril_model",
        paper_use="historical/context only",
    ),
}


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


def load_input(args: argparse.Namespace) -> pd.DataFrame:
    if args.input_csv:
        frame = pd.read_csv(args.input_csv)
        if args.text_column not in frame.columns:
            raise SystemExit(f"Text column `{args.text_column}` was not found in {args.input_csv}.")
        output = pd.DataFrame({"text": frame[args.text_column].fillna("").astype(str)})
        if args.label_column and args.label_column in frame.columns:
            output["label"] = frame[args.label_column].astype(int)
        return output

    if args.text:
        return pd.DataFrame({"text": args.text})

    raise SystemExit("Provide either --input-csv or one or more --text values.")


def selected_models(raw_keys: list[str]) -> list[ModelSpec]:
    if raw_keys == ["all"]:
        specs = [spec for spec in MODEL_REGISTRY.values() if spec.path.exists()]
    else:
        missing_keys = [key for key in raw_keys if key not in MODEL_REGISTRY]
        if missing_keys:
            valid = ", ".join(sorted(MODEL_REGISTRY))
            raise SystemExit(f"Unknown model key(s): {', '.join(missing_keys)}. Valid keys: {valid}")
        specs = [MODEL_REGISTRY[key] for key in raw_keys]

    missing_paths = [spec for spec in specs if not spec.path.exists()]
    if missing_paths:
        missing = "\n".join(f"- {spec.key}: {spec.path}" for spec in missing_paths)
        raise SystemExit(f"These checkpoint paths do not exist yet:\n{missing}")
    return specs


def predict(spec: ModelSpec, texts: list[str], batch_size: int, max_length: int, run_device: torch.device) -> tuple[list[int], list[float], float]:
    tokenizer = AutoTokenizer.from_pretrained(spec.path)
    model = AutoModelForSequenceClassification.from_pretrained(spec.path).to(run_device)
    model.eval()

    predictions: list[int] = []
    positive_scores: list[float] = []
    start = time.perf_counter()
    for offset in range(0, len(texts), batch_size):
        batch = texts[offset : offset + batch_size]
        inputs = tokenizer(
            batch,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=max_length,
        ).to(run_device)
        with torch.no_grad():
            logits = model(**inputs).logits
            probabilities = torch.nn.functional.softmax(logits, dim=-1)
        predictions.extend(probabilities.argmax(dim=-1).cpu().tolist())
        positive_scores.extend(probabilities[:, 1].cpu().tolist())

    avg_latency_ms = ((time.perf_counter() - start) * 1000) / max(len(texts), 1)
    return predictions, positive_scores, avg_latency_ms


def metrics(labels: pd.Series, predictions: list[int]) -> dict[str, float | int]:
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


def pct(value: float) -> str:
    return f"{value * 100:.1f}%"


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate or demo local mBERT/MuRIL checkpoints.")
    parser.add_argument("--model-key", action="append", default=None, help="Registered model key. Use `all` for every existing registered checkpoint.")
    parser.add_argument("--list-models", action="store_true", help="Print registered harness model keys and exit.")
    parser.add_argument("--input-csv", type=Path, default=None)
    parser.add_argument("--text", action="append", default=None, help="Ad-hoc text to classify. May be repeated.")
    parser.add_argument("--text-column", default="text")
    parser.add_argument("--label-column", default="label")
    parser.add_argument("--output", type=Path, default=ROOT / "results" / "harness_predictions.csv")
    parser.add_argument("--summary-output", type=Path, default=ROOT / "results" / "harness_summary.csv")
    parser.add_argument("--cleaning", choices=("minimal", "aggressive"), default="minimal")
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--max-length", type=int, default=128)
    args = parser.parse_args()

    if args.list_models:
        rows = [
            {
                "key": spec.key,
                "family": spec.model_family,
                "train_dataset": spec.train_dataset,
                "exists": spec.path.exists(),
                "path": str(spec.path),
                "paper_use": spec.paper_use,
            }
            for spec in MODEL_REGISTRY.values()
        ]
        print(tabulate(rows, headers="keys", tablefmt="github"))
        return

    specs = selected_models(args.model_key or ["all"])
    frame = load_input(args)
    cleaner = minimal_clean if args.cleaning == "minimal" else aggressive_clean
    frame["text"] = frame["text"].map(cleaner)
    frame = frame[frame["text"].str.len() > 0].reset_index(drop=True)
    texts = frame["text"].tolist()
    run_device = device()

    prediction_frames: list[pd.DataFrame] = []
    summary_rows: list[dict[str, float | int | str]] = []
    print(f"Using device: {run_device}")

    for spec in specs:
        print(f"Loading {spec.key} from {spec.path}")
        predictions, positive_scores, avg_latency_ms = predict(spec, texts, args.batch_size, args.max_length, run_device)
        pred_frame = pd.DataFrame(
            {
                "model_key": spec.key,
                "model_family": spec.model_family,
                "train_dataset": spec.train_dataset,
                "condition": spec.condition,
                "text": texts,
                "prediction": predictions,
                "positive_score": positive_scores,
            }
        )
        if "label" in frame.columns:
            pred_frame["true_label"] = frame["label"].to_numpy()
            row = {
                "model_key": spec.key,
                "model_family": spec.model_family,
                "train_dataset": spec.train_dataset,
                "condition": spec.condition,
                "rows": len(frame),
                "avg_latency_ms": avg_latency_ms,
            }
            row.update(metrics(frame["label"], predictions))
            summary_rows.append(row)
        prediction_frames.append(pred_frame)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    predictions_out = pd.concat(prediction_frames, ignore_index=True)
    predictions_out.to_csv(args.output, index=False)

    display = predictions_out[["model_key", "train_dataset", "prediction", "positive_score", "text"]].copy()
    display["positive_score"] = display["positive_score"].map(lambda value: f"{value:.3f}")
    print("\nPredictions")
    print(tabulate(display.head(40), headers="keys", tablefmt="github", showindex=False))
    if len(display) > 40:
        print(f"... showing first 40 of {len(display)} prediction rows")

    if summary_rows:
        summary = pd.DataFrame(summary_rows)
        summary.to_csv(args.summary_output, index=False)
        summary_display = summary[
            ["model_key", "train_dataset", "rows", "accuracy", "recall_positive", "f1_positive", "f1_macro", "tn", "fp", "fn", "tp"]
        ].copy()
        for col in ["accuracy", "recall_positive", "f1_positive", "f1_macro"]:
            summary_display[col] = summary_display[col].map(pct)
        print("\nHarness Metrics")
        print(tabulate(summary_display, headers="keys", tablefmt="github", showindex=False))
        print(f"Saved harness summary to {args.summary_output}")

    print(f"Saved harness predictions to {args.output}")


if __name__ == "__main__":
    main()
