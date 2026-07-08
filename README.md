# Cross-Dataset Hinglish Hate Speech Research

This project studies how mBERT and MuRIL behave on Hinglish and Hindi-English code-mixed hate/offensive speech detection. The original comparison was a single-dataset mBERT-vs-MuRIL setup; the current research direction is broader: evaluate whether a general multilingual model or an Indian-language-focused model generalizes better across different Indian-context datasets, label definitions, scripts, and platforms.

The original single-dataset aim is preserved as legacy context in `docs/legacy_original_aim.md`.

## Research Question

Does Indian-language-specific pretraining in MuRIL improve hate/offensive speech detection for Hinglish and Hindi-English code-mixed text compared with general multilingual pretraining in mBERT?

The current working hypothesis is that the answer may depend strongly on dataset situation:

- mBERT may do better on noisy Romanized Hinglish because much social media Hinglish uses Latin script and English-like subword patterns.
- MuRIL may do better on Indian-language-heavy or Devanagari-heavy material, especially targeted hate categories.
- The apparent winner can change when the evaluation dataset, label policy, or platform changes.

## Project Map

The clean maintained project map is `docs/project_map.md`. A shortened map is included here for quick orientation.

```text
Hinglish Research/
├── combined_hate_speech_dataset.csv      # Existing combined dataset file
├── benchmark_test.csv                    # Existing 79-row sanity benchmark
├── data/
│   ├── raw/                              # Local raw/cloned datasets; ignored by Git
│   ├── processed/                        # Standardized CSVs; ignored by Git
│   └── README.md                         # Dataset storage notes
├── docs/
│   ├── dataset_registry.md               # Dataset identity, labels, caveats, citation status
│   ├── dataset_acquisition_log.md         # What was downloaded, blocked, or context-only
│   ├── model_registry.md                 # Local checkpoint meanings and naming rules
│   ├── result_reporting_protocol.md      # Required labels for every result
│   ├── baseline_experiment_report.md     # Research-style report for TF-IDF baselines
│   ├── data_analysis_report.md           # Dataset integrity and descriptive analysis
│   ├── dataset_taxonomy.md               # Dataset situation and label comparability notes
│   ├── error_analysis_report.md          # Transformer error/disagreement analysis
│   ├── manual_error_analysis_report.md   # First-pass qualitative coding of sampled errors
│   ├── project_defense_notes.md          # Plain-language ML/research explanation and viva notes
│   ├── project_audit_2026-06-28.md       # Two-pass consistency audit and manual-check guide
│   ├── model_reload_check_2026-06-29.md  # Saved-checkpoint reload and test-script verification
│   ├── legacy_original_aim.md            # Original mBERT-vs-MuRIL aim preserved as context
│   ├── github_release_notes.md           # GitHub publishing scope and repository direction
│   ├── project_map.md                    # Clean maintained project map and commit policy
│   ├── research_rigor_roadmap.md         # What must be added before final paper strength
│   ├── mixed_dataset_experiment_plan.md  # Mixed training plan and leakage policy
│   ├── result_analysis_report.md         # Primary result interpretation and model comparisons
│   ├── transformer_cross_dataset_eval_report.md # Research-style report for transformer cross-dataset evaluation
│   ├── research_journal.md               # Running research notes
│   ├── project_chronology.md             # Timeline for paper writing
│   ├── experiment_plan.md                # Planned experiment matrix
│   └── evaluation_explanation.md         # Plain-language metric explanations
├── experiments/
│   ├── train_transformer.py              # Shared mBERT/MuRIL fine-tuning runner
│   ├── train_mac_mps.py                  # Apple Silicon/MPS wrapper
│   ├── train_colab_cuda.py               # Colab/CUDA wrapper
│   ├── train_cpu_debug.py                # CPU/smoke-test wrapper
│   ├── run_model_harness.py              # Quick CSV/text harness for registered mBERT/MuRIL checkpoints
│   ├── run_benchmark.py                  # Local checkpoint evaluation
│   └── run_baselines.py                  # TF-IDF baseline models
├── scripts/
│   ├── audit_dataset.py                  # Dataset audit utility
│   ├── prepare_kaggle_hinglish_dataset.py # Standardize/split Kaggle Hinglish source
│   ├── convert_cm_hate_speech.py         # Convert CM hate/offensive dataset
│   ├── convert_thar.py                   # Convert THAR religious hate dataset
│   ├── analyze_datasets.py               # Source integrity checks and descriptive analysis
│   ├── analyze_errors.py                 # Transformer error and disagreement analysis
│   ├── build_mixed_training_sets.py      # Build leakage-safe mixed training CSVs
│   ├── analyze_results.py                # Primary result analysis and diagnostic probe separation
│   └── make_results_summary.py           # Terminal and Markdown result summary
├── results/                              # CSV/Markdown result summaries
├── Models/                               # Local checkpoints; large weights ignored by Git
├── paper/
│   ├── build_paper_pdf.py                # Reproducible local PDF paper builder
│   ├── paper_draft.md                    # Main working paper draft
│   ├── main.tex                          # LaTeX draft source
│   ├── references.bib                    # BibTeX references
│   └── overleaf_self_contained.tex       # Copy-paste Overleaf fallback
├── output/
│   └── pdf/
│       └── hinglish_mbert_muril_research_paper_draft.pdf
└── paper_outline.md                      # Paper skeleton
```

