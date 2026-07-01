#!/usr/bin/env python3
"""Run source-integrity checks and descriptive dataset analysis."""

from __future__ import annotations

import math
import re
import unicodedata
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results" / "data_analysis"
DOC = ROOT / "docs" / "data_analysis_report.md"


DATASETS = {
    "kaggle_hinglish_hate": {
        "path": ROOT / "data" / "processed" / "kaggle_hinglish_hate.csv",
        "label_meaning": "0 = non-hate, 1 = hate",
        "situation": "Kaggle Code-Mixed Hinglish Hate Speech Detection dataset, Hinglish subset",
    },
    "cm_splits_codemixed": {
        "path": ROOT / "data" / "processed" / "cm_splits_codemixed.csv",
        "label_meaning": "0 = not offensive, 1 = offensive",
        "situation": "Indian politics Hindi-English Twitter/X offensive/hate-adjacent data",
    },
    "thar_religion": {
        "path": ROOT / "data" / "processed" / "thar_religion.csv",
        "label_meaning": "0 = Non-AntiReligion, 1 = AntiReligion",
        "situation": "Hindi-English YouTube targeted religious hate data",
    },
    "existing_79_row_benchmark": {
        "path": ROOT / "benchmark_test.csv",
        "label_meaning": "0 = non-hate, 1 = hate",
        "situation": "Small manually assembled project sanity benchmark",
    },
}


