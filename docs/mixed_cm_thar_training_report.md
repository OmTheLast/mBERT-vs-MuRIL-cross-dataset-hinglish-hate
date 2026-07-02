# Mixed CM+THAR Training Report

Date: 2026-07-02

This report records the second mixed-dataset transformer experiment. The condition combines `cm_splits_codemixed` and `thar_religion`, both Indian-context/code-mixed sources, but with different positive-label meanings.

## Experiment Question

Does training on CM plus THAR improve robustness for Indian-context hate/offensive detection, especially for MuRIL, which previously performed best on matched THAR?

This mix was chosen because:

- `cm_splits_codemixed`: positive label means offensive or hate-adjacent content in Indian political code-mixed posts.
- `thar_religion`: positive label means AntiReligion / targeted religious hate in Hindi-English code-mixed YouTube comments.
- MuRIL had previously beaten mBERT on matched THAR, so this mix tests whether adding THAR-like targeted-hate signal helps MuRIL remain useful under mixed training.

## Training Condition

| Field | Value |
|---|---|
| Mixed dataset ID | `mixed_cm_plus_thar` |
| Training file | `data/processed/mixed_train_cm_plus_thar__seed42.csv` |
| Training rows | 12,715 |
| Positive rows | 5,658 |
| Negative rows | 7,057 |
| Positive rate | 44.5% |
| Source composition | CM: 2,181 negative / 1,295 positive; THAR: 4,876 negative / 4,363 positive |
| Split/leakage policy | Mixed training CSV split internally using stratified 80/20 seed-42 validation |
| Held-out evaluations | Kaggle test split, CM source test split, THAR test split, 79-row diagnostic probe |
| Epochs | 2 |
| Seed | 42 |
| Max length | 128 |
| Learning rate | 2e-5 |
| Device | Apple MPS |

Local checkpoints:

- `Models/mbert__train-mixed_cm_plus_thar__seed42__e2`
- `Models/muril__train-mixed_cm_plus_thar__seed42__e2`

The model folders are ignored by Git because they contain large weights. The paper-facing summary file is:

```text
results/mixed_cm_plus_thar_transformer_summary.csv
```

## Internal Validation Results

| model | accuracy | positive recall | positive F1 | Macro F1 | interpretation |
|---|---:|---:|---:|---:|---|
| mBERT | 74.95% | 71.55% | 71.78% | 74.63% | Learned a usable mixed CM+THAR decision boundary. |
| MuRIL | 55.49% | 0.00% | 0.00% | 35.69% | Collapsed to all-negative predictions on validation. |

## Cross-Dataset Results At Default Threshold 0.50

| model | train_dataset | test_dataset | accuracy | recall_positive | f1_positive | f1_macro | tn | fp | fn | tp |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| mBERT | `mixed_cm_plus_thar` | `kaggle_hinglish_hate` | 52.7% | 26.5% | 30.5% | 47.3% | 405 | 178 | 274 | 99 |
| mBERT | `mixed_cm_plus_thar` | `cm_splits_codemixed` | 77.8% | 67.3% | 68.3% | 75.6% | 224 | 44 | 48 | 99 |
| mBERT | `mixed_cm_plus_thar` | `thar_religion` | 75.6% | 76.9% | 74.9% | 75.6% | 908 | 311 | 252 | 839 |
| MuRIL | `mixed_cm_plus_thar` | `kaggle_hinglish_hate` | 61.0% | 0.0% | 0.0% | 37.9% | 583 | 0 | 373 | 0 |
| MuRIL | `mixed_cm_plus_thar` | `cm_splits_codemixed` | 64.6% | 0.0% | 0.0% | 39.2% | 268 | 0 | 147 | 0 |
| MuRIL | `mixed_cm_plus_thar` | `thar_religion` | 52.8% | 0.0% | 0.0% | 34.5% | 1219 | 0 | 1091 | 0 |

The 79-row diagnostic probe was also evaluated but remains excluded from primary conclusions.

## Calibration Diagnostic

Files:

- `docs/calibration_mixed_cm_thar_mbert_report.md`
- `docs/calibration_mixed_cm_thar_muril_report.md`
- `results/collapse_diagnostics/calibration_mixed_cm_thar_mbert__summary.csv`
- `results/collapse_diagnostics/calibration_mixed_cm_thar_muril__summary.csv`

mBERT had meaningful probability separation:

- Internal validation median positive probability: 0.364.
- Internal validation 75th percentile positive probability: 0.770.
- True positives had higher mean positive probability than true negatives: 0.665 vs 0.221.
- Validation-selected threshold was 0.45.

MuRIL did not show meaningful probability separation:

- Positive probabilities were almost constant around 0.4456 across all datasets.
- True positives and true negatives had almost identical mean positive probability.
- At threshold 0.50 it predicted zero positives everywhere.
- Validation-selected threshold remained 0.50, so threshold transfer did not recover recall.

## Threshold Transfer

The threshold-transfer harness now includes `mixed_cm_plus_thar`.

Files:

- Script: `scripts/run_threshold_transfer.py`
- Result: `results/collapse_diagnostics/threshold_transfer_summary.csv`
- Report: `docs/threshold_transfer_report.md`

For mBERT, validation-selected threshold 0.45 slightly improved CM and THAR:

- Kaggle Macro F1: 47.3% to 47.5%; positive recall 26.5% to 29.8%.
- CM Macro F1: 75.6% to 76.5%; positive recall 67.3% to 71.4%.
- THAR Macro F1: 75.6% to 75.7%; positive recall 76.9% to 78.4%.

For MuRIL, validation-selected threshold 0.50 made no change:

- Kaggle, CM, and THAR positive recall stayed at 0.0%.
- This differs from the earlier Kaggle+CM MuRIL case, where a validation-selected lower threshold recovered useful positive recall.

## Interpretation

CM+THAR mBERT is strong on CM and THAR but weak on Kaggle. This supports the dataset-situation argument:

- CM and THAR share more Indian political/religious context than Kaggle.
- Kaggle's positive label is general hate, while CM is offensive/hate-adjacent and THAR is AntiReligion.
- Mixing CM and THAR helps with the CM/THAR situation but does not create a general Kaggle Hinglish hate detector.

CM+THAR MuRIL is the clearest collapse observed so far. Unlike Kaggle+CM MuRIL, the collapse is not simply a threshold problem. The probability diagnostic shows near-constant positive probabilities across examples, which means the model did not learn a useful positive/negative separation under this setup.

Paper-safe wording:

> Under the current seed-42, two-epoch CM+THAR mixed condition, mBERT learned a transferable CM/THAR boundary, while MuRIL collapsed to a near-constant all-negative classifier. This suggests that MuRIL's matched THAR advantage does not automatically survive mixed-label training, and that dataset compatibility and optimization stability must be treated as central experimental variables.

## Follow-Up

- Repeat this condition with multiple seeds before treating the MuRIL collapse as stable.
- Consider class weighting or focal loss if MuRIL repeatedly collapses on mixed datasets.
- Compare against the remaining mixed conditions: `mixed_kaggle_plus_thar` and `mixed_all_three`.
- Keep default-threshold results separate from validation-threshold diagnostics in the paper.
