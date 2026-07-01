#!/usr/bin/env python3
"""Create a first-pass qualitative coding of sampled transformer errors.

This is intentionally a transparent, editable coding aid rather than a final
human-annotation authority. The output should be manually reviewed before being
used as paper evidence.
"""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "results" / "error_analysis" / "manual_error_annotation_template.csv"
OUT_CSV = ROOT / "results" / "error_analysis" / "manual_error_annotation_first_pass.csv"
OUT_SUMMARY = ROOT / "results" / "error_analysis" / "manual_error_annotation_summary.csv"
DOC = ROOT / "docs" / "manual_error_analysis_report.md"


RELIGION = {
    "hindu",
    "hinduon",
    "muslim",
    "musalman",
    "islam",
    "christian",
    "jesus",
    "jihad",
    "jihadi",
    "hijab",
    "mandir",
    "masjid",
    "allah",
    "bhagwan",
    "deen",
    "dharam",
    "dharm",
    "mulla",
    "mullo",
    "maulla",
    "maulana",
    "molana",
    "padri",
    "paadri",
    "sanatan",
    "ram",
    "quran",
    "bible",
    "इस्लाम",
    "मुसलमान",
    "मौलाना",
    "मंदिर",
    "मस्जिद",
}

POLITICS = {
    "modi",
    "bjp",
    "rss",
    "congress",
    "gandhi",
    "savarkar",
    "golwalkar",
    "demonetisation",
    "supremecourt",
    "supreme",
    "kashmir",
    "pakistan",
    "india",
    "election",
    "tiranga",
    "farmer",
    "farmers",
    "caa",
    "uapa",
}

ABUSE = {
    "rape",
    "gandu",
    "madarchod",
    "madharchod",
    "chutiya",
    "harami",
    "kutta",
    "kutton",
    "rundi",
    "soower",
    "suvar",
    "hate",
    "nafrat",
    "terrorism",
    "terrorist",
    "kill",
    "mar",
    "maar",
    "phansi",
    "balatkari",
}

BENIGN_HATE_PATTERNS = [
    r"\bi hate (u|you|him|her|this|that|rohit|dhoni|hina|heena|thand|sabzi|luv stories|yuvraj|sallu|vikash|shanghai|srk)\b",
    r"\bhate (hoga|kr skte|kar k|hai kabhi)\b",
    r"\bhater\b",
    r"\bcondolences\b",
]

SHORT_NOISE_PATTERNS = [
    r"^user\s*[^\w\s]*$",
    r"^#?name\?$",
    r"^[a-zA-Z]{1,12}$",
    r"^[^\w]*$",
]


