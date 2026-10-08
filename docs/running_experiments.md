# Running the experiments

Obtain the source datasets and follow the [dataset registry](dataset_registry.md) before preparing local CSVs. Training does not automatically download the study datasets.

## Setup

```bash
python -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt
```

## Common Commands

## Reproduce The Headline Three-Seed Comparison

Run all commands from the repository root. Obtain the datasets from the cited
sources in `dataset_registry.md`; local access does not establish redistribution
permission. Place the Kaggle CSV at `combined_hate_speech_dataset.csv` (columns
`text`, `hate_label`, `language`; Hinglish rows selected by the preparation
script). Place the CM repository at `data/raw/cm-hate-speech-detection/`, including
`data/filled_10k.csv` and `data/splits/{train,val,test}.csv`. Place THAR's
`THAR-Dataset.csv` at `data/raw/THAR/THAR-Dataset.csv`.

```bash
.venv/bin/python scripts/prepare_kaggle_hinglish_dataset.py
.venv/bin/python scripts/convert_cm_hate_speech.py
.venv/bin/python scripts/convert_thar.py
```

Expected processed row counts: Kaggle 4,780; CM 3,900; THAR 11,549. These
commands require the source versions used in the study; upstream changes can
change the results. Check row counts and the dataset registry before training.
The following commands launch 18 expensive training jobs. They are instructions,
not jobs executed during the manuscript audit. Use a fresh output directory
and sufficient disk space; keep any existing checkpoint directories intact.

```bash
for dataset in kaggle_hinglish_hate cm_splits_codemixed thar_religion; do
  for model in mbert muril; do
    for seed in 7 13 42; do
      split_flags=()
      if [ "$dataset" = cm_splits_codemixed ]; then
        split_flags=(--split-column split --train-split train --train-split val --eval-split test)
      fi
      .venv/bin/python experiments/train_mac_mps.py \
        --model "$model" --train-csv "data/processed/$dataset.csv" \
        --text-column text --label-column label --seed "$seed" \
        --epochs 2 --max-length 128 --batch-size 8 --learning-rate 2e-5 \
        --weight-decay 0.01 --cleaning minimal --test-size 0.2 \
        "${split_flags[@]}" \
        --output-dir "Models/${model}__train-${dataset}__seed${seed}__e2"
    done
  done
done
.venv/bin/python scripts/aggregate_matched_multiseed.py \
  --datasets kaggle_hinglish_hate cm_splits_codemixed thar_religion \
  --models mbert muril --seeds 7 13 42 --epochs 2
```

The loop uses Bash/zsh arrays. CM must use those source-split flags to reproduce
the headline condition: train+val = 3,476 rows, test = 424. Kaggle uses 3,824/956
training/evaluation rows; THAR uses 9,239/2,310. The latter two splits vary by seed.
All reported evaluation sets also select the best epoch. Reproduction on other
hardware/package versions may differ numerically. The aggregator reads saved
checkpoint metrics and produces the per-seed CSV, summary CSV, report and graph;
it does not retrain or perform an independent final test.

To rebuild only the paper exports from the saved results and authoritative text:

```bash
.venv/bin/python -m pip install -r paper/requirements.txt
.venv/bin/python paper/build_manuscript.py
```

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
