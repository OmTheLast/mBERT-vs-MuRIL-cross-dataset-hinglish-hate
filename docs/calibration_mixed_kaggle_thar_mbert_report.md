# Mixed Kaggle+THAR mBERT Calibration Diagnostic

Date: 2026-07-02

Checkpoint: `Models/mbert__train-mixed_kaggle_plus_thar__seed42__e2`
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
| internal_validation  |   2613 |            1171 |                         1199 |              0.0566 |              0.1928 |                 0.4197 |              0.7653 |              0.9089 |              0.9684 |                    0.3253 |                    0.6431 |             0.7352 |                    0.7190 |                0.7105 |                       0.5800 |          0.7371 |                 0.6798 |             0.7022 | stratified_80_20_split_seed42 | /Users/ompatnaik/Documents/Code/Hinglish Research/results/collapse_diagnostics/calibration_mixed_kaggle_thar_mbert__internal_validation__probabilities.csv  |
| kaggle_hinglish_hate |    956 |             373 |                          270 |              0.0595 |              0.2214 |                 0.3074 |              0.5345 |              0.9362 |              0.9683 |                    0.3118 |                    0.5536 |             0.6825 |                    0.4987 |                0.5785 |                       0.4600 |          0.6936 |                 0.5550 |             0.6061 | stratified_80_20_split_seed42 | /Users/ompatnaik/Documents/Code/Hinglish Research/results/collapse_diagnostics/calibration_mixed_kaggle_thar_mbert__kaggle_hinglish_hate__probabilities.csv |
| cm_splits_codemixed  |    415 |             147 |                          119 |              0.0641 |              0.2675 |                 0.3731 |              0.5367 |              0.7181 |              0.9614 |                    0.3857 |                    0.4323 |             0.5408 |                    0.3401 |                0.3759 |                       0.4700 |          0.5504 |                 0.3946 |             0.4085 | provided_test_split           | /Users/ompatnaik/Documents/Code/Hinglish Research/results/collapse_diagnostics/calibration_mixed_kaggle_thar_mbert__cm_splits_codemixed__probabilities.csv  |
| thar_religion        |   2310 |            1091 |                         1200 |              0.0575 |              0.1590 |                 0.5519 |              0.7902 |              0.8972 |              0.9369 |                    0.3242 |                    0.6663 |             0.7493 |                    0.7846 |                0.7473 |                       0.4900 |          0.7511 |                 0.7919 |             0.7503 | stratified_80_20_split_seed42 | /Users/ompatnaik/Documents/Code/Hinglish Research/results/collapse_diagnostics/calibration_mixed_kaggle_thar_mbert__thar_religion__probabilities.csv        |

## Local Example File

Highest-positive-probability examples and strongest false negatives are saved at `/Users/ompatnaik/Documents/Code/Hinglish Research/results/collapse_diagnostics/calibration_mixed_kaggle_thar_mbert__examples.csv`.
