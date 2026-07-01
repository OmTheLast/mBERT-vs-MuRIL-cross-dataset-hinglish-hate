# Research Rigor Roadmap

Date: 2026-07-01

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

## Main Weakness Right Now

The main weakness is not page count. It is research rigor.

Current transformer results use:

- one random seed: `42`;
- one epoch setting: `2` epochs;
- one maximum sequence length: `128`;
- one learning rate: `2e-5`;
- one main checkpoint per model/dataset condition.

This is acceptable for a working draft, but not enough for a strong final research conclusion.

## Required Before Final Paper

### 1. Multi-Seed Runs

Run at least three random seeds for the main matched settings:

- seed 42;
- seed 43;
- seed 44.

Minimum conditions:

- mBERT and MuRIL on `kaggle_hinglish_hate`;
- mBERT and MuRIL on `cm_splits_codemixed`;
- mBERT and MuRIL on `thar_religion`.

Report:

- mean Macro F1;
- standard deviation Macro F1;
- mean positive F1;
- standard deviation positive F1.

If time allows, also run multi-seed cross-dataset transfer for the most important transfer pairs.

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

Run mixed-dataset experiments because the current paper already identifies this as the next step.

Minimum combinations:

- Kaggle + CM;
- Kaggle + THAR;
- CM + THAR;
- Kaggle + CM + THAR.

Evaluate every mixed checkpoint separately on:

- Kaggle;
- CM;
- THAR.

This will test whether broader training improves robustness or simply mixes incompatible labels.

## Paper Improvements Needed

The next paper versions should add:

- a fuller related work section;
- a reproducibility box;
- a multi-seed result table;
- a manual error example table;
- an AI-use statement;
- a clearer limitation section about label comparability;
- a final claim that remains conditional rather than universal.

## Current Defensible Claim

The current defensible claim is:

> In Hinglish and Hindi-English code-mixed harmful speech detection, model ranking is conditional on dataset situation. mBERT performs better on matched Latin-script Hinglish/offensive datasets, while MuRIL performs better on targeted religious hate and some THAR-related transfer settings. Cross-dataset evaluation reveals that dataset label policy and domain are as important as model choice.

Do not claim:

> MuRIL is better than mBERT for Indian hate speech.

Do not claim:

> mBERT is better than MuRIL for Hinglish hate speech in general.

Both are too broad for the current evidence.
