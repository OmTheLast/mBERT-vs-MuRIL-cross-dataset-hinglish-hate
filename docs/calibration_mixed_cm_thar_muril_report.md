# Mixed CM+THAR MuRIL Calibration Diagnostic

Date: 2026-07-02

Checkpoint: `Models/muril__train-mixed_cm_plus_thar__seed42__e2`
Training CSV for internal validation reconstruction: `data/processed/mixed_train_cm_plus_thar__seed42.csv`

## What This Checks

This diagnostic checks whether the all-negative result is caused by the default 0.50 threshold, or whether the model assigns low positive probability to nearly every example.

Important columns:

- `predicted_positive_at_0_50`: how many examples the normal classifier marks positive.
- `prob_positive_p95` and `prob_positive_max`: whether positive probabilities ever approach the decision threshold.
- `best_threshold_by_macro_f1`: the threshold that would maximize Macro F1 on that evaluation set.
- `best_f1_macro`: the best possible Macro F1 after threshold tuning on that same set.

## Summary

| eval_set             |   rows |   positive_rows |   predicted_positive_at_0_50 |   prob_positive_min |   prob_positive_p25 |   prob_positive_median |   prob_positive_p75 |   prob_positive_p95 |   prob_positive_max |   mean_prob_true_negative |   mean_prob_true_positive |   default_f1_macro |   default_recall_positive |   default_f1_positive |   best_threshold_by_macro_f1 |   best_f1_macro |   best_recall_positive |   best_f1_positive | split_policy                  | probabilities_file                                                                                                                                      |
|:---------------------|-------:|----------------:|-----------------------------:|--------------------:|--------------------:|-----------------------:|--------------------:|--------------------:|--------------------:|--------------------------:|--------------------------:|-------------------:|--------------------------:|----------------------:|-----------------------------:|----------------:|-----------------------:|-------------------:|:------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------|
| internal_validation  |   2527 |            1122 |                            0 |              0.4452 |              0.4456 |                 0.4456 |              0.4456 |              0.4456 |              0.4456 |                    0.4456 |                    0.4456 |             0.3573 |                    0.0000 |                0.0000 |                       0.5000 |          0.3573 |                 0.0000 |             0.0000 | stratified_80_20_split_seed42 | /Users/ompatnaik/Documents/Code/Hinglish Research/results/collapse_diagnostics/calibration_mixed_cm_thar_muril__internal_validation__probabilities.csv  |
| kaggle_hinglish_hate |    956 |             373 |                            0 |              0.4456 |              0.4456 |                 0.4456 |              0.4456 |              0.4456 |              0.4456 |                    0.4456 |                    0.4456 |             0.3788 |                    0.0000 |                0.0000 |                       0.5000 |          0.3788 |                 0.0000 |             0.0000 | stratified_80_20_split_seed42 | /Users/ompatnaik/Documents/Code/Hinglish Research/results/collapse_diagnostics/calibration_mixed_cm_thar_muril__kaggle_hinglish_hate__probabilities.csv |
| cm_splits_codemixed  |    415 |             147 |                            0 |              0.4454 |              0.4456 |                 0.4456 |              0.4456 |              0.4456 |              0.4456 |                    0.4456 |                    0.4456 |             0.3924 |                    0.0000 |                0.0000 |                       0.5000 |          0.3924 |                 0.0000 |             0.0000 | provided_test_split           | /Users/ompatnaik/Documents/Code/Hinglish Research/results/collapse_diagnostics/calibration_mixed_cm_thar_muril__cm_splits_codemixed__probabilities.csv  |
| thar_religion        |   2310 |            1091 |                            0 |              0.4453 |              0.4456 |                 0.4456 |              0.4456 |              0.4456 |              0.4456 |                    0.4456 |                    0.4456 |             0.3454 |                    0.0000 |                0.0000 |                       0.5000 |          0.3454 |                 0.0000 |             0.0000 | stratified_80_20_split_seed42 | /Users/ompatnaik/Documents/Code/Hinglish Research/results/collapse_diagnostics/calibration_mixed_cm_thar_muril__thar_religion__probabilities.csv        |

## Local Example File

Highest-positive-probability examples and strongest false negatives are saved at `/Users/ompatnaik/Documents/Code/Hinglish Research/results/collapse_diagnostics/calibration_mixed_cm_thar_muril__examples.csv`.
