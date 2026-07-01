# Hinglish Hate Speech Research Journal

## Project Direction

Working title: **Cross-Dataset Evaluation of mBERT and MuRIL for Hate Speech Detection in Hinglish Code-Mixed Text**.

Core question:

> Does Indian-language-specific pretraining in MuRIL improve Hinglish hate/offensive speech detection compared with general multilingual pretraining in mBERT, especially when models are evaluated across datasets rather than only on one split?

Current refined hypothesis:

> MuRIL may perform better on Indian-language and Devanagari-heavy material, but mBERT may remain competitive or outperform it on noisy Romanized Hinglish because much social media Hinglish uses Latin script and English-like subword patterns.

## What We Know So Far

- The current repository contains local checkpoints for mBERT and MuRIL under `Models/`.
- The local Kaggle source file has 29,550 rows before the Hinglish-only controlled subset is selected.
- A quick audit showed labels are fairly balanced: 15,825 non-hate rows and 13,725 hate rows.
- The same audit showed the dataset is not purely Hinglish:
  - `english`: 15,000 rows
  - `hindi`: 9,767 rows
  - `hinglish`: 4,783 rows
- This means the Kaggle source is useful, but the controlled research file must be the documented Hinglish subset rather than the entire raw file.
- The existing 79-row benchmark produced collapsed behavior:
  - mBERT predicted hate only once.
  - MuRIL predicted no hate at all.
  - This suggests we need better evaluation, clearer datasets, and likely better training/label handling before drawing conclusions.

## Challenges

- Dataset provenance matters: some available code-mixed datasets may reflect Pakistani or broader South Asian language use rather than Indian Hinglish.
- Twitter/X API access is no longer as simple as older Tweepy tutorials imply. Current X API access is usage-priced, and recent search is limited to recent windows unless broader access is available.
- Hate speech labels are subjective and depend on annotation guidelines.
- Keyword-based collection can bias the dataset toward obvious slurs and miss implicit hate.
- Aggressive cleaning may remove useful signals for transformer models.
- Existing public datasets use different label schemes, platforms, and definitions of hate/offensive speech.

## Current Plan

1. Improve the codebase so future experiments are reproducible.
2. Audit the Kaggle Hinglish subset and any newly added dataset with the same script.
3. Collect metadata for candidate datasets before adding them.
4. Standardize all datasets into a common processed schema:
   - `text`
   - `label`
   - `dataset`
   - optional `source`, `language`, `target_group`, `notes`
5. Run in-domain, cross-dataset, and leave-one-dataset-out experiments.
6. Use macro F1 and hate-class F1 as primary metrics, not accuracy alone.
7. Do manual error analysis for paper discussion.

## Changes Made On 2026-06-24

- Added `requirements.txt` dependencies.
- Created a local `.venv` after a global Python install produced dependency conflicts with `aider-chat`. Future runs should use `.venv/bin/python`.
- Added `scripts/audit_dataset.py` for fast CSV dataset audits without requiring pandas.
- Added `experiments/run_benchmark.py` for batched local checkpoint evaluation.
- Added `experiments/train_transformer.py` as a shared fine-tuning runner for mBERT/MuRIL, replacing the need to maintain two near-identical training scripts for future experiments.
- Added device-specific training wrappers for Mac/MPS, Colab/CUDA, and CPU/debug runs.
- Added `scripts/prepare_kaggle_hinglish_dataset.py` to standardize the Kaggle Hinglish source and split it by language.
- Added `docs/dataset_candidates.md` to track possible datasets and access concerns.
- Added `docs/experiment_plan.md` to define the experimental matrix and paper-facing methodology.
- Added this journal so future work can quickly recover context.
- Added `.gitignore` so generated environments, runs, and large model weights are not accidentally pushed to GitHub.

## Local Training Run On 2026-06-24

Environment:

- Machine: Apple M4 Max, 64 GB RAM.
- PyTorch MPS was available.
- Training used `experiments/train_mac_mps.py`.
- Dataset: `data/processed/kaggle_hinglish_hate.csv`.
- Rows: 4,780.
- Label balance: 2,914 non-hate, 1,866 hate.
- Split: 80/20 stratified, seed 42.
- Epochs: 2.
- Batch size: 8.

Saved-checkpoint benchmark before retraining:

