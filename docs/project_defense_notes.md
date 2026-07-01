# Project Defense Notes

Date: 2026-06-26

This document is written for project understanding, viva-style questions, and later paper writing. It is not the final paper. It explains what the project is doing, why each experiment matters, and how to answer common questions without getting lost in implementation details.

## One-Sentence Project Summary

This project compares mBERT and MuRIL for Hinglish and Hindi-English code-mixed harmful speech detection, with the key finding that model performance depends strongly on the dataset situation: label definition, platform, script mix, and whether the test set matches the training set.

## Current Research Question

The practical research question is:

> Does Indian-language-specific pretraining in MuRIL make it better than general multilingual mBERT for Hinglish/code-mixed hate or offensive speech detection, especially when models are tested across different datasets?

The early answer is not a simple yes or no. mBERT is stronger on the matched Kaggle Hinglish hate and CM offensive/code-mixed settings. MuRIL is stronger on THAR targeted religious hate and some THAR/CM transfer directions.

## Why The Framing Changed

The starting idea was a direct mBERT-vs-MuRIL comparison. After adding datasets, the project became more interesting: the answer changes depending on what the dataset means by a positive label.

Examples:

- `kaggle_hinglish_hate` uses a general hate/non-hate label on a Hinglish subset.
- `cm_splits_codemixed` uses an offense label, so it is hate-adjacent rather than strict hate speech.
- `thar_religion` uses a targeted AntiReligion label, so it is narrower but cleaner for religious hate.

This means the paper should not claim that one model is universally better. The stronger claim is that pretraining advantages are conditional on dataset situation.

## Model Basics

**mBERT** is multilingual BERT. It was pretrained on many languages using Wikipedia text. It is general and multilingual, but it was not specifically built for Indian social media or Hinglish.

**MuRIL** is a multilingual model focused on Indian languages. It is expected to have advantages for Indian-language text, especially when Devanagari or Indian-language morphology is important.

**Fine-tuning** means taking a pretrained model and training it further on a specific task. In this project, the task is binary classification: predict `0` or `1` for a text example.

**Checkpoint** means a saved trained model folder. A checkpoint includes learned weights, tokenizer files, and config files needed to run prediction later.

## Dataset Basics

The project currently has three primary source-backed datasets:

| Dataset ID | Positive label means | Why it matters |
|---|---|---|
| `kaggle_hinglish_hate` | hate | Main Hinglish subset from the Kaggle source |
| `cm_splits_codemixed` | offensive | Indian politics / code-mixed Twitter/X data; hate-adjacent |
| `thar_religion` | AntiReligion | Targeted religious hate in Hindi-English code-mixed YouTube comments |

The `existing_79_row_benchmark` file is not used for primary conclusions. It is kept as a diagnostic probe because its source is uncertain and it may be manually written or AI-generated.

## Important ML Terms

**Training set**: data the model learns from.

**Validation/test set**: data used to measure whether the trained model works on examples it did not train on.

**In-domain evaluation**: train and test on the same dataset situation. Example: train on `thar_religion`, test on held-out `thar_religion`.

**Cross-dataset evaluation**: train on one dataset, test on another. Example: train on `kaggle_hinglish_hate`, test on `thar_religion`. This is harder and more research-relevant because it tests generalization.

**Accuracy**: percentage of all examples classified correctly. Accuracy can be misleading if a model mostly predicts the majority class.

**Precision for positive class**: among examples the model predicted as hate/offensive, how many were actually positive.

**Recall for positive class**: among actual hate/offensive examples, how many the model caught. For harmful speech detection, low positive recall means many harmful examples are missed.

**F1 score**: balance between precision and recall.

**Macro F1**: average F1 across both classes. It is useful because it does not let the majority class dominate the result.

**False negative**: a positive/harmful example predicted as negative. In this project, false negatives are especially important because they are missed hate/offensive examples.

**False positive**: a negative/non-harmful example predicted as positive. Too many false positives can over-moderate harmless speech.

## Main Results So Far

Matched dataset results:

