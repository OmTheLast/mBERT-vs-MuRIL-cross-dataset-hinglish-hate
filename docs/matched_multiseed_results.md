# Matched Multi-Seed Transformer Results

Date: 2026-08-15

Purpose: test whether the main matched-dataset mBERT vs MuRIL findings are stable when only the random seed changes.

Scope: matched conditions only: Kaggle, CM, and THAR trained/evaluated under their controlled matched split policies.

Seeds: `42`, `7`, and `13` when all runs are present.

Primary metric: Macro F1. Positive-class recall and positive-class F1 are kept because false negatives matter in hate/offensive speech detection.

## Mean And Standard Deviation

| train_dataset        | model   | seeds   |   n_seeds | accuracy_mean   | accuracy_std   | recall_hate_mean   | recall_hate_std   | f1_hate_mean   | f1_hate_std   | f1_macro_mean   | f1_macro_std   |
|:---------------------|:--------|:--------|----------:|:----------------|:---------------|:-------------------|:------------------|:---------------|:--------------|:----------------|:---------------|
| kaggle_hinglish_hate | mbert   | 7,13,42 |         3 | 71.6%           | 2.4%           | 46.9%              | 8.5%              | 56.1%          | 4.1%          | 67.5%           | 2.1%           |
| kaggle_hinglish_hate | muril   | 7,13,42 |         3 | 68.1%           | 3.1%           | 25.1%              | 8.5%              | 37.6%          | 9.9%          | 58.1%           | 5.7%           |

## Per-Seed Results

| train_dataset        | model   |   seed | accuracy   | recall_hate   | f1_hate   | f1_macro   | split_policy            |
|:---------------------|:--------|-------:|:-----------|:--------------|:----------|:-----------|:------------------------|
| kaggle_hinglish_hate | mbert   |      7 | 69.5%      | 56.0%         | 58.9%     | 67.3%      | stratified_80_20_seed7  |
| kaggle_hinglish_hate | mbert   |     13 | 74.2%      | 45.6%         | 57.9%     | 69.6%      | stratified_80_20_seed13 |
| kaggle_hinglish_hate | mbert   |     42 | 71.1%      | 39.1%         | 51.4%     | 65.4%      |                         |
| kaggle_hinglish_hate | muril   |      7 | 71.7%      | 34.9%         | 49.0%     | 64.7%      | stratified_80_20_seed7  |
| kaggle_hinglish_hate | muril   |     13 | 66.2%      | 19.3%         | 30.8%     | 54.2%      | stratified_80_20_seed13 |
| kaggle_hinglish_hate | muril   |     42 | 66.5%      | 21.2%         | 33.1%     | 55.4%      |                         |

## Interpretation Notes

- Multi-seed results are a stability check, not a new model architecture or new dataset.
- If a model wins by less than the seed-to-seed standard deviation, the safer claim is that the models are close under that condition.
- If one model has better Macro F1 but lower positive recall, the moderation interpretation should mention missed positive examples.
- These matched results should be discussed separately from cross-dataset and mixed-training results because they answer a different question.
