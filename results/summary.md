# Results Summary

Generated from saved experiment outputs. These tables are intended for quick reference and later paper drafting.

## Kaggle Hinglish Hate Dataset Context

- `kaggle_hinglish_hate.csv`: 4,780 rows after de-duplication.
- Label distribution: 2,914 non-hate and 1,866 hate.
- Source attribution: Shardul Dhekane, `Code-Mixed Hinglish Hate Speech Detection Dataset`, Kaggle.

## Transformer Validation Results

| model   | train_dataset        | accuracy   | precision_hate   | recall_hate   | f1_hate   | f1_macro   |
|:--------|:---------------------|:-----------|:-----------------|:--------------|:----------|:-----------|
| mbert   | kaggle_hinglish_hate | 71.1%      | 74.9%            | 39.1%         | 51.4%     | 65.4%      |
| muril   | kaggle_hinglish_hate | 66.5%      | 75.2%            | 21.2%         | 33.1%     | 55.4%      |
| mbert   | cm_splits_codemixed  | 80.9%      | 74.8%            | 69.3%         | 72.0%     | 78.7%      |
| muril   | cm_splits_codemixed  | 79.2%      | 79.2%            | 56.0%         | 65.6%     | 75.4%      |
| mbert   | thar_religion        | 74.8%      | 71.4%            | 77.7%         | 74.5%     | 74.8%      |
| muril   | thar_religion        | 77.9%      | 74.7%            | 80.3%         | 77.4%     | 77.9%      |

## Existing Saved Checkpoints At Session Start On 79-Row Benchmark

These results come from the checkpoints that already existed in the project before the code cleanup and retraining work. They are useful because they show the model behavior that motivated the current investigation.

| model   | accuracy   | precision_hate   | recall_hate   | f1_hate   | f1_macro   |   tn |   fp |   fn |   tp |
|:--------|:-----------|:-----------------|:--------------|:----------|:-----------|-----:|-----:|-----:|-----:|
| mbert   | 51.9%      | 100.0%           | 2.6%          | 5.0%      | 36.4%      |   40 |    0 |   38 |    1 |
| muril   | 50.6%      | 0.0%             | 0.0%          | 0.0%      | 33.6%      |   40 |    0 |   39 |    0 |

## Retrained Hinglish Checkpoints On 79-Row Benchmark

| model   | accuracy   | precision_hate   | recall_hate   | f1_hate   | f1_macro   |   tn |   fp |   fn |   tp |
|:--------|:-----------|:-----------------|:--------------|:----------|:-----------|-----:|-----:|-----:|-----:|
| mbert   | 51.9%      | 60.0%            | 7.7%          | 13.6%     | 40.2%      |   38 |    2 |   36 |    3 |
| muril   | 64.6%      | 82.4%            | 35.9%         | 50.0%     | 61.3%      |   37 |    3 |   25 |   14 |

## Earlier TF-IDF Baseline Results

| model                     | evaluation                      | accuracy   | precision_hate   | recall_hate   | f1_hate   | f1_macro   |   tn |   fp |   fn |   tp |
|:--------------------------|:--------------------------------|:-----------|:-----------------|:--------------|:----------|:-----------|-----:|-----:|-----:|-----:|
| tfidf_logistic_regression | kaggle_hinglish_hate_validation | 63.0%      | 52.4%            | 55.2%         | 53.8%     | 61.4%      |  396 |  187 |  167 |  206 |
| tfidf_logistic_regression | existing_79_row_benchmark       | 54.4%      | 54.5%            | 46.2%         | 50.0%     | 54.1%      |   25 |   15 |   21 |   18 |
| tfidf_linear_svm          | kaggle_hinglish_hate_validation | 62.9%      | 52.4%            | 52.3%         | 52.3%     | 61.0%      |  406 |  177 |  178 |  195 |
| tfidf_linear_svm          | existing_79_row_benchmark       | 41.8%      | 42.6%            | 51.3%         | 46.5%     | 41.3%      |   13 |   27 |   19 |   20 |