| Test dataset | Best transformer | Training dataset | Macro F1 | Positive F1 | Positive recall |
|---|---|---|---:|---:|---:|
| `kaggle_hinglish_hate` | mBERT | `kaggle_hinglish_hate` | 65.6% | 51.3% | 38.6% |
| `cm_splits_codemixed` | mBERT | `cm_splits_codemixed` | 78.3% | 71.4% | 68.7% |
| `thar_religion` | MuRIL | `thar_religion` | 77.9% | 77.4% | 80.3% |

Interpretation:

- mBERT currently wins on matched Latin-script-heavy Hinglish/offensive settings.
- MuRIL currently wins on matched targeted religious hate.
- Every dataset is best served by a model trained on that same dataset, which means cross-dataset transfer is weak.

## Why Baselines Matter

The TF-IDF baselines are simple models that use word/character patterns rather than deep contextual pretraining. They are important because if a simple model performs similarly to a transformer, the dataset may contain strong lexical cues.

In this project, TF-IDF baselines are competitive and sometimes beat transformers in transfer conditions. That is not a failure; it is evidence that harmful speech datasets often contain repeated keywords, slogans, target terms, and platform-specific language.

## Why The 79-Row Probe Is Excluded

The 79-row file is useful for debugging but weak as scientific evidence because:

- provenance is uncertain;
- it may be manually written or AI-generated;
- labels appear noisy;
- positive examples are sometimes generic negativity rather than targeted hate;
- it has no confirmed source citation.

It can be mentioned as a lesson about evaluation quality, but it should not support final model-superiority claims.

## Why Initial Saved Project Checkpoints Looked Collapsed

The initial saved project checkpoints predicted mostly non-hate on the 79-row probe. That does not prove the models were broken in a universal sense. Likely explanations include:

- the checkpoint training data or label mapping may not match the 79-row probe;
- the checkpoint may have learned a conservative decision boundary, predicting positive only when cues are very strong;
- the probe's labels may not match strict hate-speech definitions;
- if training data was imbalanced or noisy, the model may have found non-hate prediction safer;
- saved checkpoints alone do not preserve full experimental context unless training data, split, seed, hyperparameters, and preprocessing are recorded.

For paper writing, call them "initial saved project checkpoints" and treat them as diagnostic context, not as a formal experimental condition.

## Error Analysis Takeaways

The error analysis shows where models fail, not only their scores.

Key findings:

- Kaggle-trained models miss many THAR positives, so broad Hinglish hate training does not transfer cleanly to targeted religious hate.
- THAR-trained models still miss many Kaggle positives, so targeted religious hate training does not create a general Hinglish hate detector.
- mBERT has fewer false negatives on matched Kaggle and CM.
- MuRIL has fewer false negatives on matched THAR and THAR-to-CM transfer.
- Devanagari-only rows have high false-negative rates, which supports further investigation of script effects.

## Why THAR Is Methodologically Useful

THAR is not just another dataset. It helps us see what a more formal research dataset looks like:

- it has a specific target: religious hate;
- it separates targeted hate from general non-hate;
- it has a clearer domain: YouTube comments;
- it includes target-group framing;
- it shows that narrow, well-defined datasets can produce different conclusions from broad Hinglish datasets.

Our project can borrow this discipline: every dataset section should state source, platform, label meaning, target, script profile, and caveats.

## Likely Questions And Good Answers

**Why compare mBERT and MuRIL?**

mBERT is a general multilingual model, while MuRIL is designed around Indian languages. Hinglish sits between English, Hindi, transliteration, and Indian social media usage, so the comparison tests whether Indian-language-specific pretraining helps.

**Why not just use accuracy?**

Accuracy can hide missed hate speech. A model can look accurate by predicting the majority class. Macro F1 and positive recall are more useful because we care about both classes and especially missed positive examples.

**Why do results change across datasets?**

The datasets are not identical tasks. Some label hate, some label offense, and THAR labels targeted religious hate. They also differ in platform, script, and topic. Models learn the dataset situation, not only a universal concept of hate.

