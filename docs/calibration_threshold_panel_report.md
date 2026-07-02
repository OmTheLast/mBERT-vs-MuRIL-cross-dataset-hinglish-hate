# Calibration And Threshold Diagnostic Panel

Date: 2026-07-02

This report checks whether the models are genuinely unable to detect positive hate/offensive examples, or whether they assign positive examples probabilities below the default `0.50` decision threshold.

The combined result file is:

```text
results/collapse_diagnostics/calibration_panel_summary.csv
```

Full row-level probability files were generated locally but are ignored by Git because they contain dataset text.

## Checkpoints Compared

| Training condition | Model checkpoints |
|---|---|
| Initial saved project checkpoints | `Models/mbert_model`, `Models/muril_model` |
| Kaggle-only controlled checkpoints | `Models/mbert__train-kaggle_hinglish_hate__seed42__e2`, `Models/muril__train-kaggle_hinglish_hate__seed42__e2` |
| Mixed Kaggle+CM checkpoints | `Models/mbert__train-mixed_kaggle_plus_cm__seed42__e2`, `Models/muril__train-mixed_kaggle_plus_cm__seed42__e2` |

## Main Finding

The user's memory was correct: hesitancy to call examples positive appeared from the beginning of the project.

This is visible in two ways:

- Many checkpoints predict relatively few positives at the default `0.50` threshold.
- Lower thresholds often recover much higher positive recall and Macro F1.

Important caveat:

The `best_threshold_by_macro_f1` values in this diagnostic are selected directly on each evaluation set. They are useful for diagnosis, but they are not yet a fair paper result. A fair threshold experiment must select the threshold on validation data only, then apply that fixed threshold to held-out test sets.

## Key Examples

| Condition | Model | Evaluation | Default Macro F1 | Best Diagnostic Threshold | Best Diagnostic Macro F1 | Positive Recall: Default -> Best |
|---|---|---|---:|---:|---:|---:|
| initial | mBERT | Kaggle | 57.8% | 0.36 | 65.6% | 23.1% -> 53.1% |
| initial | MuRIL | THAR | 43.8% | 0.29 | 58.9% | 11.2% -> 61.9% |
| Kaggle-only | mBERT | THAR | 44.8% | 0.26 | 56.0% | 15.9% -> 51.0% |
| Kaggle-only | MuRIL | Kaggle | 56.6% | 0.35 | 64.6% | 22.3% -> 52.0% |
| Mixed Kaggle+CM | mBERT | CM | 71.5% | 0.44 | 75.0% | 59.9% -> 70.1% |
| Mixed Kaggle+CM | MuRIL | Kaggle | 37.9% | 0.40 | 61.2% | 0.0% -> 64.3% |
| Mixed Kaggle+CM | MuRIL | THAR | 34.5% | 0.38 | 56.9% | 0.0% -> 46.4% |

## Interpretation

The evidence suggests that several checkpoints learned some positive-class ranking signal, but the default `0.50` threshold often makes them too conservative.

The strongest case is mixed Kaggle+CM MuRIL:

- At threshold `0.50`, it predicts zero positives.
- Its positive probabilities are compressed below `0.50`, with maximum probability around `0.466`.
- Lowering the threshold recovers substantial Macro F1 and positive recall.

This means the collapse should be described carefully:

> Under the mixed Kaggle+CM condition, MuRIL did not simply learn nothing. It learned a weak positive-class signal whose scores stayed below the default classification threshold.

## Research Meaning

This adds a new methodological result to the project:

- Cross-dataset robustness is not only about model architecture and dataset choice.
- Calibration and threshold choice also affect whether a model appears usable for hate-speech detection.
- Accuracy and default-threshold F1 may hide weak but recoverable positive-class signal.

This is especially important for hate-speech detection because false negatives are costly. A conservative model can look stable while missing many harmful examples.

## Next Fair Experiment

The next step should be threshold transfer:

1. For each checkpoint, choose a threshold using only its validation set.
2. Apply that fixed threshold to Kaggle, CM, and THAR held-out evaluations.
3. Compare default-threshold results against validation-tuned-threshold results.

This avoids test-set threshold leakage and gives a paper-safe answer to:

> Are mBERT and MuRIL actually failing to identify hate/offensive text, or are they poorly calibrated under the default threshold?

