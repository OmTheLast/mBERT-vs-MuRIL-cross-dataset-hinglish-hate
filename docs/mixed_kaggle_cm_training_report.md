# Mixed Kaggle+CM Training Report

Date: 2026-07-01

This report records the first mixed-dataset transformer experiment after the project moved from single-dataset comparison to cross-dataset robustness.

## Experiment Question

Does training on both `kaggle_hinglish_hate` and `cm_splits_codemixed` improve robustness compared with training on either dataset alone?

This mix was chosen first because both datasets are mostly Latin-script / Romanized Hindi-English social-media data, but their labels are not identical:

- `kaggle_hinglish_hate`: positive label means hate.
- `cm_splits_codemixed`: positive label means offensive or hate-adjacent content.

## Training Condition

| Field | Value |
|---|---|
| Mixed dataset ID | `mixed_kaggle_plus_cm` |
| Training file | `data/processed/mixed_train_kaggle_plus_cm__seed42.csv` |
| Training rows | 7,300 |
| Positive rows | 2,788 |
| Negative rows | 4,512 |
| Positive rate | 38.2% |
| Split/leakage policy | Kaggle stratified train split only; CM source train+val only |
| Held-out evaluations | Kaggle test split, CM source test split, THAR test split, 79-row diagnostic probe |
| Epochs | 2 |
| Seed | 42 |
| Max length | 128 |
| Learning rate | 2e-5 |

Local checkpoints:

- `Models/mbert__train-mixed_kaggle_plus_cm__seed42__e2`
- `Models/muril__train-mixed_kaggle_plus_cm__seed42__e2`

The model folders are ignored by Git because they contain large weights. The paper-facing summary file is:

```text
results/mixed_kaggle_plus_cm_transformer_summary.csv
```

## Results

| model | train_dataset | test_dataset | accuracy | recall_positive | f1_positive | f1_macro | tn | fp | fn | tp |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| mBERT | `mixed_kaggle_plus_cm` | `kaggle_hinglish_hate` | 72.9% | 45.3% | 56.6% | 68.5% | 528 | 55 | 204 | 169 |
| mBERT | `mixed_kaggle_plus_cm` | `cm_splits_codemixed` | 74.5% | 59.9% | 62.4% | 71.5% | 221 | 47 | 59 | 88 |
| mBERT | `mixed_kaggle_plus_cm` | `thar_religion` | 54.9% | 22.9% | 32.4% | 49.3% | 1018 | 201 | 841 | 250 |
| MuRIL | `mixed_kaggle_plus_cm` | `kaggle_hinglish_hate` | 61.0% | 0.0% | 0.0% | 37.9% | 583 | 0 | 373 | 0 |
| MuRIL | `mixed_kaggle_plus_cm` | `cm_splits_codemixed` | 64.6% | 0.0% | 0.0% | 39.2% | 268 | 0 | 147 | 0 |
| MuRIL | `mixed_kaggle_plus_cm` | `thar_religion` | 52.8% | 0.0% | 0.0% | 34.5% | 1219 | 0 | 1091 | 0 |

The 79-row diagnostic probe was also evaluated but remains excluded from primary conclusions.

## Interpretation

mBERT benefited from the Kaggle+CM mix on Kaggle evaluation compared with the earlier Kaggle-only mBERT result:

- Kaggle-only mBERT on Kaggle: Macro F1 65.6%, positive F1 51.3%, positive recall 38.6%.
- Kaggle+CM mBERT on Kaggle: Macro F1 68.5%, positive F1 56.6%, positive recall 45.3%.

However, the same mBERT mixed checkpoint was weaker on CM than the earlier CM-only mBERT checkpoint:

- CM-only mBERT on CM: Macro F1 78.3%, positive F1 71.4%, positive recall 68.7%.
- Kaggle+CM mBERT on CM: Macro F1 71.5%, positive F1 62.4%, positive recall 59.9%.

This means the mixed condition improved Kaggle coverage but diluted CM-specific performance. It did not solve THAR transfer:

- Kaggle+CM mBERT on THAR: Macro F1 49.3%, positive recall 22.9%.
- THAR remains a different dataset situation because the positive label is targeted religious hate, not general hate/offense.

MuRIL collapsed to all-negative predictions in this condition. Across Kaggle, CM, and THAR, MuRIL produced zero true positives and zero false positives. This is not a universal claim about MuRIL, because MuRIL performed well in the earlier THAR-only and CM-only experiments. The safer interpretation is:

> Under the current two-epoch, seed-42 Kaggle+CM mixed training condition, MuRIL learned an overly conservative decision boundary and failed to identify the positive class.

This needs follow-up before the final paper:

- check at least two additional seeds;
- inspect validation logits/probabilities to see whether positives are near the threshold or fully separated as negative;
- consider class weighting or threshold tuning;
- compare with a THAR-including mix to see whether MuRIL needs a more Indian-context / targeted-hate signal to remain useful.

## Paper Use

This result should be used as an early mixed-training finding, not as a final conclusion. The current paper claim becomes more precise:

> Mixed training can improve one dataset situation while hurting another, and model behavior differs sharply by base model. Simply adding more code-mixed data does not automatically create a robust hate-speech detector.

