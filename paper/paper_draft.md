# Cross-Dataset Evaluation of mBERT and MuRIL for Hate Speech Detection in Hinglish Code-Mixed Text

Working draft started: 2026-06-25

## Abstract

Hinglish hate speech detection is difficult because social media text often mixes Hindi and English, uses inconsistent Romanization, and varies sharply across platform and topic. This project compares mBERT, a general multilingual BERT model, with MuRIL, an Indian-language-focused model, for binary hate/offensive speech detection across multiple Hindi-English code-mixed dataset situations. Current results show that the apparent winner depends strongly on the training dataset, evaluation dataset, and positive-label definition. mBERT is stronger on matched Kaggle Hinglish hate and CM code-mixed offensive evaluation, while MuRIL is stronger on matched THAR targeted religious hate and on THAR-to-CM transfer. These findings motivate a cross-dataset framing rather than a single-dataset model comparison.

## 1. Introduction

Hindi-English code-mixed text is common in online Indian and South Asian social media. Users frequently combine Hindi vocabulary, English vocabulary, Romanized Hindi spellings, abbreviations, slang, and platform-specific expressions in the same sentence. This makes hate speech detection harder than standard monolingual classification because the model must understand both multilingual content and unstable transliteration.

This paper studies whether MuRIL's Indian-language-specific pretraining improves Hinglish hate/offensive speech detection compared with mBERT's broader multilingual pretraining. The original project question was a direct mBERT-vs-MuRIL comparison on one Hinglish dataset. The current research direction is broader: model performance is evaluated across dataset situations, because early experiments showed that the model ranking changes depending on the evaluation set.

Research question:

> Does Indian-language-specific pretraining in MuRIL improve hate/offensive speech detection for Hinglish and Hindi-English code-mixed text compared with general multilingual pretraining in mBERT?

Working hypothesis:

- mBERT may perform better on noisy Romanized Hinglish because many tokens resemble English or Latin-script subword patterns.
- MuRIL may improve when the data contains more Indian-language structure, targeted Indian-context content, or religious hate categories.
- Dataset definition and label definition may matter as much as model architecture.

## 2. Datasets

All results in this project are labeled by training dataset, test dataset, label meaning, and dataset situation. This is necessary because the positive label is not identical across all datasets.

### 2.1 Kaggle Hinglish Hate Dataset

Dataset ID: `kaggle_hinglish_hate`

Source: Shardul Dhekane, `Code-Mixed Hinglish Hate Speech Detection Dataset`, Kaggle.  
Source URL: https://www.kaggle.com/datasets/sharduldhekane/code-mixed-hinglish-hate-speech-detection-dataset

Local processed file: `data/processed/kaggle_hinglish_hate.csv`

This dataset is used as the first controlled Hinglish hate-speech dataset. The local raw file contains English, Hindi, and Hinglish rows, so the controlled experiments use the Hinglish subset. The project label mapping is:

- `0 = non-hate`
- `1 = hate`

Current processed audit:

| Dataset | Rows | Label 0 | Label 1 |
|---|---:|---:|---:|
| `kaggle_hinglish_hate` | 4,780 | 2,914 | 1,866 |

### 2.2 CM Code-Mixed Offensive Dataset

Dataset ID: `cm_splits_codemixed`

Source repository: https://github.com/shikharras/cm-hate-speech-detection

This dataset contains Indian politics Hindi-English code-mixed Twitter/X data. It is treated as offensive/hate-adjacent rather than strict hate speech because the local conversion maps the source `offense` label to the project's binary label.

- `0 = not offensive`
- `1 = offensive`

Current processed audit:

| Dataset | Rows | Label 0 | Label 1 | Duplicate Texts |
|---|---:|---:|---:|---:|
| `cm_splits_codemixed` | 3,900 | 2,455 | 1,445 | 82 |

### 2.3 THAR Targeted Religious Hate Dataset

Dataset ID: `thar_religion`

