# Running the experiments

Obtain the source datasets and follow the [dataset registry](dataset_registry.md) before preparing local CSVs. Training does not automatically download the study datasets.

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
.venv/bin/python experiments/train_mac_mps.py --model mbert --train-csv data/processed/kaggle_hinglish_hate.csv --label-column label --output-dir Models/mbert__train-kaggle_hinglish_hate__seed42__e2
.venv/bin/python experiments/train_mac_mps.py --model muril --train-csv data/processed/kaggle_hinglish_hate.csv --label-column label --output-dir Models/muril__train-kaggle_hinglish_hate__seed42__e2
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