| Model | Accuracy | Hate F1 | Hate Recall | Macro F1 | TP | FN |
|---|---:|---:|---:|---:|---:|---:|
| mBERT existing checkpoint | 0.519 | 0.050 | 0.026 | 0.364 | 1 | 38 |
| MuRIL existing checkpoint | 0.506 | 0.000 | 0.000 | 0.336 | 0 | 39 |

Hinglish-only validation after retraining:

| Model | Accuracy | Hate F1 | Hate Recall | Macro F1 |
|---|---:|---:|---:|---:|
| mBERT | 0.711 | 0.514 | 0.391 | 0.654 |
| MuRIL | 0.665 | 0.331 | 0.212 | 0.554 |

Original 79-row benchmark after Hinglish-only retraining:

| Model | Accuracy | Hate F1 | Hate Recall | Macro F1 | TP | FN |
|---|---:|---:|---:|---:|---:|---:|
| mBERT | 0.519 | 0.136 | 0.077 | 0.402 | 3 | 36 |
| MuRIL | 0.646 | 0.500 | 0.359 | 0.613 | 14 | 25 |

Interpretation:

- The existing saved checkpoints at the start of this session had collapsed toward predicting non-hate.
- Retraining on the Hinglish-only subset restores hate detection.
- mBERT performs better on the held-out split from the Kaggle Hinglish Hate subset.
- MuRIL performs better on the small handmade benchmark.
- The 79-row benchmark appears definitionally noisy: many positive labels are generic negative statements rather than strict targeted hate, while both models still miss several clearly targeted/religious examples.
- This supports the broader research direction: results depend heavily on dataset definition, domain, label policy, and evaluation set.
- Transformers 4.57.6 emits a `fix_mistral_regex` warning when loading the saved BERT/MuRIL tokenizers. Trying that flag crashes BERT tokenizers, so the code intentionally does not use it.

## Near-Term TODO

- Run the audit script on each processed dataset whenever the Python environment is ready.
- Move legacy benchmark outputs into `results/` after confirming nothing depends on the old location.
- Download or request access to candidate datasets.
- Create conversion scripts for each dataset once files are available locally.
- Build a single training script that accepts `--model`, `--train-csv`, and `--test-csv`.
- Add a paper outline in `paper/outline.md` once the dataset set is finalized.

## Changes Added After Initial Training

- Added `docs/evaluation_explanation.md` to explain benchmark, validation, accuracy, precision, recall, F1, and confusion matrix terminology.
- Added `experiments/run_baselines.py` for TF-IDF + Logistic Regression and TF-IDF + Linear SVM baselines.
- Added `scripts/make_results_summary.py` to generate `results/summary.md` with clean paper-facing tables.
- Added `paper_outline.md` in the project root.
- Added `docs/project_chronology.md` to preserve the full sequence from the existing project state at the start of this session through current experiments.
- Updated experiment scripts so benchmark/baseline/summary results print clean terminal tables and save labeled CSV/Markdown files.
- Deleted duplicate default benchmark outputs: `results/benchmark_summary.csv` and `results/benchmark_results_detailed.csv`.
- Added `data/README.md` to document raw/processed data handling and GitHub safety.
- Cloned and inspected `cm-hate-speech-detection` under `data/raw/`.
- Added `scripts/convert_cm_hate_speech.py` and converted the usable text-bearing files into project schema.
- Cloned and inspected THAR under `data/raw/THAR`; it contains `THAR-Dataset.csv`.
- Added `scripts/convert_thar.py` for the THAR targeted religious hate dataset.
- Added `docs/dataset_registry.md` and `docs/result_reporting_protocol.md` so future paper sections label dataset situation and citation/caveats clearly.
- Added `docs/model_registry.md` to explain current checkpoint folders and define dataset-aware names for future trained models.
- Added `docs/dataset_acquisition_log.md` to separate usable datasets from blocked/contact-only/context-only sources.

## External Dataset Notes On 2026-06-24

First inspected dataset:

- `cm-hate-speech-detection`
- Indian politics / Hindi-English code-mixed context.
- Usable converted code-mixed file: `data/processed/cm_splits_codemixed.csv`.
- Rows: 3,900.
- Label distribution: 2,455 label `0`, 1,445 label `1`.
- Important caveat: label is mapped from `offense`, so this should be described as offensive/hate-adjacent until source definitions are reviewed.
- License was not obvious in the repository; review required before publishing derived data.

