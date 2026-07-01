# Transformer Cross-Dataset Evaluation Report

Date: 2026-06-24

## Purpose

This report documents the first cross-dataset evaluation of local transformer checkpoints. The goal is to test whether the mBERT and MuRIL models trained on `kaggle_hinglish_hate` generalize to other available dataset situations before training additional transformer checkpoints.

This is an evaluation-only step. No new transformer model was trained for this report.

## Evaluated Checkpoints

| Model | Checkpoint | Training Dataset | Condition |
|---|---|---|---|
| mBERT | `Models/mbert__train-kaggle_hinglish_hate__seed42__e2` | `kaggle_hinglish_hate` | trained during this session on the Hinglish-only subset |
| MuRIL | `Models/muril__train-kaggle_hinglish_hate__seed42__e2` | `kaggle_hinglish_hate` | trained during this session on the Hinglish-only subset |

Model registry: `docs/model_registry.md`

## Evaluation Datasets

The evaluator uses the same dataset test conditions as the cross-dataset baseline run.

| Dataset ID | Test Rows | Positive Label | Split Policy | Caveat |
|---|---:|---|---|---|
| `kaggle_hinglish_hate` | 956 | `1 = hate` | stratified 80/20 split, seed 42 | Indian-context status unclear/mixed |
| `cm_splits_codemixed` | 415 | `1 = offensive` | source-provided test split, after de-duplication | offensive/hate-adjacent, not strict hate |
| `thar_religion` | 2,310 | `1 = AntiReligion` | stratified 80/20 split, seed 42 | narrow targeted religious hate |
| `existing_79_row_benchmark` | 79 | `1 = hate` | fixed sanity benchmark | too small and label-noisy for final conclusions |

## Script And Outputs

Script:

```bash
.venv/bin/python experiments/run_transformer_cross_dataset_eval.py
```

Saved outputs:

| Output | Path |
|---|---|
| Summary metrics | `results/transformer_cross_dataset_summary.csv` |
| Detailed predictions | `results/transformer_cross_dataset_predictions.csv` |
| Combined result summary | `results/summary.md` |

Runtime:

- Device used: Apple MPS.
- Cleaning: minimal cleaning.
- De-duplication: enabled.
- Batch size: 16.
- Max sequence length: 128.

The Hugging Face tokenizer warning about `fix_mistral_regex` appeared again. This warning is already documented in the research journal. The flag is intentionally not used because it was previously tested and caused BERT/MuRIL tokenizer loading to fail.

## Results

| Model | Train Dataset | Test Dataset | Test Rows | Accuracy | Positive Recall | Positive F1 | Macro F1 | TP | FN | FP | TN |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| mBERT | `kaggle_hinglish_hate` | `kaggle_hinglish_hate` | 956 | 71.4% | 38.6% | 51.3% | 65.6% | 144 | 229 | 44 | 539 |
| mBERT | `kaggle_hinglish_hate` | `cm_splits_codemixed` | 415 | 63.1% | 19.7% | 27.5% | 51.4% | 29 | 118 | 35 | 233 |
| mBERT | `kaggle_hinglish_hate` | `thar_religion` | 2,310 | 52.6% | 15.9% | 24.0% | 44.8% | 173 | 918 | 178 | 1,041 |
| mBERT | `kaggle_hinglish_hate` | `existing_79_row_benchmark` | 79 | 51.9% | 7.7% | 13.6% | 40.2% | 3 | 36 | 2 | 38 |
| MuRIL | `kaggle_hinglish_hate` | `kaggle_hinglish_hate` | 956 | 67.5% | 22.3% | 34.8% | 56.6% | 83 | 290 | 21 | 562 |
| MuRIL | `kaggle_hinglish_hate` | `cm_splits_codemixed` | 415 | 65.8% | 14.3% | 22.8% | 50.4% | 21 | 126 | 16 | 252 |
| MuRIL | `kaggle_hinglish_hate` | `thar_religion` | 2,310 | 53.1% | 8.2% | 14.2% | 41.0% | 90 | 1,001 | 83 | 1,136 |
| MuRIL | `kaggle_hinglish_hate` | `existing_79_row_benchmark` | 79 | 64.6% | 35.9% | 50.0% | 61.3% | 14 | 25 | 3 | 37 |

## Interpretation

The `kaggle_hinglish_hate`-trained mBERT model performs best on the matched `kaggle_hinglish_hate` validation condition, with 65.6% macro F1 and 51.3% positive-class F1. This closely matches the earlier validation result and confirms that the new evaluator is using a comparable test condition.

The same mBERT checkpoint generalizes weakly to the external datasets:

- On `cm_splits_codemixed`, positive recall drops to 19.7%.
- On `thar_religion`, positive recall drops to 15.9%.

The `kaggle_hinglish_hate`-trained MuRIL model is more conservative on external datasets:

