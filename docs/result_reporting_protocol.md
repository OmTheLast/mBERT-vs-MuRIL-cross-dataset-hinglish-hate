# Result Reporting Protocol

This file defines how future result sections should be written so the paper remains clear as datasets multiply.

## Required Fields For Every Result

Every result table or paragraph must include:

- **Train dataset**: exact dataset identifier from `docs/dataset_registry.md`.
- **Test dataset**: exact dataset identifier from `docs/dataset_registry.md`.
- **Model**: mBERT, MuRIL, TF-IDF baseline, etc.
- **Condition**: initial saved project checkpoint, trained on Kaggle Hinglish Hate, trained on THAR, cross-dataset, diagnostic probe, etc.
- **Task category**: strict hate, targeted hate, offensive language, aggression, or hate-adjacent.
- **Dataset situation**: Indian politics, religious YouTube comments, mixed/unclear, etc.
- **Primary metric**: macro F1 and hate/offensive-class F1.
- **Caveat**: label noise, narrow domain, non-Indian context, small sample, or license limitations.

## Standard Result Paragraph Template

Use this style:

```text
In the [dataset situation] condition, [model] was trained on [train dataset] and evaluated on [test dataset].
The task label represented [label meaning].
Under this condition, [model] achieved [macro F1] macro F1 and [class F1] positive-class F1.
This result should be interpreted with caution because [dataset caveat].
```

## Example From Current Work

```text
In the Kaggle Hinglish Hate validation condition, mBERT was trained and evaluated on a stratified split of `kaggle_hinglish_hate`.
The label represented the dataset's binary hate/non-hate annotation.
Under this condition, mBERT achieved 65.4% macro F1 and 51.4% hate-class F1.
This result should be interpreted with caution because the source dataset is filtered from a larger mixed English/Hindi/Hinglish dataset and is not purely Indian-context.
```

## Why This Matters

Early results already show dataset sensitivity:

- mBERT performs better on the Kaggle Hinglish Hate held-out split.
- MuRIL performs better on the 79-row diagnostic probe, but this probe is excluded from primary paper conclusions because provenance is uncertain.
- TF-IDF baselines are competitive with transformer models.

Therefore, the paper should not say a model is universally better unless the claim is backed by multiple dataset situations.
