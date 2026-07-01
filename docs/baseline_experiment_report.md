# Baseline Experiment Report

Date: 2026-06-24

## Purpose

This baseline experiment establishes a non-transformer reference point before expanding mBERT and MuRIL training across multiple datasets. The goal is not to beat transformer models, but to understand how much of the task can be captured by lexical signals and how strongly performance changes when the training and evaluation dataset differ.

This matters for the research question because early transformer results already showed dataset sensitivity: mBERT performed better on the held-out `kaggle_hinglish_hate` split, while MuRIL performed better on the small 79-row benchmark. The baseline experiment tests whether the same dataset-dependence appears even with simpler models.

## Datasets

| Dataset ID | Rows Used | Role | Positive Label | Dataset Situation | Caveat |
|---|---:|---|---|---|---|
| `kaggle_hinglish_hate` | 4,780 | Train/test | `1 = hate` | Hinglish subset filtered from the existing combined dataset | Indian-context status is unclear/mixed. |
| `cm_splits_codemixed` | 3,818 after de-duplication | Train/test | `1 = offensive` | Indian politics Hindi-English code-mixed Twitter/X data | Offensive/hate-adjacent, not strict hate. |
| `thar_religion` | 11,549 | Train/test | `1 = AntiReligion` | Hindi-English code-mixed YouTube comments about targeted religious hate | Narrow religious-hate domain. |
| `existing_79_row_benchmark` | 79 | Sanity evaluation only | `1 = hate` | Small manually available benchmark | Too small and label-noisy for final conclusions. |

Dataset provenance and access notes are recorded in:

- `docs/dataset_registry.md`
- `docs/dataset_acquisition_log.md`
- `docs/dataset_candidates.md`

## Models

Two classical machine-learning baselines were used:

| Model ID | Description |
|---|---|
| `tfidf_logistic_regression` | Word-level TF-IDF features with Logistic Regression and balanced class weights. |
| `tfidf_linear_svm` | Word-level TF-IDF features with Linear SVM and balanced class weights. |

TF-IDF used word unigrams and bigrams, `min_df=2`, `max_features=50000`, and sublinear term frequency scaling.

## Evaluation Setup

Script:

```bash
.venv/bin/python experiments/run_cross_dataset_baselines.py
```

Saved outputs:

| Output | Path |
|---|---|
| Summary metrics | `results/cross_dataset_baseline_summary.csv` |
| Detailed predictions | `results/cross_dataset_baseline_predictions.csv` |
| Combined result summary | `results/summary.md` |

Split policy:

| Dataset | Split |
|---|---|
| `kaggle_hinglish_hate` | Stratified 80/20 split, seed 42 |
| `thar_religion` | Stratified 80/20 split, seed 42 |
| `cm_splits_codemixed` | Source-provided split; train+val used for training, test used for evaluation |

Deduplication was enabled by default. This mostly affects `cm_splits_codemixed`, which had 82 duplicate texts before de-duplication.

Primary metrics:

- Macro F1
- Positive-class F1
- Positive-class recall

Accuracy is reported but not treated as the headline metric because a model can appear accurate while missing many positive examples.

## In-Domain Results

The table below reports the stronger model by macro F1 for each in-domain dataset condition.

| Train Dataset | Test Dataset | Model | Test Rows | Accuracy | Positive Recall | Positive F1 | Macro F1 | TP | FN | FP | TN |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `kaggle_hinglish_hate` | `kaggle_hinglish_hate` | `tfidf_logistic_regression` | 956 | 63.0% | 55.2% | 53.8% | 61.4% | 206 | 167 | 187 | 396 |
| `cm_splits_codemixed` | `cm_splits_codemixed` | `tfidf_logistic_regression` | 415 | 79.0% | 75.5% | 71.8% | 77.6% | 111 | 36 | 51 | 217 |
| `thar_religion` | `thar_religion` | `tfidf_logistic_regression` | 2,310 | 70.6% | 70.2% | 69.3% | 70.6% | 766 | 325 | 354 | 865 |

Logistic Regression is strongest in-domain across all three datasets by both macro F1 and positive-class F1.

## Cross-Dataset Results

The table below reports the stronger model by macro F1 for each cross-dataset condition, excluding the 79-row sanity benchmark.