Source repository: https://github.com/aakash-dl/THAR  
Paper page noted in project registry: https://dl.acm.org/doi/10.1145/3653017

THAR is a Hindi-English code-mixed dataset for targeted hate speech against religion, collected from YouTube comments. It is narrower than general hate speech because the positive class is specifically anti-religion content.

- `0 = Non-AntiReligion`
- `1 = AntiReligion`

Current processed audit:

| Dataset | Rows | Label 0 | Label 1 |
|---|---:|---:|---:|
| `thar_religion` | 11,549 | 6,095 | 5,454 |

### 2.4 79-Row Diagnostic Probe

Dataset ID: `existing_79_row_benchmark`

This is a small project probe file already present in the project. Its provenance is uncertain and it may have been manually written or AI-generated. It is therefore excluded from primary conclusions. It remains useful only as a diagnostic example of why evaluation provenance matters.

## 3. Models

This project compares:

- mBERT: `bert-base-multilingual-cased`
- MuRIL: `google/muril-base-cased`

The project also uses TF-IDF baselines:

- TF-IDF + Logistic Regression
- TF-IDF + Linear SVM

The baselines are not the main research target, but they help answer whether transformer behavior is genuinely stronger than simpler lexical models under each dataset condition.

## 4. Methodology

All transformer runs use binary sequence classification with two labels. For datasets without an official split, the project uses a stratified 80/20 split with seed 42. For `cm_splits_codemixed`, the source-provided train/validation/test split is used, with train+validation used for training and test used for evaluation.

Default transformer training settings:

| Setting | Value |
|---|---|
| Epochs | 2 |
| Batch size on Mac MPS | 8 |
| Learning rate | 2e-5 |
| Max sequence length | 128 |
| Cleaning | minimal URL/user normalization |
| Seed | 42 |

Metrics:

- Accuracy: overall fraction of correct predictions.
- Positive recall: among actual positive examples, the fraction caught by the model.
- Positive F1: harmonic mean of positive precision and positive recall.
- Macro F1: average F1 across both classes; useful when classes are imbalanced.
- Confusion matrix: true negatives, false positives, false negatives, true positives.

## 5. Current Results

The paper-facing result source is `docs/result_analysis_report.md`, backed by `results/transformer_cross_dataset_summary.csv` and `results/cross_dataset_baseline_summary.csv`. Primary conclusions use only source-backed datasets: `kaggle_hinglish_hate`, `cm_splits_codemixed`, and `thar_religion`.

### 5.1 Initial Saved Project Checkpoints

The previously saved project checkpoints showed very low positive-class recall on the 79-row diagnostic probe. Because the probe provenance is uncertain and the checkpoint training assumptions still need reconstruction, this result should be treated as diagnostic project context rather than controlled evidence.

### 5.2 Kaggle Hinglish Hate Training

On the matched Kaggle Hinglish hate paper-facing evaluation condition, mBERT outperformed MuRIL:

| Model | Train Dataset | Accuracy | Positive Recall | Positive F1 | Macro F1 |
|---|---|---:|---:|---:|---:|
| mBERT | `kaggle_hinglish_hate` | 71.4% | 38.6% | 51.3% | 65.6% |
| MuRIL | `kaggle_hinglish_hate` | 67.5% | 22.3% | 34.8% | 56.6% |

The later result analysis excludes the 79-row probe from primary conclusions. On source-backed primary data, the key Kaggle result is that mBERT outperforms MuRIL on the matched Kaggle Hinglish hate condition.

### 5.3 CM Code-Mixed Training

On matched CM evaluation, mBERT again outperformed MuRIL:

| Model | Train Dataset | Accuracy | Positive Recall | Positive F1 | Macro F1 |
|---|---|---:|---:|---:|---:|
| mBERT | `cm_splits_codemixed` | 80.5% | 68.7% | 71.4% | 78.3% |
| MuRIL | `cm_splits_codemixed` | 78.8% | 55.1% | 64.8% | 74.8% |

