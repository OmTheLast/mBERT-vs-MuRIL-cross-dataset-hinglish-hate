# One-Page Research Summary

Working Paper Draft v0.3: 2026-08-27

## Project Question

Does Indian-language-specific pretraining in MuRIL make it more effective than general multilingual mBERT for Hinglish and Hindi-English code-mixed harmful-speech detection?

Current answer: not universally. Model ranking depends on dataset situation. mBERT performs better on matched Kaggle Hinglish hate and CM code-mixed/offensive settings, while MuRIL performs better on THAR targeted religious hate.

## Datasets

| Dataset | Rows | Positive label | Situation |
|---|---:|---|---|
| `kaggle_hinglish_hate` | 4,780 | hate | Kaggle Hinglish subset; 100% Latin script in the processed file |
| `cm_splits_codemixed` | 3,900 | offensive | Indian politics / Twitter/X code-mixed content; hate-adjacent |
| `thar_religion` | 11,549 | AntiReligion | YouTube targeted religious hate against religious groups |

The 79-row benchmark is excluded from primary conclusions because its provenance is uncertain and it may be manually written or AI-generated.

## Methods

- Fine-tuned mBERT and MuRIL as binary classifiers.
- Evaluated matched training/testing, cross-dataset transfer, TF-IDF baselines, and mixed-dataset training.
- Primary metric: Macro F1, because accuracy can hide majority-class behavior.
- Positive recall is tracked because false negatives are missed harmful examples.

## Strongest Current Evidence

Matched multi-seed results use seeds `7`, `13`, and `42`.

| Dataset | Better model | mBERT Macro F1 | MuRIL Macro F1 | Interpretation |
|---|---|---:|---:|---|
| Kaggle Hinglish Hate | mBERT | 67.5 +/- 2.1 | 58.1 +/- 5.7 | mBERT clear win; MuRIL misses many positives |
| CM Code-mixed | mBERT, narrow | 77.7 +/- 1.9 | 76.1 +/- 2.3 | Both competitive; labels are offense-like |
| THAR Religion | MuRIL | 74.7 +/- 0.1 | 76.5 +/- 1.3 | MuRIL wins targeted religious hate |

## Main Claim

The project's strongest claim is conditional: dataset label definition, platform, topic, script mix, and train/test match affect which model performs better. Cross-dataset robustness is weak, and this weakness is itself a core finding.

## Limitations

- Mixed-dataset and cross-dataset transformer results are mostly single-seed evidence.
- Hate, offensive, and AntiReligion labels are related but not interchangeable.
- Dataset citation and license metadata still need final verification.
- Manual error analysis needs more polished, anonymized examples before final sharing.
- Hyperparameters were controlled rather than extensively tuned.

## Feedback Requested

[OM VERIFY] Before sending to professors, ask for feedback on whether the conditional claim is clear, whether the dataset caveats are acceptable, and which experiment should receive the next multi-seed repeat: mixed all-three training, Kaggle+THAR, CM+THAR, or a selected cross-dataset transfer pair.

