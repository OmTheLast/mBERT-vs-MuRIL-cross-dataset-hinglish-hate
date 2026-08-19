# Project Reference Summary

Date: 2026-08-19

Use this as the first reference page before meetings, paper writing, or project defense. It summarizes what has been done, where the detailed evidence lives, and what the main results currently mean.

## Current Project Claim

The project compares mBERT and MuRIL for Hinglish and Hindi-English code-mixed harmful speech detection. The main finding is conditional rather than universal: mBERT is stronger on the matched Kaggle Hinglish hate and CM code-mixed/offensive settings, while MuRIL is stronger on the matched THAR targeted religious-hate setting. Cross-dataset and mixed-training results show that label definition, platform, topic, and script mix strongly affect model behavior.

## Primary Datasets

| Dataset ID | Source situation | Positive label meaning | Main caveat |
|---|---|---|---|
| `kaggle_hinglish_hate` | Hinglish subset prepared from Shardul Dhekane's Kaggle code-mixed Hinglish hate dataset | hate | Main source file is multilingual; the controlled project file uses the Hinglish subset. |
| `cm_splits_codemixed` | Hindi-English code-mixed political/social media dataset | offensive/hate-adjacent | Positive label is offense, not exactly strict hate speech. |
| `thar_religion` | THAR targeted religious hate dataset | AntiReligion / targeted religious hate | Narrower and more topic-specific than general Hinglish hate. |

The 79-row benchmark is kept only as a diagnostic probe. Its provenance is uncertain, and it should not support final model-superiority claims.

## Key Matched Multi-Seed Results

These are the strongest matched-condition results because they use three random seeds: `7`, `13`, and `42`.

| Dataset | Better model | mBERT Macro F1 | MuRIL Macro F1 | Interpretation |
|---|---|---:|---:|---|
| `kaggle_hinglish_hate` | mBERT | 67.5% +/- 2.1% | 58.1% +/- 5.7% | mBERT has a clear matched advantage; MuRIL is more hesitant on positives. |
| `cm_splits_codemixed` | mBERT, narrowly | 77.7% +/- 1.9% | 76.1% +/- 2.3% | Both models are competitive; mBERT is slightly stronger and more stable on positive recall. |
| `thar_religion` | MuRIL | 74.7% +/- 0.1% | 76.5% +/- 1.3% | MuRIL wins this targeted religious-hate setting across all three seeds. |

Important defense point: THAR seed 42 made MuRIL look especially strong, but the three-seed mean shows a smaller and more honest advantage. That is exactly why multi-seed testing matters.

## Main Behavioral Findings

- mBERT is currently stronger on Latin-script-heavy or broader Hinglish/offensive matched settings.
- MuRIL is currently stronger on THAR targeted religious hate, where the task is closer to Indian-language and religious-target cues.
- MuRIL often shows lower positive recall on Kaggle and less stable positive recall on CM, meaning it misses more positive examples in those settings.
- Cross-dataset transfer is weak: a model trained on one dataset often performs much worse on another because the positive label and domain change.
- TF-IDF baselines can be strong because hate/offensive datasets often contain repeated keywords, slogans, target terms, and platform-specific lexical cues.
- The early saved project checkpoints looked collapsed on the 79-row probe because their training context and label meaning likely did not match that probe, and the probe itself is noisy.

## Where To Find Details

| Need | File |
|---|---|
| Dataset identities, citations, caveats | `docs/dataset_registry.md` |
| Dataset situation comparison | `docs/dataset_taxonomy.md` |
| Descriptive data analysis | `docs/data_analysis_report.md` |
| Overall result interpretation | `docs/result_analysis_report.md` |
| Multi-seed matched tables | `docs/matched_multiseed_results.md` |
| Quantitative error analysis | `docs/error_analysis_report.md` |
| Manual error examples and categories | `docs/manual_error_analysis_report.md` |
| Viva/project defense explanations | `docs/project_defense_notes.md` |
| Full chronological project journal | `docs/research_journal.md` |
| Current rigor gaps and next work | `docs/research_rigor_roadmap.md` |

## What To Say If Asked For The Core Evidence

The strongest evidence is the matched multi-seed table plus the cross-dataset result tables. The matched multi-seed results show that the model winner changes by dataset: mBERT wins Kaggle and narrowly wins CM, while MuRIL wins THAR. The cross-dataset results show that models do not generalize cleanly across datasets, which means the dataset situation is part of the task, not just background information.

## Current Next Steps

1. Add the same multi-seed rigor to the most important mixed-training condition if disk space allows.
2. Expand manual error analysis with clear anonymized examples.
3. Update the paper draft so matched multi-seed results replace older one-seed claims.
4. Verify dataset licenses/citations before public final release.
5. Keep pushing significant research updates to GitHub in chronological commits.
