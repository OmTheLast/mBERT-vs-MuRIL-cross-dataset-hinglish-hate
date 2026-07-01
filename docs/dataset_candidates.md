# Dataset Candidates

This file tracks datasets that may help test whether mBERT or MuRIL is stronger for Hinglish/code-mixed hate speech detection. Each dataset still needs local download, license/access review, and schema conversion before being used in final experiments.

## Current Local Dataset

### Code-Mixed Hinglish Hate Speech Detection Dataset

- Local file: `combined_hate_speech_dataset.csv`
- Search/source page: https://www.kaggle.com/datasets/sharduldhekane/code-mixed-hinglish-hate-speech-detection-dataset
- Reported size: 29K+ samples.
- Local audit:
  - 29,550 rows
  - 15,825 non-hate rows
  - 13,725 hate rows
  - only 4,783 rows marked `hinglish`
- Concern: despite the name, the file includes large English and Hindi subsets. Hinglish-specific analysis should filter or stratify by `language`.

## High-Priority Candidates

### Indian Politics Hinglish Hate Speech Dataset / CM Hate Speech Detection

- GitHub: https://github.com/shikharras/cm-hate-speech-detection
- Description from project page: evaluates large language models and BERT-based models on an existing Indian Politics Hinglish hate speech dataset and a custom Hindi-English code-mixed hate speech dataset.
- Value: very aligned with the Indian-context concern; likely closer to Indian political Hinglish than Pakistani or generic South Asian data.
- Local inspection on 2026-06-24:
  - Repository was cloned under `data/raw/cm-hate-speech-detection` for local inspection.
  - `data/filled_10k.csv` contains 10,000 rows with `tweet_text`, `aggression`, `offense`, and `codemixed`.
  - Split files exist under `data/splits/`.
  - `data/hinglish_hatespeech.csv` contains tweet IDs and labels, but no text, so it is not directly usable until tweet text is available.
  - No obvious license file was found during local inspection.
- Current conversion:
  - `scripts/convert_cm_hate_speech.py` maps `offense` to binary `label`.
  - This should be described as offensive/hate-adjacent classification unless the source definition is verified more precisely.
- Concerns:
  - Need license/citation review before publishing or redistributing derived data.
  - Need decide whether to use all rows or code-mixed-only rows.
  - `offense` is not necessarily identical to strict hate speech.

### HASOC English-Hindi Code-Mix

- Official dataset page: https://hasocfire.github.io/hasoc/2021/dataset.html
- HASOC 2024 page also lists English-Hindi code-mix downloads: https://hasocfire.github.io/hasoc/2024/dataset.html
- Relevant task: English-Hindi code-mix offensive/hate identification.
- Value: established shared-task benchmark; useful for comparing against prior systems.
- Local acquisition attempt on 2026-06-24:
  - Downloaded `ICHCL_train.zip` and `subtask2_test.zip` to `data/raw/HASOC2021/`.
  - Zip directory listings are visible, but JSON/PDF entries are encrypted/password-protected.
  - Official page says registration is required for the key.
- Concerns:
  - Access may require registration or password.
  - Labels may be offensive-language-oriented rather than strictly hate speech.
  - Need to map labels into binary `0/1` carefully.

### THAR: Targeted Hate Speech Against Religion

- Paper page: https://dl.acm.org/doi/10.1145/3653017
- GitHub: https://github.com/aakash-dl/THAR
- Kaggle: https://www.kaggle.com/datasets/aakash941/thar-dataset
- Reported size: 11,549 Hindi-English code-mixed YouTube comments.
- Value: Indian code-mixed targeted religious hate; strong fit for the project.
- Local inspection on 2026-06-24:
  - Repository was cloned under `data/raw/THAR`.
  - `THAR-Dataset.csv` contains 11,549 comments.
  - Binary labels: `AntiReligion` and `Non-AntiReligion`.
  - Target labels: Islam, Hinduism, Christianity, and none.
  - Converted to `data/processed/thar_religion.csv` with `scripts/convert_thar.py`.
- Concerns:
  - Narrow domain: religious hate only.
  - Platform is YouTube comments, not tweets.
  - May be too target-specific to generalize to all Hinglish hate.

### Hindi-English Code-Mixed Social Media Text for Hate Speech Detection

- ACL page: https://aclanthology.org/W18-1105/
- Dataset catalogue entry: https://hatespeechdata.com/
- Dataset link listed in catalogue: https://github.com/deepanshu1995/HateSpeech-Hindi-English-Code-Mixed-Social-Media-Text
- Reported size in catalogue: 4,575 posts.
- Reported labels: binary hate/not.
- Value: older, focused Hindi-English Twitter hate speech dataset; useful as a classic baseline.
- Local acquisition attempt on 2026-06-24:
  - Repository was cloned under `data/raw/HateSpeech-Hindi-English-Code-Mixed-Social-Media-Text`.
  - It contains `id_annotated.tsv` with 4,114 tweet IDs and labels.
  - It does not contain tweet text; the README says text must be requested from the authors.
- Concerns:
  - The GitHub repository may need verification/download.
  - Tweet availability can decay over time if only IDs are shared.

### Indo-HateSpeech

