# Research Rigor Roadmap

Date: 2026-08-25

This file tracks what is strong in the project right now, what is still weak, and what must be added before the work is treated as a final research paper.

## Current Strengths

- The project has moved beyond a single mBERT-vs-MuRIL score and now tests cross-dataset behavior.
- Three source-backed dataset situations are documented and separated:
  - `kaggle_hinglish_hate`
  - `cm_splits_codemixed`
  - `thar_religion`
- The paper-facing results are labeled by model, train dataset, test dataset, and metric.
- The 79-row diagnostic probe has been excluded from primary claims because its provenance is uncertain.
- TF-IDF baselines are included, which prevents overclaiming transformer superiority.
- Dataset analysis, result analysis, and error analysis are separately documented.
- Matched multi-seed transformer results are completed for the three primary matched settings using seeds `7`, `13`, and `42`.
- Mixed-dataset training is completed for Kaggle+CM, Kaggle+THAR, CM+THAR, and all three datasets, with each mixed checkpoint evaluated separately on Kaggle, CM, and THAR.

## Main Weakness Right Now

The main weakness is not page count. It is remaining research rigor.

Matched single-dataset results now have three-seed coverage. Mixed-dataset and cross-dataset conclusions still rely mostly on one seed per condition.

Current transformer controls still use:

- one epoch setting: `2` epochs;
- one maximum sequence length: `128`;
- one learning rate: `2e-5`;
- limited hyperparameter search;
- single-seed mixed-training and transfer results.

This is acceptable for an application research draft, but not enough for a final strong paper conclusion.

## Required Before Final Paper

### 1. Multi-Seed Runs

Status: completed for the main matched settings.

Completed seeds:

- seed `7`;
- seed `13`;
- seed `42`.

Completed conditions:

- mBERT and MuRIL on `kaggle_hinglish_hate`;
- mBERT and MuRIL on `cm_splits_codemixed`;
- mBERT and MuRIL on `thar_religion`.

Reported in `docs/matched_multiseed_results.md`:

- mean Macro F1;
- standard deviation Macro F1;
- mean positive F1;
- standard deviation positive F1.

Remaining seed work:

- run multi-seed evaluation for the most important mixed-training condition if disk space and time allow;
- optionally run multi-seed cross-dataset transfer for the most important transfer pairs.

### 2. Confidence Intervals Or Bootstrap Intervals

For primary test conditions, add confidence intervals or bootstrap intervals for Macro F1 and positive F1.

This will make the paper more defensible because small differences such as 1-2 percentage points may not be meaningful.

### 3. Explain The Two-Epoch Choice

The paper must explain why two epochs were used.

Current likely explanation:

- two epochs were chosen as a controlled first-pass setting across all model/dataset combinations;
- the project prioritized comparable cross-dataset coverage over hyperparameter tuning;
- future work should tune epochs or use validation-based early stopping.

### 4. Citation And License Verification

Before final submission, verify:

- full THAR author list and venue details;
- THAR license/data-use terms;
- CM repository citation and license status;
- Kaggle dataset license/source metadata;
- whether any processed text can be redistributed.

### 5. Human Error Examples

Add 8-12 concrete manual error examples to the final paper.

Rules:

- mask usernames and URLs;
- avoid unnecessary slur reproduction;
- paraphrase when direct text is not needed;
- label each example by error category;
- explain what the example teaches about model behavior or dataset policy.

Target categories:

- cross-dataset label mismatch;
- generic profanity or abuse;
- target-group or religion cue;
- political context or slogan;
- short/contextless text;
- Devanagari or mixed-script difficulty;
- false positive from lexical trigger;
- false negative from subtle targeted hate.

### 6. Mixed-Dataset Training

Status: completed where applicable for the current experimental matrix, but not yet repeated across multiple seeds.

Completed combinations:

- Kaggle + CM, documented in `docs/mixed_kaggle_cm_training_report.md`;
- Kaggle + THAR, documented in `docs/mixed_kaggle_thar_training_report.md`;
- CM + THAR, documented in `docs/mixed_cm_thar_training_report.md`;
- Kaggle + CM + THAR, documented in `docs/mixed_all_three_training_report.md`.

Each mixed checkpoint was evaluated separately on:

- Kaggle;
- CM;
- THAR.

These experiments test whether broader training improves robustness or simply mixes incompatible labels. Remaining gap: the mixed-training conclusions should be treated as single-seed evidence until repeated under multiple seeds.

## Paper Improvements Needed

The next paper versions should add:

- a fuller related work section;
- a reproducibility box;
- a multi-seed result table;
- a manual error example table;
- an AI-use statement;
- a clearer limitation section about label comparability;
- a final claim that remains conditional rather than universal;
- a one-page application research summary PDF for review and feedback.

## Current Defensible Claim

The current defensible claim is:

> In Hinglish and Hindi-English code-mixed harmful speech detection, model ranking is conditional on dataset situation. mBERT performs better on matched Latin-script Hinglish/offensive datasets, while MuRIL performs better on targeted religious hate and some THAR-related transfer settings. Cross-dataset evaluation reveals that dataset label policy and domain are as important as model choice.

Do not claim:

> MuRIL is better than mBERT for Indian hate speech.

Do not claim:

> mBERT is better than MuRIL for Hinglish hate speech in general.

Both are too broad for the current evidence.
