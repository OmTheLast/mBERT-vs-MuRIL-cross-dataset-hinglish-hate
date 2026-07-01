# Result Analysis Report

Date: 2026-06-25

This report analyzes saved model outputs after separating primary datasets from the 79-row diagnostic probe. The primary analysis uses only registered source-backed datasets: `kaggle_hinglish_hate`, `cm_splits_codemixed`, and `thar_religion`.

## Primary Matched Transformer Results

| model   | train_dataset        | test_dataset         | accuracy   | recall_positive   | f1_positive   | f1_macro   |   tn |   fp |   fn |   tp |
|:--------|:---------------------|:---------------------|:-----------|:------------------|:--------------|:-----------|-----:|-----:|-----:|-----:|
| mbert   | cm_splits_codemixed  | cm_splits_codemixed  | 80.5%      | 68.7%             | 71.4%         | 78.3%      |  233 |   35 |   46 |  101 |
| muril   | cm_splits_codemixed  | cm_splits_codemixed  | 78.8%      | 55.1%             | 64.8%         | 74.8%      |  246 |   22 |   66 |   81 |
| mbert   | kaggle_hinglish_hate | kaggle_hinglish_hate | 71.4%      | 38.6%             | 51.3%         | 65.6%      |  539 |   44 |  229 |  144 |
| muril   | kaggle_hinglish_hate | kaggle_hinglish_hate | 67.5%      | 22.3%             | 34.8%         | 56.6%      |  562 |   21 |  290 |   83 |
| mbert   | thar_religion        | thar_religion        | 74.8%      | 77.7%             | 74.5%         | 74.8%      |  880 |  339 |  243 |  848 |
| muril   | thar_religion        | thar_religion        | 77.9%      | 80.3%             | 77.4%         | 77.9%      |  923 |  296 |  215 |  876 |

Interpretation: mBERT is stronger on matched Kaggle Hinglish hate and matched CM offensive/code-mixed evaluation, while MuRIL is stronger on matched THAR targeted religious hate.

## mBERT Versus MuRIL By Train/Test Situation

| train_dataset        | test_dataset         | winner_by_macro_f1   | macro_f1_gap   | winner_by_positive_f1   | positive_f1_gap   | winner_by_positive_recall   | positive_recall_gap   |
|:---------------------|:---------------------|:---------------------|:---------------|:------------------------|:------------------|:----------------------------|:----------------------|
| cm_splits_codemixed  | cm_splits_codemixed  | mbert                | 3.5%           | mbert                   | 6.6%              | mbert                       | 13.6%                 |
| cm_splits_codemixed  | kaggle_hinglish_hate | muril                | 1.7%           | muril                   | 0.9%              | mbert                       | 0.3%                  |
| cm_splits_codemixed  | thar_religion        | muril                | 1.4%           | muril                   | 7.2%              | muril                       | 14.8%                 |
| kaggle_hinglish_hate | cm_splits_codemixed  | mbert                | 1.0%           | mbert                   | 4.7%              | mbert                       | 5.4%                  |
| kaggle_hinglish_hate | kaggle_hinglish_hate | mbert                | 9.0%           | mbert                   | 16.5%             | mbert                       | 16.4%                 |
| kaggle_hinglish_hate | thar_religion        | mbert                | 3.8%           | mbert                   | 9.8%              | mbert                       | 7.6%                  |
| thar_religion        | cm_splits_codemixed  | muril                | 5.3%           | muril                   | 9.3%              | muril                       | 12.9%                 |
| thar_religion        | kaggle_hinglish_hate | muril                | 0.6%           | muril                   | 2.2%              | muril                       | 2.7%                  |
| thar_religion        | thar_religion        | muril                | 3.1%           | muril                   | 3.0%              | muril                       | 2.6%                  |

Interpretation: the winner changes by dataset situation. This is the central result: model choice cannot be separated from the training domain, target domain, script mix, and label definition.

## Best Transformer For Each Primary Test Dataset

