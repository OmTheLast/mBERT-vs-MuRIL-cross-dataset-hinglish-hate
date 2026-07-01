# Dataset Taxonomy

Date: 2026-06-26

This document classifies every dataset situation used in the project. It is meant to prevent a common research mistake: treating all `label = 1` rows as if they mean the same thing.

## Taxonomy Table

| Dataset ID | Source | Local file | Rows | Positive label | Task category | Platform/domain | Script profile | Indian-context status | Paper role | Main caveat |
|---|---|---|---:|---|---|---|---|---|---|---|
| `kaggle_hinglish_hate` | Shardul Dhekane Kaggle Code-Mixed Hinglish Hate Speech Detection Dataset | `data/processed/kaggle_hinglish_hate.csv` | 4,780 | hate | hate speech | mixed/unclear from local metadata | 100% Latin script in processed Hinglish subset | unclear/mixed; do not call purely Indian without more source review | primary dataset | source collection/annotation details need final citation review |
| `cm_splits_codemixed` | `shikharras/cm-hate-speech-detection` | `data/processed/cm_splits_codemixed.csv` | 3,900 | offensive | offensive/hate-adjacent | Twitter/X political/social content | mostly Latin, with some mixed Latin-Devanagari | strong Indian-context candidate | primary external dataset | positive label is offense, not strict hate |
| `thar_religion` | THAR repository and paper | `data/processed/thar_religion.csv` | 11,549 | AntiReligion | targeted religious hate | YouTube comments | mostly Latin, meaningful Devanagari portion | strong Indian-context candidate | primary targeted-hate dataset | narrow religious-hate domain, not general Hinglish hate |
| `existing_79_row_benchmark` | local project file with uncertain provenance | `benchmark_test.csv` | 79 | hate | diagnostic only | artificial/manual/unclear | 100% Latin script | mixed/unclear | diagnostic probe only | possible manual or synthetic origin; excluded from primary conclusions |

## Label Comparability

The biggest methodological issue is that positive labels are not identical across datasets.

`kaggle_hinglish_hate` is the closest to the original project goal: general Hinglish hate speech detection. However, its platform/domain and annotation details require more source review before the final paper.

`cm_splits_codemixed` is useful because it is Indian-context and code-mixed, but its positive label is mapped from offense. Offensive language may include insults, profanity, political attacks, or aggressive tone that would not always meet a strict hate-speech definition.

`thar_religion` is more targeted and semantically precise. A positive row means AntiReligion content, not general hate or general offense. This is why THAR can produce cleaner MuRIL gains while still transferring poorly to broader Hinglish hate.

`existing_79_row_benchmark` should not be treated as a scientific dataset. It remains useful as a reminder that small, unclear benchmarks can create misleading model rankings.

## Dataset Situation Variables

Every result should be described using these variables:

| Variable | Why it matters |
|---|---|
| Label definition | A model trained on offense may not learn strict hate; a model trained on religious hate may not learn general hate |
| Platform | Twitter/X, YouTube, and manual examples differ in length, style, context, and noise |
| Script | Latin-script Hinglish and Devanagari-heavy Hindi-English text may favor different tokenization behavior |
| Topic/domain | Politics, religion, sports, and casual abuse use different cues |
| Target group | Targeted hate requires recognizing who is being attacked, not only whether the sentence is rude |
| Provenance | Source-backed data can support paper claims; uncertain data should stay diagnostic |
| Split policy | Source splits and random stratified splits are not directly identical conditions |

## Current Dataset Situations

### `kaggle_hinglish_hate`

Situation: broad Hinglish hate/non-hate classification from the Kaggle source.

Use in paper:

- main starting dataset;
- matched mBERT-vs-MuRIL comparison;
- example of Latin-script Hinglish behavior.

Current finding:

- mBERT outperforms MuRIL on the matched held-out condition.

Interpretive caution:

- because the processed subset is 100% Latin script, MuRIL's Indian-language pretraining may not automatically help.
- source metadata must be reviewed before making strong claims about platform or Indian-only context.

### `cm_splits_codemixed`

Situation: Indian political/social Twitter/X code-mixed offensive language.

Use in paper:

- external Indian-context code-mixed dataset;
- test of whether the models generalize beyond the Kaggle source;
- comparison between hate and offense definitions.

Current finding:

- mBERT is stronger than MuRIL on matched CM.
- MuRIL is stronger in some CM/THAR transfer directions.

Interpretive caution:

- offense is broader than hate speech.
- duplicates and duplicate-label conflicts exist, so deduplication and source splits must be documented.

### `thar_religion`

Situation: targeted religious hate in Hindi-English code-mixed YouTube comments.

Use in paper:

- stricter targeted-hate comparison;
- test of Indian-language-focused MuRIL under a domain where Indian language/script cues may matter more;
- methodological reference for clear dataset definition.

Current finding:

- MuRIL outperforms mBERT on matched THAR.
- THAR-trained MuRIL also transfers better to CM than THAR-trained mBERT.

Interpretive caution:

- THAR is not general Hinglish hate speech.
- high matched performance does not mean the model becomes a universal harmful-speech detector.

### `existing_79_row_benchmark`

Situation: small diagnostic probe with uncertain source.

Use in paper:

- optional methods note or appendix example about evaluation quality;
- not primary evidence.

Current finding:

- it produced unstable model rankings and exposed label/provenance problems.

Interpretive caution:

- do not use it for final claims.

## Why THAR Matters As Research Inspiration

THAR gives this project a methodological lesson: a strong research dataset is not only a CSV. It is a documented situation.

Important features to imitate:

- state the target phenomenon clearly;
- state the platform clearly;
- define the positive and negative labels;
- identify target groups where relevant;
- report dataset composition;
- connect experiments back to the label definition.

For this project, that means every result section should say something like:

> Model X trained on dataset A was evaluated on dataset B, where the positive label means Y. Therefore, this score measures transfer from situation A to situation B, not universal hate detection.

## Result Labeling Rule

Every future table should include at least:

- model family;
- pretrained model;
- train dataset;
- test dataset;
- positive-label meaning for train dataset;
- positive-label meaning for test dataset;
- script/domain note;
- split policy;
- metric columns.

This keeps the paper honest and prevents accidental overclaiming.

## Recommended Grouping For Paper Sections

Dataset section:

- introduce the three primary datasets separately;
- explain why the 79-row probe is excluded;
- include a table with rows, positive rates, platform, label meaning, and script profile.

Methods section:

- explain in-domain, cross-dataset, and baseline experiments;
- explain that labels are harmonized numerically as `0/1` but not semantically identical.

Results section:

- report matched results first;
- then report cross-dataset results;
- then compare against TF-IDF baselines;
- then discuss error analysis.

Discussion section:

- interpret mBERT wins as Latin-script/matched-dataset strength;
- interpret MuRIL wins as targeted religious-hate and Indian-language/domain strength;
- emphasize weak cross-dataset generalization.

Limitations section:

- label mismatch;
- source metadata gaps;
- platform differences;
- limited manual error coding so far;
- no mixed-dataset or leave-one-dataset-out training yet.