## Cross-Dataset TF-IDF Baseline Results

These results train each baseline on one usable dataset and evaluate it across all usable test sets plus the 79-row sanity benchmark. The positive label means different things across datasets, so interpret these as dataset-situation results, not direct universal hate-speech scores.

| model                     | train_dataset        | test_dataset              |   test_rows | accuracy   | recall_positive   | f1_positive   | f1_macro   |   tn |   fp |   fn |   tp |
|:--------------------------|:---------------------|:--------------------------|------------:|:-----------|:------------------|:--------------|:-----------|-----:|-----:|-----:|-----:|
| tfidf_logistic_regression | kaggle_hinglish_hate | kaggle_hinglish_hate      |         956 | 63.0%      | 55.2%             | 53.8%         | 61.4%      |  396 |  187 |  167 |  206 |
| tfidf_logistic_regression | kaggle_hinglish_hate | cm_splits_codemixed       |         415 | 36.6%      | 70.1%             | 43.9%         | 35.5%      |   49 |  219 |   44 |  103 |
| tfidf_logistic_regression | kaggle_hinglish_hate | thar_religion             |        2310 | 50.3%      | 61.9%             | 54.0%         | 49.9%      |  486 |  733 |  416 |  675 |
| tfidf_logistic_regression | kaggle_hinglish_hate | existing_79_row_benchmark |          79 | 54.4%      | 46.2%             | 50.0%         | 54.1%      |   25 |   15 |   21 |   18 |
| tfidf_linear_svm          | kaggle_hinglish_hate | kaggle_hinglish_hate      |         956 | 62.9%      | 52.3%             | 52.3%         | 61.0%      |  406 |  177 |  178 |  195 |
| tfidf_linear_svm          | kaggle_hinglish_hate | cm_splits_codemixed       |         415 | 39.5%      | 63.3%             | 42.6%         | 39.3%      |   71 |  197 |   54 |   93 |
| tfidf_linear_svm          | kaggle_hinglish_hate | thar_religion             |        2310 | 49.4%      | 63.1%             | 54.1%         | 48.9%      |  453 |  766 |  403 |  688 |
| tfidf_linear_svm          | kaggle_hinglish_hate | existing_79_row_benchmark |          79 | 41.8%      | 51.3%             | 46.5%         | 41.3%      |   13 |   27 |   19 |   20 |
| tfidf_logistic_regression | cm_splits_codemixed  | kaggle_hinglish_hate      |         956 | 42.9%      | 65.7%             | 47.3%         | 42.5%      |  165 |  418 |  128 |  245 |
| tfidf_logistic_regression | cm_splits_codemixed  | cm_splits_codemixed       |         415 | 79.0%      | 75.5%             | 71.8%         | 77.6%      |  217 |   51 |   36 |  111 |
| tfidf_logistic_regression | cm_splits_codemixed  | thar_religion             |        2310 | 53.5%      | 73.1%             | 59.7%         | 52.3%      |  438 |  781 |  294 |  797 |
| tfidf_logistic_regression | cm_splits_codemixed  | existing_79_row_benchmark |          79 | 65.8%      | 74.4%             | 68.2%         | 65.6%      |   23 |   17 |   10 |   29 |
| tfidf_linear_svm          | cm_splits_codemixed  | kaggle_hinglish_hate      |         956 | 49.8%      | 44.2%             | 40.7%         | 48.6%      |  311 |  272 |  208 |  165 |
| tfidf_linear_svm          | cm_splits_codemixed  | cm_splits_codemixed       |         415 | 77.3%      | 71.4%             | 69.1%         | 75.6%      |  216 |   52 |   42 |  105 |
| tfidf_linear_svm          | cm_splits_codemixed  | thar_religion             |        2310 | 53.8%      | 56.7%             | 53.7%         | 53.8%      |  624 |  595 |  472 |  619 |
| tfidf_linear_svm          | cm_splits_codemixed  | existing_79_row_benchmark |          79 | 58.2%      | 43.6%             | 50.7%         | 57.2%      |   29 |   11 |   22 |   17 |
| tfidf_logistic_regression | thar_religion        | kaggle_hinglish_hate      |         956 | 57.6%      | 26.8%             | 33.1%         | 51.0%      |  451 |  132 |  273 |  100 |
| tfidf_logistic_regression | thar_religion        | cm_splits_codemixed       |         415 | 68.4%      | 34.7%             | 43.8%         | 60.9%      |  233 |   35 |   96 |   51 |
| tfidf_logistic_regression | thar_religion        | thar_religion             |        2310 | 70.6%      | 70.2%             | 69.3%         | 70.6%      |  865 |  354 |  325 |  766 |
| tfidf_logistic_regression | thar_religion        | existing_79_row_benchmark |          79 | 50.6%      | 5.1%              | 9.3%          | 37.7%      |   38 |    2 |   37 |    2 |
| tfidf_linear_svm          | thar_religion        | kaggle_hinglish_hate      |         956 | 56.5%      | 29.0%             | 34.2%         | 50.8%      |  432 |  151 |  265 |  108 |
| tfidf_linear_svm          | thar_religion        | cm_splits_codemixed       |         415 | 67.0%      | 34.0%             | 42.2%         | 59.5%      |  228 |   40 |   97 |   50 |
| tfidf_linear_svm          | thar_religion        | thar_religion             |        2310 | 68.5%      | 66.4%             | 66.6%         | 68.4%      |  859 |  360 |  367 |  724 |
| tfidf_linear_svm          | thar_religion        | existing_79_row_benchmark |          79 | 39.2%      | 5.1%              | 7.7%          | 31.2%      |   29 |   11 |   37 |    2 |

