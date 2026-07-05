# Mixed All-Three MuRIL Calibration Diagnostic

Date: 2026-07-02

Checkpoint: `Models/muril__train-mixed_all_three__seed42__e2`
Training CSV for internal validation reconstruction: `data/processed/mixed_train_all_three__seed42.csv`

## What This Checks

This diagnostic checks whether the all-negative result is caused by the default 0.50 threshold, or whether the model assigns low positive probability to nearly every example.

Important columns:

- `predicted_positive_at_0_50`: how many examples the normal classifier marks positive.
- `prob_positive_p95` and `prob_positive_max`: whether positive probabilities ever approach the decision threshold.
- `best_threshold_by_macro_f1`: the threshold that would maximize Macro F1 on that evaluation set.
- `best_f1_macro`: the best possible Macro F1 after threshold tuning on that same set.

## Summary

| eval_set             |   rows |   positive_rows |   predicted_positive_at_0_50 |   prob_positive_min |   prob_positive_p25 |   prob_positive_median |   prob_positive_p75 |   prob_positive_p95 |   prob_positive_max |   mean_prob_true_negative |   mean_prob_true_positive |   default_f1_macro |   default_recall_positive |   default_f1_positive |   best_threshold_by_macro_f1 |   best_f1_macro |   best_recall_positive |   best_f1_positive | split_policy                  | probabilities_file                                                                                                                                        |
|:---------------------|-------:|----------------:|-----------------------------:|--------------------:|--------------------:|-----------------------:|--------------------:|--------------------:|--------------------:|--------------------------:|--------------------------:|-------------------:|--------------------------:|----------------------:|-----------------------------:|----------------:|-----------------------:|-------------------:|:------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------|
| internal_validation  |   3292 |            1421 |                         1297 |              0.1401 |              0.1503 |                 0.2307 |              0.7801 |              0.8033 |              0.8045 |                    0.2654 |                    0.6059 |             0.7763 |                    0.7051 |                0.7373 |                       0.4200 |          0.7822 |                 0.7333 |             0.7486 | stratified_80_20_split_seed42 | /Users/ompatnaik/Documents/Code/Hinglish Research/results/collapse_diagnostics/calibration_mixed_all_three_muril__internal_validation__probabilities.csv  |
| kaggle_hinglish_hate |    956 |             373 |                          235 |              0.1402 |              0.1606 |                 0.2189 |              0.4847 |              0.8019 |              0.8040 |                    0.2633 |                    0.4491 |             0.6720 |                    0.4504 |                0.5526 |                       0.3100 |          0.6984 |                 0.5818 |             0.6182 | stratified_80_20_split_seed42 | /Users/ompatnaik/Documents/Code/Hinglish Research/results/collapse_diagnostics/calibration_mixed_all_three_muril__kaggle_hinglish_hate__probabilities.csv |
| cm_splits_codemixed  |    415 |             147 |                          118 |              0.1401 |              0.1463 |                 0.1788 |              0.6345 |              0.8020 |              0.8044 |                    0.2382 |                    0.5437 |             0.7422 |                    0.5850 |                0.6491 |                       0.2800 |          0.7716 |                 0.7347 |             0.7105 | provided_test_split           | /Users/ompatnaik/Documents/Code/Hinglish Research/results/collapse_diagnostics/calibration_mixed_all_three_muril__cm_splits_codemixed__probabilities.csv  |
| thar_religion        |   2310 |            1091 |                         1137 |              0.1399 |              0.1501 |                 0.4679 |              0.7932 |              0.8037 |              0.8044 |                    0.3132 |                    0.6438 |             0.7625 |                    0.7699 |                0.7540 |                       0.5200 |          0.7632 |                 0.7635 |             0.7532 | stratified_80_20_split_seed42 | /Users/ompatnaik/Documents/Code/Hinglish Research/results/collapse_diagnostics/calibration_mixed_all_three_muril__thar_religion__probabilities.csv        |

## Local Example File

Highest-positive-probability examples and strongest false negatives are saved at `/Users/ompatnaik/Documents/Code/Hinglish Research/results/collapse_diagnostics/calibration_mixed_all_three_muril__examples.csv`.
