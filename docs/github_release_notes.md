# GitHub Release Notes

Date: 2026-07-01

This note describes how the repository should be presented on GitHub.

## Repository Direction

Current aim:

> Cross-dataset evaluation of mBERT and MuRIL for Hinglish and Hindi-English code-mixed harmful speech detection.

Legacy/original aim:

> A direct mBERT-vs-MuRIL comparison for Hinglish hate speech detection.

The original aim is preserved in `docs/legacy_original_aim.md`. It should be described as the starting point that led to the broader cross-dataset research question.

## What Should Be Pushed

Push:

- code in `scripts/`, `experiments/`, and `Training/`;
- documentation in `docs/`;
- paper draft files under `paper/`;
- the current lightweight PDF draft under `output/pdf/` when intentionally refreshed;
- lightweight result summaries and generated figures under `results/`;
- `README.md`, `requirements.txt`, `.gitignore`.

Do not push:

- raw datasets;
- processed datasets containing third-party text;
- model weights/checkpoints;
- virtual environments;
- training run folders;
- large prediction dumps;
- downloaded source PDFs or local dataset PDFs.

These are ignored in `.gitignore`.

## Paper-Facing Source Of Truth

For final writing, prefer:

- `docs/dataset_registry.md`
- `docs/dataset_taxonomy.md`
- `docs/result_analysis_report.md`
- `docs/error_analysis_report.md`
- `docs/manual_error_analysis_report.md`
- `docs/project_defense_notes.md`

Use `docs/research_journal.md` and `docs/project_chronology.md` for timeline and journey, not as final result tables.

## Suggested Repository Description

Cross-dataset evaluation of mBERT and MuRIL for Hinglish/Hindi-English code-mixed harmful speech detection.

## Suggested First Commit Message

```text
Initial cross-dataset mBERT vs MuRIL research scaffold
```

## Ongoing Commit Policy

From 2026-07-01 onward, significant research updates should be committed and pushed in sequence.

Commit after:

- a new experiment family;
- a new dataset conversion or dataset decision;
- a new paper draft version;
- a new result analysis or graph set;
- a meaningful reproducibility or defense-documentation update.

Commit messages should describe the research step, not only the file edit.