- On `cm_splits_codemixed`, it catches only 21 of 147 positive examples.
- On `thar_religion`, it catches only 90 of 1,091 positive examples.

However, MuRIL still performs better on the 79-row sanity benchmark, with 61.3% macro F1 and 50.0% positive-class F1. This repeats the earlier pattern: mBERT looks stronger on the held-out `kaggle_hinglish_hate` split, while MuRIL looks stronger on the small benchmark.

## Comparison Against Baselines

The Kaggle-Hinglish-Hate-trained transformers do not clearly dominate the TF-IDF baselines across datasets.

| Train Dataset | Test Dataset | Best Kaggle-Hinglish-Hate Transformer Macro F1 | Best Same-Train TF-IDF Macro F1 | Observation |
|---|---|---:|---:|---|
| `kaggle_hinglish_hate` | `kaggle_hinglish_hate` | 65.6% | 61.4% | mBERT improves macro F1 but has lower positive recall than Logistic Regression. |
| `kaggle_hinglish_hate` | `cm_splits_codemixed` | 51.4% | 39.3% | mBERT improves macro F1, but recall is far lower than TF-IDF. |
| `kaggle_hinglish_hate` | `thar_religion` | 44.8% | 49.9% | TF-IDF is stronger overall and catches more positives. |
| `kaggle_hinglish_hate` | `existing_79_row_benchmark` | 61.3% | 54.1% | MuRIL is strongest, but benchmark is tiny and label-noisy. |

The important pattern is not simply "transformers win" or "baselines win." Instead, each model family fails differently:

- Transformers trained on `kaggle_hinglish_hate` are conservative on external positive classes.
- TF-IDF baselines often catch more positives but also produce many false positives across dataset boundaries.

## Research Implications

This result strengthens the central paper argument:

- Training and evaluation dataset definitions strongly affect conclusions.
- `kaggle_hinglish_hate` training alone is not enough for reliable cross-dataset hate/offensive detection.
- MuRIL's advantage is not automatic, even though it is Indian-language-focused.
- mBERT's advantage on Romanized Hinglish does not automatically transfer to targeted religious hate or offensive political code-mix.

The next transformer experiments should train on `cm_splits_codemixed` and `thar_religion` directly. Only then can we test whether MuRIL improves when the training data is more Indian-context or Devanagari-heavy.

## Limitations

- Only `kaggle_hinglish_hate`-trained transformer checkpoints were evaluated here.
- `cm_splits_codemixed` and `thar_religion` use different positive-label definitions from `kaggle_hinglish_hate`.
- The 79-row benchmark should remain a sanity check, not a final evaluation set.
- No threshold tuning was performed; predictions use the default class with highest probability.

## Next Step Recorded At The Time

Train paired mBERT and MuRIL checkpoints on `cm_splits_codemixed`, then evaluate them with this same script. After that, repeat for `thar_religion`.

## Update: CM-Trained Checkpoints Added On 2026-06-25

The next step above was completed for `cm_splits_codemixed`. See `docs/cm_transformer_training_report.md` for the full training report.

New checkpoints:

| Model | Checkpoint | Training Dataset |
|---|---|---|
| mBERT | `Models/mbert__train-cm_splits_codemixed__seed42__e2` | `cm_splits_codemixed` |
| MuRIL | `Models/muril__train-cm_splits_codemixed__seed42__e2` | `cm_splits_codemixed` |

The combined transformer cross-dataset results are now saved in `results/transformer_cross_dataset_summary.csv`. The important new pattern is that CM-trained mBERT is strongest on matched CM evaluation, while CM-trained MuRIL transfers better to `thar_religion` on positive-class recall/F1.

## Update: THAR-Trained Checkpoints Added On 2026-06-25

The THAR training step has now been completed. See `docs/thar_transformer_training_report.md` for the full training report.

New checkpoints:

| Model | Checkpoint | Training Dataset |
|---|---|---|
| mBERT | `Models/mbert__train-thar_religion__seed42__e2` | `thar_religion` |
| MuRIL | `Models/muril__train-thar_religion__seed42__e2` | `thar_religion` |

The current full transformer matrix now contains six controlled checkpoints: paired mBERT/MuRIL runs trained on `kaggle_hinglish_hate`, `cm_splits_codemixed`, and `thar_religion`.

Key updated pattern:

- mBERT remains stronger on matched `kaggle_hinglish_hate`.
- mBERT remains stronger on matched `cm_splits_codemixed`.
- MuRIL is stronger on matched `thar_religion`.
- MuRIL is also stronger for THAR-to-CM transfer.
- No trained transformer is consistently strong across all dataset situations, and the 79-row benchmark remains unstable/noisy.

This update sharpens the paper argument: the project should not claim that either mBERT or MuRIL is universally better. It should report a conditional model comparison by dataset situation and label definition.
