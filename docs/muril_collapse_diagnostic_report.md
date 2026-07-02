# MuRIL Collapse Diagnostic Report

Date: 2026-07-02

Checkpoint: `Models/muril__train-mixed_kaggle_plus_cm__seed42__e2`
Training CSV for internal validation reconstruction: `data/processed/mixed_train_kaggle_plus_cm__seed42.csv`

## What This Checks

This diagnostic checks whether the all-negative result is caused by the default 0.50 threshold, or whether the model assigns low positive probability to nearly every example.

Important columns:

- `predicted_positive_at_0_50`: how many examples the normal classifier marks positive.
- `prob_positive_p95` and `prob_positive_max`: whether positive probabilities ever approach the decision threshold.
- `best_threshold_by_macro_f1`: the threshold that would maximize Macro F1 on that evaluation set.
- `best_f1_macro`: the best possible Macro F1 after threshold tuning on that same set.

## Summary

| eval_set                  |   rows |   positive_rows |   predicted_positive_at_0_50 |   prob_positive_min |   prob_positive_p25 |   prob_positive_median |   prob_positive_p75 |   prob_positive_p95 |   prob_positive_max |   mean_prob_true_negative |   mean_prob_true_positive |   default_f1_macro |   default_recall_positive |   default_f1_positive |   best_threshold_by_macro_f1 |   best_f1_macro |   best_recall_positive |   best_f1_positive | split_policy                  | probabilities_file                                                                                                                                 |
|:--------------------------|-------:|----------------:|-----------------------------:|--------------------:|--------------------:|-----------------------:|--------------------:|--------------------:|--------------------:|--------------------------:|--------------------------:|-------------------:|--------------------------:|----------------------:|-----------------------------:|----------------:|-----------------------:|-------------------:|:------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------|
| internal_mixed_validation |   1444 |             548 |                            0 |              0.3496 |              0.3658 |                 0.3957 |              0.4338 |              0.4659 |              0.4659 |                    0.3935 |                    0.4150 |             0.3829 |                    0.0000 |                0.0000 |                       0.4200 |          0.6187 |                 0.5164 |             0.5231 | stratified_80_20_split_seed42 | /Users/ompatnaik/Documents/Code/Hinglish Research/results/collapse_diagnostics/muril_mixed_kaggle_cm__internal_mixed_validation__probabilities.csv |
| kaggle_hinglish_hate      |    956 |             373 |                            0 |              0.3520 |              0.3679 |                 0.3993 |              0.4347 |              0.4659 |              0.4659 |                    0.3956 |                    0.4180 |             0.3788 |                    0.0000 |                0.0000 |                       0.4000 |          0.6120 |                 0.6434 |             0.5674 | stratified_80_20_split_seed42 | /Users/ompatnaik/Documents/Code/Hinglish Research/results/collapse_diagnostics/muril_mixed_kaggle_cm__kaggle_hinglish_hate__probabilities.csv      |
| cm_splits_codemixed       |    415 |             147 |                            0 |              0.3502 |              0.3655 |                 0.3936 |              0.4346 |              0.4659 |              0.4659 |                    0.3939 |                    0.4118 |             0.3924 |                    0.0000 |                0.0000 |                       0.4300 |          0.5924 |                 0.4354 |             0.4588 | provided_test_split           | /Users/ompatnaik/Documents/Code/Hinglish Research/results/collapse_diagnostics/muril_mixed_kaggle_cm__cm_splits_codemixed__probabilities.csv       |
| thar_religion             |   2310 |            1091 |                            0 |              0.3500 |              0.3613 |                 0.3706 |              0.4191 |              0.4659 |              0.4659 |                    0.3846 |                    0.3948 |             0.3454 |                    0.0000 |                0.0000 |                       0.3800 |          0.5687 |                 0.4638 |             0.5088 | stratified_80_20_split_seed42 | /Users/ompatnaik/Documents/Code/Hinglish Research/results/collapse_diagnostics/muril_mixed_kaggle_cm__thar_religion__probabilities.csv             |

## Local Example File

Highest-positive-probability examples and strongest false negatives are saved at `/Users/ompatnaik/Documents/Code/Hinglish Research/results/collapse_diagnostics/muril_mixed_kaggle_cm__examples.csv`.

## Initial Interpretation

This is not a total information failure. The model is assigning slightly higher positive probabilities to true positive rows than to true negative rows, but the entire probability distribution is compressed below the default 0.50 decision threshold.

Evidence:

- At the normal 0.50 threshold, every evaluated set has `predicted_positive_at_0_50 = 0`.
- The maximum positive probability is only about 0.466 across all evaluated sets.
- True positives have higher average positive probability than true negatives, but the gap is small.
- Lowering the threshold improves Macro F1 substantially:
  - internal mixed validation: 38.3% default Macro F1 to 61.9% at threshold 0.42;
  - Kaggle: 37.9% default Macro F1 to 61.2% at threshold 0.40;
  - CM: 39.2% default Macro F1 to 59.2% at threshold 0.43;
  - THAR: 34.5% default Macro F1 to 56.9% at threshold 0.38.

The current best explanation is calibration/decision-boundary collapse rather than complete representational collapse. In plain terms: MuRIL seems to have learned a weak ordering signal, but it is not confident enough to cross the standard positive threshold.

## Follow-Up Checks

Next checks before making a paper claim:

- Run at least two more seeds for the same Kaggle+CM MuRIL condition.
- Evaluate threshold tuning on validation only, then apply that fixed threshold to the held-out datasets.
- Try class weighting or focal loss if the all-negative tendency repeats.
- Compare with a THAR-including mix to see whether MuRIL needs more Indian-context targeted-hate signal.
- Compare the same probability diagnostic for mBERT, because this tells us whether mBERT separates classes with a wider probability margin.
