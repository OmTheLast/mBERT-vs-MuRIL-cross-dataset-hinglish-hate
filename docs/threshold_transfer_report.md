# Validation-Selected Threshold Transfer

Date: 2026-07-02

This report applies thresholds selected on validation probability files to held-out evaluation sets.

Threshold search step: `0.01`

## Important Caveat

For the Kaggle-only checkpoints, the reconstructed internal validation split is the same split used as the Kaggle held-out evaluation in the earlier experiments. Therefore, the Kaggle matched rows for those two checkpoints are diagnostic rather than paper-safe. Their CM and THAR transfer rows remain independent of that Kaggle validation split.

For the mixed Kaggle+CM checkpoints, the internal validation split comes from the mixed training CSV, while Kaggle, CM, and THAR evaluations are held-out source test sets. Those rows are the cleanest threshold-transfer evidence in this first pass.

## Summary

| training_condition   | model   | test_dataset         |   selected_threshold |   default_f1_macro |   threshold_f1_macro |   macro_f1_delta |   default_recall_positive |   threshold_recall_positive |   positive_recall_delta |   default_f1_positive |   threshold_f1_positive | leakage_caveat   |
|:---------------------|:--------|:---------------------|---------------------:|-------------------:|---------------------:|-----------------:|--------------------------:|----------------------------:|------------------------:|----------------------:|------------------------:|:-----------------|
| kaggle_hinglish_hate | mbert   | kaggle_hinglish_hate |                 0.32 |              0.656 |                0.672 |            0.017 |                     0.386 |                       0.598 |                   0.212 |                 0.513 |                   0.599 | True             |
| kaggle_hinglish_hate | mbert   | cm_splits_codemixed  |                 0.32 |              0.514 |                0.537 |            0.023 |                     0.197 |                       0.435 |                   0.238 |                 0.275 |                   0.417 | False            |
| kaggle_hinglish_hate | mbert   | thar_religion        |                 0.32 |              0.448 |                0.537 |            0.089 |                     0.159 |                       0.375 |                   0.216 |                 0.24  |                   0.443 | False            |
| kaggle_hinglish_hate | muril   | kaggle_hinglish_hate |                 0.35 |              0.566 |                0.646 |            0.08  |                     0.223 |                       0.52  |                   0.298 |                 0.348 |                   0.552 | True             |
| kaggle_hinglish_hate | muril   | cm_splits_codemixed  |                 0.35 |              0.504 |                0.341 |           -0.163 |                     0.143 |                       0.823 |                   0.68  |                 0.228 |                   0.481 | False            |
| kaggle_hinglish_hate | muril   | thar_religion        |                 0.35 |              0.41  |                0.532 |            0.123 |                     0.082 |                       0.46  |                   0.378 |                 0.142 |                   0.484 | False            |
| mixed_kaggle_plus_cm | mbert   | kaggle_hinglish_hate |                 0.41 |              0.685 |                0.705 |            0.02  |                     0.453 |                       0.579 |                   0.126 |                 0.566 |                   0.623 | False            |
| mixed_kaggle_plus_cm | mbert   | cm_splits_codemixed  |                 0.41 |              0.715 |                0.744 |            0.029 |                     0.599 |                       0.707 |                   0.109 |                 0.624 |                   0.678 | False            |
| mixed_kaggle_plus_cm | mbert   | thar_religion        |                 0.41 |              0.493 |                0.538 |            0.045 |                     0.229 |                       0.348 |                   0.119 |                 0.324 |                   0.43  | False            |
| mixed_kaggle_plus_cm | muril   | kaggle_hinglish_hate |                 0.42 |              0.379 |                0.609 |            0.23  |                     0     |                       0.523 |                   0.523 |                 0     |                   0.523 | False            |
| mixed_kaggle_plus_cm | muril   | cm_splits_codemixed  |                 0.42 |              0.392 |                0.584 |            0.192 |                     0     |                       0.476 |                   0.476 |                 0     |                   0.468 | False            |
| mixed_kaggle_plus_cm | muril   | thar_religion        |                 0.42 |              0.345 |                0.52  |            0.175 |                     0     |                       0.294 |                   0.294 |                 0     |                   0.386 | False            |
| mixed_cm_plus_thar   | mbert   | kaggle_hinglish_hate |                 0.45 |              0.473 |                0.475 |            0.002 |                     0.265 |                       0.298 |                   0.032 |                 0.305 |                   0.325 | False            |
| mixed_cm_plus_thar   | mbert   | cm_splits_codemixed  |                 0.45 |              0.756 |                0.765 |            0.009 |                     0.673 |                       0.714 |                   0.041 |                 0.683 |                   0.7   | False            |
| mixed_cm_plus_thar   | mbert   | thar_religion        |                 0.45 |              0.756 |                0.757 |            0.001 |                     0.769 |                       0.784 |                   0.015 |                 0.749 |                   0.753 | False            |
| mixed_cm_plus_thar   | muril   | kaggle_hinglish_hate |                 0.5  |              0.379 |                0.379 |            0     |                     0     |                       0     |                   0     |                 0     |                   0     | False            |
| mixed_cm_plus_thar   | muril   | cm_splits_codemixed  |                 0.5  |              0.392 |                0.392 |            0     |                     0     |                       0     |                   0     |                 0     |                   0     | False            |
| mixed_cm_plus_thar   | muril   | thar_religion        |                 0.5  |              0.345 |                0.345 |            0     |                     0     |                       0     |                   0     |                 0     |                   0     | False            |

## Interpretation

- If threshold tuning improves positive recall and Macro F1, the default `0.50` cutoff was hiding useful positive-class signal.
- If threshold tuning improves recall but hurts Macro F1, the model may be trading too many false positives for recall.
- These results should be interpreted alongside the default-threshold results, not as a replacement for model comparison.
