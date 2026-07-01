#!/usr/bin/env python3
"""Fine-tune one transformer model for binary Hinglish hate/offensive detection."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd
from datasets import Dataset
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from sklearn.model_selection import train_test_split
from transformers import AutoModelForSequenceClassification, AutoTokenizer, Trainer, TrainingArguments


ROOT = Path(__file__).resolve().parents[1]
MODEL_CHECKPOINTS = {
    "mbert": "bert-base-multilingual-cased",
    "muril": "google/muril-base-cased",
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


def load_binary_dataset(
    path: Path,
    text_column: str,
    label_column: str,
    cleaning: str,
    split_column: str | None = None,
) -> pd.DataFrame:
    frame = pd.read_csv(path)
    keep_columns = [text_column, label_column]
    if split_column and split_column in frame.columns:
        keep_columns.append(split_column)
    frame = frame[keep_columns].dropna(subset=[text_column, label_column])
    frame = frame.rename(columns={text_column: "text", label_column: "label"})
    frame["label"] = frame["label"].astype(int)

    cleaner = minimal_clean if cleaning == "minimal" else aggressive_clean
    frame["text"] = frame["text"].map(cleaner)
    frame = frame[frame["text"].str.len() > 0]
    return frame.reset_index(drop=True)


def split_dataset(
    frame: pd.DataFrame,
    split_column: str | None,
    train_splits: list[str],
    eval_split: str | None,
    test_size: float,
    seed: int,
) -> tuple[pd.DataFrame, pd.DataFrame, str]:
    if split_column and split_column in frame.columns and eval_split:
        train_frame = frame[frame[split_column].astype(str).isin(train_splits)].copy()
        eval_frame = frame[frame[split_column].astype(str) == eval_split].copy()
        if train_frame.empty or eval_frame.empty:
            raise ValueError(
                f"Split selection produced train={len(train_frame)} eval={len(eval_frame)} rows. "
                f"Check --split-column, --train-split, and --eval-split."
            )
        return train_frame, eval_frame, f"{split_column}:train={'+'.join(train_splits)},eval={eval_split}"

    train_frame, eval_frame = train_test_split(
        frame,
        test_size=test_size,
        random_state=seed,
        stratify=frame["label"],
    )
    return train_frame, eval_frame, f"stratified_{int((1 - test_size) * 100)}_{int(test_size * 100)}_seed{seed}"


def compute_metrics(eval_prediction) -> dict[str, float]:
    labels = eval_prediction.label_ids
    predictions = np.argmax(eval_prediction.predictions, axis=-1)
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
    return {
        "accuracy": accuracy_score(labels, predictions),
        "precision_hate": precision_hate,
        "recall_hate": recall_hate,
        "f1_hate": f1_hate,
        "precision_macro": precision_macro,
        "recall_macro": recall_macro,
        "f1_macro": f1_macro,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Fine-tune mBERT or MuRIL on a binary CSV dataset.")
    parser.add_argument("--model", choices=MODEL_CHECKPOINTS.keys(), required=True)
    parser.add_argument("--train-csv", type=Path, default=ROOT / "combined_hate_speech_dataset.csv")
    parser.add_argument("--text-column", default="text")
    parser.add_argument("--label-column", default="hate_label")
    parser.add_argument("--split-column", default=None, help="Optional split column for source-provided train/eval splits.")
    parser.add_argument("--train-split", action="append", default=None, help="Split value to use for training. May be repeated.")
    parser.add_argument("--eval-split", default=None, help="Split value to use for evaluation.")
    parser.add_argument("--output-dir", type=Path, default=None)
    parser.add_argument("--cleaning", choices=("minimal", "aggressive"), default="minimal")
    parser.add_argument("--max-length", type=int, default=128)
    parser.add_argument("--test-size", type=float, default=0.2)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--epochs", type=float, default=2)
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--learning-rate", type=float, default=2e-5)
    parser.add_argument("--weight-decay", type=float, default=0.01)
    parser.add_argument("--max-samples", type=int, default=None, help="Optional cap for quick smoke tests.")
    args = parser.parse_args()

    checkpoint = MODEL_CHECKPOINTS[args.model]
    output_dir = args.output_dir or (ROOT / "Models" / f"{args.model}_model")
    run_dir = ROOT / "runs" / args.model

    frame = load_binary_dataset(args.train_csv, args.text_column, args.label_column, args.cleaning, args.split_column)
    if args.max_samples is not None and len(frame) > args.max_samples:
        per_label = max(1, args.max_samples // max(frame["label"].nunique(), 1))
        sampled_parts = []
        for _, group in frame.groupby("label"):
            sampled_parts.append(group.sample(min(len(group), per_label), random_state=args.seed))
        frame = pd.concat(sampled_parts, ignore_index=True).sample(frac=1, random_state=args.seed).reset_index(drop=True)

    train_splits = args.train_split or ["train"]
    train_frame, eval_frame, split_policy = split_dataset(
        frame,
        args.split_column,
        train_splits,
        args.eval_split,
        args.test_size,
        args.seed,
    )

    tokenizer = AutoTokenizer.from_pretrained(checkpoint)

    def tokenize(batch):
        return tokenizer(batch["text"], padding="max_length", truncation=True, max_length=args.max_length)

    train_dataset = Dataset.from_pandas(train_frame.reset_index(drop=True)).map(tokenize, batched=True)
    eval_dataset = Dataset.from_pandas(eval_frame.reset_index(drop=True)).map(tokenize, batched=True)

    model = AutoModelForSequenceClassification.from_pretrained(checkpoint, num_labels=2)
    training_args = TrainingArguments(
        output_dir=str(run_dir),
        learning_rate=args.learning_rate,
        per_device_train_batch_size=args.batch_size,
        per_device_eval_batch_size=args.batch_size,
        num_train_epochs=args.epochs,
        weight_decay=args.weight_decay,
        eval_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="f1_macro",
        greater_is_better=True,
        report_to="none",
        seed=args.seed,
        dataloader_pin_memory=False,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        compute_metrics=compute_metrics,
    )

    trainer.train()
    metrics = trainer.evaluate()
    output_dir.mkdir(parents=True, exist_ok=True)
    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)

    metrics_path = output_dir / "eval_metrics.json"
    metrics_path.write_text(json.dumps(metrics, indent=2, sort_keys=True), encoding="utf-8")
    metadata = {
        "model": args.model,
        "base_checkpoint": checkpoint,
        "train_csv": str(args.train_csv),
        "text_column": args.text_column,
        "label_column": args.label_column,
        "split_policy": split_policy,
        "train_rows": len(train_frame),
        "eval_rows": len(eval_frame),
        "cleaning": args.cleaning,
        "max_length": args.max_length,
        "seed": args.seed,
        "epochs": args.epochs,
        "batch_size": args.batch_size,
        "learning_rate": args.learning_rate,
        "weight_decay": args.weight_decay,
    }
    (output_dir / "training_metadata.json").write_text(json.dumps(metadata, indent=2, sort_keys=True), encoding="utf-8")

    print(f"Saved model to {output_dir}")
    print(f"Saved metrics to {metrics_path}")
    print(f"Split policy: {split_policy}")
    print("Evaluation metrics:")
    for key, value in sorted(metrics.items()):
        print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