But in transfer from CM training to THAR targeted religious hate, MuRIL became stronger:

| Model | Train Dataset | Test Dataset | Positive Recall | Positive F1 | Macro F1 |
|---|---|---|---:|---:|---:|
| mBERT | `cm_splits_codemixed` | `thar_religion` | 44.6% | 51.0% | 58.3% |
| MuRIL | `cm_splits_codemixed` | `thar_religion` | 59.5% | 58.3% | 59.7% |

This is currently the strongest evidence that MuRIL may help in certain Indian-context transfer settings, even when it does not win on the matched Romanized/code-mixed dataset.

### 5.4 THAR Training

On matched THAR targeted religious hate evaluation, MuRIL outperformed mBERT:

| Model | Train Dataset | Accuracy | Positive Recall | Positive F1 | Macro F1 |
|---|---|---:|---:|---:|---:|
| mBERT | `thar_religion` | 74.8% | 77.7% | 74.5% | 74.8% |
| MuRIL | `thar_religion` | 77.9% | 80.3% | 77.4% | 77.9% |

THAR-to-CM transfer also favored MuRIL:

| Model | Train Dataset | Test Dataset | Positive Recall | Positive F1 | Macro F1 |
|---|---|---|---:|---:|---:|
| mBERT | `thar_religion` | `cm_splits_codemixed` | 40.1% | 45.0% | 59.8% |
| MuRIL | `thar_religion` | `cm_splits_codemixed` | 53.1% | 54.4% | 65.1% |

However, THAR-trained checkpoints transferred weakly to `kaggle_hinglish_hate`, with macro F1 below 47% for both models. This suggests that targeted religious hate training does not automatically generalize to broader Hinglish hate definitions.

## 6. Discussion

The current results do not support a simple statement that either mBERT or MuRIL is universally better. Instead, the model ranking changes by dataset situation.

Early interpretation:

- mBERT is stronger on matched Kaggle Hinglish hate and matched CM code-mixed offensive evaluation.
- MuRIL is more conservative after Kaggle Hinglish hate training.
- CM-trained MuRIL transfers better to THAR targeted religious hate than CM-trained mBERT.
- THAR-trained MuRIL is stronger than THAR-trained mBERT on matched THAR and THAR-to-CM transfer.
- THAR-trained models do not transfer well to the Kaggle Hinglish hate test condition.
- The 79-row diagnostic probe is excluded from primary conclusions because it may be synthetic/manual and has uncertain provenance.
- Cross-dataset evaluation is essential because in-domain performance alone hides transfer failures.

## 7. Limitations

Current limitations:

- The Kaggle source details need a final citation/metadata check.
- The positive class differs across datasets: hate, offensive, and AntiReligion are related but not identical.
- Some datasets are platform-specific, such as Twitter/X or YouTube.
- The 79-row diagnostic probe is provenance-uncertain and excluded from primary results.
- No threshold tuning has been performed yet.
- The project has not yet added a newly collected India-focused tweet dataset.

## 8. Conclusion

This project began as a direct comparison of mBERT and MuRIL for Hinglish hate speech detection, but current evidence shows that the more important research object is cross-dataset behavior. mBERT currently performs better in matched Romanized/code-mixed Kaggle and CM settings, while MuRIL offers advantages on the THAR targeted religious hate condition and in some Indian-context transfer settings. The final conclusion should be written after further dataset acquisition, error analysis, and possibly mixed-dataset training are complete.

## References

- Shardul Dhekane. `Code-Mixed Hinglish Hate Speech Detection Dataset`. Kaggle. https://www.kaggle.com/datasets/sharduldhekane/code-mixed-hinglish-hate-speech-detection-dataset
- THAR project repository. https://github.com/aakash-dl/THAR
- CM hate speech detection repository. https://github.com/shikharras/cm-hate-speech-detection
- mBERT: `bert-base-multilingual-cased`.
- MuRIL: `google/muril-base-cased`.
