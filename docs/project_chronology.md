# Project Chronology

This file records the project in sequence so the final paper can explain how the research question, code, datasets, and results evolved over time.

## Stage 0: Existing Project State At Start Of This Session

Approximate status before the current cleanup:

- The project had been already present at the start of this session.
- It already contained:
  - `combined_hate_speech_dataset.csv`
  - saved local model checkpoints under `Models/mbert_model` and `Models/muril_model`
  - individual training scripts for mBERT and MuRIL
  - `benchmark.py`
  - `benchmark_test.csv`
  - `benchmark_results_detailed.csv`
- Some code still had path assumptions that did not match the Mac folder:
  - Code referenced `./models/...`
  - Actual folder was `./Models/...`
- `requirements.txt` was empty.
- The training scripts had duplicated logic.
- The benchmark evaluated models one text at a time.

## Stage 1: Initial Project Inspection

Date: 2026-06-24

The project goal was clarified:

> Compare whether a general multilingual model, mBERT, or an Indian-language-specific model, MuRIL, is better for Hinglish hate speech detection.

Initial folder inspection showed:

- Saved checkpoints for both models existed locally.
- A combined dataset existed locally.
- A 79-row benchmark file existed locally.
- The project already had a THAR paper PDF and extracted text.

Initial concern:

- The existing saved models appeared to predict almost everything as non-hate.

## Stage 2: Dataset Audit

Date: 2026-06-24

The local Kaggle source file was audited.

Findings:

| Property | Value |
|---|---:|
| Total rows | 29,550 |
| Non-hate rows | 15,825 |
| Hate rows | 13,725 |
| English rows | 15,000 |
| Hindi rows | 9,767 |
| Hinglish rows | 4,783 |

Main interpretation:

- The dataset name suggests Hinglish, but most rows are English or Hindi.
- The project should not treat the full dataset as purely Hinglish.
- A Hinglish-only subset is needed for the core research question.

## Stage 3: Existing Saved-Model Benchmark

Date: 2026-06-24

The existing saved checkpoints were evaluated on the existing 79-row benchmark.

These results represent the model behavior before retraining and before code cleanup.

| Model | Accuracy | Hate F1 | Hate Recall | Macro F1 | True Positives | False Negatives |
|---|---:|---:|---:|---:|---:|---:|
| mBERT existing checkpoint | 51.9% | 5.0% | 2.6% | 36.4% | 1 | 38 |
| MuRIL existing checkpoint | 50.6% | 0.0% | 0.0% | 33.6% | 0 | 39 |

Interpretation:

- mBERT detected only 1 of 39 hate-labeled examples.
- MuRIL detected 0 of 39 hate-labeled examples.
- Both existing saved checkpoints were strongly biased toward predicting non-hate.
- This explained the earlier concern that the models were “collapsed.”

## Stage 4: Research Reframing

Date: 2026-06-24

The project was reframed from:

> Which model is better on one dataset?

to:

> How do mBERT and MuRIL behave across different Hinglish/code-mixed hate speech datasets, especially Indian-context datasets?

Reason:

- Dataset identity matters.
- Some available Hindi-English datasets may be Pakistani, South Asian broadly, or not Indian-specific.
- Hate speech definitions differ across datasets.
- Cross-dataset testing is more research-worthy than a single train/test split.

## Stage 5: Codebase Cleanup And Reproducibility

Date: 2026-06-24

Changes made:

- Added a local Python environment using `.venv`.
- Added dependencies to `requirements.txt`.
- Added `.gitignore` for GitHub safety.
- Added shared reusable training code:
  - `experiments/train_transformer.py`
- Added device-specific entrypoints:
  - `experiments/train_mac_mps.py`
  - `experiments/train_colab_cuda.py`
  - `experiments/train_cpu_debug.py`
- Added dataset tools:
  - `scripts/audit_dataset.py`
  - `scripts/prepare_kaggle_hinglish_dataset.py`
- Added benchmark runner:
  - `experiments/run_benchmark.py`
