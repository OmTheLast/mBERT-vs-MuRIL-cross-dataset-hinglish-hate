# Dataset Registry

This registry is the paper-facing source of truth for dataset identity, label meaning, situation, and citation status.

## Rule For Future Results

Every result must state:

- training dataset;
- test/evaluation dataset;
- label definition;
- model condition;
- whether the dataset is Indian-context, broader South Asian, or unclear;
- whether the task is strict hate speech, targeted hate, offensive language, aggression, or hate-adjacent.

This is necessary because our early results already showed that changing the evaluation set can change which model appears stronger.

## Registered Datasets

### `kaggle_hinglish_hate`

- Local processed file: `data/processed/kaggle_hinglish_hate.csv`
- Raw source file: `combined_hate_speech_dataset.csv`
- Source page: https://www.kaggle.com/datasets/sharduldhekane/code-mixed-hinglish-hate-speech-detection-dataset
- Source attribution: Shardul Dhekane, `Code-Mixed Hinglish Hate Speech Detection Dataset`, Kaggle.
- Situation: code-mixed Hinglish hate-speech dataset sourced from Kaggle. The local raw file also contains English and Hindi rows, so the controlled dataset used here is the Hinglish subset.
- Current role: initial in-domain training/validation dataset.
- Platform/domain: mixed/unclear from local file metadata.
- Indian-context status: unclear/mixed. Local preview includes non-Indian South Asian context, so do not describe it as purely Indian.
- Label meaning in project: `0 = non-hate`, `1 = hate`.
- Task category: hate speech.
- Caveat: source-level collection and annotation details need more review before the final paper citation is frozen.
- Current audit:
  - rows: 4,780
  - label `0`: 2,914
  - label `1`: 1,866

### `existing_79_row_benchmark`

- Local file: `benchmark_test.csv`
- Situation: small manually available benchmark/test file already present in the project.
- Current role: sanity-check benchmark only.
- Platform/domain: artificial or manually assembled examples; unclear.
- Indian-context status: mixed/unclear.
- Label meaning in file: `0 = non-hate`, `1 = hate`.
- Caveat: label-noisy. Many positive examples are generic negative statements rather than strict targeted hate.
- Current audit:
  - rows: 79
  - label `0`: 40
  - label `1`: 39
- Paper usage: do not use for final conclusions; use only to explain why evaluation quality matters.

### `cm_splits_codemixed`

- Local processed file: `data/processed/cm_splits_codemixed.csv`
- Raw local source: `data/raw/cm-hate-speech-detection`
- Source repository: https://github.com/shikharras/cm-hate-speech-detection
- Situation: Indian politics / Hindi-English code-mixed offensive speech dataset.
- Current role: first external Indian-context code-mixed dataset.
- Platform/domain: Twitter/X political/social content.
- Indian-context status: strong Indian-context candidate.
- Label meaning in project: mapped from source `offense`; `0 = not offensive`, `1 = offensive`.
- Task category: offensive/hate-adjacent, not automatically strict hate speech.
- Caveat: no obvious license file found during local inspection; citation/license review needed.
- Current audit:
  - rows: 3,900
  - label `0`: 2,455
  - label `1`: 1,445
  - duplicate texts: 82

### `thar_religion`

- Local processed file: `data/processed/thar_religion.csv`
- Raw local source: `data/raw/THAR/THAR-Dataset.csv`
- Source repository: https://github.com/aakash-dl/THAR
- Paper: `THAR- Targeted Hate Speech Against Religion- A high-quality Hindi-English code-mixed dataset with the application of deep learning models for automatic detection`
- Paper page noted: https://dl.acm.org/doi/10.1145/3653017
- Situation: targeted religious hate speech against Islam, Hinduism, and Christianity.
- Current role: stricter targeted-hate dataset; useful for testing whether models detect specific religious hate.
- Platform/domain: YouTube comments.
- Indian-context status: strong Indian-context candidate.
- Label meaning in project: `0 = Non-AntiReligion`, `1 = AntiReligion`.
- Task category: targeted religious hate, narrow domain.
- Caveat: not general Hinglish hate speech; domain is religion-focused and YouTube-specific.
- Current audit before conversion:
  - rows: 11,549
  - `Non-AntiReligion`: 6,095
  - `AntiReligion`: 5,454
  - targets: Islam 3,714, Hinduism 1,349, Christianity 391, none 6,095

## Candidate Datasets Not Yet Registered For Experiments

These are not yet converted or fully inspected:

- HASOC English-Hindi code-mix: https://hasocfire.github.io/hasoc/2021/dataset.html
- Hindi-English Code-Mixed Social Media Text for Hate Speech Detection: https://aclanthology.org/W18-1105/
- Indo-HateSpeech: https://data.mendeley.com/datasets/snc7mxpj6t
- HOT: https://github.com/pmathur5k10/Hinglish-Offensive-Text-Classification
- HECM/HHSD-related datasets: https://aclanthology.org/2024.icon-1.9.pdf
