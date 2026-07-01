# Model Registry

Last updated: 2026-06-25

This file explains the local checkpoint folders under `Models/`. It is meant to prevent ambiguous names once the project starts training on multiple datasets.

## Current Local Checkpoints

| Folder | Base model | Training data | Session role | Paper use |
|---|---|---|---|---|
| `Models/mbert_model` | `bert-base-multilingual-cased` | Initial saved project checkpoint | Diagnostic/context checkpoint | Use only when discussing initial project behavior. Do not treat as a fresh controlled run. |
| `Models/muril_model` | `google/muril-base-cased` | Initial saved project checkpoint | Diagnostic/context checkpoint | Use only when discussing initial project behavior. Do not treat as a fresh controlled run. |
| `Models/smoke_mbert_model` | `bert-base-multilingual-cased` | Small 256-row sample from `kaggle_hinglish_hate` | Pipeline smoke test | Do not use as a research result. This only proves the training script can run end-to-end. |
| `Models/mbert__train-kaggle_hinglish_hate__seed42__e2` | `bert-base-multilingual-cased` | `data/processed/kaggle_hinglish_hate.csv` | Controlled mBERT Kaggle Hinglish hate run | Usable as a session result. Primary paper use should rely on source-backed datasets, not the 79-row diagnostic probe. |
| `Models/muril__train-kaggle_hinglish_hate__seed42__e2` | `google/muril-base-cased` | `data/processed/kaggle_hinglish_hate.csv` | Controlled MuRIL Kaggle Hinglish hate run | Usable as a session result. Primary paper use should rely on source-backed datasets, not the 79-row diagnostic probe. |
| `Models/mbert__train-cm_splits_codemixed__seed42__e2` | `bert-base-multilingual-cased` | `data/processed/cm_splits_codemixed.csv` using train+val for training and source test for evaluation | Controlled mBERT run on Indian politics code-mixed offensive/hate-adjacent data | Usable as a session result. Remember that the positive label means offensive, not strict hate. |
| `Models/muril__train-cm_splits_codemixed__seed42__e2` | `google/muril-base-cased` | `data/processed/cm_splits_codemixed.csv` using train+val for training and source test for evaluation | Controlled MuRIL run on Indian politics code-mixed offensive/hate-adjacent data | Usable as a session result. Remember that the positive label means offensive, not strict hate. |
| `Models/mbert__train-thar_religion__seed42__e2` | `bert-base-multilingual-cased` | `data/processed/thar_religion.csv` | Controlled mBERT run on targeted religious hate data | Usable as a session result. Remember that the positive label is AntiReligion, not general hate. |
| `Models/muril__train-thar_religion__seed42__e2` | `google/muril-base-cased` | `data/processed/thar_religion.csv` | Controlled MuRIL run on targeted religious hate data | Usable as a session result. Remember that the positive label is AntiReligion, not general hate. |

## Naming Rule For Future Checkpoints

Use dataset-aware names:

```text
Models/{model}__train-{dataset_id}__seed{seed}__e{epochs}
```

Examples:

```text
Models/mbert__train-kaggle_hinglish_hate__seed42__e2
Models/muril__train-thar_religion__seed42__e2
Models/mbert__train-cm_splits_codemixed__seed42__e2
```

If a checkpoint is trained on multiple datasets, use:

```text
Models/{model}__train-mixed-{short_dataset_ids}__seed{seed}__e{epochs}
```

Example:

```text
Models/muril__train-mixed-kaggle-thar-cm__seed42__e2
```

## Required Metadata For Every New Checkpoint

Every trained checkpoint should save or be documented with:

- Base model name.
- Training dataset ID.
- Evaluation dataset ID or split.
- Cleaning mode.
- Train/validation/test split policy.
- Random seed.
- Epochs.
- Batch size.
- Learning rate.
- Device used.
- Result file path.
- Known caveats.

The dataset ID must match `docs/dataset_registry.md`.

## GitHub Handling

Model weights are large and are ignored by `.gitignore`. The GitHub repository should usually contain code, documentation, dataset conversion scripts, result summaries, and lightweight metadata. If trained weights need to be shared later, use Git LFS or a model host such as Hugging Face and link the model card from this registry.
