# Legacy Original Aim

Date: 2026-07-01

This note preserves the original project aim while making clear that the current repository direction has changed.

## Original Aim

The project began as a direct comparison:

> Is mBERT better than MuRIL for Hinglish hate speech detection, or does MuRIL's Indian-language-focused pretraining help more?

In that framing, the main intended dataset was a Hinglish hate-speech dataset, and the expected output was a single mBERT-vs-MuRIL comparison.

## Why The Aim Changed

After auditing datasets and running experiments, the project showed that a simple model-vs-model answer is not stable. The apparent winner changes when the dataset changes.

Important examples:

- mBERT performs better on matched `kaggle_hinglish_hate`.
- mBERT performs better on matched `cm_splits_codemixed`.
- MuRIL performs better on matched `thar_religion`.
- MuRIL transfers better between CM and THAR in both directions.
- Cross-dataset transfer is weak overall.

This means the stronger research direction is not merely "which model wins?" but:

> How do mBERT and MuRIL behave across different Hinglish/Hindi-English code-mixed harmful-speech dataset situations?

## Current Aim

The current project aim is:

> Cross-dataset evaluation of mBERT and MuRIL for Hinglish and Hindi-English code-mixed harmful speech detection.

This includes hate speech, offensive/hate-adjacent labels, and targeted religious hate, while clearly documenting that these labels are not semantically identical.

## Paper-Writing Guidance

Use the original aim as historical motivation in the introduction, but do not frame the final paper as a single-dataset contest.

Recommended wording:

> The project began with a direct mBERT-vs-MuRIL comparison for Hinglish hate speech detection. However, experiments across multiple datasets showed that model rankings depend on dataset definition, label policy, script, platform, and target domain. Therefore, this work reframes the comparison as a cross-dataset robustness study.

Avoid implying that the original aim was wrong. It was the starting question that led to the broader research finding.