Second inspected dataset:

- `THAR`
- Targeted religious hate / Hindi-English code-mixed YouTube comments.
- Usable converted file: `data/processed/thar_religion.csv`.
- Rows: 11,549.
- Label distribution: 6,095 label `0`, 5,454 label `1`.
- Important caveat: this is narrow targeted religious hate, not general Hinglish hate speech.

## Cross-Dataset Baseline Run On 2026-06-24

Added and ran `experiments/run_cross_dataset_baselines.py`.

Setup:

- Models: TF-IDF + Logistic Regression and TF-IDF + Linear SVM.
- Usable datasets:
  - `kaggle_hinglish_hate`
  - `cm_splits_codemixed`
  - `thar_religion`
- Extra sanity evaluation:
  - `existing_79_row_benchmark`
- Deduplication: enabled by default. This removes duplicate text rows before splitting/training, mainly affecting `cm_splits_codemixed`.
- Split policy:
  - `kaggle_hinglish_hate`: stratified 80/20 split, seed 42.
  - `thar_religion`: stratified 80/20 split, seed 42.
  - `cm_splits_codemixed`: source-provided train/val/test split; train+val used for training, test used for evaluation.

Saved outputs:

- Summary metrics: `results/cross_dataset_baseline_summary.csv`
- Detailed predictions: `results/cross_dataset_baseline_predictions.csv`
- Paper-facing summary: `results/summary.md`
- Research-style report: `docs/baseline_experiment_report.md`

Key results by positive-class F1:

| Train dataset | Test dataset | Best baseline | Positive F1 | Macro F1 |
|---|---|---|---:|---:|
| `kaggle_hinglish_hate` | `kaggle_hinglish_hate` | Logistic Regression | 53.8% | 61.4% |
| `cm_splits_codemixed` | `cm_splits_codemixed` | Logistic Regression | 71.8% | 77.6% |
| `thar_religion` | `thar_religion` | Logistic Regression | 69.3% | 70.6% |
| `kaggle_hinglish_hate` | `cm_splits_codemixed` | Logistic Regression | 43.9% | 35.5% |
| `kaggle_hinglish_hate` | `thar_religion` | Linear SVM | 54.1% | 48.9% |
| `cm_splits_codemixed` | `kaggle_hinglish_hate` | Logistic Regression | 47.3% | 42.5% |
| `cm_splits_codemixed` | `thar_religion` | Logistic Regression | 59.7% | 52.3% |
| `thar_religion` | `kaggle_hinglish_hate` | Linear SVM | 34.2% | 50.8% |
| `thar_religion` | `cm_splits_codemixed` | Logistic Regression | 43.8% | 60.9% |

Interpretation:

- In-domain baselines are strong, especially on `cm_splits_codemixed` and `thar_religion`.
- Cross-dataset performance drops sharply in several directions, confirming that dataset situation and label definition matter.
- Training on `thar_religion` transfers poorly to the 79-row benchmark: both baselines catch only 2 of 39 positive benchmark examples. This is a useful sign that narrow targeted religious hate data does not automatically generalize to the benchmark's mixed/noisy positive labels.
- Training on `cm_splits_codemixed` gives the strongest baseline result on the 79-row benchmark, but that should be interpreted carefully because `cm_splits_codemixed` uses an offensive/hate-adjacent label, not strict hate.

## Transformer Cross-Dataset Evaluation On 2026-06-24

Added and ran `experiments/run_transformer_cross_dataset_eval.py`.

Setup:

- Evaluated existing session-trained transformer checkpoints:
  - `Models/mbert__train-kaggle_hinglish_hate__seed42__e2`
  - `Models/muril__train-kaggle_hinglish_hate__seed42__e2`
- Training dataset for both checkpoints: `kaggle_hinglish_hate`
- Evaluation datasets:
  - `kaggle_hinglish_hate`
  - `cm_splits_codemixed`
  - `thar_religion`
  - `existing_79_row_benchmark`
- Device: Apple MPS.
- Cleaning: minimal.
- Deduplication: enabled.

Saved outputs:

- Summary metrics: `results/transformer_cross_dataset_summary.csv`
- Detailed predictions: `results/transformer_cross_dataset_predictions.csv`
- Research-style report: `docs/transformer_cross_dataset_eval_report.md`
- Combined result summary: `results/summary.md`

