# Mixed CM+THAR mBERT Calibration Diagnostic

Date: 2026-07-02

Checkpoint: `Models/mbert__train-mixed_cm_plus_thar__seed42__e2`
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
| internal_validation  |   2527 |            1122 |                         1145 |              0.0218 |              0.0665 |                 0.3635 |              0.7703 |              0.8929 |              0.9066 |                    0.2206 |                    0.6652 |             0.7996 |                    0.7870 |                0.7790 |                       0.4500 |          0.8042 |                 0.8075 |             0.7868 | stratified_80_20_split_seed42 | /Users/ompatnaik/Documents/Code/Hinglish Research/results/collapse_diagnostics/calibration_mixed_cm_thar_mbert__internal_validation__probabilities.csv  |
| kaggle_hinglish_hate |    956 |             373 |                          277 |              0.0222 |              0.0690 |                 0.2303 |              0.5730 |              0.8141 |              0.8982 |                    0.3391 |                    0.2988 |             0.4732 |                    0.2654 |                0.3046 |                       0.2200 |          0.4876 |                 0.5040 |             0.4367 | stratified_80_20_split_seed42 | /Users/ompatnaik/Documents/Code/Hinglish Research/results/collapse_diagnostics/calibration_mixed_cm_thar_mbert__kaggle_hinglish_hate__probabilities.csv |
| cm_splits_codemixed  |    415 |             147 |                          143 |              0.0223 |              0.0532 |                 0.2197 |              0.6317 |              0.8464 |              0.8976 |                    0.2142 |                    0.5752 |             0.7562 |                    0.6735 |                0.6828 |                       0.4000 |          0.7695 |                 0.7619 |             0.7134 | provided_test_split           | /Users/ompatnaik/Documents/Code/Hinglish Research/results/collapse_diagnostics/calibration_mixed_cm_thar_mbert__cm_splits_codemixed__probabilities.csv  |
| thar_religion        |   2310 |            1091 |                         1150 |              0.0220 |              0.0821 |                 0.4938 |              0.7926 |              0.8949 |              0.9059 |                    0.2750 |                    0.6525 |             0.7561 |                    0.7690 |                0.7488 |                       0.5200 |          0.7573 |                 0.7635 |             0.7484 | stratified_80_20_split_seed42 | /Users/ompatnaik/Documents/Code/Hinglish Research/results/collapse_diagnostics/calibration_mixed_cm_thar_mbert__thar_religion__probabilities.csv        |

## Local Example File

Highest-positive-probability examples and strongest false negatives are saved at `/Users/ompatnaik/Documents/Code/Hinglish Research/results/collapse_diagnostics/calibration_mixed_cm_thar_mbert__examples.csv`.
