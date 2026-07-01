# Dataset Acquisition Log

Last updated: 2026-06-24

This log records dataset acquisition attempts separately from `docs/dataset_registry.md`. A dataset belongs in the registry only when it is locally inspectable enough to define its schema, label meaning, provenance, and caveats.

## Status Key

- `usable`: text and labels are locally available and converted or ready to convert.
- `usable-with-caveats`: text and labels are available, but provenance/licensing/task meaning needs caution.
- `blocked`: dataset exists, but access, password, API, or missing text prevents immediate use.
- `context-only`: useful for provenance or related work, but not a new training/evaluation dataset.

## Acquisition Attempts

| Dataset/source | Local path | Status | What happened | Next action |
|---|---|---|---|---|
| Current combined Hinglish dataset | `combined_hate_speech_dataset.csv`; `data/processed/kaggle_hinglish_hate.csv` | `usable-with-caveats` | Already local. Filtered Hinglish subset has 4,780 rows. Local inspection showed the larger file mixes English, Hindi, and Hinglish. | Keep as the first controlled dataset, but do not describe as purely Indian-context. |
| CM Hate Speech Detection | `data/raw/cm-hate-speech-detection`; `data/processed/cm_splits_codemixed.csv` | `usable-with-caveats` | Cloned and converted. Code-mixed split has 3,900 rows. Label is mapped from source `offense`, so this is offensive/hate-adjacent rather than strict hate. | Decide whether to de-duplicate 82 duplicate texts before formal training. |
| THAR | `data/raw/THAR`; `data/processed/thar_religion.csv` | `usable` | Cloned and converted. Targeted religious hate dataset has 11,549 rows. | Use as a narrow targeted-hate dataset, not a general Hinglish hate dataset. |
| HASOC 2021 English-Hindi code-mix / ICHCL | `data/raw/HASOC2021/ICHCL_train.zip`; `data/raw/HASOC2021/subtask2_test.zip` | `blocked` | Official zips downloaded, but file entries are encrypted/password-protected. Directory structure is visible; actual `data.json` and `labels.json` entries require the official key. | Register/request HASOC key. After access, write a converter for JSON conversations and labels. |
| Bohra et al. Hindi-English Code-Mixed Hate Speech | `data/raw/HateSpeech-Hindi-English-Code-Mixed-Social-Media-Text` | `blocked` | Repository cloned. It contains `id_annotated.tsv` with 4,114 tweet IDs and labels, but no tweet text. README says text must be requested from the authors. | Contact authors or attempt hydration only if X/Twitter API access and policy allow it. |
| Hinglish_Hate_Detection / "Does aggression lead to hate?" repo | `data/raw/Hinglish_Hate_Detection` | `context-only` for now | Repository cloned. It bundles model/test artifacts and a `hate_speech.tsv` that overlaps almost exactly with `kaggle_hinglish_hate` source material. It also includes task outputs for hate/aggression/humor/sarcasm/stance. | Use for provenance and related work. Do not add as an independent dataset unless we isolate a non-overlapping, cleanly documented split. |
| HOT / Hinglish Offensive Tweet Dataset | not downloaded separately | `blocked` | Source repository states the full HOT tweet dataset is not publicly shared due to Twitter policy and requires author consent. | Treat as contact-required; use only the available profanity list if needed for lexical analysis, not as a main dataset. |
| Indo-HateSpeech | not downloaded | `blocked` | Mendeley page metadata verified: published 2024-12-02, DOI `10.17632/snc7mxpj6t.1`, CC BY 4.0. Static page did not expose file list/download path during this pass. | Manually download via browser if available, or use an authenticated/working Mendeley download route. Then inspect schema and convert. |

## Important Notes

- Do not treat Twitter-ID-only datasets as usable text datasets unless text is lawfully hydrated or obtained from authors.
- Do not merge offensive/aggression labels into hate labels without documenting the exact mapping.
- Do not publish raw local datasets to GitHub unless the dataset license explicitly allows redistribution.
- Every converted dataset must be added to `docs/dataset_registry.md` before training results are reported.