| Train Dataset | Test Dataset | Model | Test Rows | Accuracy | Positive Recall | Positive F1 | Macro F1 | TP | FN | FP | TN |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `kaggle_hinglish_hate` | `cm_splits_codemixed` | `tfidf_linear_svm` | 415 | 39.5% | 63.3% | 42.6% | 39.3% | 93 | 54 | 197 | 71 |
| `kaggle_hinglish_hate` | `thar_religion` | `tfidf_logistic_regression` | 2,310 | 50.3% | 61.9% | 54.0% | 49.9% | 675 | 416 | 733 | 486 |
| `cm_splits_codemixed` | `kaggle_hinglish_hate` | `tfidf_linear_svm` | 956 | 49.8% | 44.2% | 40.7% | 48.6% | 165 | 208 | 272 | 311 |
| `cm_splits_codemixed` | `thar_religion` | `tfidf_linear_svm` | 2,310 | 53.8% | 56.7% | 53.7% | 53.8% | 619 | 472 | 595 | 624 |
| `thar_religion` | `kaggle_hinglish_hate` | `tfidf_logistic_regression` | 956 | 57.6% | 26.8% | 33.1% | 51.0% | 100 | 273 | 132 | 451 |
| `thar_religion` | `cm_splits_codemixed` | `tfidf_logistic_regression` | 415 | 68.4% | 34.7% | 43.8% | 60.9% | 51 | 96 | 35 | 233 |

## Benchmark Sanity Results

The 79-row benchmark is not used for final conclusions, but it remains useful as a continuity check.

| Train Dataset | Best Model By Macro F1 | Accuracy | Positive Recall | Positive F1 | Macro F1 | TP | FN |
|---|---|---:|---:|---:|---:|---:|---:|
| `kaggle_hinglish_hate` | `tfidf_logistic_regression` | 54.4% | 46.2% | 50.0% | 54.1% | 18 | 21 |
| `cm_splits_codemixed` | `tfidf_logistic_regression` | 65.8% | 74.4% | 68.2% | 65.6% | 29 | 10 |
| `thar_religion` | `tfidf_logistic_regression` | 50.6% | 5.1% | 9.3% | 37.7% | 2 | 37 |

The `cm_splits_codemixed` baseline transfers best to the 79-row benchmark, but this should not be over-interpreted because `cm_splits_codemixed` uses an offensive/hate-adjacent label while the benchmark uses hate/non-hate labels.

## Interpretation

The main finding is that cross-dataset generalization is unstable even for simple lexical models. In-domain performance is reasonably strong, especially on `cm_splits_codemixed` and `thar_religion`, but performance drops when the train and test datasets differ.

This supports the current research framing:

- Dataset identity is not a background detail; it changes the measured behavior.
- Label meaning matters. `hate`, `offensive`, and `AntiReligion` are related but not identical.
- Domain matters. Twitter/X politics, YouTube religious comments, and mixed-source Hinglish text behave differently.
- Positive-class recall and macro F1 can tell different stories; both should be reported.

For the paper, this baseline run provides a useful control: if mBERT or MuRIL improves cross-dataset generalization, that improvement should be measured against these classical baselines rather than only against each other.

## Limitations

- The baseline models are lexical and do not capture deeper context, sarcasm, or implicit hate reliably.
- Cross-dataset comparisons are affected by label mismatch across datasets.
- `kaggle_hinglish_hate` has unclear/mixed Indian-context status.
- `cm_splits_codemixed` is offensive/hate-adjacent, not strict hate.
- `thar_religion` is narrow targeted religious hate and may not generalize to broader Hinglish hate speech.
- The 79-row benchmark is too small and label-noisy for final claims.

## Next Experimental Use

This report should be used to choose transformer experiments. The strongest next transformer matrix is:

1. Train mBERT and MuRIL on `cm_splits_codemixed`; evaluate on its test split, `kaggle_hinglish_hate`, `thar_religion`, and the 79-row benchmark.
2. Train mBERT and MuRIL on `thar_religion`; evaluate on its held-out split, `kaggle_hinglish_hate`, `cm_splits_codemixed`, and the 79-row benchmark.
3. Compare these against the already trained `kaggle_hinglish_hate` mBERT/MuRIL checkpoints.
4. Add error analysis for examples where mBERT and MuRIL disagree.