## Transformer Cross-Dataset Evaluation

These results evaluate local transformer checkpoints across the same dataset test conditions used by the cross-dataset baselines. Rows are labeled by the training dataset used to create each checkpoint.

| model   | train_dataset        | test_dataset              |   test_rows | accuracy   | recall_positive   | f1_positive   | f1_macro   |   tn |   fp |   fn |   tp |
|:--------|:---------------------|:--------------------------|------------:|:-----------|:------------------|:--------------|:-----------|-----:|-----:|-----:|-----:|
| mbert   | kaggle_hinglish_hate | kaggle_hinglish_hate      |         956 | 71.4%      | 38.6%             | 51.3%         | 65.6%      |  539 |   44 |  229 |  144 |
| mbert   | kaggle_hinglish_hate | cm_splits_codemixed       |         415 | 63.1%      | 19.7%             | 27.5%         | 51.4%      |  233 |   35 |  118 |   29 |
| mbert   | kaggle_hinglish_hate | thar_religion             |        2310 | 52.6%      | 15.9%             | 24.0%         | 44.8%      | 1041 |  178 |  918 |  173 |
| mbert   | kaggle_hinglish_hate | existing_79_row_benchmark |          79 | 51.9%      | 7.7%              | 13.6%         | 40.2%      |   38 |    2 |   36 |    3 |
| muril   | kaggle_hinglish_hate | kaggle_hinglish_hate      |         956 | 67.5%      | 22.3%             | 34.8%         | 56.6%      |  562 |   21 |  290 |   83 |
| muril   | kaggle_hinglish_hate | cm_splits_codemixed       |         415 | 65.8%      | 14.3%             | 22.8%         | 50.4%      |  252 |   16 |  126 |   21 |
| muril   | kaggle_hinglish_hate | thar_religion             |        2310 | 53.1%      | 8.2%              | 14.2%         | 41.0%      | 1136 |   83 | 1001 |   90 |
| muril   | kaggle_hinglish_hate | existing_79_row_benchmark |          79 | 64.6%      | 35.9%             | 50.0%         | 61.3%      |   37 |    3 |   25 |   14 |
| mbert   | cm_splits_codemixed  | kaggle_hinglish_hate      |         956 | 52.5%      | 50.1%             | 45.2%         | 51.6%      |  315 |  268 |  186 |  187 |
| mbert   | cm_splits_codemixed  | cm_splits_codemixed       |         415 | 80.5%      | 68.7%             | 71.4%         | 78.3%      |  233 |   35 |   46 |  101 |
| mbert   | cm_splits_codemixed  | thar_religion             |        2310 | 59.6%      | 44.6%             | 51.0%         | 58.3%      |  889 |  330 |  604 |  487 |
| mbert   | cm_splits_codemixed  | existing_79_row_benchmark |          79 | 46.8%      | 2.6%              | 4.5%          | 33.9%      |   36 |    4 |   38 |    1 |
| muril   | cm_splits_codemixed  | kaggle_hinglish_hate      |         956 | 54.5%      | 49.9%             | 46.1%         | 53.4%      |  335 |  248 |  187 |  186 |
| muril   | cm_splits_codemixed  | cm_splits_codemixed       |         415 | 78.8%      | 55.1%             | 64.8%         | 74.8%      |  246 |   22 |   66 |   81 |
| muril   | cm_splits_codemixed  | thar_religion             |        2310 | 59.7%      | 59.5%             | 58.3%         | 59.7%      |  731 |  488 |  442 |  649 |
| muril   | cm_splits_codemixed  | existing_79_row_benchmark |          79 | 50.6%      | 2.6%              | 4.9%          | 35.8%      |   39 |    1 |   38 |    1 |
| mbert   | thar_religion        | kaggle_hinglish_hate      |         956 | 52.9%      | 20.6%             | 25.5%         | 45.5%      |  429 |  154 |  296 |   77 |
| mbert   | thar_religion        | cm_splits_codemixed       |         415 | 65.3%      | 40.1%             | 45.0%         | 59.8%      |  212 |   56 |   88 |   59 |
| mbert   | thar_religion        | thar_religion             |        2310 | 74.8%      | 77.7%             | 74.5%         | 74.8%      |  880 |  339 |  243 |  848 |
| mbert   | thar_religion        | existing_79_row_benchmark |          79 | 51.9%      | 5.1%              | 9.5%          | 38.4%      |   39 |    1 |   37 |    2 |
| muril   | thar_religion        | kaggle_hinglish_hate      |         956 | 52.5%      | 23.3%             | 27.7%         | 46.2%      |  415 |  168 |  286 |   87 |
| muril   | thar_religion        | cm_splits_codemixed       |         415 | 68.4%      | 53.1%             | 54.4%         | 65.1%      |  206 |   62 |   69 |   78 |
| muril   | thar_religion        | thar_religion             |        2310 | 77.9%      | 80.3%             | 77.4%         | 77.9%      |  923 |  296 |  215 |  876 |
| muril   | thar_religion        | existing_79_row_benchmark |          79 | 53.2%      | 5.1%              | 9.8%          | 39.1%      |   40 |    0 |   37 |    2 |

## Initial Interpretation

- The existing saved checkpoints at the start of this session were strongly biased toward predicting non-hate.
- Retraining on `kaggle_hinglish_hate` restored hate detection, but hate recall remains a weakness.
- mBERT is stronger than MuRIL on both matched `kaggle_hinglish_hate` and matched `cm_splits_codemixed` transformer test conditions.
- MuRIL is stronger than mBERT on matched `thar_religion` transformer evaluation.
- MuRIL remains stronger on the tiny 79-row benchmark when trained on `kaggle_hinglish_hate`, but CM-trained and THAR-trained transformers perform poorly there.
- CM-trained transformers transfer better to `thar_religion` than Kaggle-Hinglish-Hate-trained transformers, especially MuRIL on positive-class recall/F1.
- THAR-trained MuRIL transfers better to `cm_splits_codemixed` than THAR-trained mBERT, but both THAR-trained models transfer weakly to `kaggle_hinglish_hate`.
- The 79-row benchmark is useful for sanity checks but too small and label-noisy for final conclusions.
- The 79-row benchmark issue is paper-relevant: many positive labels are generic negative phrases rather than strict targeted hate, while both models still miss several targeted/religious examples.