| test_dataset         | model   | train_dataset        | accuracy   | recall_positive   | f1_positive   | f1_macro   |   tn |   fp |   fn |   tp |
|:---------------------|:--------|:---------------------|:-----------|:------------------|:--------------|:-----------|-----:|-----:|-----:|-----:|
| cm_splits_codemixed  | mbert   | cm_splits_codemixed  | 80.5%      | 68.7%             | 71.4%         | 78.3%      |  233 |   35 |   46 |  101 |
| kaggle_hinglish_hate | mbert   | kaggle_hinglish_hate | 71.4%      | 38.6%             | 51.3%         | 65.6%      |  539 |   44 |  229 |  144 |
| thar_religion        | muril   | thar_religion        | 77.9%      | 80.3%             | 77.4%         | 77.9%      |  923 |  296 |  215 |  876 |

Interpretation: each primary test dataset is best served by a model trained on the same dataset. This indicates strong in-domain specialization and weak universal transfer.

## Cross-Dataset Generalization Gaps

| model   | train_dataset        | test_dataset         | matched_f1_macro   | test_f1_macro   | generalization_gap   | recall_positive   | f1_positive   |
|:--------|:---------------------|:---------------------|:-------------------|:----------------|:---------------------|:------------------|:--------------|
| muril   | thar_religion        | kaggle_hinglish_hate | 77.9%              | 46.2%           | 31.7%                | 23.3%             | 27.7%         |
| mbert   | thar_religion        | kaggle_hinglish_hate | 74.8%              | 45.5%           | 29.3%                | 20.6%             | 25.5%         |
| mbert   | cm_splits_codemixed  | kaggle_hinglish_hate | 78.3%              | 51.6%           | 26.6%                | 50.1%             | 45.2%         |
| muril   | cm_splits_codemixed  | kaggle_hinglish_hate | 74.8%              | 53.4%           | 21.4%                | 49.9%             | 46.1%         |
| mbert   | kaggle_hinglish_hate | thar_religion        | 65.6%              | 44.8%           | 20.8%                | 15.9%             | 24.0%         |
| mbert   | cm_splits_codemixed  | thar_religion        | 78.3%              | 58.3%           | 20.0%                | 44.6%             | 51.0%         |
| muril   | kaggle_hinglish_hate | thar_religion        | 56.6%              | 41.0%           | 15.6%                | 8.2%              | 14.2%         |
| muril   | cm_splits_codemixed  | thar_religion        | 74.8%              | 59.7%           | 15.1%                | 59.5%             | 58.3%         |
| mbert   | thar_religion        | cm_splits_codemixed  | 74.8%              | 59.8%           | 15.0%                | 40.1%             | 45.0%         |
| mbert   | kaggle_hinglish_hate | cm_splits_codemixed  | 65.6%              | 51.4%           | 14.2%                | 19.7%             | 27.5%         |
| muril   | thar_religion        | cm_splits_codemixed  | 77.9%              | 65.1%           | 12.8%                | 53.1%             | 54.4%         |
| muril   | kaggle_hinglish_hate | cm_splits_codemixed  | 56.6%              | 50.4%           | 6.1%                 | 14.3%             | 22.8%         |

Interpretation: the largest drops occur when a model trained on one positive-label definition is evaluated against another. Kaggle-trained models are especially conservative on THAR, while THAR-trained models do not become general Hinglish hate detectors.

## Best Transformer Versus Best TF-IDF Baseline