Key results:

| Model | Train dataset | Test dataset | Positive F1 | Macro F1 | Positive recall |
|---|---|---|---:|---:|---:|
| mBERT | `kaggle_hinglish_hate` | `kaggle_hinglish_hate` | 51.3% | 65.6% | 38.6% |
| mBERT | `kaggle_hinglish_hate` | `cm_splits_codemixed` | 27.5% | 51.4% | 19.7% |
| mBERT | `kaggle_hinglish_hate` | `thar_religion` | 24.0% | 44.8% | 15.9% |
| mBERT | `kaggle_hinglish_hate` | `existing_79_row_benchmark` | 13.6% | 40.2% | 7.7% |
| MuRIL | `kaggle_hinglish_hate` | `kaggle_hinglish_hate` | 34.8% | 56.6% | 22.3% |
| MuRIL | `kaggle_hinglish_hate` | `cm_splits_codemixed` | 22.8% | 50.4% | 14.3% |
| MuRIL | `kaggle_hinglish_hate` | `thar_religion` | 14.2% | 41.0% | 8.2% |
| MuRIL | `kaggle_hinglish_hate` | `existing_79_row_benchmark` | 50.0% | 61.3% | 35.9% |

Interpretation:

- Kaggle-Hinglish-Hate-trained transformers are conservative on external positive labels.
- mBERT remains stronger on the held-out `kaggle_hinglish_hate` condition.
- MuRIL remains stronger on the 79-row sanity benchmark.
- Neither Kaggle-Hinglish-Hate-trained transformer transfers strongly to `cm_splits_codemixed` or `thar_religion`.
- The next model training should use `cm_splits_codemixed` and `thar_religion` directly, then evaluate with the same cross-dataset script.

## Paper Figure Generation On 2026-06-25

Added and ran `scripts/make_figures.py`.

Purpose:

- Generate reproducible paper-facing figures directly from saved results.
- Avoid manually editing charts, so figures remain consistent with CSV outputs.
- Save both PNG files for quick viewing and SVG files for paper-quality vector graphics.

Generated figures under `results/figures/`:

| Figure | Purpose |
|---|---|
| `dataset_size_label_balance` | Shows dataset size and label balance for `kaggle_hinglish_hate`, `cm_splits_codemixed`, and `thar_religion`. |
| `baseline_cross_dataset_macro_f1` | Heatmap showing best TF-IDF macro F1 across train/test dataset pairs. |
| `transformer_cross_dataset_macro_f1` | Heatmap showing best transformer macro F1 across train/test dataset pairs. |
| `transformer_cross_dataset_positive_recall` | Heatmap showing best transformer positive recall across train/test dataset pairs. |
| `best_transformer_condition_by_test_dataset` | Bar chart showing the best transformer training condition for each test dataset. |
| `kaggle_hinglish_hate_baseline_vs_transformer` | Bar chart comparing best TF-IDF vs best transformer when trained on `kaggle_hinglish_hate`. |
| `transformer_positive_recall_kaggle_hinglish_hate` | Bar chart showing mBERT vs MuRIL positive recall after Kaggle-Hinglish-Hate training. |

Initial paper use:

- Dataset section: dataset size/label balance.
- Results section: baseline heatmap and transformer heatmap.
- Discussion/limitations: baseline-vs-transformer and positive-recall comparison.

## CM Transformer Training And Evaluation On 2026-06-25

Trained paired transformer checkpoints on `cm_splits_codemixed`.

New checkpoints:

- `Models/mbert__train-cm_splits_codemixed__seed42__e2`
- `Models/muril__train-cm_splits_codemixed__seed42__e2`

Training-script matched test results:

| Model | Train dataset | Test split | Accuracy | Positive F1 | Macro F1 | Positive recall |
|---|---|---|---:|---:|---:|---:|
| mBERT | `cm_splits_codemixed` | source `test`, 424 rows | 80.9% | 72.0% | 78.7% | 69.3% |
| MuRIL | `cm_splits_codemixed` | source `test`, 424 rows | 79.2% | 65.6% | 75.4% | 56.0% |

Cross-dataset evaluation was rerun with four controlled checkpoints:

- Kaggle-Hinglish-Hate-trained mBERT
- Kaggle-Hinglish-Hate-trained MuRIL
- CM-trained mBERT
- CM-trained MuRIL

Key cross-dataset observations:

- Matched CM test: mBERT is stronger than MuRIL, with 78.3% macro F1 vs 74.8%.
- CM to THAR: MuRIL is stronger than mBERT, with 59.7% macro F1 vs 58.3% and 59.5% positive recall vs 44.6%.
- CM to Kaggle Hinglish Hate: both models perform only moderately, but MuRIL is slightly stronger by macro F1.
- CM to 79-row benchmark: both models catch only 1 of 39 positive examples, reinforcing that the benchmark is not aligned with this training condition.

Updated outputs:

- `results/transformer_cross_dataset_summary.csv`
- `results/transformer_cross_dataset_predictions.csv`
- `results/summary.md`
- `results/figures/transformer_cross_dataset_macro_f1.png`
- `results/figures/transformer_cross_dataset_positive_recall.png`
- `docs/cm_transformer_training_report.md`

Interpretation:

The result no longer supports a simple one-model-wins framing. The emerging research argument is that mBERT vs MuRIL depends heavily on dataset situation and label definition. mBERT looks stronger on matched CM offensive/code-mixed evaluation, while MuRIL looks more promising for transfer from CM to targeted religious hate.

## THAR Transformer Training And Evaluation On 2026-06-25

Trained paired transformer checkpoints on `thar_religion`.

New checkpoints:

- `Models/mbert__train-thar_religion__seed42__e2`
- `Models/muril__train-thar_religion__seed42__e2`

Training-script matched test results:

| Model | Train dataset | Test split | Accuracy | Positive F1 | Macro F1 | Positive recall |
|---|---|---|---:|---:|---:|---:|
| mBERT | `thar_religion` | stratified 20%, 2,310 rows | 74.8% | 74.5% | 74.8% | 77.7% |
| MuRIL | `thar_religion` | stratified 20%, 2,310 rows | 77.9% | 77.4% | 77.9% | 80.3% |

The full transformer cross-dataset matrix was rerun with six controlled checkpoints:

- Kaggle-Hinglish-Hate-trained mBERT and MuRIL
- CM-trained mBERT and MuRIL
- THAR-trained mBERT and MuRIL

Key cross-dataset observations:

- Matched THAR test: MuRIL is stronger than mBERT, with 77.9% macro F1 vs 74.8%.
- THAR to CM: MuRIL transfers better than mBERT, with 65.1% macro F1 vs 59.8% and 53.1% positive recall vs 40.1%.
- THAR to Kaggle Hinglish Hate: both models transfer weakly; MuRIL is slightly stronger by macro F1, but both are below 47%.
- THAR to 79-row benchmark: both models catch only 2 of 39 positive examples, showing that narrow targeted religious hate training does not align with the benchmark's mixed/noisy positive labels.

Updated outputs:

- `results/transformer_cross_dataset_summary.csv`
- `results/transformer_cross_dataset_predictions.csv`
- `results/summary.md`
- `results/figures/transformer_cross_dataset_macro_f1.png`
- `results/figures/transformer_cross_dataset_positive_recall.png`
- `results/figures/best_transformer_condition_by_test_dataset.png`
- `docs/thar_transformer_training_report.md`

Interpretation:

THAR training gives the clearest MuRIL win so far, but only within the THAR dataset situation and in transfer to the CM offensive/code-mixed test. It does not make MuRIL a universal Hinglish hate detector. The stronger paper framing is now: model rankings are conditional on dataset situation, script/domain, label definition, and transfer direction.

## Primary Result Analysis On 2026-06-25

Added and ran `scripts/analyze_results.py`.

Purpose:

- Separate primary source-backed datasets from the 79-row diagnostic probe.
- Analyze matched results, cross-dataset transfer, mBERT-vs-MuRIL gaps, and transformer-vs-TF-IDF gaps.
- Produce paper-facing tables and figures without using the 79-row probe as primary evidence.

Primary datasets:

- `kaggle_hinglish_hate`
- `cm_splits_codemixed`
- `thar_religion`

Diagnostic-only dataset:

- `existing_79_row_benchmark`

Saved outputs:

- `docs/result_analysis_report.md`
- `results/result_analysis/primary_matched_transformer_results.csv`
- `results/result_analysis/mbert_vs_muril_pairwise_gaps.csv`
- `results/result_analysis/best_transformer_by_primary_test_dataset.csv`
- `results/result_analysis/transformer_generalization_gaps.csv`
- `results/result_analysis/best_transformer_vs_best_tfidf.csv`
- `results/result_analysis/diagnostic_79_row_probe_results.csv`
- `results/result_analysis/transformer_primary_macro_f1_matrix.png`
- `results/result_analysis/transformer_generalization_gaps.png`
- `results/result_analysis/transformer_vs_tfidf_delta.png`

Primary matched transformer conclusions:

| Test dataset | Best transformer | Train dataset | Macro F1 | Positive F1 | Positive recall |
|---|---|---|---:|---:|---:|
| `kaggle_hinglish_hate` | mBERT | `kaggle_hinglish_hate` | 65.6% | 51.3% | 38.6% |
| `cm_splits_codemixed` | mBERT | `cm_splits_codemixed` | 78.3% | 71.4% | 68.7% |
| `thar_religion` | MuRIL | `thar_religion` | 77.9% | 77.4% | 80.3% |

Main interpretation:

- The 79-row probe should be excluded from primary paper conclusions because it may be synthetic/manual and has uncertain provenance.
- Every primary test dataset is best served by an in-domain trained transformer, so cross-dataset transfer remains weak.
- mBERT is stronger on matched Latin-script Kaggle and CM conditions.
- MuRIL is stronger on THAR and on several THAR/CM transfer directions.
- TF-IDF baselines remain competitive; in two transfer directions, the best TF-IDF baseline beats the best transformer by macro F1.
- The paper should frame the finding as conditional model behavior across dataset situations, not a universal mBERT or MuRIL victory.

## Transformer Error Analysis On 2026-06-26

Added and ran `scripts/analyze_errors.py`.

Purpose:

- Pair mBERT and MuRIL predictions on the same primary dataset examples.
- Exclude the 79-row diagnostic probe from primary error analysis.
- Measure false negatives, false positives, model disagreements, hard false negatives, and heuristic feature-level error signals.
- Save a manual annotation template for later qualitative coding.

Saved outputs:

- `docs/error_analysis_report.md`
- `results/error_analysis/paired_transformer_predictions_primary.csv`
- `results/error_analysis/error_rate_summary.csv`
- `results/error_analysis/error_outcome_summary.csv`
- `results/error_analysis/feature_error_summary.csv`
- `results/error_analysis/error_samples.csv`
- `results/error_analysis/hard_false_negative_samples.csv`
- `results/error_analysis/top_error_terms.csv`
- `results/error_analysis/manual_error_annotation_template.csv`
- `results/error_analysis/false_negative_rates.png`
- `results/error_analysis/model_disagreement_advantage.png`

Key error-analysis findings:

- Kaggle-trained mBERT misses 84.1% of THAR positives; Kaggle-trained MuRIL misses 91.8% of THAR positives. This confirms severe under-transfer from broad Hinglish hate to targeted religious hate.
- THAR-trained models still miss many Kaggle positives: 79.4% false-negative rate for mBERT and 76.7% for MuRIL.
- On matched Kaggle, mBERT has lower false-negative rate than MuRIL: 61.4% vs 77.7%.
- On matched CM, mBERT also has lower false-negative rate than MuRIL: 31.3% vs 44.9%.
- On matched THAR, MuRIL has lower false-negative rate than mBERT: 19.7% vs 22.3%.
- On THAR-to-CM transfer, MuRIL has lower false-negative rate than mBERT: 46.9% vs 59.9%, though its false-positive rate is slightly higher.

Interpretation:

The error analysis supports the main paper story: mBERT is better at catching positives in matched Latin-script Kaggle/CM settings, while MuRIL becomes more useful for THAR and THAR-to-CM religious/offensive transfer. The remaining work is manual qualitative coding of sampled errors to explain whether failures come from label ambiguity, target-group cues, political context, transliteration, script, generic profanity, or missing context.

## Project Defense And Dataset Taxonomy Notes On 2026-06-26

Added two paper-support documents:

- `docs/project_defense_notes.md`
- `docs/dataset_taxonomy.md`

Purpose:

- make the project explainable in plain language for learning, viva-style questions, and future paper writing;
- separate model results from dataset situation so the paper does not accidentally treat all positive labels as equivalent;
- record why THAR is useful as methodological inspiration, not only as another dataset;
- preserve the correct terminology for the initial saved project checkpoints and the 79-row diagnostic probe.

