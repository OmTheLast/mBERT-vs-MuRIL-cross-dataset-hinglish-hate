#!/usr/bin/env python3
"""Audit text-classification CSV datasets for the Hinglish hate speech project."""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path


def detect_columns(fieldnames: list[str], text_column: str | None, label_column: str | None) -> tuple[str, str]:
    lower_to_original = {name.lower(): name for name in fieldnames}

    if text_column is None:
        for candidate in ("text", "tweet", "comment", "post", "content"):
            if candidate in lower_to_original:
                text_column = lower_to_original[candidate]
                break

    if label_column is None:
        for candidate in ("hate_label", "label", "class", "task_1", "category"):
            if candidate in lower_to_original:
                label_column = lower_to_original[candidate]
                break

    if text_column not in fieldnames:
        raise SystemExit(f"Could not find text column. Available columns: {fieldnames}")
    if label_column not in fieldnames:
        raise SystemExit(f"Could not find label column. Available columns: {fieldnames}")

    return text_column, label_column


def audit_csv(path: Path, text_column: str | None, label_column: str | None, top_n: int) -> None:
    encodings = ("utf-8", "utf-8-sig", "latin-1")
    last_error: Exception | None = None

    for encoding in encodings:
        try:
            with path.open(newline="", encoding=encoding) as handle:
                reader = csv.DictReader(handle)
                if reader.fieldnames is None:
                    raise SystemExit(f"No header row found in {path}")

                text_col, label_col = detect_columns(reader.fieldnames, text_column, label_column)
                label_counts: Counter[str] = Counter()
                source_counts: Counter[str] = Counter()
                language_counts: Counter[str] = Counter()
                seen_texts: set[str] = set()
                duplicate_count = 0
                empty_text_count = 0
                row_count = 0
                text_lengths: list[int] = []
                word_counts: list[int] = []

                for row in reader:
                    row_count += 1
                    text = (row.get(text_col) or "").strip()
                    label = (row.get(label_col) or "").strip()
                    label_counts[label] += 1

                    if not text:
                        empty_text_count += 1
                    if text in seen_texts:
                        duplicate_count += 1
                    else:
                        seen_texts.add(text)

                    text_lengths.append(len(text))
                    word_counts.append(len(text.split()))

                    if "source" in row:
                        source_counts[(row.get("source") or "").strip()] += 1
                    if "language" in row:
                        language_counts[(row.get("language") or "").strip()] += 1

            break
        except UnicodeDecodeError as exc:
            last_error = exc
    else:
        raise SystemExit(f"Could not decode {path}: {last_error}")

    def mean(values: list[int]) -> float:
        return sum(values) / len(values) if values else 0.0

    print(f"Dataset: {path}")
    print(f"Rows: {row_count}")
    print(f"Columns: {reader.fieldnames}")
    print(f"Text column: {text_col}")
    print(f"Label column: {label_col}")
    print(f"Empty texts: {empty_text_count}")
    print(f"Duplicate texts: {duplicate_count}")
    print(f"Average characters: {mean(text_lengths):.2f}")
    print(f"Average words: {mean(word_counts):.2f}")

    print("\nLabel distribution:")
    for label, count in label_counts.most_common():
        pct = (count / row_count * 100) if row_count else 0
        print(f"  {label or '<empty>'}: {count} ({pct:.2f}%)")

    if source_counts:
        print("\nTop sources:")
        for value, count in source_counts.most_common(top_n):
            print(f"  {value or '<empty>'}: {count}")

    if language_counts:
        print("\nTop languages:")
        for value, count in language_counts.most_common(top_n):
            print(f"  {value or '<empty>'}: {count}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit a CSV dataset before training/evaluation.")
    parser.add_argument("csv_path", type=Path, help="Path to the dataset CSV file.")
    parser.add_argument("--text-column", default=None, help="Override the text column name.")
    parser.add_argument("--label-column", default=None, help="Override the label column name.")
    parser.add_argument("--top-n", type=int, default=10, help="Number of source/language values to print.")
    args = parser.parse_args()

    audit_csv(args.csv_path, args.text_column, args.label_column, args.top_n)


if __name__ == "__main__":
    main()
