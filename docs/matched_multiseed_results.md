# Matched Multi-Seed Transformer Results

Date: 2026-08-18

Purpose: test whether the main matched-dataset mBERT vs MuRIL findings are stable when only the random seed changes.

Scope: matched conditions included in this aggregation: `cm_splits_codemixed`, `kaggle_hinglish_hate`. Each condition is trained/evaluated under its controlled matched split policy.

Seeds included: `7`, `13`, `42`.

Primary metric: Macro F1. Positive-class recall and positive-class F1 are kept because false negatives matter in hate/offensive speech detection.

## Mean And Standard Deviation

| train_dataset        | model   | seeds   |   n_seeds | accuracy_mean   | accuracy_std   | recall_hate_mean   | recall_hate_std   | f1_hate_mean   | f1_hate_std   | f1_macro_mean   | f1_macro_std   |
|:---------------------|:--------|:--------|----------:|:----------------|:---------------|:-------------------|:------------------|:---------------|:--------------|:----------------|:---------------|
| cm_splits_codemixed  | mbert   | 7,13,42 |         3 | 79.6%           | 2.0%           | 70.7%              | 1.3%              | 71.1%          | 2.0%          | 77.7%           | 1.9%           |
| cm_splits_codemixed  | muril   | 7,13,42 |         3 | 78.8%           | 1.9%           | 64.4%              | 8.3%              | 68.1%          | 3.8%          | 76.1%           | 2.3%           |
| kaggle_hinglish_hate | mbert   | 7,13,42 |         3 | 71.6%           | 2.4%           | 46.9%              | 8.5%              | 56.1%          | 4.1%          | 67.5%           | 2.1%           |
| kaggle_hinglish_hate | muril   | 7,13,42 |         3 | 68.1%           | 3.1%           | 25.1%              | 8.5%              | 37.6%          | 9.9%          | 58.1%           | 5.7%           |

## Per-Seed Results

| train_dataset        | model   |   seed | accuracy   | recall_hate   | f1_hate   | f1_macro   | split_policy                    |
|:---------------------|:--------|-------:|:-----------|:--------------|:----------|:-----------|:--------------------------------|
| cm_splits_codemixed  | mbert   |      7 | 77.4%      | 70.7%         | 68.8%     | 75.5%      | split:train=train+val,eval=test |
| cm_splits_codemixed  | mbert   |     13 | 80.7%      | 72.0%         | 72.5%     | 78.8%      | split:train=train+val,eval=test |
| cm_splits_codemixed  | mbert   |     42 | 80.9%      | 69.3%         | 72.0%     | 78.7%      | split:train=train+val,eval=test |
| cm_splits_codemixed  | muril   |      7 | 80.4%      | 72.7%         | 72.4%     | 78.6%      | split:train=train+val,eval=test |
| cm_splits_codemixed  | muril   |     13 | 76.7%      | 64.7%         | 66.2%     | 74.2%      | split:train=train+val,eval=test |
| cm_splits_codemixed  | muril   |     42 | 79.2%      | 56.0%         | 65.6%     | 75.4%      | split:train=train+val,eval=test |
| kaggle_hinglish_hate | mbert   |      7 | 69.5%      | 56.0%         | 58.9%     | 67.3%      | stratified_80_20_seed7          |
| kaggle_hinglish_hate | mbert   |     13 | 74.2%      | 45.6%         | 57.9%     | 69.6%      | stratified_80_20_seed13         |
| kaggle_hinglish_hate | mbert   |     42 | 71.1%      | 39.1%         | 51.4%     | 65.4%      |                                 |
| kaggle_hinglish_hate | muril   |      7 | 71.7%      | 34.9%         | 49.0%     | 64.7%      | stratified_80_20_seed7          |
| kaggle_hinglish_hate | muril   |     13 | 66.2%      | 19.3%         | 30.8%     | 54.2%      | stratified_80_20_seed13         |
| kaggle_hinglish_hate | muril   |     42 | 66.5%      | 21.2%         | 33.1%     | 55.4%      |                                 |

## Interpretation Notes

- Multi-seed results are a stability check, not a new model architecture or new dataset.
- If a model wins by less than the seed-to-seed standard deviation, the safer claim is that the models are close under that condition.
- If one model has better Macro F1 but lower positive recall, the moderation interpretation should mention missed positive examples.
- These matched results should be discussed separately from cross-dataset and mixed-training results because they answer a different question.