## Datasets

The dataset registry is the source of truth: `docs/dataset_registry.md`.

Currently standardized datasets include:

| Dataset ID | Local processed file | Situation | Label meaning |
|---|---|---|---|
| `kaggle_hinglish_hate` | `data/processed/kaggle_hinglish_hate.csv` | Shardul Dhekane Kaggle Code-Mixed Hinglish Hate Speech Detection dataset, controlled Hinglish subset | `0 = non-hate`, `1 = hate` |
| `existing_79_row_benchmark` | `benchmark_test.csv` | Small sanity benchmark, label-noisy | `0 = non-hate`, `1 = hate` |
| `cm_splits_codemixed` | `data/processed/cm_splits_codemixed.csv` | Indian politics Hindi-English code-mixed Twitter/X data | mapped from source `offense`; hate-adjacent |
| `thar_religion` | `data/processed/thar_religion.csv` | Hindi-English code-mixed targeted religious hate YouTube comments | `0 = Non-AntiReligion`, `1 = AntiReligion` |

Raw and processed external datasets are local. They are not silently downloaded during training.

The current dataset integrity and descriptive analysis report is `docs/data_analysis_report.md`.

## Models

The model registry is the source of truth: `docs/model_registry.md`.

Current local checkpoint folders:

| Folder | Meaning |
|---|---|
| `Models/mbert_model` | Existing saved mBERT checkpoint present at the start of this session |
| `Models/muril_model` | Existing saved MuRIL checkpoint present at the start of this session |
| `Models/mbert__train-kaggle_hinglish_hate__seed42__e2` | mBERT trained during this session on `kaggle_hinglish_hate` |
| `Models/muril__train-kaggle_hinglish_hate__seed42__e2` | MuRIL trained during this session on `kaggle_hinglish_hate` |
| `Models/mbert__train-cm_splits_codemixed__seed42__e2` | mBERT trained during this session on `cm_splits_codemixed` |
| `Models/muril__train-cm_splits_codemixed__seed42__e2` | MuRIL trained during this session on `cm_splits_codemixed` |
| `Models/mbert__train-thar_religion__seed42__e2` | mBERT trained during this session on `thar_religion` |
| `Models/muril__train-thar_religion__seed42__e2` | MuRIL trained during this session on `thar_religion` |
| `Models/smoke_mbert_model` | Small pipeline smoke test; not a paper result |

Future checkpoints should use dataset-aware names:

```text
Models/{model}__train-{dataset_id}__seed{seed}__e{epochs}
```

Example:

```text
Models/muril__train-thar_religion__seed42__e2
```

## Setup

```bash
python -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt
```

## Common Commands