def normalize(text: object) -> str:
    value = str(text).lower()
    value = re.sub(r"http\S+|www\S+|https\S+", " url ", value)
    value = re.sub(r"@\w+", " user ", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value


def tokens(text: object) -> set[str]:
    return set(re.findall(r"[a-zA-Z\u0900-\u097F]+", normalize(text)))


def parse_true_label(pattern: str) -> int:
    match = re.search(r"true=(\d)", str(pattern))
    return int(match.group(1)) if match else -1


def code_row(row: pd.Series) -> tuple[str, str, str]:
    text = str(row["text"])
    norm = normalize(text)
    toks = tokens(text)
    true_label = parse_true_label(row["prediction_pattern"])
    train = str(row["train_dataset"])
    test = str(row["test_dataset"])
    outcome = str(row["outcome"])
    script = str(row["script_bucket"])

    reasons: list[str] = []
    notes: list[str] = []
    relevance: list[str] = []

    cross_dataset = train != test
    if cross_dataset:
        reasons.append("cross_dataset_label_mismatch")
        relevance.append("Shows transfer failure when training and test label definitions/domains differ.")

    if script == "devanagari_only":
        reasons.append("script_mismatch_devanagari")
        relevance.append("Supports script-specific analysis for Devanagari examples.")
    elif script == "mixed_latin_devanagari":
        reasons.append("mixed_script_complexity")
        relevance.append("Shows code-mixing/script mixing as an error source.")

    if toks & RELIGION:
        reasons.append("target_group_or_religion_cue")
        relevance.append("Useful for explaining religious/targeted hate behavior.")

    if toks & POLITICS:
        reasons.append("political_context_or_slogan")
        relevance.append("Shows dependence on political context and dataset topic.")

    if toks & ABUSE:
        reasons.append("generic_profanity_or_abuse")
        relevance.append("Shows that lexical abuse cues can dominate model behavior.")

    if any(re.search(pattern, norm) for pattern in BENIGN_HATE_PATTERNS):
        reasons.append("non_hateful_lexical_trigger")
        notes.append("The text contains a lexical cue such as 'hate' but may not be targeted hate.")
        relevance.append("Important for false-positive discussion and label ambiguity.")

    if any(re.search(pattern, norm) for pattern in SHORT_NOISE_PATTERNS) or len(toks) <= 3:
        reasons.append("short_or_contextless_text")
        notes.append("Very short/context-poor example; label may depend on missing conversation context.")
        relevance.append("Shows why social-media context loss matters.")

    if true_label == 1 and "mbert=0;muril=0" in row["prediction_pattern"]:
        notes.append("Hard positive miss by both transformers under this condition.")
    if true_label == 0 and "mbert=1;muril=1" in row["prediction_pattern"]:
        notes.append("Both transformers mark this negative example as positive.")

    # Dataset-specific interpretation. These are deliberately cautious.
    if test == "cm_splits_codemixed":
        if true_label == 1:
            notes.append("CM positive label is offense/hate-adjacent, not necessarily strict hate.")
        else:
            notes.append("CM negative examples can still contain political or religious discussion.")
    elif test == "kaggle_hinglish_hate":
        if true_label == 1 and ("non_hateful_lexical_trigger" in reasons or len(toks) <= 3):
            notes.append("Kaggle positive label may include generic hate/profanity rather than targeted hate.")
        elif true_label == 0 and toks & ABUSE:
            notes.append("Kaggle negative label may include abusive words used non-targetedly or conversationally.")
    elif test == "thar_religion":
        if true_label == 1 and not (toks & RELIGION):
            notes.append("THAR positive may rely on implicit religious context not captured by keyword flags.")
        elif true_label == 0 and toks & RELIGION:
            notes.append("THAR negative can discuss religion without being AntiReligion.")

    if outcome == "mbert_only_correct":
        relevance.append("Model disagreement case: mBERT handles this example better than MuRIL.")
    elif outcome == "muril_only_correct":
        relevance.append("Model disagreement case: MuRIL handles this example better than mBERT.")
    elif outcome == "hard_false_negative":
        relevance.append("High-priority false-negative example for qualitative reading.")
    elif outcome == "both_wrong_same_prediction":
        relevance.append("Shared failure; useful for dataset/label analysis.")

    if not reasons:
        reasons.append("implicit_context_or_unclear_signal")
        notes.append("No obvious lexical/script cue; likely needs conversation context or human domain knowledge.")

    return (
        ";".join(dict.fromkeys(reasons)),
        " ".join(dict.fromkeys(notes)),
        " ".join(dict.fromkeys(relevance)),
    )


def md_table(frame: pd.DataFrame) -> str:
    return frame.to_markdown(index=False)


def main() -> None:
    df = pd.read_csv(INPUT)
    coded = df.apply(code_row, axis=1, result_type="expand")
    df["manual_reason"] = coded[0]
    df["label_quality_note"] = coded[1]
    df["paper_relevance"] = coded[2]
    df.to_csv(OUT_CSV, index=False)

    reason_counts = Counter()
    for value in df["manual_reason"]:
        reason_counts.update(str(value).split(";"))
    summary = (
        pd.DataFrame(reason_counts.items(), columns=["manual_reason", "rows"])
        .sort_values("rows", ascending=False)
        .reset_index(drop=True)
    )
    summary["share"] = summary["rows"] / len(df)
    summary.to_csv(OUT_SUMMARY, index=False)

    by_dataset = (
        df.assign(primary_reason=df["manual_reason"].str.split(";").str[0])
        .groupby(["train_dataset", "test_dataset", "primary_reason"])
        .size()
        .reset_index(name="rows")
        .sort_values(["test_dataset", "train_dataset", "rows"], ascending=[True, True, False])
    )

    def first_non_cross(value: str) -> str:
        for reason in str(value).split(";"):
            if reason != "cross_dataset_label_mismatch":
                return reason
        return "cross_dataset_label_mismatch_only"

    by_dataset_non_cross = (
        df.assign(non_cross_primary_reason=df["manual_reason"].map(first_non_cross))
        .groupby(["train_dataset", "test_dataset", "non_cross_primary_reason"])
        .size()
        .reset_index(name="rows")
        .sort_values(["test_dataset", "train_dataset", "rows"], ascending=[True, True, False])
    )

    examples = df[
        [
            "train_dataset",
            "test_dataset",
            "outcome",
            "prediction_pattern",
            "manual_reason",
            "label_quality_note",
            "text",
        ]
    ].head(30)

    lines = [
        "# Manual Error Analysis Report",
        "",
        "Date: 2026-06-27",
        "",
        "This report is a first-pass qualitative coding of `results/error_analysis/manual_error_annotation_template.csv`. It should be treated as a structured reading aid, not as final human-ground-truth annotation.",
        "",
        "## Coding Codebook",
        "",
        "| Code | Meaning |",
        "|---|---|",
        "| `cross_dataset_label_mismatch` | Training and test datasets use different label meanings or domains. |",
        "| `target_group_or_religion_cue` | Text contains religion or target-group cues that may drive hate/offense decisions. |",
        "| `political_context_or_slogan` | Text depends on political entities, slogans, or platform-specific political context. |",
        "| `generic_profanity_or_abuse` | Text contains abuse/profanity or violent terms. |",
        "| `non_hateful_lexical_trigger` | Text contains words such as hate/profanity but appears not to be targeted hate. |",
        "| `script_mismatch_devanagari` | Devanagari-only row; may stress tokenizer/script handling. |",
        "| `mixed_script_complexity` | Row mixes Latin and Devanagari scripts. |",
        "| `short_or_contextless_text` | Example is too short or context-poor to interpret confidently. |",
        "| `implicit_context_or_unclear_signal` | No obvious surface cue; likely requires conversation/context. |",
        "",
        "## Overall First-Pass Code Counts",
        "",
        md_table(summary.assign(share=summary["share"].map(lambda x: f"{x * 100:.1f}%"))),
        "",
        "## Primary Reason By Train/Test Pair",
        "",
        md_table(by_dataset.head(60)),
        "",
        "## Main Qualitative Reason Under Cross-Dataset Transfer",
        "",
        "This table ignores `cross_dataset_label_mismatch` when another code is present, so it shows the more specific reason underneath transfer failure.",
        "",
        md_table(by_dataset_non_cross.head(80)),
        "",
        "## Main Qualitative Findings",
        "",
        "- Many sampled errors are cross-dataset failures. This supports the central claim that a model trained on one dataset situation does not automatically transfer to another.",
        "- Religion and target-group cues are frequent in the error sample, especially whenever THAR is involved. This explains why THAR changes the mBERT-vs-MuRIL story.",
        "- Kaggle examples often contain generic uses of `hate`, celebrity/sports dislikes, or profanity. This helps explain why a model can learn lexical triggers without learning strict targeted hate.",
        "- CM examples often require political context or source-specific offense definitions. Some positives are subtle or slogan-like, and some negatives still contain religious/political terms.",
        "- Devanagari and mixed-script examples appear as recurring difficult cases, especially in THAR and CM transfer.",
        "- Short/contextless examples are genuinely hard to judge without surrounding thread context, so these should be treated carefully in the paper.",
        "",
        "## Example Coded Rows",
        "",
        md_table(examples),
        "",
        "## How To Use This File",
        "",
        "The output CSV is `results/error_analysis/manual_error_annotation_first_pass.csv`. Review it row by row and edit the three qualitative columns if you disagree:",
        "",
        "- `manual_reason`",
        "- `label_quality_note`",
        "- `paper_relevance`",
        "",
        "For paper writing, do not treat every code as final. Use these annotations to select examples and justify broader patterns already supported by quantitative metrics.",
        "",
        "## How To Manually Review It Yourself",
        "",
        "1. Open `results/error_analysis/manual_error_annotation_first_pass.csv` in Excel, Numbers, Google Sheets, or VS Code.",
        "2. Filter one train/test pair at a time. Start with matched datasets first because they are easier to interpret.",
        "3. Read `prediction_pattern`: `true=1;mbert=0;muril=0` means both models missed a positive example; `true=0;mbert=1;muril=1` means both models produced a false positive.",
        "4. Read the text and ask: is the gold label obvious, or does it need missing thread/context?",
        "5. Check whether the current `manual_reason` fits. If not, replace it with a better code from the codebook.",
        "6. Use `label_quality_note` to record doubts such as `label seems ambiguous`, `generic dislike not hate`, `religion mention but not attack`, or `needs conversation context`.",
        "7. Use `paper_relevance` only when the row teaches a broader point, such as script failure, label mismatch, or a clear mBERT/MuRIL disagreement.",
        "8. Do not overuse examples containing slurs in the paper. Prefer paraphrased examples or short excerpts when possible.",
        "",
        "A good manual-coding habit: if you are unsure, write `uncertain` in `label_quality_note` rather than forcing a confident interpretation.",
        "",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")

    print(f"Wrote {OUT_CSV.relative_to(ROOT)}")
    print(f"Wrote {OUT_SUMMARY.relative_to(ROOT)}")
    print(f"Wrote {DOC.relative_to(ROOT)}")
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
