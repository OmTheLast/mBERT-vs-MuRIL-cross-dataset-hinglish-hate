# Mixed All-Three mBERT Calibration Diagnostic

Date: 2026-07-02

Checkpoint: `Models/mbert__train-mixed_all_three__seed42__e2`
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
| internal_validation  |   3292 |            1421 |                         1316 |              0.0122 |              0.0807 |                 0.3104 |              0.7663 |              0.9507 |              0.9905 |                    0.2163 |                    0.6714 |             0.8065 |                    0.7452 |                0.7738 |                       0.4700 |          0.8081 |                 0.7643 |             0.7788 | stratified_80_20_split_seed42 | /Users/ompatnaik/Documents/Code/Hinglish Research/results/collapse_diagnostics/calibration_mixed_all_three_mbert__internal_validation__probabilities.csv  |
| kaggle_hinglish_hate |    956 |             373 |                          243 |              0.0222 |              0.1065 |                 0.2361 |              0.5065 |              0.9769 |              0.9906 |                    0.2311 |                    0.5404 |             0.6887 |                    0.4772 |                0.5779 |                       0.3500 |          0.7100 |                 0.5979 |             0.6335 | stratified_80_20_split_seed42 | /Users/ompatnaik/Documents/Code/Hinglish Research/results/collapse_diagnostics/calibration_mixed_all_three_mbert__kaggle_hinglish_hate__probabilities.csv |
| cm_splits_codemixed  |    415 |             147 |                          129 |              0.0120 |              0.0425 |                 0.2101 |              0.6380 |              0.8738 |              0.9641 |                    0.1977 |                    0.5624 |             0.7449 |                    0.6190 |                0.6594 |                       0.3800 |          0.7486 |                 0.7075 |             0.6820 | provided_test_split           | /Users/ompatnaik/Documents/Code/Hinglish Research/results/collapse_diagnostics/calibration_mixed_all_three_mbert__cm_splits_codemixed__probabilities.csv  |
| thar_religion        |   2310 |            1091 |                         1132 |              0.0162 |              0.0896 |                 0.4770 |              0.8036 |              0.9483 |              0.9721 |                    0.2850 |                    0.6593 |             0.7403 |                    0.7443 |                0.7305 |                       0.3600 |          0.7445 |                 0.8093 |             0.7496 | stratified_80_20_split_seed42 | /Users/ompatnaik/Documents/Code/Hinglish Research/results/collapse_diagnostics/calibration_mixed_all_three_mbert__thar_religion__probabilities.csv        |

## Local Example File

Highest-positive-probability examples and strongest false negatives are saved at `/Users/ompatnaik/Documents/Code/Hinglish Research/results/collapse_diagnostics/calibration_mixed_all_three_mbert__examples.csv`.