Audit datasets:

```bash
.venv/bin/python scripts/audit_dataset.py data/processed/kaggle_hinglish_hate.csv --text-column text --label-column label
.venv/bin/python scripts/audit_dataset.py data/processed/cm_splits_codemixed.csv --text-column text --label-column label
.venv/bin/python scripts/audit_dataset.py data/processed/thar_religion.csv --text-column text --label-column label
```

Prepare or convert datasets:

```bash
.venv/bin/python scripts/prepare_kaggle_hinglish_dataset.py
.venv/bin/python scripts/convert_cm_hate_speech.py
.venv/bin/python scripts/convert_thar.py
```

Analyze registered datasets:

```bash
.venv/bin/python scripts/analyze_datasets.py
```

Analyze saved results:

```bash
.venv/bin/python scripts/analyze_results.py
```

Analyze transformer errors:

```bash
.venv/bin/python scripts/analyze_errors.py
.venv/bin/python scripts/first_pass_manual_error_coding.py
```

Build mixed training sets:

```bash
.venv/bin/python scripts/build_mixed_training_sets.py
```

Train on Apple Silicon/MPS:

```bash
.venv/bin/python experiments/train_mac_mps.py --model mbert --train-csv data/processed/kaggle_hinglish_hate.csv --output-dir Models/mbert__train-kaggle_hinglish_hate__seed42__e2
.venv/bin/python experiments/train_mac_mps.py --model muril --train-csv data/processed/kaggle_hinglish_hate.csv --output-dir Models/muril__train-kaggle_hinglish_hate__seed42__e2
```

Run benchmark and baselines:

```bash
.venv/bin/python experiments/run_benchmark.py --input benchmark_test.csv --evaluation-name benchmark_test_79 --dataset-name existing_79_row_benchmark --condition ad_hoc
.venv/bin/python experiments/run_baselines.py
.venv/bin/python scripts/make_results_summary.py
```

Run the transformer harness:

```bash
.venv/bin/python experiments/run_model_harness.py --list-models
.venv/bin/python experiments/run_model_harness.py --model-key all --input-csv benchmark_test.csv --output results/harness_benchmark_predictions.csv --summary-output results/harness_benchmark_summary.csv
.venv/bin/python experiments/run_model_harness.py --model-key mbert_kaggle_hinglish_hate --model-key muril_kaggle_hinglish_hate --text "sample Hinglish text here"
```

## Results So Far

The current paper-facing analysis is `docs/result_analysis_report.md`. `results/summary.md` is a running project summary and includes earlier validation/diagnostic tables.

Important current interpretation:

- The initial saved project checkpoints were strongly biased toward predicting non-hate on the 79-row diagnostic probe.
- Retraining on `kaggle_hinglish_hate` improved hate detection.
- mBERT performed better than MuRIL on the held-out split from `kaggle_hinglish_hate`.
- The 79-row diagnostic probe is excluded from primary conclusions because its provenance is uncertain.
- mBERT performed better on the matched `cm_splits_codemixed` condition, while MuRIL transferred better from CM to `thar_religion`.
- MuRIL performed better on the matched `thar_religion` condition and on THAR-to-CM transfer.
- These contradictions are not noise to ignore; they are evidence that dataset definition, label policy, and evaluation domain are central to the research question.

## GitHub Notes

Large model weights and local datasets are ignored by `.gitignore`. The repository should publish code, documentation, conversion scripts, result summaries, and lightweight metadata. If trained weights are shared later, use Git LFS or a model host such as Hugging Face.

From 2026-07-01 onward, significant project updates should be committed and pushed in order. The detailed commit policy is in `docs/project_map.md`.

Current research rigor roadmap: `docs/research_rigor_roadmap.md`.

## Licensing
* **Source Code & Scripts**: This project's code is licensed under the [MIT License](LICENSE).
* **Research Paper & Text Documentation**: The textual content of the research paper and documentation in this repository is licensed under the [Creative Commons Attribution 4.0 International License (CC-BY-4.0)](https://creativecommons.org).
