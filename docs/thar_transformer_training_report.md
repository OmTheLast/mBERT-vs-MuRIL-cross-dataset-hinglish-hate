# THAR Transformer Training Report

Date: 2026-06-25

## Purpose

This report documents the controlled transformer training runs on `thar_religion`. The reason for this step was to test whether mBERT and MuRIL behave differently when trained on a narrower Hindi-English code-mixed targeted religious hate dataset rather than on the broader Kaggle Hinglish hate or CM offensive datasets.

## Dataset Situation

| Dataset ID | Local Path | Rows | Label Meaning | Context | Caveat |
|---|---|---:|---|---|---|
| `thar_religion` | `data/processed/thar_religion.csv` | 11,549 | `0 = Non-AntiReligion`, `1 = AntiReligion` | Hindi-English code-mixed YouTube comments about targeted religious hate | Narrow targeted religious hate, not general hate speech |

The training script used a stratified 80/20 split with seed 42.

- Training rows: 9,239
- Evaluation rows: 2,310
- Cleaning: minimal URL/user normalization
- Epochs: 2
- Device: Apple MPS

## Commands

```bash
.venv/bin/python experiments/train_mac_mps.py --model mbert --train-csv data/processed/thar_religion.csv --text-column text --label-column label --output-dir Models/mbert__train-thar_religion__seed42__e2
```

```bash
.venv/bin/python experiments/train_mac_mps.py --model muril --train-csv data/processed/thar_religion.csv --text-column text --label-column label --output-dir Models/muril__train-thar_religion__seed42__e2
```

## Training-Script Test Results

| Model | Train Dataset | Test Split | Accuracy | Positive Precision | Positive Recall | Positive F1 | Macro F1 |
|---|---|---|---:|---:|---:|---:|---:|
| mBERT | `thar_religion` | stratified 20%, 2,310 rows | 74.8% | 71.4% | 77.7% | 74.5% | 74.8% |
| MuRIL | `thar_religion` | stratified 20%, 2,310 rows | 77.9% | 74.7% | 80.3% | 77.4% | 77.9% |

On the matched THAR split, MuRIL is stronger than mBERT across accuracy, positive recall, positive F1, and macro F1.

## Cross-Dataset Evaluation Results

The trained checkpoints were evaluated with the full six-checkpoint matrix:

```bash
.venv/bin/python experiments/run_transformer_cross_dataset_eval.py \
  --checkpoint mbert:kaggle_hinglish_hate:transformer_trained_on_kaggle_hinglish_hate:Models/mbert__train-kaggle_hinglish_hate__seed42__e2 \
  --checkpoint muril:kaggle_hinglish_hate:transformer_trained_on_kaggle_hinglish_hate:Models/muril__train-kaggle_hinglish_hate__seed42__e2 \
  --checkpoint mbert:cm_splits_codemixed:transformer_trained_on_cm_splits_codemixed:Models/mbert__train-cm_splits_codemixed__seed42__e2 \
  --checkpoint muril:cm_splits_codemixed:transformer_trained_on_cm_splits_codemixed:Models/muril__train-cm_splits_codemixed__seed42__e2 \
  --checkpoint mbert:thar_religion:transformer_trained_on_thar_religion:Models/mbert__train-thar_religion__seed42__e2 \
  --checkpoint muril:thar_religion:transformer_trained_on_thar_religion:Models/muril__train-thar_religion__seed42__e2 \
  --output results/transformer_cross_dataset_summary.csv \
  --detailed-output results/transformer_cross_dataset_predictions.csv
```

Key THAR-trained transformer rows:

| Model | Train Dataset | Test Dataset | Test Rows | Accuracy | Positive Recall | Positive F1 | Macro F1 |
|---|---|---|---:|---:|---:|---:|---:|
| mBERT | `thar_religion` | `kaggle_hinglish_hate` | 956 | 52.9% | 20.6% | 25.5% | 45.5% |
| mBERT | `thar_religion` | `cm_splits_codemixed` | 415 | 65.3% | 40.1% | 45.0% | 59.8% |
| mBERT | `thar_religion` | `thar_religion` | 2,310 | 74.8% | 77.7% | 74.5% | 74.8% |
| mBERT | `thar_religion` | `existing_79_row_benchmark` | 79 | 51.9% | 5.1% | 9.5% | 38.4% |
| MuRIL | `thar_religion` | `kaggle_hinglish_hate` | 956 | 52.5% | 23.3% | 27.7% | 46.2% |
| MuRIL | `thar_religion` | `cm_splits_codemixed` | 415 | 68.4% | 53.1% | 54.4% | 65.1% |
| MuRIL | `thar_religion` | `thar_religion` | 2,310 | 77.9% | 80.3% | 77.4% | 77.9% |
| MuRIL | `thar_religion` | `existing_79_row_benchmark` | 79 | 53.2% | 5.1% | 9.8% | 39.1% |

## Interpretation

This is the clearest MuRIL-favorable result so far. When the training and test situation is THAR targeted religious hate, MuRIL beats mBERT by 3.1 macro F1 points and 2.9 positive F1 points. MuRIL also transfers better from THAR training to the CM code-mixed offensive test set.

The result does not generalize to every setting:

- THAR-trained checkpoints transfer weakly to `kaggle_hinglish_hate`.
- THAR-trained checkpoints perform poorly on the 79-row sanity benchmark, catching only 2 of 39 positive examples.
- The THAR positive label is AntiReligion, so strong THAR results should not be described as proof of general Hinglish hate-speech performance.

## Paper-Relevant Takeaway

The THAR result supports a conditional conclusion: MuRIL can outperform mBERT when the dataset situation is closer to targeted Indian religious hate, but it does not automatically solve cross-dataset Hinglish hate detection. The paper should avoid a single leaderboard framing and instead report model behavior by training dataset, test dataset, and label definition.
