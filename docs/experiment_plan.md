# Experiment Plan

## Research Question

Does MuRIL's Indian-language-focused pretraining improve Hinglish/code-mixed hate speech detection compared with mBERT's general multilingual pretraining?

## Model Set

Primary models:

- `bert-base-multilingual-cased` as mBERT.
- `google/muril-base-cased` as MuRIL.

Recommended additional baselines:

- TF-IDF + Logistic Regression.
- TF-IDF + Linear SVM.
- Optional Indic model such as IndicBERT if time permits.

## Dataset Schema

Every processed dataset should become a CSV with:

```text
text,label,dataset,source,language
```

Required:

- `text`: cleaned or minimally normalized text.
- `label`: `0` for non-hate/non-offensive, `1` for hate/offensive.
- `dataset`: short dataset name such as `current`, `thar`, `hasoc21`.

Optional but useful:

- `source`: source platform or original source file.
- `language`: `english`, `hindi`, `hinglish`, `mixed`, or `unknown`.

## Cleaning Policy

Default to minimal cleaning for transformer models:

- Replace URLs with `URL`.
- Replace mentions with `USER`.
- Normalize whitespace.
- Keep hashtags, punctuation, emojis, and casing unless a specific experiment tests aggressive cleaning.

Reason: aggressive cleaning may remove signal from noisy social media text.

Current runner:

```bash
.venv/bin/python experiments/train_transformer.py \
  --model mbert \
  --train-csv combined_hate_speech_dataset.csv \
  --text-column text \
  --label-column hate_label \
  --cleaning minimal
```

Swap `--model muril` for MuRIL. Use `--cleaning aggressive` only as an ablation experiment.

Device-specific entrypoints:

```bash
.venv/bin/python experiments/train_mac_mps.py --model mbert --train-csv data/processed/kaggle_hinglish_hate.csv --label-column label
.venv/bin/python experiments/train_colab_cuda.py --model muril --train-csv data/processed/kaggle_hinglish_hate.csv --label-column label
.venv/bin/python experiments/train_cpu_debug.py --model mbert --train-csv data/processed/kaggle_hinglish_hate.csv --label-column label
```

## Evaluation Metrics

Primary:

- Macro F1.
- Hate-class F1.
- Hate-class recall.

Secondary:

- Accuracy.
- Precision.
- Confusion matrix.
- Average inference latency.

Accuracy should never be the headline metric because a non-hate-biased classifier can look deceptively good.

## Reporting Requirement

Before adding a new result to the paper, check:

- `docs/dataset_registry.md` for dataset identity and caveats.
- `docs/result_reporting_protocol.md` for the result paragraph format.

No result should be reported without the training dataset, test dataset, label meaning, and dataset situation.

## Experiment Matrix

### 1. In-Domain Evaluation

Train and test on splits from the same dataset.

Purpose: measure standard performance.

```text
train: A train split
test: A test split
```

### 2. Cross-Dataset Evaluation

Train on one dataset and test on another.

Purpose: measure generalization.

```text
train: A
test: B
```

### 3. Leave-One-Dataset-Out Evaluation

Train on all datasets except one and test on the held-out dataset.

Purpose: strongest robustness test for the paper.

```text
train: all datasets except A
test: A
```

### 4. Hinglish-Only Evaluation

Filter to code-mixed/Hinglish examples where metadata allows it.

Purpose: answer the actual Hinglish question instead of broader multilingual hate detection.

```text
train: Hinglish/code-mixed only
test: Hinglish/code-mixed only
```

## Error Analysis

For each major experiment, save examples from:

- mBERT correct, MuRIL wrong.
- MuRIL correct, mBERT wrong.
- both wrong.
- both correct but low confidence.
- both wrong and high confidence.

Manual analysis categories:

- Romanized Hindi spelling variation.
- Religious or caste references.
- Sarcasm.
- Implicit hate without slurs.
- Profanity that is not hate.
- English-only hate.
- Hindi/Devanagari-heavy text.

## Paper Sections

1. Abstract.
2. Introduction.
3. Related work.
4. Datasets.
5. Methodology.
6. Experiments.
7. Results.
8. Error analysis.
9. Discussion.
10. Limitations.
11. Conclusion and future work.
