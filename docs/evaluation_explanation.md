# Evaluation Explanation

This note explains the evaluation terms used in the project. It is written as a plain-language reference for future paper writing.

## What Is A Benchmark?

A benchmark is a fixed test set used to compare models.

In this project, `benchmark_test.csv` is a small 79-row diagnostic probe. Both mBERT and MuRIL are tested on exactly the same 79 examples, so their diagnostic results can be compared directly.

This probe is useful for quick sanity checks, but it is not enough for final research conclusions because:

- 79 rows is very small.
- Some labels look subjective or inconsistent.
- Some examples labeled hate are generic negativity rather than clear targeted hate speech.
- A few examples are duplicates or near-duplicates.

## What Is A Validation Split?

A validation split is a held-out part of a dataset that the model does not train on.

For the Kaggle Hinglish Hate-only run:

- 80% of `kaggle_hinglish_hate.csv` was used for training.
- 20% was held out for validation.
- The split was stratified, meaning both train and validation kept a similar hate/non-hate label balance.

Validation results tell us how well the model performs on unseen examples from the same dataset.

## Why Accuracy Is Not Enough

Accuracy means:

> How many total examples did the model classify correctly?

This can be misleading for hate speech detection. If most examples are non-hate, a model can predict non-hate for everything and still get a decent accuracy score.

Example:

```text
100 examples
90 are non-hate
10 are hate
```

A model that always predicts non-hate gets 90% accuracy, but it detects zero hate speech.

That is why we focus on F1, precision, recall, and confusion matrices.

## Precision, Recall, And F1

For the hate class:

- **Precision**: of everything the model called hate, how much was actually hate?
- **Recall**: of all real hate examples, how many did the model catch?
- **F1**: a combined score balancing precision and recall.

For this project, hate recall is especially important because missing hate speech is a major failure.

## Confusion Matrix Terms

For binary labels:

```text
0 = non-hate
1 = hate
```

The confusion matrix terms are:

- **TN**: true negative. Non-hate correctly predicted as non-hate.
- **FP**: false positive. Non-hate incorrectly predicted as hate.
- **FN**: false negative. Hate incorrectly predicted as non-hate.
- **TP**: true positive. Hate correctly predicted as hate.

In hate speech detection, false negatives are especially important because they are harmful content the model missed.

## What We Learned So Far

The existing saved checkpoints at the start of this session were heavily biased toward non-hate. On the 79-row diagnostic probe:

- the existing mBERT checkpoint caught only 1 out of 39 hate examples.
- the existing MuRIL checkpoint caught 0 out of 39 hate examples.

After retraining on the Hinglish-only subset:

- mBERT improved on validation data from the same dataset.
- MuRIL performed better than mBERT on the small 79-row diagnostic probe.

This means model performance depends heavily on the evaluation set. That is one of the main research findings so far.

## Why Label Quality Matters

Some diagnostic-probe examples labeled as hate are not clearly hate speech. For example, generic negative statements may be rude or negative without targeting a protected group.

This matters because different datasets may define labels differently:

- hate speech
- offensive language
- profanity
- aggression
- toxicity
- targeted abuse

These are related, but they are not identical. The paper must be clear about how labels are mapped into binary `hate` and `non-hate`.
