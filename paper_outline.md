# Paper Outline

Working title:

**Cross-Dataset Evaluation of mBERT and MuRIL for Hate Speech Detection in Hinglish Code-Mixed Text**

## Abstract

Briefly describe:

- Hinglish/code-mixed hate speech detection problem.
- Comparison between mBERT and MuRIL.
- Dataset issue: public datasets differ in language, region, platform, and label definitions.
- Main experimental setup.
- Key result once finalized.

## 1. Introduction

Topics to cover:

- Growth of Hindi-English code-mixed social media text in India.
- Why hate speech detection is socially important.
- Why code-mixing makes NLP difficult.
- Why Indian Hinglish is different from generic multilingual text.
- Motivation for comparing mBERT and MuRIL.

Potential research question:

> Does Indian-language-specific pretraining in MuRIL improve Hinglish hate speech detection compared with mBERT, especially across datasets?

## 2. Related Work

Discuss:

- Hate speech and offensive language detection.
- Code-mixed NLP.
- Hinglish/Hindi-English hate speech datasets.
- mBERT and multilingual pretraining.
- MuRIL and Indian-language-specific pretraining.
- HASOC, THAR, HOT, Indo-HateSpeech, and other relevant datasets.

## 3. Datasets

For each dataset:

- Name.
- Source.
- Platform, such as Twitter/X, YouTube, Facebook.
- Region/context, especially Indian vs broader South Asian.
- Number of examples.
- Label schema.
- Language/script distribution.
- Preprocessing decisions.

Current local dataset notes:

- Original dataset has 29,550 rows.
- It contains English, Hindi, and Hinglish rows.
- Hinglish-only subset after de-duplication has 4,780 rows.
- This motivates careful dataset filtering.
- Current usable processed datasets are `kaggle_hinglish_hate`, `cm_splits_codemixed`, and `thar_religion`.
- HASOC and Indo-HateSpeech remain high-value candidates, but are not yet locally usable.

## 4. Methodology

Models:

- mBERT: `bert-base-multilingual-cased`.
- MuRIL: `google/muril-base-cased`.
- Baselines: TF-IDF + Logistic Regression, TF-IDF + Linear SVM.

Training setup:

- 80/20 stratified split for in-domain experiments.
- 2 epochs for initial runs.
- Batch size 8 on Mac MPS.
- Minimal cleaning as default.

Metrics:

- Macro F1.
- Hate-class F1.
- Hate-class recall.
- Accuracy as a secondary metric.
- Confusion matrix.

## 5. Experiments

Completed experiments:

- Initial saved project checkpoints on the 79-row diagnostic probe.
- Retrained mBERT/MuRIL on Hinglish-only subset.
- TF-IDF baselines on the same split.
- Cross-dataset TF-IDF baselines across `kaggle_hinglish_hate`, `cm_splits_codemixed`, and `thar_religion`.
- Cross-dataset evaluation of `kaggle_hinglish_hate`-trained mBERT and MuRIL checkpoints.
- Training and cross-dataset evaluation of `cm_splits_codemixed`-trained mBERT and MuRIL checkpoints.
- Cross-dataset evaluation for mBERT/MuRIL checkpoints trained on `thar_religion`.
- Result analysis, error analysis, and first-pass manual error coding.

Planned experiments:

- Leave-one-dataset-out evaluation.
- Mixed-dataset training.
- Hinglish-only evaluation where metadata allows filtering.

## 6. Results

Include:

- Transformer validation table.
- 79-row diagnostic probe table only if it is clearly marked as non-primary.
- TF-IDF baseline table.
- Cross-dataset baseline result matrix.
- Full mBERT/MuRIL cross-dataset matrix after training on Kaggle Hinglish hate, CM code-mixed, and THAR.

Use `docs/result_analysis_report.md` as the paper-facing source for current primary tables. Use `results/summary.md` only as a running project summary because it also preserves earlier validation/diagnostic tables. Use `docs/baseline_experiment_report.md` for the baseline experiment write-up, and `docs/transformer_cross_dataset_eval_report.md` plus `docs/thar_transformer_training_report.md` for transformer write-ups.

Candidate figures generated in `results/figures/`:

- Dataset size and label balance.
- Cross-dataset TF-IDF macro F1 heatmap.
- Transformer macro F1 heatmap.
- Transformer positive-recall heatmap.
- Best TF-IDF vs best transformer bar chart for Kaggle-Hinglish-Hate training.
- mBERT vs MuRIL positive recall bar chart for Kaggle-Hinglish-Hate training.

## 7. Error Analysis

Analyze examples where:

- mBERT is correct and MuRIL is wrong.
- MuRIL is correct and mBERT is wrong.
- both models miss hate speech.
- both models produce false positives.

Current observation:

- Both models still miss several targeted/religious examples.
- The 79-row diagnostic probe includes generic negative phrases labeled as hate, which creates label-definition noise.

## 8. Discussion

Questions to answer:

- Does MuRIL actually help for Romanized Hinglish?
- Does mBERT generalize better because Romanized Hinglish often resembles English-token patterns?
- Are model differences smaller than dataset-definition differences?
- How much does label quality affect conclusions?
- Do simple lexical baselines already capture much of the in-domain signal, and where do transformers improve cross-dataset generalization?
- Are Kaggle-Hinglish-Hate-trained transformers too conservative on external positive labels?

## 9. Limitations

Current limitations:

- The original Kaggle source is not purely Hinglish; the current controlled file is the Hinglish subset.
- 79-row diagnostic probe is too small, provenance-uncertain, and noisy.
- Public datasets may have different regional contexts.
- Some datasets may be offensive-language datasets rather than strict hate-speech datasets.
- Annotation subjectivity is a major issue.

## 10. Conclusion

Summarize:

- What model performed best under which setting.
- Whether Indian-language-specific pretraining helped.
- Why cross-dataset evaluation matters.
- Future work: build a carefully annotated India-focused Hinglish evaluation set.

## Appendix

Possible appendices:

- Label mapping rules.
- Hyperparameters.
- Dataset audit tables.
- Extra error-analysis examples.
- Full cross-dataset baseline matrix.
- Full-size generated figures or additional confusion matrices.