- Added documentation:
  - `docs/research_journal.md`
  - `docs/dataset_candidates.md`
  - `docs/experiment_plan.md`
  - `docs/evaluation_explanation.md`
  - `paper_outline.md`

## Stage 6: Hinglish-Only Dataset Preparation

Date: 2026-06-24

The Kaggle source file was standardized and split by language.

Generated files:

- `data/processed/kaggle_hinglish_hate_all.csv`
- `data/processed/kaggle_hinglish_hate_english.csv`
- `data/processed/kaggle_hinglish_hate_hindi.csv`
- `data/processed/kaggle_hinglish_hate.csv`

The Hinglish-only subset had:

| Property | Value |
|---|---:|
| Rows | 4,780 |
| Non-hate | 2,914 |
| Hate | 1,866 |

Interpretation:

- This subset better matches the research question than the full combined dataset.
- The label distribution is not perfectly balanced, but it is usable.

## Stage 7: Local Mac Training

Date: 2026-06-24

Environment:

- Machine: Apple M4 Max
- RAM: 64 GB
- Framework: PyTorch + Hugging Face Transformers
- Acceleration: Apple MPS
- Not used: MLX

Training setup:

- Dataset: `data/processed/kaggle_hinglish_hate.csv`
- Split: 80/20 stratified train/validation
- Epochs: 2
- Batch size: 8
- Cleaning: minimal cleaning

Validation results:

| Model | Accuracy | Hate F1 | Hate Recall | Macro F1 |
|---|---:|---:|---:|---:|
| mBERT retrained | 71.1% | 51.4% | 39.1% | 65.4% |
| MuRIL retrained | 66.5% | 33.1% | 21.2% | 55.4% |

Interpretation:

- On the held-out validation split from the Kaggle Hinglish Hate subset, mBERT performed better.
- Both models still had weak hate recall.
- The models were no longer fully collapsed after retraining.

## Stage 8: Retrained Models On Original 79-Row Benchmark

Date: 2026-06-24

The newly retrained models were evaluated on the existing 79-row benchmark.

| Model | Accuracy | Hate F1 | Hate Recall | Macro F1 | True Positives | False Negatives |
|---|---:|---:|---:|---:|---:|---:|
| mBERT retrained | 51.9% | 13.6% | 7.7% | 40.2% | 3 | 36 |
| MuRIL retrained | 64.6% | 50.0% | 35.9% | 61.3% | 14 | 25 |

Interpretation:

- MuRIL performed better on the small benchmark.
- mBERT performed better on the held-out validation split.
- This contradiction is important: model ranking changes depending on the evaluation set.
- The 79-row benchmark appears label-noisy and too small for final conclusions.

## Stage 9: Simple Baseline Models

Date: 2026-06-24

TF-IDF baselines were added:

- TF-IDF + Logistic Regression
- TF-IDF + Linear SVM

Results:

| Model | Evaluation | Accuracy | Hate F1 | Hate Recall | Macro F1 |
|---|---|---:|---:|---:|---:|
| TF-IDF Logistic Regression | Hinglish validation | 63.0% | 53.8% | 55.2% | 61.4% |
| TF-IDF Linear SVM | Hinglish validation | 62.9% | 52.3% | 52.3% | 61.0% |
| TF-IDF Logistic Regression | 79-row benchmark | 54.4% | 50.0% | 46.2% | 54.1% |
| TF-IDF Linear SVM | 79-row benchmark | 41.8% | 46.5% | 51.3% | 41.3% |

Interpretation:

- The simple TF-IDF models are competitive with the transformers on hate-class F1.
- This is a meaningful finding.
- It may indicate that `kaggle_hinglish_hate` contains lexical signals that simpler models can capture.
- It also means the transformer setup may need more tuning, better datasets, or cleaner labels before it clearly outperforms classical methods.

## Stage 10: Current Research Interpretation

Date: 2026-06-24

Main findings so far:

