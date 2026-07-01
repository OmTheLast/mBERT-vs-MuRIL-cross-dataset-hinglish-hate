#!/usr/bin/env python3
"""Build mixed-dataset training CSVs without leaking held-out test rows."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split


ROOT = Path(__file__).resolve().parents[1]

DATASETS = {
    "kaggle_hinglish_hate": {
        "path": ROOT / "data" / "processed" / "kaggle_hinglish_hate.csv",
        "label_meaning": "0 = non-hate, 1 = hate",
        "source_split": "stratified_train_seed{seed}",
    },
    "cm_splits_codemixed": {
        "path": ROOT / "data" / "processed" / "cm_splits_codemixed.csv",
        "label_meaning": "0 = not offensive, 1 = offensive",
        "source_split": "provided_train_plus_val",
    },
    "thar_religion": {
        "path": ROOT / "data" / "processed" / "thar_religion.csv",
        "label_meaning": "0 = Non-AntiReligion, 1 = AntiReligion",
        "source_split": "stratified_train_seed{seed}",
    },
}

MIXES = {
    "kaggle_plus_cm": ["kaggle_hinglish_hate", "cm_splits_codemixed"],
    "kaggle_plus_thar": ["kaggle_hinglish_hate", "thar_religion"],
    "cm_plus_thar": ["cm_splits_codemixed", "thar_religion"],
    "all_three": ["kaggle_hinglish_hate", "cm_splits_codemixed", "thar_religion"],
}


def load_training_portion(dataset_id: str, seed: int, test_size: float) -> pd.DataFrame:
    spec = DATASETS[dataset_id]
    frame = pd.read_csv(spec["path"])
    frame = frame.dropna(subset=["text", "label"]).copy()
    frame["label"] = frame["label"].astype(int)

    if dataset_id == "cm_splits_codemixed":
        if "split" not in frame.columns:
            raise ValueError("CM dataset must contain a split column.")
        train = frame[frame["split"].astype(str).isin(["train", "val"])].copy()
        split_policy = spec["source_split"]
    else:
        train, _ = train_test_split(
            frame,
            test_size=test_size,
            random_state=seed,
            stratify=frame["label"],
        )
        split_policy = spec["source_split"].format(seed=seed)

    train = train[["text", "label"]].copy()
    train["source_dataset"] = dataset_id
    train["label_meaning"] = spec["label_meaning"]
    train["source_split_policy"] = split_policy
    return train.reset_index(drop=True)


def build_mix(name: str, dataset_ids: list[str], seed: int, test_size: float, output_dir: Path) -> pd.DataFrame:
    parts = [load_training_portion(dataset_id, seed=seed, test_size=test_size) for dataset_id in dataset_ids]
    mixed = pd.concat(parts, ignore_index=True)
    mixed = mixed.sample(frac=1, random_state=seed).reset_index(drop=True)
    mixed["mix_id"] = name

    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"mixed_train_{name}__seed{seed}.csv"
    mixed.to_csv(output_path, index=False)
    return mixed


def summarize_mix(name: str, frame: pd.DataFrame) -> dict[str, object]:
    counts = frame.groupby(["source_dataset", "label"]).size().unstack(fill_value=0)
    return {
        "mix_id": name,
        "rows": len(frame),
        "label_0": int((frame["label"] == 0).sum()),
        "label_1": int((frame["label"] == 1).sum()),
        "positive_rate": (frame["label"] == 1).mean(),
        "source_breakdown": "; ".join(
            f"{idx}:0={int(row.get(0, 0))},1={int(row.get(1, 0))}" for idx, row in counts.iterrows()
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Build leakage-safe mixed training datasets.")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--test-size", type=float, default=0.2)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "data" / "processed")
    parser.add_argument("--summary-output", type=Path, default=ROOT / "results" / "mixed_training_set_summary.csv")
    args = parser.parse_args()

    summaries = []
    for name, dataset_ids in MIXES.items():
        frame = build_mix(name, dataset_ids, seed=args.seed, test_size=args.test_size, output_dir=args.output_dir)
        summaries.append(summarize_mix(name, frame))

    summary = pd.DataFrame(summaries)
    args.summary_output.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(args.summary_output, index=False)

    print(summary.to_string(index=False))
    print(f"\nSaved summary to {args.summary_output}")


if __name__ == "__main__":
    main()