| train_dataset        | test_dataset         | best_transformer   | transformer_f1_macro   | best_baseline             | baseline_f1_macro   | transformer_minus_baseline   |   transformer_recall_positive |   baseline_recall_positive |
|:---------------------|:---------------------|:-------------------|:-----------------------|:--------------------------|:--------------------|:-----------------------------|------------------------------:|---------------------------:|
| cm_splits_codemixed  | cm_splits_codemixed  | mbert              | 78.3%                  | tfidf_logistic_regression | 77.6%               | 0.7%                         |                         0.687 |                      0.755 |
| cm_splits_codemixed  | kaggle_hinglish_hate | muril              | 53.4%                  | tfidf_linear_svm          | 48.6%               | 4.8%                         |                         0.499 |                      0.442 |
| cm_splits_codemixed  | thar_religion        | muril              | 59.7%                  | tfidf_linear_svm          | 53.8%               | 5.9%                         |                         0.595 |                      0.567 |
| kaggle_hinglish_hate | cm_splits_codemixed  | mbert              | 51.4%                  | tfidf_linear_svm          | 39.3%               | 12.0%                        |                         0.197 |                      0.633 |
| kaggle_hinglish_hate | kaggle_hinglish_hate | mbert              | 65.6%                  | tfidf_logistic_regression | 61.4%               | 4.1%                         |                         0.386 |                      0.552 |
| kaggle_hinglish_hate | thar_religion        | mbert              | 44.8%                  | tfidf_logistic_regression | 49.9%               | -5.2%                        |                         0.159 |                      0.619 |
| thar_religion        | cm_splits_codemixed  | muril              | 65.1%                  | tfidf_logistic_regression | 60.9%               | 4.2%                         |                         0.531 |                      0.347 |
| thar_religion        | kaggle_hinglish_hate | muril              | 46.2%                  | tfidf_logistic_regression | 51.0%               | -4.9%                        |                         0.233 |                      0.268 |
| thar_religion        | thar_religion        | muril              | 77.9%                  | tfidf_logistic_regression | 70.6%               | 7.3%                         |                         0.803 |                      0.702 |

Interpretation: transformers do not uniformly dominate TF-IDF. TF-IDF is competitive where lexical cues are strong or where cross-dataset transfer rewards broad keyword overlap. Transformers are strongest on matched dataset conditions.

## 79-Row Diagnostic Probe

The 79-row file is excluded from primary conclusions because it may be manually written or AI-generated, has no confirmed source provenance, contains duplicated rows, and has no text overlap with the registered datasets. It remains useful only as a diagnostic probe.

| model_family   | model                     | train_dataset        | accuracy   | recall_positive   | f1_positive   | f1_macro   |   tn |   fp |   fn |   tp |
|:---------------|:--------------------------|:---------------------|:-----------|:------------------|:--------------|:-----------|-----:|-----:|-----:|-----:|
| tfidf_baseline | tfidf_linear_svm          | cm_splits_codemixed  | 58.2%      | 43.6%             | 50.7%         | 57.2%      |   29 |   11 |   22 |   17 |
| tfidf_baseline | tfidf_logistic_regression | cm_splits_codemixed  | 65.8%      | 74.4%             | 68.2%         | 65.6%      |   23 |   17 |   10 |   29 |
| tfidf_baseline | tfidf_linear_svm          | kaggle_hinglish_hate | 41.8%      | 51.3%             | 46.5%         | 41.3%      |   13 |   27 |   19 |   20 |
| tfidf_baseline | tfidf_logistic_regression | kaggle_hinglish_hate | 54.4%      | 46.2%             | 50.0%         | 54.1%      |   25 |   15 |   21 |   18 |
| tfidf_baseline | tfidf_linear_svm          | thar_religion        | 39.2%      | 5.1%              | 7.7%          | 31.2%      |   29 |   11 |   37 |    2 |
| tfidf_baseline | tfidf_logistic_regression | thar_religion        | 50.6%      | 5.1%              | 9.3%          | 37.7%      |   38 |    2 |   37 |    2 |
| transformer    | mbert                     | cm_splits_codemixed  | 46.8%      | 2.6%              | 4.5%          | 33.9%      |   36 |    4 |   38 |    1 |
| transformer    | muril                     | cm_splits_codemixed  | 50.6%      | 2.6%              | 4.9%          | 35.8%      |   39 |    1 |   38 |    1 |
| transformer    | mbert                     | kaggle_hinglish_hate | 51.9%      | 7.7%              | 13.6%         | 40.2%      |   38 |    2 |   36 |    3 |
| transformer    | muril                     | kaggle_hinglish_hate | 64.6%      | 35.9%             | 50.0%         | 61.3%      |   37 |    3 |   25 |   14 |
| transformer    | mbert                     | thar_religion        | 51.9%      | 5.1%              | 9.5%          | 38.4%      |   39 |    1 |   37 |    2 |
| transformer    | muril                     | thar_religion        | 53.2%      | 5.1%              | 9.8%          | 39.1%      |   40 |    0 |   37 |    2 |

