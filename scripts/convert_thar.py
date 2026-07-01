#!/usr/bin/env python3
"""Convert THAR into the project schema."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "THAR" / "THAR-Dataset.csv"
OUT = ROOT / "data" / "processed" / "thar_religion.csv"


def main() -> None:
    if not RAW.exists():
        raise SystemExit("Missing THAR dataset. Clone https://github.com/aakash-dl/THAR into data/raw/THAR first.")

    frame = pd.read_csv(RAW)
    label_map = {"Non-AntiReligion": 0, "AntiReligion": 1}
    converted = pd.DataFrame(
        {
            "text": frame["Comment"].fillna("").astype(str),
            "label": frame["SubTask1"].map(label_map).astype(int),
            "dataset": "thar",
            "source": "youtube_comments",
            "language": "hindi_english_code_mixed",
            "target_group": frame["SubTask2"].fillna("none"),
            "identifier": frame["Identifier"],
            "subtask1_original": frame["SubTask1"],
            "subtask2_original": frame["SubTask2"].fillna("none"),
        }
    )
    converted = converted[converted["text"].str.strip().str.len() > 0].reset_index(drop=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    converted.to_csv(OUT, index=False)
    print(f"Wrote {len(converted):,} rows to {OUT}")
    print("Label mapping: Non-AntiReligion -> 0, AntiReligion -> 1")


if __name__ == "__main__":
    main()
