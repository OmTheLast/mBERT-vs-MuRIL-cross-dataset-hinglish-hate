#!/usr/bin/env python3
"""Convert the cm-hate-speech-detection dataset into the project schema."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw" / "cm-hate-speech-detection" / "data"
OUT_DIR = ROOT / "data" / "processed"


def convert_frame(frame: pd.DataFrame, dataset_name: str, source_name: str) -> pd.DataFrame:
    converted = pd.DataFrame(
        {
            "text": frame["tweet_text"].fillna("").astype(str),
            "label": frame["offense"].astype(int),
            "dataset": dataset_name,
            "source": source_name,
            "language": frame["codemixed"].map({1: "hinglish_or_code_mixed", 0: "non_codemixed_or_unknown"}).fillna("unknown"),
            "tweet_id": frame["tweet_id"],
            "aggression": frame["aggression"],
            "offense": frame["offense"],
            "codemixed": frame["codemixed"],
        }
    )
    converted = converted[converted["text"].str.strip().str.len() > 0]
    return converted.reset_index(drop=True)


def write_csv(frame: pd.DataFrame, name: str) -> None:
    path = OUT_DIR / f"{name}.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(path, index=False)
    print(f"Wrote {len(frame):,} rows to {path}")


def main() -> None:
    filled_path = RAW_DIR / "filled_10k.csv"
    if not filled_path.exists():
        raise SystemExit(f"Missing {filled_path}. Clone https://github.com/shikharras/cm-hate-speech-detection first.")

    full = convert_frame(pd.read_csv(filled_path), "cm_hate_speech_filled_10k", "filled_10k.csv")
    write_csv(full, "cm_filled_10k_all")
    write_csv(full[full["codemixed"] == 1], "cm_filled_10k_codemixed")

    split_frames = []
    for split_name in ("train", "val", "test"):
        split_path = RAW_DIR / "splits" / f"{split_name}.csv"
        if not split_path.exists():
            continue
        split = convert_frame(pd.read_csv(split_path), "cm_hate_speech_splits", f"splits/{split_name}.csv")
        split["split"] = split_name
        write_csv(split, f"cm_{split_name}_all")
        write_csv(split[split["codemixed"] == 1], f"cm_{split_name}_codemixed")
        split_frames.append(split)

    if split_frames:
        combined_splits = pd.concat(split_frames, ignore_index=True)
        write_csv(combined_splits, "cm_splits_all")
        write_csv(combined_splits[combined_splits["codemixed"] == 1], "cm_splits_codemixed")

    tweet_id_only = RAW_DIR / "hinglish_hatespeech.csv"
    if tweet_id_only.exists():
        note = OUT_DIR / "cm_hinglish_hatespeech_tweet_id_only_NOTE.txt"
        note.write_text(
            "data/raw/cm-hate-speech-detection/data/hinglish_hatespeech.csv contains tweet IDs and labels, "
            "but no tweet text. It is not directly usable for model training until texts are available.\n",
            encoding="utf-8",
        )
        print(f"Wrote note to {note}")


if __name__ == "__main__":
    main()
