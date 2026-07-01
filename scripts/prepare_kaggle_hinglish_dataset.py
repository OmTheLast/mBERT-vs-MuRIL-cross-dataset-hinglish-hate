#!/usr/bin/env python3
"""Create processed files from the Kaggle Hinglish hate dataset."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "combined_hate_speech_dataset.csv"
OUT_DIR = ROOT / "data" / "processed"


def write_subset(frame: pd.DataFrame, name: str) -> None:
    path = OUT_DIR / f"{name}.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(path, index=False)
    print(f"Wrote {len(frame):,} rows to {path}")


def main() -> None:
    frame = pd.read_csv(RAW)
    standardized = pd.DataFrame(
        {
            "text": frame["text"].fillna("").astype(str),
            "label": frame["hate_label"].astype(int),
            "dataset": "kaggle_hinglish_hate_source",
            "source": frame.get("source", "unknown"),
            "language": frame.get("language", "unknown"),
        }
    )
    standardized = standardized.drop_duplicates(subset=["text", "label"]).reset_index(drop=True)

    write_subset(standardized, "kaggle_hinglish_hate_all")
    for language in sorted(standardized["language"].dropna().unique()):
        safe_language = str(language).replace("/", "_").replace(" ", "_").lower()
        output_name = "kaggle_hinglish_hate" if safe_language == "hinglish" else f"kaggle_hinglish_hate_{safe_language}"
        write_subset(standardized[standardized["language"] == language], output_name)


if __name__ == "__main__":
    main()
