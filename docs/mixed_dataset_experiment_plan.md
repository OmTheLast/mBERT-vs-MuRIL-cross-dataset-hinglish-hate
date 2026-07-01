# Mixed-Dataset Experiment Plan

Date: 2026-07-01

## Why This Comes Next

Mixed-dataset evaluation should happen before broad hyperparameter sweeps.

Reason:

- Mixed training tests the central research question: can mBERT or MuRIL become more robust when trained on multiple dataset situations?
- Hyperparameter sweeps multiply the experiment grid and can make the project harder to interpret before we know whether mixed training helps.
- Seeds and confidence intervals are still necessary later, but mixed training gives the next major result family.

## Key Leakage Rule

Mixed training must not train on rows that later appear in evaluation.

Current rule:

- For `kaggle_hinglish_hate`, use only the stratified training portion with seed 42.
- For `thar_religion`, use only the stratified training portion with seed 42.
- For `cm_splits_codemixed`, use source `train` + `val`, and keep source `test` for evaluation.

The builder script is:

```bash
.venv/bin/python scripts/build_mixed_training_sets.py
```

It creates local ignored CSVs under `data/processed/` and a lightweight summary under:

```text
results/mixed_training_set_summary.csv
```

## Mixed Training Sets

Planned mixed training datasets:

| Mix ID | Sources | Purpose |
|---|---|---|
| `kaggle_plus_cm` | Kaggle + CM | Broad Latin/code-mixed harmful/offensive training |
| `kaggle_plus_thar` | Kaggle + THAR | Broad Hinglish hate plus targeted religious hate |
| `cm_plus_thar` | CM + THAR | Indian political/offensive plus targeted religious hate |
| `all_three` | Kaggle + CM + THAR | Broadest current training condition |

## Checkpoint Naming

Use:

```text
Models/{model}__train-mixed_{mix_id}__seed42__e2
```

Examples:

```text
Models/mbert__train-mixed_all_three__seed42__e2
Models/muril__train-mixed_all_three__seed42__e2
```

## Training Commands

Example:

```bash
.venv/bin/python experiments/train_mac_mps.py \
  --model mbert \
  --train-csv data/processed/mixed_train_all_three__seed42.csv \
  --label-column label \
  --output-dir Models/mbert__train-mixed_all_three__seed42__e2
```

Repeat for:

- model: `mbert`, `muril`;
- mix: `kaggle_plus_cm`, `kaggle_plus_thar`, `cm_plus_thar`, `all_three`.

That gives 8 new controlled mixed checkpoints.

## Evaluation Plan

After training, evaluate each mixed checkpoint on:

- `kaggle_hinglish_hate`;
- `cm_splits_codemixed`;
- `thar_religion`;
- optionally the 79-row diagnostic probe, but only as diagnostic context.

The paper-facing comparison should answer:

- Does mixed training improve average Macro F1 across datasets?
- Does mixed training improve the weakest transfer directions?
- Does mixed training reduce false negatives on THAR?
- Does mixed training hurt matched in-domain performance?
- Does mBERT or MuRIL benefit more from mixed training?

## Expected Interpretations To Watch For

Possible good result:

- Mixed training improves cross-dataset Macro F1 without heavily reducing matched performance.

Possible warning result:

- Mixed training improves one dataset but hurts another, meaning label definitions may be incompatible.

Possible model-specific result:

- MuRIL may benefit more from mixes involving THAR.
- mBERT may remain stronger when the mixed data is mostly Latin-script and offense/hate-adjacent.

## How This Fits The Paper

This becomes the next major section after current cross-dataset transfer:

> Mixed-dataset training tests whether the cross-dataset weakness is caused by narrow training exposure or by deeper incompatibility between dataset label definitions.

If mixed training works, the paper can claim a path toward robustness.

If mixed training fails or is inconsistent, the paper can claim that label-policy mismatch is a deeper barrier than simply adding more data.
