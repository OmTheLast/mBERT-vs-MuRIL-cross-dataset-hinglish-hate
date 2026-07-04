# Mixed Kaggle+THAR MuRIL Calibration Diagnostic

Date: 2026-07-02

Checkpoint: `Models/muril__train-mixed_kaggle_plus_thar__seed42__e2`
Training CSV for internal validation reconstruction: `data/processed/mixed_train_kaggle_plus_thar__seed42.csv`

## What This Checks

This diagnostic checks whether the all-negative result is caused by the default 0.50 threshold, or whether the model assigns low positive probability to nearly every example.

Important columns:

- `predicted_positive_at_0_50`: how many examples the normal classifier marks positive.
- `prob_positive_p95` and `prob_positive_max`: whether positive probabilities ever approach the decision threshold.
- `best_threshold_by_macro_f1`: the threshold that would maximize Macro F1 on that evaluation set.
- `best_f1_macro`: the best possible Macro F1 after threshold tuning on that same set.

## Summary

| eval_set             |   rows |   positive_rows |   predicted_positive_at_0_50 |   prob_positive_min |   prob_positive_p25 |   prob_positive_median |   prob_positive_p75 |   prob_positive_p95 |   prob_positive_max |   mean_prob_true_negative |   mean_prob_true_positive |   default_f1_macro |   default_recall_positive |   default_f1_positive |   best_threshold_by_macro_f1 |   best_f1_macro |   best_recall_positive |   best_f1_positive | split_policy                  | probabilities_file                                                                                                                                          |
|:---------------------|-------:|----------------:|-----------------------------:|--------------------:|--------------------:|-----------------------:|--------------------:|--------------------:|--------------------:|--------------------------:|--------------------------:|-------------------:|--------------------------:|----------------------:|-----------------------------:|----------------:|-----------------------:|-------------------:|:------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------|
| internal_validation  |   2613 |            1171 |                         1168 |              0.1392 |              0.1578 |                 0.3069 |              0.8133 |              0.8305 |              0.8311 |                    0.3170 |                    0.6372 |             0.7434 |                    0.7156 |                0.7165 |                       0.6700 |          0.7488 |                 0.6815 |             0.7128 | stratified_80_20_split_seed42 | /Users/ompatnaik/Documents/Code/Hinglish Research/results/collapse_diagnostics/calibration_mixed_kaggle_thar_muril__internal_validation__probabilities.csv  |
| kaggle_hinglish_hate |    956 |             373 |                          275 |              0.1396 |              0.1688 |                 0.2459 |              0.6687 |              0.8302 |              0.8308 |                    0.2928 |                    0.5135 |             0.6662 |                    0.4853 |                0.5586 |                       0.6800 |          0.6822 |                 0.4638 |             0.5672 | stratified_80_20_split_seed42 | /Users/ompatnaik/Documents/Code/Hinglish Research/results/collapse_diagnostics/calibration_mixed_kaggle_thar_muril__kaggle_hinglish_hate__probabilities.csv |
| cm_splits_codemixed  |    415 |             147 |                          106 |              0.1406 |              0.1811 |                 0.2459 |              0.5106 |              0.8181 |              0.8305 |                    0.3317 |                    0.4267 |             0.5935 |                    0.3741 |                0.4348 |                       0.3700 |          0.6012 |                 0.4694 |             0.4792 | provided_test_split           | /Users/ompatnaik/Documents/Code/Hinglish Research/results/collapse_diagnostics/calibration_mixed_kaggle_thar_muril__cm_splits_codemixed__probabilities.csv  |
| thar_religion        |   2310 |            1091 |                         1160 |              0.1390 |              0.1510 |                 0.5162 |              0.8160 |              0.8305 |              0.8311 |                    0.3210 |                    0.6738 |             0.7648 |                    0.7828 |                0.7588 |                       0.6700 |          0.7701 |                 0.7498 |             0.7557 | stratified_80_20_split_seed42 | /Users/ompatnaik/Documents/Code/Hinglish Research/results/collapse_diagnostics/calibration_mixed_kaggle_thar_muril__thar_religion__probabilities.csv        |

## Local Example File

Highest-positive-probability examples and strongest false negatives are saved at `/Users/ompatnaik/Documents/Code/Hinglish Research/results/collapse_diagnostics/calibration_mixed_kaggle_thar_muril__examples.csv`.