- The existing saved checkpoints were biased toward non-hate.
- The full combined dataset is not purely Hinglish.
- Filtering to Hinglish changes the experimental setup substantially.
- Retraining improved hate detection.
- mBERT currently performs better on the `kaggle_hinglish_hate` held-out validation split.
- MuRIL currently performs better on the tiny 79-row benchmark.
- Simple TF-IDF baselines are surprisingly competitive.
- The project needs more Indian-context datasets before making strong claims.
- The small 79-row benchmark appears label-noisy: many positive labels are generic negative phrases rather than strict targeted hate, while both models still miss several targeted/religious examples.
- This is an important paper point: evaluation-set definition and domain can change the apparent winner.

Main research direction now:

> The project should study whether mBERT or MuRIL generalizes better across Indian Hinglish/code-mixed hate speech datasets, rather than declaring a winner from one dataset.

## Stage 11: First External Dataset Acquisition

Date: 2026-06-24

The first Indian-context external dataset candidate was inspected:

- Repository: `https://github.com/shikharras/cm-hate-speech-detection`
- Local path: `data/raw/cm-hate-speech-detection`
- Project description: Hindi-English code-mixed hate/offensive speech detection with an Indian politics dataset and a custom Hindi-English code-mixed dataset.

Important inspection result:

- `data/filled_10k.csv` contains text and labels.
- `data/splits/train.csv`, `val.csv`, and `test.csv` contain text and labels.
- `data/hinglish_hatespeech.csv` contains tweet IDs and labels, but no tweet text, so it is not directly usable for training without text recovery.
- No obvious license file was found during local inspection, so redistribution/publication constraints still need review.

Conversion script added:

- `scripts/convert_cm_hate_speech.py`

Converted files:

| File | Rows | Notes |
|---|---:|---|
| `cm_splits_all.csv` | 8,512 | all text rows from train/val/test splits |
| `cm_splits_codemixed.csv` | 3,900 | only rows marked code-mixed |
| `cm_train_codemixed.csv` | 3,074 | code-mixed train split |
| `cm_val_codemixed.csv` | 402 | code-mixed validation split |
| `cm_test_codemixed.csv` | 424 | code-mixed test split |

Audit of `cm_splits_codemixed.csv`:

| Property | Value |
|---|---:|
| Rows | 3,900 |
| Non-offensive/non-hate-adjacent label | 2,455 |
| Offensive/hate-adjacent label | 1,445 |
| Duplicate texts | 82 |
| Average words | 26.78 |

Interpretation:

- This is a promising Indian-context code-mixed dataset.
- The label column is `offense`, so it should initially be described as offensive/hate-adjacent, not automatically strict hate speech.
- This dataset can support cross-dataset testing against the current local Hinglish dataset.

## Stage 12: Second External Dataset Acquisition

Date: 2026-06-24

The THAR targeted religious hate speech dataset was inspected and converted.

- Repository: `https://github.com/aakash-dl/THAR`
- Local path: `data/raw/THAR`
- Raw file: `data/raw/THAR/THAR-Dataset.csv`
- Converted file: `data/processed/thar_religion.csv`

Dataset situation:

- Hindi-English code-mixed YouTube comments.
- Narrow task: targeted hate speech against religion.
- Binary label: `AntiReligion` vs `Non-AntiReligion`.
- Multi-class target labels: Islam, Hinduism, Christianity, none.
- Strong Indian-context candidate, but domain is religious YouTube comments rather than general Hinglish social media.

Audit of `thar_religion.csv`:

| Property | Value |
|---|---:|
| Rows | 11,549 |
| Non-AntiReligion / label 0 | 6,095 |
| AntiReligion / label 1 | 5,454 |
| Duplicate texts | 0 |
| Average words | 24.90 |

Interpretation:

- THAR gives the project a stricter targeted-hate dataset than the current local dataset or CM offensive dataset.
- It includes both Devanagari and Romanized/code-mixed text, so model behavior may differ from Romanized-only Hinglish.
- This dataset is useful for testing whether MuRIL benefits from Indian-language and Devanagari-heavy pretraining.
