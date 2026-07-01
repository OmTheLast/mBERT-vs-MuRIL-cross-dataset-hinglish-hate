# Model Reload Check

Date: 2026-06-29

This note verifies that the saved local model checkpoints still load and reproduce the stored evaluation results.

## Checkpoint Presence

The project currently has the following usable saved checkpoints:

| Checkpoint folder | Role |
|---|---|
| `Models/mbert__train-kaggle_hinglish_hate__seed42__e2` | controlled mBERT trained on `kaggle_hinglish_hate` |
| `Models/muril__train-kaggle_hinglish_hate__seed42__e2` | controlled MuRIL trained on `kaggle_hinglish_hate` |
| `Models/mbert__train-cm_splits_codemixed__seed42__e2` | controlled mBERT trained on `cm_splits_codemixed` |
| `Models/muril__train-cm_splits_codemixed__seed42__e2` | controlled MuRIL trained on `cm_splits_codemixed` |
| `Models/mbert__train-thar_religion__seed42__e2` | controlled mBERT trained on `thar_religion` |
| `Models/muril__train-thar_religion__seed42__e2` | controlled MuRIL trained on `thar_religion` |
| `Models/mbert_model` | initial saved project checkpoint; context only |
| `Models/muril_model` | initial saved project checkpoint; context only |

Each checkpoint folder contains the expected model and tokenizer files needed for local inference.

## Scripts Rerun

The following saved-model test scripts were rerun:

```bash
.venv/bin/python experiments/run_model_harness.py \
  --model-key all \
  --input-csv benchmark_test.csv \
  --output results/model_reload_check_benchmark_predictions_2026-06-29.csv \
  --summary-output results/model_reload_check_benchmark_summary_2026-06-29.csv

.venv/bin/python experiments/run_transformer_cross_dataset_eval.py \
  --checkpoint mbert:kaggle_hinglish_hate:reload_check_2026_06_29:Models/mbert__train-kaggle_hinglish_hate__seed42__e2 \
  --checkpoint muril:kaggle_hinglish_hate:reload_check_2026_06_29:Models/muril__train-kaggle_hinglish_hate__seed42__e2 \
  --checkpoint mbert:cm_splits_codemixed:reload_check_2026_06_29:Models/mbert__train-cm_splits_codemixed__seed42__e2 \
  --checkpoint muril:cm_splits_codemixed:reload_check_2026_06_29:Models/muril__train-cm_splits_codemixed__seed42__e2 \
  --checkpoint mbert:thar_religion:reload_check_2026_06_29:Models/mbert__train-thar_religion__seed42__e2 \
  --checkpoint muril:thar_religion:reload_check_2026_06_29:Models/muril__train-thar_religion__seed42__e2 \
  --output results/model_reload_check_transformer_summary_2026-06-29.csv \
  --detailed-output results/model_reload_check_transformer_predictions_2026-06-29.csv

.venv/bin/python experiments/run_benchmark.py \
  --input benchmark_test.csv \
  --output results/model_reload_check_initial_saved_benchmark_detailed_2026-06-29.csv \
  --summary-output results/model_reload_check_initial_saved_benchmark_summary_2026-06-29.csv \
  --evaluation-name reload_check_initial_saved_79_probe \
  --dataset-name existing_79_row_benchmark \
  --condition initial_saved_project_checkpoints
```

## Cross-Dataset Reload Result

The reload check produced `results/model_reload_check_transformer_summary_2026-06-29.csv`.

This file was compared against the existing paper-facing transformer result file:

- existing: `results/transformer_cross_dataset_summary.csv`
- reload check: `results/model_reload_check_transformer_summary_2026-06-29.csv`

Comparison keys:

- `model`
- `train_dataset`
- `test_dataset`

Compared metric columns:

- `accuracy`
- `precision_positive`
- `recall_positive`
- `f1_positive`
- `precision_macro`
- `recall_macro`
- `f1_macro`
- `tn`
- `fp`
- `fn`
- `tp`

Result:

| Check | Result |
|---|---|
| Existing rows | 24 |
| Reload rows | 24 |
| Matched rows | 24 |
| Maximum metric difference | 0 |
| Status | pass |

Interpretation: the six controlled saved checkpoints reproduce the stored cross-dataset results exactly.

## 79-Row Diagnostic Probe Reload Result

The full harness over all registered checkpoints produced:

| Model key | Train dataset | Accuracy | Positive recall | Positive F1 | Macro F1 | TP | FN |
|---|---|---:|---:|---:|---:|---:|---:|
| `mbert_kaggle_hinglish_hate` | `kaggle_hinglish_hate` | 51.9% | 7.7% | 13.6% | 40.2% | 3 | 36 |
| `muril_kaggle_hinglish_hate` | `kaggle_hinglish_hate` | 64.6% | 35.9% | 50.0% | 61.3% | 14 | 25 |
| `mbert_cm_splits_codemixed` | `cm_splits_codemixed` | 46.8% | 2.6% | 4.5% | 33.9% | 1 | 38 |
| `muril_cm_splits_codemixed` | `cm_splits_codemixed` | 50.6% | 2.6% | 4.9% | 35.8% | 1 | 38 |
| `mbert_thar_religion` | `thar_religion` | 51.9% | 5.1% | 9.5% | 38.4% | 2 | 37 |
| `muril_thar_religion` | `thar_religion` | 53.2% | 5.1% | 9.8% | 39.1% | 2 | 37 |
| `mbert_session_start` | unknown existing checkpoint | 51.9% | 2.6% | 5.0% | 36.4% | 1 | 38 |
| `muril_session_start` | unknown existing checkpoint | 50.6% | 0.0% | 0.0% | 33.6% | 0 | 39 |

Interpretation: the diagnostic-probe behavior also reproduces. The initial saved project checkpoints remain strongly biased toward predicting non-hate on this probe. This is still context only, not a primary paper result.

## Warning Observed

Transformers emitted a tokenizer warning about `fix_mistral_regex=True` while loading BERT/MuRIL tokenizers. This warning has appeared before in the project. Earlier testing showed that passing this flag breaks these BERT-style tokenizers in this environment, so the project intentionally does not use the flag.

The warning should be documented as an environment/tooling warning, not interpreted as a new model result.

## Conclusion

The saved checkpoints are usable. The controlled saved models reproduce the stored cross-dataset metrics exactly, and the diagnostic-probe outputs reproduce the previously documented behavior.

