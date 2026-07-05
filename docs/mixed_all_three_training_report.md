# Mixed All-Three Training Report

Date: 2026-07-05

This report records the `mixed_all_three` experiment: training mBERT and MuRIL on the combined Kaggle Hinglish hate, CM code-mixed offensive, and THAR AntiReligion training sources, then evaluating each checkpoint on each dataset situation separately.

## Purpose

The goal was to test whether training on all available dataset situations improves cross-dataset robustness, or whether the largest/source-dominant dataset still shapes model behavior.

## Training Data

| Field | Value |
|---|---|
| Mixed dataset ID | `mixed_all_three` |
| Training file | `data/processed/mixed_train_all_three__seed42.csv` |
| Rows | 16,539 |
| Label counts | 9,388 negative, 7,151 positive |
| Positive rate | 43.2% |
| Source counts | THAR 9,239; Kaggle 3,824; CM 3,476 |
| Source balance caveat | THAR is the largest source, so all-three results may be pulled toward THAR-style targeted religious-hate behavior. |

## Checkpoints

| Model | Checkpoint | Internal Macro F1 | Internal Positive F1 | Internal Positive Recall |
|---|---|---:|---:|---:|
| mBERT | `Models/mbert__train-mixed_all_three__seed42__e2` | 72.4% | 67.9% | 65.5% |
| MuRIL | `Models/muril__train-mixed_all_three__seed42__e2` | 73.7% | 69.6% | 67.9% |

Internal validation uses the stratified 80/20 split reconstructed from the mixed training CSV. These numbers show that both models learned the combined training condition and did not collapse during training.

## Cross-Dataset Results

Primary source: `results/mixed_all_three_transformer_summary.csv`

| Model | Train dataset | Test dataset | Accuracy | Positive recall | Positive F1 | Macro F1 | TN | FP | FN | TP |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| mBERT | `mixed_all_three` | `kaggle_hinglish_hate` | 72.8% | 47.7% | 57.8% | 68.9% | 518 | 65 | 195 | 178 |
| mBERT | `mixed_all_three` | `cm_splits_codemixed` | 77.3% | 61.9% | 65.9% | 74.5% | 230 | 38 | 56 | 91 |
| mBERT | `mixed_all_three` | `thar_religion` | 74.1% | 74.4% | 73.1% | 74.0% | 899 | 320 | 279 | 812 |
| MuRIL | `mixed_all_three` | `kaggle_hinglish_hate` | 71.5% | 45.0% | 55.3% | 67.2% | 516 | 67 | 205 | 168 |
| MuRIL | `mixed_all_three` | `cm_splits_codemixed` | 77.6% | 58.5% | 64.9% | 74.2% | 236 | 32 | 61 | 86 |
| MuRIL | `mixed_all_three` | `thar_religion` | 76.3% | 77.0% | 75.4% | 76.2% | 922 | 297 | 251 | 840 |

The 79-row diagnostic probe remains excluded from the primary interpretation because its provenance and label quality are uncertain.

## Calibration Results

Calibration reports:

- `docs/calibration_mixed_all_three_mbert_report.md`
- `docs/calibration_mixed_all_three_muril_report.md`
- `docs/threshold_transfer_report.md`

Key calibration findings:

- Neither all-three checkpoint collapsed to all-negative predictions.
- mBERT had a wider positive-probability range, roughly 0.01 to 0.99.
- MuRIL had a more compressed probability range, roughly 0.14 to 0.80.
- Validation-selected thresholds were close to the default threshold: mBERT 0.47, MuRIL 0.42.
- Threshold transfer changed all-three Macro F1 only slightly, so the main dataset-level differences are not just default-threshold artifacts.

Calibration caveat: the diagnostic script reconstructs its internal validation split after cleaning and deduplicating text. The official internal validation numbers in the checkpoint table come from the training script's own split and `eval_metrics.json`; the calibration validation rows are used only for probability/threshold analysis.

## Interpretation

- All-three training produced the most balanced mixed-condition result so far: both models learned positives and transferred reasonably to CM and THAR.
- mBERT remained slightly stronger on Kaggle-style general Hinglish hate and slightly stronger on CM by Macro F1.
- MuRIL was stronger on THAR, matching the broader pattern that MuRIL can benefit from Indic/Indian-context targeted religious-hate data.
- The all-three mix did not erase cross-dataset differences. Kaggle positive recall remained below 50% for both models, while THAR positive recall was around 74-77%.
- Because the all-three training file is THAR-heavy, MuRIL's THAR strength should be interpreted with the source-balance caveat.

## Paper Implication

The all-three result strengthens the conditional claim: mBERT is generally more stable on Kaggle/CM-style code-mixed general hate or offensive data, while MuRIL can be competitive or stronger on THAR-style targeted religious hate. More data alone does not make the task universal, because dataset label definitions and source domains still shape the decision boundary.

## Figures

Updated mixed-training figures:

- `results/result_analysis/mixed_training_macro_f1.png`
- `results/result_analysis/mixed_training_macro_f1.svg`
- `results/result_analysis/mixed_training_muril_minus_mbert.png`
- `results/result_analysis/mixed_training_muril_minus_mbert.svg`
