# Project Audit

Date: 2026-06-28

This audit was created after a two-pass check of the project folder, result files, and documentation. Its purpose is to make it easier to manually verify the research state before more experiments or paper writing.

## Pass 1: File And Result Presence

Checked that the main documentation, processed datasets, result files, and model folders exist.

Required documentation present:

- `README.md`
- `docs/research_journal.md`
- `docs/dataset_registry.md`
- `docs/model_registry.md`
- `docs/data_analysis_report.md`
- `docs/result_analysis_report.md`
- `docs/error_analysis_report.md`
- `docs/manual_error_analysis_report.md`
- `docs/project_defense_notes.md`
- `docs/dataset_taxonomy.md`
- `paper/paper_draft.md`

Required result files present:

- `results/cross_dataset_baseline_summary.csv`
- `results/transformer_cross_dataset_summary.csv`
- `results/transformer_cross_dataset_predictions.csv`
- `results/error_analysis/manual_error_annotation_first_pass.csv`

Dataset row checks:

| Dataset | Expected rows | Observed rows | Status |
|---|---:|---:|---|
| `kaggle_hinglish_hate` | 4,780 | 4,780 | pass |
| `cm_splits_codemixed` | 3,900 | 3,900 | pass |
| `thar_religion` | 11,549 | 11,549 | pass |
| `existing_79_row_benchmark` | 79 | 79 | diagnostic only |

Result-shape checks:

| File | Expected | Observed | Status |
|---|---:|---:|---|
| `results/result_analysis/primary_matched_transformer_results.csv` | 6 rows | 6 rows | pass |
| `results/transformer_cross_dataset_summary.csv` | 24 rows | 24 rows | pass |
| `results/cross_dataset_baseline_summary.csv` | 24 rows | 24 rows | pass |

The 79-row diagnostic probe is not present in `primary_matched_transformer_results.csv`, which is correct.

## Pass 2: Regenerated Analysis Outputs

The following scripts were rerun successfully:

- `scripts/analyze_datasets.py`
- `scripts/analyze_results.py`
- `scripts/analyze_errors.py`
- `scripts/first_pass_manual_error_coding.py`

The regenerated primary matched transformer results remain:

| Test dataset | Best model | Train dataset | Positive recall | Positive F1 | Macro F1 |
|---|---|---|---:|---:|---:|
| `kaggle_hinglish_hate` | mBERT | `kaggle_hinglish_hate` | 38.6% | 51.3% | 65.6% |
| `cm_splits_codemixed` | mBERT | `cm_splits_codemixed` | 68.7% | 71.4% | 78.3% |
| `thar_religion` | MuRIL | `thar_religion` | 80.3% | 77.4% | 77.9% |

The regenerated manual error coding summary remains:

| Code | Rows | Share |
|---|---:|---:|
| `cross_dataset_label_mismatch` | 191 | 67.0% |
| `generic_profanity_or_abuse` | 78 | 27.4% |
| `target_group_or_religion_cue` | 64 | 22.5% |
| `political_context_or_slogan` | 47 | 16.5% |
| `implicit_context_or_unclear_signal` | 37 | 13.0% |
| `non_hateful_lexical_trigger` | 27 | 9.5% |
| `short_or_contextless_text` | 26 | 9.1% |
| `mixed_script_complexity` | 9 | 3.2% |
| `script_mismatch_devanagari` | 8 | 2.8% |

## Issues Found And Fixed

- `paper_outline.md` still described THAR transformer evaluation as planned. It is now listed as completed.
- `paper_outline.md` used "Old saved checkpoints"; this has been changed to "initial saved project checkpoints."
- `paper/paper_draft.md` used earlier training-script metrics for matched Kaggle and CM tables. These tables now use the paper-facing cross-evaluation numbers from `docs/result_analysis_report.md`.
- `docs/evaluation_explanation.md` now calls the 79-row file a diagnostic probe instead of treating it as a normal benchmark.
- `paper_outline.md` now points to `docs/result_analysis_report.md` as the paper-facing result source. `results/summary.md` is still useful as a running project summary but contains earlier validation/diagnostic tables too.

## Remaining Caveats

- `results/summary.md`, `docs/research_journal.md`, and `docs/project_chronology.md` preserve chronological history. They may contain earlier terms such as "79-row benchmark" because they document what happened at the time. For paper writing, prefer `docs/result_analysis_report.md`, `docs/dataset_taxonomy.md`, and `docs/project_defense_notes.md`.
- Some source metadata still needs final review, especially the Kaggle dataset collection/annotation details and CM repository license/citation status.
- The first-pass manual error coding is a structured aid, not final human-ground-truth annotation.
- The project still needs mixed-dataset and leave-one-dataset-out experiments before the final paper can make stronger robustness claims.

## Paper-Facing Source Of Truth

Use these files first when writing or checking the paper:

- Dataset identity and caveats: `docs/dataset_registry.md`
- Dataset comparability: `docs/dataset_taxonomy.md`
- Main result interpretation: `docs/result_analysis_report.md`
- Error analysis: `docs/error_analysis_report.md`
- Manual qualitative coding: `docs/manual_error_analysis_report.md`
- Project explanation and viva notes: `docs/project_defense_notes.md`
- Timeline and journey: `docs/research_journal.md` and `docs/project_chronology.md`

