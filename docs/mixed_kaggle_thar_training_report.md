# Mixed Kaggle+THAR Training Report

Date: 2026-07-04

This report records the third two-source mixed-dataset transformer experiment. The condition combines `kaggle_hinglish_hate` and `thar_religion`, pairing broad Hinglish hate-speech labels with targeted religious-hate labels.

## Experiment Question

Does adding THAR targeted religious-hate data to the Kaggle Hinglish hate dataset improve cross-dataset robustness, and does it allow MuRIL to recover from the mixed-training collapse seen in earlier conditions?

This mix was chosen because:

- `kaggle_hinglish_hate`: positive label means general Hinglish hate speech.
- `thar_religion`: positive label means AntiReligion / targeted religious hate in Hindi-English code-mixed YouTube comments.
- Matched THAR previously favored MuRIL, while matched Kaggle favored mBERT.
- Earlier mixed conditions showed mBERT stability and MuRIL instability, so this condition tests whether Kaggle+THAR is a more compatible mix for MuRIL.

## Training Condition

| Field | Value |
|---|---|
| Mixed dataset ID | `mixed_kaggle_plus_thar` |
| Training file | `data/processed/mixed_train_kaggle_plus_thar__seed42.csv` |
| Training rows | 13,063 |
| Positive rows | 5,856 |
| Negative rows | 7,207 |
| Positive rate | 44.8% |
| Source composition | Kaggle: 3,824 rows; THAR: 9,239 rows |
| Split/leakage policy | Mixed training CSV split internally using stratified 80/20 seed-42 validation |
| Held-out evaluations | Kaggle test split, CM source test split, THAR test split, 79-row diagnostic probe |
| Epochs | 2 |
| Seed | 42 |
| Max length | 128 |
| Learning rate | 2e-5 |
| Device | Apple MPS |

Local checkpoints:

- `Models/mbert__train-mixed_kaggle_plus_thar__seed42__e2`
- `Models/muril__train-mixed_kaggle_plus_thar__seed42__e2`

The model folders are ignored by Git because they contain large weights. The paper-facing summary file is:

```text
results/mixed_kaggle_plus_thar_transformer_summary.csv
```

## Internal Validation Results

| model | accuracy | positive recall | positive F1 | Macro F1 | interpretation |
|---|---:|---:|---:|---:|---|
| mBERT | 72.45% | 69.00% | 69.18% | 72.13% | Learned a usable mixed Kaggle+THAR boundary. |
| MuRIL | 73.78% | 69.68% | 70.44% | 73.44% | Also learned the mixed boundary; no collapse on this condition. |

## Cross-Dataset Results At Default Threshold 0.50

| model | train_dataset | test_dataset | accuracy | recall_positive | f1_positive | f1_macro | tn | fp | fn | tp |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| mBERT | `mixed_kaggle_plus_thar` | `kaggle_hinglish_hate` | 71.7% | 49.9% | 57.9% | 68.2% | 499 | 84 | 187 | 186 |
| mBERT | `mixed_kaggle_plus_thar` | `cm_splits_codemixed` | 60.0% | 34.0% | 37.6% | 54.1% | 199 | 69 | 97 | 50 |
| mBERT | `mixed_kaggle_plus_thar` | `thar_religion` | 74.9% | 78.5% | 74.7% | 74.9% | 875 | 344 | 235 | 856 |
| MuRIL | `mixed_kaggle_plus_thar` | `kaggle_hinglish_hate` | 70.1% | 48.5% | 55.9% | 66.6% | 489 | 94 | 192 | 181 |
| MuRIL | `mixed_kaggle_plus_thar` | `cm_splits_codemixed` | 65.5% | 37.4% | 43.5% | 59.3% | 217 | 51 | 92 | 55 |
| MuRIL | `mixed_kaggle_plus_thar` | `thar_religion` | 76.5% | 78.3% | 75.9% | 76.5% | 913 | 306 | 237 | 854 |

The 79-row diagnostic probe was also evaluated, but it remains excluded from primary conclusions because its provenance is unresolved and it performs poorly for both models.

## Calibration Diagnostic

Files:

- `docs/calibration_mixed_kaggle_thar_mbert_report.md`
- `docs/calibration_mixed_kaggle_thar_muril_report.md`
- `results/collapse_diagnostics/calibration_mixed_kaggle_thar_mbert__summary.csv`
- `results/collapse_diagnostics/calibration_mixed_kaggle_thar_muril__summary.csv`

mBERT showed meaningful probability separation:

- Internal validation median positive probability: 0.420.
- True positives had higher mean positive probability than true negatives: 0.643 vs 0.325.
- Best internal validation threshold by Macro F1 was 0.58.

MuRIL also showed meaningful probability separation:

- Internal validation median positive probability: 0.307.
- True positives had higher mean positive probability than true negatives: 0.637 vs 0.317.
- Best internal validation threshold by Macro F1 was 0.67.
- Unlike the CM+THAR MuRIL checkpoint, this run did not collapse to all-negative predictions or near-constant probabilities.

## Threshold Transfer

The threshold-transfer harness now includes `mixed_kaggle_plus_thar`.

Files:

- Script: `scripts/run_threshold_transfer.py`
- Result: `results/collapse_diagnostics/threshold_transfer_summary.csv`
- Report: `docs/threshold_transfer_report.md`

For mBERT, validation-selected threshold 0.58 did not improve the main held-out datasets:

- Kaggle Macro F1: 68.2% to 66.3%.
- CM Macro F1: 54.1% to 54.1%.
- THAR Macro F1: 74.9% to 74.6%.

For MuRIL, validation-selected threshold 0.67 gave small mixed effects:

- Kaggle Macro F1: 66.6% to 68.0%.
- CM Macro F1: 59.3% to 57.2%.
- THAR Macro F1: 76.5% to 77.0%.

This means threshold tuning is not the main explanation for the Kaggle+THAR behavior. The default-threshold results are already fairly representative.

## Interpretation

Kaggle+THAR is the first mixed condition where MuRIL avoids collapse and slightly leads mBERT on two of the three primary held-out datasets:

- mBERT remains slightly better on Kaggle-style general Hinglish hate.
- MuRIL is better on THAR targeted religious hate.
- MuRIL is also better on CM, even though CM was not part of this training mix.

The most likely explanation is dataset situation rather than a simple model ranking:

- THAR dominates the mixed training file by row count, so the model sees much more targeted religious-hate structure than Kaggle structure.
- MuRIL's Indic pretraining may help when the dataset contains more Indian-context or religious/cultural cues.
- Kaggle and THAR do not share identical positive-label definitions, so gains on THAR do not automatically transfer to Kaggle.
- CM remains a partially different situation because its positive class is offensive/hate-adjacent rather than strictly hate or AntiReligion.

Paper-safe wording:

> Under the current seed-42, two-epoch Kaggle+THAR mixed condition, both mBERT and MuRIL learned usable classifiers. MuRIL slightly outperformed mBERT on THAR and CM, while mBERT remained slightly stronger on Kaggle. This shows that MuRIL's earlier collapse is not universal, and that the relative advantage depends strongly on dataset mixture and label situation.

## Follow-Up

- Run multiple seeds before treating the MuRIL recovery as stable.
- Train the all-three mixed condition to test whether broader mixture improves CM without losing Kaggle or THAR.
- Consider balanced source sampling, because Kaggle+THAR is THAR-heavy.
- Keep default-threshold results separate from validation-threshold diagnostics in the paper.