- Mendeley Data: https://data.mendeley.com/datasets/snc7mxpj6t
- Description: Hindi-English code-mixed dataset for identifying hate speech in social media.
- Value: newer dataset; directly relevant.
- Local acquisition attempt on 2026-06-24:
  - Mendeley metadata was verified: DOI `10.17632/snc7mxpj6t.1`, published 2024-12-02, license CC BY 4.0.
  - Static page did not expose a direct downloadable file path during this pass.
- Local suitability review on 2026-06-30:
  - Downloaded `Indo-HateSpeech_Dataset.xlsx` and `Readme.pdf` under `data/raw/Indo-HateSpeech/`.
  - Dataset file hash matched Mendeley metadata:
    - `Indo-HateSpeech_Dataset.xlsx`: `087bec9cb08bc1d06c215d6e18f5925619c09fac0b139e95c392cf56cab9ba8e`
    - `Readme.pdf`: `b4747a80db81613db5518dea40b7bcb90d338865250bf8e731cb8f3f3aae9487`
  - Workbook sheet: `PostID Edited Comments Hindi`.
  - Rows: 77,926.
  - Text column: `Comment`.
  - Label column: `Label`.
  - Readme label meanings:
    - `HS0` = No Hateful
    - `HS1` = Hateful
    - `HSN` = Extreme Hateful
  - Raw label counts:
    - `HS0`: 64,194
    - `HS1`: 11,034
    - `HSN`: 2,698
  - Missing comments: 1,360.
  - Source/domain: all rows appear to be Instagram comments from 31 post IDs.
  - Script profile:
    - Latin-only: 56,046
    - Devanagari-only: 7,077
    - mixed Latin-Devanagari: 1,465
    - other/symbolic: 13,338
  - Text-length concern: median word count is 4; many examples are very short.
  - Duplicate concern: 20,288 duplicated normalized comment rows.
  - After dropping symbolic rows, empty text, word count under 3, and deduplicating normalized text, about 46,901 rows remain with a binary positive rate of about 23.6% if `HS1` and `HSN` are mapped to positive.
- Suitability decision on 2026-06-30:
  - Do not add it to the primary experiment set before mixed training.
  - It is accessible and citable, but the concentration in 31 Instagram posts, many short/duplicate comments, and signs of label ambiguity make it risky as an immediate fourth primary dataset.
  - It may be useful later as a secondary robustness or ablation dataset if we build a careful filtered conversion and clearly label it as Instagram-comment hate/extreme-hate data.
- Concerns:
  - Need local download and inspection.
  - Need license and annotation-schema review.

### Hinglish_Hate_Detection / Does aggression lead to hate?

- GitHub: https://github.com/victor7246/Hinglish_Hate_Detection
- Paper DOI noted in repo: https://doi.org/10.1016/j.neucom.2021.11.053
- Value: relevant related work on multiple offensive traits in Hinglish code-mixed texts.
- Local acquisition attempt on 2026-06-24:
  - Repository was cloned under `data/raw/Hinglish_Hate_Detection`.
  - It contains model/test artifacts and task outputs.
  - It bundles `data/raw/Hate-speech-dataset/hate_speech.tsv`, which overlaps almost exactly with the `kaggle_hinglish_hate` source material already processed.
- Current status: context-only unless a clean, non-overlapping, well-documented split is isolated.

## Lower-Priority / Contact-Required

### HOT: Hinglish Offensive Tweet Dataset

- ACL Anthology paper: https://aclanthology.org/W18-5118/
- Project/GitHub page: https://github.com/pmathur5k10/Hinglish-Offensive-Text-Classification
- Value: well-known Hinglish offensive tweet dataset.
- Concern: repository says Twitter policy prevents sharing the full HOT tweet dataset publicly without author consent, so this may require contacting authors.

### HECM / HHSD-Related Datasets

- Paper example: https://aclanthology.org/2024.icon-1.9.pdf
- Reported value: Hindi-English code-mixed posts labeled hateful/non-hateful.
- Reported size: HECM has about 9.4K posts in the cited paper.
- Concern: availability and licensing need verification before use.

### Aggression-Annotated Hindi-English Code-Mixed Corpus

- Catalogue entry: https://hatespeechdata.com/
- Publication: https://arxiv.org/pdf/1803.09402
- Data noted in catalogue: https://github.com/kraiyani/Facebook-Post-Aggression-Identification
- Reported language: Hindi-English.
- Reported platform: Facebook.
- Value: India-adjacent abusive/aggressive language benchmark; useful as an auxiliary offensive-language dataset.
- Concerns:
  - Aggression is not the same as hate speech.
  - Labels are hierarchical, so binary mapping needs careful justification.

## Custom Dataset Idea For Later

Create a small India-focused Hinglish evaluation set using X/Twitter or another platform. This should be treated as a pilot or challenge set unless it has clear annotation guidelines and multiple annotators.

Proposed scope:

- 1,000-2,000 examples.
- Indian context.
- Romanized Hinglish emphasis.
- Balanced or at least carefully reported label distribution.
- Store no unnecessary personal metadata.
- Use minimal cleaning as the default.

This is postponed until after the current code and public-dataset pipeline are stable.
