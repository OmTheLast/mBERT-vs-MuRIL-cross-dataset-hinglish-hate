# CM Transformer Training Report

Date: 2026-06-25

## Purpose

This report documents the first controlled transformer training run on `cm_splits_codemixed`. The reason for this step was to stop relying only on the `kaggle_hinglish_hate` dataset and begin testing whether mBERT and MuRIL behave differently when trained on a more clearly Indian-context code-mixed dataset.

## Dataset Situation

| Dataset ID | Local Path | Rows | Label Meaning | Context | Caveat |
|---|---|---:|---|---|---|
| `cm_splits_codemixed` | `data/processed/cm_splits_codemixed.csv` | 3,900 before evaluator de-duplication | `0 = not offensive`, `1 = offensive` | Indian politics Hindi-English code-mixed Twitter/X data | Offensive/hate-adjacent, not strict hate speech |

The source-provided split was used:

- Train splits used for training: `train` + `val`
- Evaluation split: `test`
- Training script evaluation rows: 424
- Cross-dataset evaluator test rows after de-duplication: 415

The difference between 424 and 415 happens because the cross-dataset evaluator de-duplicates text rows before evaluation. This should be mentioned whenever training-script metrics are compared with cross-dataset metrics.

## Commands

```bash
.venv/bin/python experiments/train_mac_mps.py --model mbert --train-csv data/processed/cm_splits_codemixed.csv --text-column text --label-column label --split-column split --train-split train --train-split val --eval-split test --output-dir Models/mbert__train-cm_splits_codemixed__seed42__e2
```

```bash
.venv/bin/python experiments/train_mac_mps.py --model muril --train-csv data/processed/cm_splits_codemixed.csv --text-column text --label-column label --split-column split --train-split train --train-split val --eval-split test --output-dir Models/muril__train-cm_splits_codemixed__seed42__e2
```

## Training-Script Test Results

| Model | Train Dataset | Test Split | Accuracy | Positive Precision | Positive Recall | Positive F1 | Macro F1 |
|---|---|---|---:|---:|---:|---:|---:|
| mBERT | `cm_splits_codemixed` | source `test`, 424 rows | 80.9% | 74.8% | 69.3% | 72.0% | 78.7% |
| MuRIL | `cm_splits_codemixed` | source `test`, 424 rows | 79.2% | 79.2% | 56.0% | 65.6% | 75.4% |

On the matched CM test split, mBERT is stronger than MuRIL by positive-class F1 and macro F1. MuRIL has higher positive precision, but lower positive recall.

## Cross-Dataset Evaluation Results

The trained checkpoints were evaluated with:

```bash
.venv/bin/python experiments/run_transformer_cross_dataset_eval.py \
  --checkpoint mbert:kaggle_hinglish_hate:transformer_trained_on_kaggle_hinglish_hate:Models/mbert__train-kaggle_hinglish_hate__seed42__e2 \
  --checkpoint muril:kaggle_hinglish_hate:transformer_trained_on_kaggle_hinglish_hate:Models/muril__train-kaggle_hinglish_hate__seed42__e2 \
  --checkpoint mbert:cm_splits_codemixed:transformer_trained_on_cm_splits_codemixed:Models/mbert__train-cm_splits_codemixed__seed42__e2 \
  --checkpoint muril:cm_splits_codemixed:transformer_trained_on_cm_splits_codemixed:Models/muril__train-cm_splits_codemixed__seed42__e2 \
  --output results/transformer_cross_dataset_summary.csv \
  --detailed-output results/transformer_cross_dataset_predictions.csv
```

Key CM-trained transformer rows:

| Model | Train Dataset | Test Dataset | Test Rows | Accuracy | Positive Recall | Positive F1 | Macro F1 |
|---|---|---|---:|---:|---:|---:|---:|
| mBERT | `cm_splits_codemixed` | `kaggle_hinglish_hate` | 956 | 52.5% | 50.1% | 45.2% | 51.6% |
| mBERT | `cm_splits_codemixed` | `cm_splits_codemixed` | 415 | 80.5% | 68.7% | 71.4% | 78.3% |
| mBERT | `cm_splits_codemixed` | `thar_religion` | 2,310 | 59.6% | 44.6% | 51.0% | 58.3% |
| mBERT | `cm_splits_codemixed` | `existing_79_row_benchmark` | 79 | 46.8% | 2.6% | 4.5% | 33.9% |
| MuRIL | `cm_splits_codemixed` | `kaggle_hinglish_hate` | 956 | 54.5% | 49.9% | 46.1% | 53.4% |
| MuRIL | `cm_splits_codemixed` | `cm_splits_codemixed` | 415 | 78.8% | 55.1% | 64.8% | 74.8% |
| MuRIL | `cm_splits_codemixed` | `thar_religion` | 2,310 | 59.7% | 59.5% | 58.3% | 59.7% |
| MuRIL | `cm_splits_codemixed` | `existing_79_row_benchmark` | 79 | 50.6% | 2.6% | 4.9% | 35.8% |

## Interpretation

This result complicates the simple question "Is mBERT better than MuRIL?" in a useful way.

- On matched `cm_splits_codemixed` evaluation, mBERT is stronger.
- On transfer from CM to `thar_religion`, MuRIL is stronger on positive recall, positive F1, and macro F1.
- Both CM-trained transformers perform badly on the 79-row benchmark, catching only 1 of 39 positive examples. This supports the earlier warning that the 79-row benchmark has a different label/domain situation and should not be treated as a final test set.
- CM training makes both transformers less conservative on external positive examples compared with Kaggle-Hinglish-Hate training. This is especially visible on `thar_religion`.

## Paper-Relevant Takeaway

This stage suggested that model choice is less important than the interaction between model, training dataset, target dataset, and label definition. mBERT looked stronger for matched Romanized/code-mixed offensive data, while MuRIL looked more useful when transferring from CM to religious-targeted hate. The later THAR-trained checkpoints are documented in `docs/thar_transformer_training_report.md`.