Important paper-facing reminder:

- call the starting checkpoint folders "initial saved project checkpoints" rather than "old models";
- treat the 79-row file as a diagnostic probe, not a primary dataset;
- describe each result as a train-dataset/test-dataset situation with a specific positive-label meaning.

## Manual Error Coding First Pass On 2026-06-27

Added and ran `scripts/first_pass_manual_error_coding.py`.

Saved outputs:

- `results/error_analysis/manual_error_annotation_first_pass.csv`
- `results/error_analysis/manual_error_annotation_summary.csv`
- `docs/manual_error_analysis_report.md`

Purpose:

- create a first-pass qualitative coding of sampled transformer errors;
- keep the original blank annotation template unchanged;
- identify recurring reasons behind errors for paper discussion;
- provide a step-by-step guide so the annotations can be manually reviewed later.

Important caveat:

This is a first-pass structured coding aid, not final human-ground-truth annotation. The next human step is to read and revise rows in `manual_error_annotation_first_pass.csv`, especially examples marked as label ambiguity, short/contextless text, or cross-dataset label mismatch.

## Saved Model Reload Check On 2026-06-29

Reran saved-model test scripts to verify that local checkpoints still load and reproduce stored results.

Scripts/checks:

- Listed registered harness models with `experiments/run_model_harness.py --list-models`.
- Ran `experiments/run_model_harness.py --model-key all` on `benchmark_test.csv`.
- Ran `experiments/run_transformer_cross_dataset_eval.py` over all six controlled checkpoints.
- Ran legacy `experiments/run_benchmark.py` on the initial saved project checkpoints.

Saved outputs:

- `docs/model_reload_check_2026-06-29.md`
- `results/model_reload_check_benchmark_summary_2026-06-29.csv`
- `results/model_reload_check_benchmark_predictions_2026-06-29.csv`
- `results/model_reload_check_transformer_summary_2026-06-29.csv`
- `results/model_reload_check_transformer_predictions_2026-06-29.csv`
- `results/model_reload_check_initial_saved_benchmark_summary_2026-06-29.csv`
- `results/model_reload_check_initial_saved_benchmark_detailed_2026-06-29.csv`

Result:

- The six controlled saved checkpoints reproduce `results/transformer_cross_dataset_summary.csv` exactly across 24 model/train/test rows.
- Maximum difference across accuracy, precision, recall, F1, and confusion-matrix metrics was 0.
- The initial saved project checkpoints still reproduce the diagnostic-probe behavior: mBERT catches 1 of 39 positives; MuRIL catches 0 of 39 positives.

Observed warning:

- Transformers emitted the known `fix_mistral_regex=True` tokenizer warning while loading BERT/MuRIL checkpoints.
- Earlier testing showed this flag breaks these BERT-style tokenizers in this environment, so the project intentionally does not use it.

## Indo-HateSpeech Candidate Review On 2026-06-30

Reviewed Indo-HateSpeech as a possible additional dataset before mixed training.

Source:

- Mendeley Data: https://data.mendeley.com/datasets/snc7mxpj6t
- DOI: `10.17632/snc7mxpj6t.1`
- License listed by Mendeley: CC BY 4.0
- Contributor listed by Mendeley: Pravin Kaware

Downloaded files:

- `data/raw/Indo-HateSpeech/Indo-HateSpeech_Dataset.xlsx`
- `data/raw/Indo-HateSpeech/Readme.pdf`

Findings:

- Rows: 77,926.
- Labels:
  - `HS0` = No Hateful
  - `HS1` = Hateful
  - `HSN` = Extreme Hateful
- Raw label counts:
  - `HS0`: 64,194
  - `HS1`: 11,034
  - `HSN`: 2,698
- Missing comments: 1,360.
- All rows appear to come from Instagram comments across 31 post IDs.
- Median word count is 4, so many examples are very short/context-poor.
- Duplicate normalized comment rows: 20,288.
- Some sampled labels appear ambiguous, including examples marked `HS0` that still contain religiously charged or abusive language.

Decision:

- Do not add Indo-HateSpeech to the main experiment set before mixed training.
- Treat it as an accessible but noisy candidate for later secondary robustness work.
- Proceed with mixed training using the three already-audited primary datasets: `kaggle_hinglish_hate`, `cm_splits_codemixed`, and `thar_religion`.