Interpretation: results on this probe should not be used to claim model superiority. Its main value is methodological: it exposed how unstable conclusions become when evaluation provenance is unclear.

## First Mixed-Dataset Result: Kaggle + CM

Date: 2026-07-01

The first mixed training condition combines `kaggle_hinglish_hate` and `cm_splits_codemixed`. The exact training condition is labeled `mixed_kaggle_plus_cm` in the result files.

Primary source:

- `results/mixed_kaggle_plus_cm_transformer_summary.csv`

| model | train_dataset | test_dataset | accuracy | recall_positive | f1_positive | f1_macro | tn | fp | fn | tp |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| mBERT | `mixed_kaggle_plus_cm` | `kaggle_hinglish_hate` | 72.9% | 45.3% | 56.6% | 68.5% | 528 | 55 | 204 | 169 |
| mBERT | `mixed_kaggle_plus_cm` | `cm_splits_codemixed` | 74.5% | 59.9% | 62.4% | 71.5% | 221 | 47 | 59 | 88 |
| mBERT | `mixed_kaggle_plus_cm` | `thar_religion` | 54.9% | 22.9% | 32.4% | 49.3% | 1018 | 201 | 841 | 250 |
| MuRIL | `mixed_kaggle_plus_cm` | `kaggle_hinglish_hate` | 61.0% | 0.0% | 0.0% | 37.9% | 583 | 0 | 373 | 0 |
| MuRIL | `mixed_kaggle_plus_cm` | `cm_splits_codemixed` | 64.6% | 0.0% | 0.0% | 39.2% | 268 | 0 | 147 | 0 |
| MuRIL | `mixed_kaggle_plus_cm` | `thar_religion` | 52.8% | 0.0% | 0.0% | 34.5% | 1219 | 0 | 1091 | 0 |

Interpretation:

- mBERT gained on Kaggle compared with Kaggle-only training, suggesting that additional similar code-mixed/offensive data can help recall more Kaggle positives.
- mBERT lost on CM compared with CM-only training, suggesting that mixing label definitions can dilute dataset-specific performance.
- mBERT remained weak on THAR, so Kaggle+CM mixing does not solve targeted religious-hate transfer.
- MuRIL collapsed to all-negative predictions under this exact condition. This is a major warning result and should be followed up with additional seeds, threshold/logit inspection, or class weighting before making strong claims.

Paper implication:

- Mixed training is not automatically robust training. Dataset compatibility matters, and the base model can respond differently to the same mixed data.

## Figures

- `results/result_analysis/transformer_primary_macro_f1_matrix.png`
- `results/result_analysis/transformer_primary_macro_f1_matrix.svg`
- `results/result_analysis/transformer_generalization_gaps.png`
- `results/result_analysis/transformer_generalization_gaps.svg`
- `results/result_analysis/transformer_vs_tfidf_delta.png`
- `results/result_analysis/transformer_vs_tfidf_delta.svg`

## Paper-Level Takeaways

- The cleanest paper claim is conditional, not absolute: mBERT wins some dataset situations and MuRIL wins others.
- mBERT is stronger on matched Latin-script Kaggle Hinglish hate and CM offensive/code-mixed data.
- MuRIL is stronger on matched THAR targeted religious hate and also improves THAR-to-CM transfer.
- In-domain training is consistently stronger than cross-dataset transfer, showing that dataset definitions are not interchangeable.
- TF-IDF baselines remain important because lexical cues are strong; any transformer claim should be compared against them.
- The 79-row diagnostic probe should be excluded from primary tables and figures in the final paper.
- The first Kaggle+CM mixed run shows that mixing related datasets can improve one target condition while hurting another, and can even trigger model collapse for one base model.