**Why include TF-IDF baselines?**

Baselines show whether deep transformers are actually adding value. If a simple lexical model performs well, the dataset may be strongly keyword-driven.

**Can we claim MuRIL is better for Indian hate speech?**

Not universally. Current evidence supports a narrower claim: MuRIL is stronger on THAR targeted religious hate and some THAR-related transfer settings, while mBERT is stronger on matched Kaggle and CM conditions.

**What is the biggest limitation right now?**

Label comparability. The positive class does not mean exactly the same thing across datasets. The paper must be honest about this and treat cross-dataset results as robustness evidence, not a single clean universal task.

## Next Experiments To Understand The Models Better

1. Manual error coding: label sampled errors by reason, such as label ambiguity, target-group cue, political context, transliteration, script issue, generic profanity, or missing context.
2. Mixed-dataset training: train one mBERT and one MuRIL on combined primary datasets, then test separately on each dataset.
3. Leave-one-dataset-out training: train on two datasets and test on the third to measure transfer.
4. Script-specific analysis: separate Latin-only, Devanagari-only, and mixed-script examples.
5. Label-harmonization experiment: define a broader "harmful speech" label and clearly state that it is not strict hate speech.

## Paper Claim To Aim For

A defensible paper claim is:

> In Hinglish and Hindi-English code-mixed harmful speech detection, model ranking is conditional on dataset situation. mBERT performs better on matched Latin-script Hinglish/offensive datasets, while MuRIL performs better on targeted religious hate and some related transfer settings. Cross-dataset evaluation reveals that dataset label policy and domain are as important as model choice.

## What You Should Be Able To Defend Yourself

If someone asks about this project, the goal is not to memorize every number. The goal is to understand the logic of the research.

### 1. Why The Project Matters

You should be able to say:

> Hinglish hate speech detection is hard because the text mixes Hindi, English, transliteration, slang, and platform-specific context. A model that works on one dataset may fail on another because the positive label may mean hate, offense, or targeted religious hate.

### 2. Why mBERT Versus MuRIL Is Interesting

You should be able to say:

> mBERT is a general multilingual model. MuRIL is focused on Indian languages. Since Hinglish sits between English, Hindi, Romanized Hindi, and Indian social media, the comparison tests whether Indian-language-specific pretraining actually helps.

### 3. Why The Answer Is Conditional

You should be able to say:

> The answer changes by dataset. mBERT currently wins on matched Kaggle Hinglish and CM code-mixed offensive data. MuRIL wins on THAR targeted religious hate and some THAR-related transfer. So the research finding is not "mBERT wins" or "MuRIL wins"; it is that dataset situation changes the winner.

### 4. Why Cross-Dataset Testing Is The Core

You should be able to say:

> In-domain testing only tells us whether a model learned one dataset. Cross-dataset testing tells us whether it generalizes. Since performance drops a lot across datasets, this project shows that label policy and domain are major parts of hate-speech evaluation.

### 5. Why The Project Is Not Final Yet

You should be able to say:

> The main limitation is rigor. Current transformer runs use one seed and one main hyperparameter setting. We have started mixed-dataset training with Kaggle + CM, but before making final claims we still need multi-seed results, mean and standard deviation, confidence intervals or bootstrap intervals, stronger citation/license verification, and the remaining mixed-dataset conditions.

### 6. How AI Was Used

You should be honest and calm:

> AI tools helped with coding, debugging, documentation, and report organization. The research direction, dataset choices, interpretation, and final claims were reviewed and directed by me.

### 7. The Cleanest One-Minute Explanation

Use this when someone asks, "What is your project?"

> My project compares mBERT and MuRIL for Hinglish and Hindi-English code-mixed harmful speech detection. At first, the question was whether MuRIL is better because it is Indian-language-focused. After testing multiple datasets, the better finding is that the winner changes by dataset situation. mBERT does better on matched Latin-script Hinglish and offensive data, while MuRIL does better on targeted religious hate and some THAR-related transfer. The project shows that dataset label definition, platform, and script mix matter as much as model choice.