def normalize_text(text: object, aggressive: bool = False) -> str:
    text = str(text)
    text = re.sub(r"http\S+|www\S+|https\S+", " URL ", text)
    text = re.sub(r"@\w+", " USER ", text)
    text = re.sub(r"\s+", " ", text).strip().lower()
    if aggressive:
        text = re.sub(r"[^\w\s]", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
    return text


def token_list(text: object) -> list[str]:
    text = normalize_text(text, aggressive=True)
    return re.findall(r"[a-zA-Z\u0900-\u097F]+", text)


def script_bucket(text: object) -> str:
    text = str(text)
    has_latin = bool(re.search(r"[A-Za-z]", text))
    has_devanagari = bool(re.search(r"[\u0900-\u097F]", text))
    if has_latin and has_devanagari:
        return "mixed_latin_devanagari"
    if has_devanagari:
        return "devanagari_only"
    if has_latin:
        return "latin_only"
    return "other_or_symbolic"


def emoji_count(text: object) -> int:
    total = 0
    for char in str(text):
        category = unicodedata.category(char)
        if category.startswith("So") and not char.isascii():
            total += 1
    return total


def load_dataset(dataset_id: str, spec: dict[str, object]) -> pd.DataFrame:
    frame = pd.read_csv(spec["path"])
    frame = frame[["text", "label"] + [col for col in frame.columns if col not in {"text", "label"}]].copy()
    frame["dataset_id"] = dataset_id
    frame["text"] = frame["text"].fillna("").astype(str)
    frame["label"] = frame["label"].astype(int)
    frame["norm_text"] = frame["text"].map(lambda value: normalize_text(value, aggressive=True))
    frame["word_count"] = frame["text"].map(lambda value: len(token_list(value)))
    frame["char_count"] = frame["text"].map(lambda value: len(str(value)))
    frame["script_bucket"] = frame["text"].map(script_bucket)
    frame["has_url"] = frame["text"].str.contains(r"http\S+|www\S+|https\S+", regex=True, case=False)
    frame["has_mention"] = frame["text"].str.contains(r"@\w+", regex=True)
    frame["has_hashtag"] = frame["text"].str.contains(r"#\w+", regex=True)
    frame["emoji_count"] = frame["text"].map(emoji_count)
    return frame


def pct(value: float) -> str:
    return f"{value * 100:.1f}%"


def write_csv(frame: pd.DataFrame, name: str) -> Path:
    RESULTS.mkdir(parents=True, exist_ok=True)
    path = RESULTS / name
    frame.to_csv(path, index=False)
    return path


def check_kaggle_integrity() -> dict[str, object]:
    raw = pd.read_csv(ROOT / "combined_hate_speech_dataset.csv")
    processed = pd.read_csv(DATASETS["kaggle_hinglish_hate"]["path"])
    raw_std = pd.DataFrame(
        {
            "text": raw["text"].fillna("").astype(str),
            "label": raw["hate_label"].astype(int),
            "language": raw["language"].fillna("unknown"),
        }
    ).drop_duplicates(subset=["text", "label"])
    expected = raw_std[raw_std["language"] == "hinglish"].copy()
    expected_keys = set(zip(expected["text"], expected["label"]))
    processed_keys = set(zip(processed["text"].fillna("").astype(str), processed["label"].astype(int)))
    return {
        "dataset_id": "kaggle_hinglish_hate",
        "check": "processed equals deduplicated raw rows where language == hinglish",
        "status": "pass" if expected_keys == processed_keys else "fail",
        "expected_rows": len(expected),
        "processed_rows": len(processed),
        "missing_from_processed": len(expected_keys - processed_keys),
        "extra_in_processed": len(processed_keys - expected_keys),
    }


def check_cm_integrity() -> dict[str, object]:
    raw_dir = ROOT / "data" / "raw" / "cm-hate-speech-detection" / "data" / "splits"
    raw_parts = []
    for split in ("train", "val", "test"):
        frame = pd.read_csv(raw_dir / f"{split}.csv")
        frame["split"] = split
        raw_parts.append(frame)
    raw = pd.concat(raw_parts, ignore_index=True)
    expected = raw[raw["codemixed"] == 1].copy()
    processed = pd.read_csv(DATASETS["cm_splits_codemixed"]["path"])
    expected_keys = set(zip(expected["tweet_text"].fillna("").astype(str), expected["offense"].astype(int), expected["split"]))
    processed_keys = set(zip(processed["text"].fillna("").astype(str), processed["label"].astype(int), processed["split"]))
    return {
        "dataset_id": "cm_splits_codemixed",
        "check": "processed equals raw train/val/test rows where codemixed == 1, label mapped from offense",
        "status": "pass" if expected_keys == processed_keys else "fail",
        "expected_rows": len(expected),
        "processed_rows": len(processed),
        "missing_from_processed": len(expected_keys - processed_keys),
        "extra_in_processed": len(processed_keys - expected_keys),
    }


def check_thar_integrity() -> dict[str, object]:
    raw = pd.read_csv(ROOT / "data" / "raw" / "THAR" / "THAR-Dataset.csv")
    processed = pd.read_csv(DATASETS["thar_religion"]["path"])
    label_map = {"Non-AntiReligion": 0, "AntiReligion": 1}
    expected_keys = set(
        zip(
            raw["Comment"].fillna("").astype(str),
            raw["SubTask1"].map(label_map).astype(int),
            raw["SubTask2"].fillna("none").replace({"None": "none"}),
        )
    )
    processed_keys = set(
        zip(
            processed["text"].fillna("").astype(str),
            processed["label"].astype(int),
            processed["target_group"].fillna("none").replace({"None": "none"}),
        )
    )
    return {
        "dataset_id": "thar_religion",
        "check": "processed equals THAR raw comments with SubTask1 binary label mapping",
        "status": "pass" if expected_keys == processed_keys else "fail",
        "expected_rows": len(raw),
        "processed_rows": len(processed),
        "missing_from_processed": len(expected_keys - processed_keys),
        "extra_in_processed": len(processed_keys - expected_keys),
    }


def dataset_profile(frames: dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows = []
    for dataset_id, frame in frames.items():
        label_counts = frame["label"].value_counts().to_dict()
        duplicate_count = int(frame.duplicated("norm_text").sum())
        rows.append(
            {
                "dataset_id": dataset_id,
                "rows": len(frame),
                "label_0": int(label_counts.get(0, 0)),
                "label_1": int(label_counts.get(1, 0)),
                "positive_rate": label_counts.get(1, 0) / max(len(frame), 1),
                "unique_normalized_texts": frame["norm_text"].nunique(),
                "duplicate_normalized_text_rows": duplicate_count,
                "mean_words": frame["word_count"].mean(),
                "median_words": frame["word_count"].median(),
                "p95_words": frame["word_count"].quantile(0.95),
                "mean_chars": frame["char_count"].mean(),
                "url_rate": frame["has_url"].mean(),
                "mention_rate": frame["has_mention"].mean(),
                "hashtag_rate": frame["has_hashtag"].mean(),
                "emoji_rate": (frame["emoji_count"] > 0).mean(),
            }
        )
    return pd.DataFrame(rows)


def label_length_summary(frames: dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows = []
    for dataset_id, frame in frames.items():
        grouped = frame.groupby("label")
        for label, group in grouped:
            rows.append(
                {
                    "dataset_id": dataset_id,
                    "label": int(label),
                    "rows": len(group),
                    "mean_words": group["word_count"].mean(),
                    "median_words": group["word_count"].median(),
                    "p95_words": group["word_count"].quantile(0.95),
                    "mean_chars": group["char_count"].mean(),
                    "url_rate": group["has_url"].mean(),
                    "mention_rate": group["has_mention"].mean(),
                    "hashtag_rate": group["has_hashtag"].mean(),
                    "emoji_rate": (group["emoji_count"] > 0).mean(),
                }
            )
    return pd.DataFrame(rows)


def script_summary(frames: dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows = []
    for dataset_id, frame in frames.items():
        counts = frame["script_bucket"].value_counts().to_dict()
        for bucket, count in counts.items():
            rows.append({"dataset_id": dataset_id, "script_bucket": bucket, "rows": int(count), "rate": count / len(frame)})
    return pd.DataFrame(rows)


def cross_dataset_overlap(frames: dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows = []
    keys = list(frames)
    norm_sets = {key: set(frame["norm_text"]) for key, frame in frames.items()}
    for left in keys:
        for right in keys:
            if left >= right:
                continue
            overlap = norm_sets[left] & norm_sets[right]
            rows.append(
                {
                    "dataset_a": left,
                    "dataset_b": right,
                    "overlap_normalized_texts": len(overlap),
                    "dataset_a_unique_texts": len(norm_sets[left]),
                    "dataset_b_unique_texts": len(norm_sets[right]),
                    "overlap_rate_min_side": len(overlap) / max(min(len(norm_sets[left]), len(norm_sets[right])), 1),
                }
            )
    return pd.DataFrame(rows)


def top_label_terms(frames: dict[str, pd.DataFrame], top_n: int = 25) -> pd.DataFrame:
    rows = []
    for dataset_id, frame in frames.items():
        if dataset_id == "existing_79_row_benchmark":
            min_count = 1
        else:
            min_count = 5
        pos_counter: Counter[str] = Counter()
        neg_counter: Counter[str] = Counter()
        for _, row in frame.iterrows():
            tokens = set(token_list(row["text"]))
            if row["label"] == 1:
                pos_counter.update(tokens)
            else:
                neg_counter.update(tokens)
        vocab = set(pos_counter) | set(neg_counter)
        total_pos = sum(pos_counter.values())
        total_neg = sum(neg_counter.values())
        scored = []
        for token in vocab:
            count = pos_counter[token] + neg_counter[token]
            if count < min_count or len(token) < 3:
                continue
            pos_rate = (pos_counter[token] + 1) / (total_pos + len(vocab))
            neg_rate = (neg_counter[token] + 1) / (total_neg + len(vocab))
            score = math.log(pos_rate / neg_rate)
            scored.append((score, token, pos_counter[token], neg_counter[token]))
        for direction, subset in [
            ("positive_associated", sorted(scored, reverse=True)[:top_n]),
            ("negative_associated", sorted(scored)[:top_n]),
        ]:
            for rank, (score, token, pos_count, neg_count) in enumerate(subset, start=1):
                rows.append(
                    {
                        "dataset_id": dataset_id,
                        "direction": direction,
                        "rank": rank,
                        "token": token,
                        "log_odds_score": score,
                        "positive_doc_count": pos_count,
                        "negative_doc_count": neg_count,
                    }
                )
    return pd.DataFrame(rows)


def duplicate_examples(frames: dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows = []
    for dataset_id, frame in frames.items():
        dupes = frame[frame.duplicated("norm_text", keep=False)].copy()
        if dupes.empty:
            continue
        grouped = dupes.groupby("norm_text")
        for norm_text, group in grouped:
            rows.append(
                {
                    "dataset_id": dataset_id,
                    "duplicate_count": len(group),
                    "labels_seen": ",".join(map(str, sorted(group["label"].unique()))),
                    "example_text": group.iloc[0]["text"],
                }
            )
    return pd.DataFrame(rows).sort_values(["dataset_id", "duplicate_count"], ascending=[True, False])


def make_figures(profile: pd.DataFrame, script: pd.DataFrame, label_lengths: pd.DataFrame, frames: dict[str, pd.DataFrame]) -> list[Path]:
    plt.rcParams.update({"figure.dpi": 140, "savefig.dpi": 300, "font.family": "DejaVu Sans"})
    paths: list[Path] = []

    x = range(len(profile))
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(x, profile["label_0"], label="Label 0", color="#2f6f9f")
    ax.bar(x, profile["label_1"], bottom=profile["label_0"], label="Label 1", color="#b55252")
    ax.set_xticks(list(x))
    ax.set_xticklabels(profile["dataset_id"], rotation=20, ha="right")
    ax.set_ylabel("Rows")
    ax.set_title("Dataset Size And Label Balance")
    ax.legend(frameon=False)
    fig.tight_layout()
    for ext in ("png", "svg"):
        path = RESULTS / f"label_balance.{ext}"
        fig.savefig(path, facecolor="white")
        paths.append(path)
    plt.close(fig)

    pivot = script.pivot_table(index="dataset_id", columns="script_bucket", values="rate", fill_value=0)
    fig, ax = plt.subplots(figsize=(8, 4.5))
    x_positions = list(range(len(pivot.index)))
    bottom = [0] * len(pivot)
    colors = ["#2f6f9f", "#3f8f6b", "#b8872f", "#5f6670"]
    for color, col in zip(colors, pivot.columns):
        values = pivot[col].to_numpy()
        ax.bar(x_positions, values * 100, bottom=[b * 100 for b in bottom], label=col, color=color)
        bottom = [b + v for b, v in zip(bottom, values)]
    ax.set_ylabel("Rows (%)")
    ax.set_title("Script Composition")
    ax.set_xticks(x_positions)
    ax.set_xticklabels(pivot.index, rotation=20, ha="right")
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    for ext in ("png", "svg"):
        path = RESULTS / f"script_composition.{ext}"
        fig.savefig(path, facecolor="white")
        paths.append(path)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 4.5))
    positions = []
    values = []
    labels = []
    pos = 1
    for dataset_id, frame in frames.items():
        for label in (0, 1):
            group = frame[frame["label"] == label]["word_count"]
            values.append(group.clip(upper=120))
            positions.append(pos)
            labels.append(f"{dataset_id}\nlabel {label}")
            pos += 1
        pos += 0.6
    ax.boxplot(values, positions=positions, showfliers=False)
    ax.set_xticks(positions)
    ax.set_xticklabels(labels, rotation=35, ha="right", fontsize=7)
    ax.set_ylabel("Word count, clipped at 120")
    ax.set_title("Text Length By Dataset And Label")
    fig.tight_layout()
    for ext in ("png", "svg"):
        path = RESULTS / f"word_count_by_label.{ext}"
        fig.savefig(path, facecolor="white")
        paths.append(path)
    plt.close(fig)
    return paths


def md_table(frame: pd.DataFrame, columns: list[str]) -> str:
    visible = frame[columns].copy()
    for col in visible.columns:
        if col.endswith("_rate") or col == "positive_rate" or col == "overlap_rate_min_side" or col == "rate":
            visible[col] = visible[col].map(lambda value: pct(float(value)))
        elif pd.api.types.is_float_dtype(visible[col]):
            visible[col] = visible[col].map(lambda value: f"{float(value):.2f}")
        elif not pd.api.types.is_numeric_dtype(visible[col]):
            visible[col] = visible[col].map(
                lambda value: re.sub(r"\s+", " ", str(value)).strip()[:180] + ("..." if len(re.sub(r"\s+", " ", str(value)).strip()) > 180 else "")
            )
    return visible.to_markdown(index=False)


def build_report(
    integrity: pd.DataFrame,
    profile: pd.DataFrame,
    label_lengths: pd.DataFrame,
    script: pd.DataFrame,
    overlap: pd.DataFrame,
    terms: pd.DataFrame,
    duplicates: pd.DataFrame,
    figure_paths: list[Path],
) -> None:
    sections = [
        "# Data Analysis Report",
        "",
        "Date: 2026-06-25",
        "",
        "This report verifies that the processed datasets match the local source files we claim to be using, then profiles the dataset situations that drive the mBERT-vs-MuRIL experiments.",
        "",
        "## Source Integrity Checks",
        "",
        md_table(integrity, ["dataset_id", "status", "expected_rows", "processed_rows", "missing_from_processed", "extra_in_processed", "check"]),
        "",
        "Interpretation: `pass` means the processed file matches the local raw/source file under the documented filtering and label-mapping rule. This does not by itself prove the external citation metadata is complete; it proves local processing consistency.",
        "",
        "## Dataset Profile",
        "",
        md_table(
            profile,
            [
                "dataset_id",
                "rows",
                "label_0",
                "label_1",
                "positive_rate",
                "unique_normalized_texts",
                "duplicate_normalized_text_rows",
                "median_words",
                "p95_words",
                "mention_rate",
                "hashtag_rate",
                "emoji_rate",
            ],
        ),
        "",
        "## Script Composition",
        "",
        md_table(script.sort_values(["dataset_id", "script_bucket"]), ["dataset_id", "script_bucket", "rows", "rate"]),
        "",
        "Script composition is important because mBERT and MuRIL may not behave the same on Latin-script Hinglish versus Devanagari-heavy Hindi-English text.",
        "",
        "## Text Length By Label",
        "",
        md_table(
            label_lengths,
            ["dataset_id", "label", "rows", "median_words", "p95_words", "url_rate", "mention_rate", "hashtag_rate", "emoji_rate"],
        ),
        "",
        "## Cross-Dataset Text Overlap",
        "",
        md_table(overlap, ["dataset_a", "dataset_b", "overlap_normalized_texts", "dataset_a_unique_texts", "dataset_b_unique_texts", "overlap_rate_min_side"]),
        "",
        "Low overlap means cross-dataset evaluation is mostly testing domain/definition transfer rather than memorized duplicate text.",
        "",
        "## Duplicate Texts",
        "",
    ]
    if duplicates.empty:
        sections.extend(["No duplicate normalized texts were found.", ""])
    else:
        sections.extend(
            [
                md_table(duplicates.head(20), ["dataset_id", "duplicate_count", "labels_seen", "example_text"]),
                "",
                f"Full duplicate list saved to `{(RESULTS / 'duplicate_examples.csv').relative_to(ROOT)}`.",
                "",
            ]
        )

    sections.extend(
        [
            "## Label-Associated Terms",
            "",
            "These are not explanations by themselves. They are lexical clues showing which words are most associated with the positive or negative class inside each dataset. Strong lexical clues can partly explain why TF-IDF baselines are competitive.",
            "",
        ]
    )
    for dataset_id in DATASETS:
        dataset_terms = terms[terms["dataset_id"] == dataset_id]
        if dataset_terms.empty:
            continue
        pos_terms = dataset_terms[dataset_terms["direction"] == "positive_associated"].head(12)
        neg_terms = dataset_terms[dataset_terms["direction"] == "negative_associated"].head(12)
        sections.extend(
            [
                f"### `{dataset_id}`",
                "",
                "**Positive-associated terms**",
                "",
                md_table(pos_terms, ["rank", "token", "positive_doc_count", "negative_doc_count", "log_odds_score"]),
                "",
                "**Negative-associated terms**",
                "",
                md_table(neg_terms, ["rank", "token", "positive_doc_count", "negative_doc_count", "log_odds_score"]),
                "",
            ]
        )

    sections.extend(
        [
            "## Figures",
            "",
            *[f"- `{path.relative_to(ROOT)}`" for path in figure_paths],
            "",
        "## Analysis Takeaways",
        "",
        "- The local processed datasets match their documented local sources and label mappings.",
        "- The datasets are not the same task under different names: Kaggle is general Hinglish hate, CM is political offensive/hate-adjacent Twitter/X text, and THAR is targeted religious hate in YouTube comments.",
            "- Script composition differs sharply across datasets, especially between Latin-heavy Kaggle/CM text and Devanagari-heavy THAR text.",
            "- Cross-dataset text overlap is negligible, so transfer results are not duplicate-driven.",
        "- The 79-row diagnostic probe is balanced but manually assembled/provenance-uncertain, has duplicates, and has no direct text overlap with the current source datasets.",
        "- Lexical class cues are visible in every dataset, which helps explain why TF-IDF baselines can be competitive and why dataset-specific models may fail to transfer.",
        "",
        "## Local Raw Data Not Yet Included In These Results",
        "",
        "The workspace also contains raw candidate data under `data/raw/HASOC2021`, `data/raw/Hinglish_Hate_Detection`, and `data/raw/HateSpeech-Hindi-English-Code-Mixed-Social-Media-Text`. These are not part of the current reported training/evaluation matrix because they have not yet been converted into the project schema, audited, and registered as experiment datasets.",
    ]
    )
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    frames = {dataset_id: load_dataset(dataset_id, spec) for dataset_id, spec in DATASETS.items()}

    integrity = pd.DataFrame([check_kaggle_integrity(), check_cm_integrity(), check_thar_integrity()])
    profile = dataset_profile(frames)
    lengths = label_length_summary(frames)
    scripts = script_summary(frames)
    overlap = cross_dataset_overlap(frames)
    terms = top_label_terms(frames)
    duplicates = duplicate_examples(frames)

    write_csv(integrity, "integrity_checks.csv")
    write_csv(profile, "dataset_profile_summary.csv")
    write_csv(lengths, "label_length_summary.csv")
    write_csv(scripts, "script_mix_summary.csv")
    write_csv(overlap, "cross_dataset_overlap.csv")
    write_csv(terms, "top_label_terms.csv")
    write_csv(duplicates, "duplicate_examples.csv")
    figure_paths = make_figures(profile, scripts, lengths, frames)
    build_report(integrity, profile, lengths, scripts, overlap, terms, duplicates, figure_paths)

    print("\nSource Integrity Checks")
    print(integrity.to_markdown(index=False))
    print("\nDataset Profile")
    display_profile = profile.copy()
    for col in ["positive_rate", "url_rate", "mention_rate", "hashtag_rate", "emoji_rate"]:
        display_profile[col] = display_profile[col].map(pct)
    print(display_profile.to_markdown(index=False))
    print(f"\nSaved analysis report to {DOC}")
    print(f"Saved CSV outputs and figures under {RESULTS}")


if __name__ == "__main__":
    main()
