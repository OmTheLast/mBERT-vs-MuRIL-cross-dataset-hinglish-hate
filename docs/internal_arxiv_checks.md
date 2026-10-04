# Internal arXiv Readiness Checks

Date: 2026-10-04

This file is an internal working checklist for arXiv preparation. It records checks that affect what the paper can honestly claim. It is not written as a public-facing paper section.

## Current Public Claim Status

The current results can form the core of an application research paper if they are described as controlled, selection-set comparisons rather than untouched final-test results.

Safe central claim:

> In Hinglish and Hindi-English code-mixed harmful-speech detection, mBERT and MuRIL rankings depend on dataset situation. mBERT performs better on the matched Kaggle Hinglish hate and CM code-mixed/offensive settings, while MuRIL performs better on the THAR targeted religious-hate setting. Cross-dataset and mixed-training results show that label definition, platform, topic, and script mix strongly affect model behavior.

Do not claim:

- that either model is universally better;
- that the matched scores are blind final-test results;
- that CM and THAR raw data can be redistributed under an open license;
- that hate, offensive, and AntiReligion labels are interchangeable.

## Evaluation Split And Best-Epoch Check

Training script: `experiments/train_transformer.py`.

Relevant behavior:

- `eval_strategy="epoch"`;
- `save_strategy="epoch"`;
- `load_best_model_at_end=True`;
- `metric_for_best_model="f1_macro"`;
- `greater_is_better=True`.

Implication:

- The reported matched evaluation split was also used to select the best epoch.
- Therefore, matched results are selection-set results, not untouched final-test results.
- For CM, the source test split was used as the evaluation split in this setup, so it is not an untouched final test.
- For Kaggle and THAR, seeds `7`, `13`, and `42` change both model-training randomness and stratified split membership.

Paper wording to keep:

> The reported matched scores are selection-set scores because the same evaluation split was used for best-epoch selection. They support comparative trends, but future work should add a separate held-out test set or nested validation protocol.

## Dataset Citation And Permission Status

### Kaggle Hinglish Hate

Source:

- https://www.kaggle.com/datasets/sharduldhekane/code-mixed-hinglish-hate-speech-detection-dataset

Check performed:

- `curl -k -sS https://www.kaggle.com/api/v1/datasets/view/sharduldhekane/code-mixed-hinglish-hate-speech-detection-dataset`

Observed metadata on 2026-10-04:

- title: `Code-Mixed Hinglish Hate Speech Detection Dataset`
- owner: `Shardul Dhekane`
- license fields: `MIT`
- last updated: `2025-09-11T10:40:07.327Z`

Current permission stance:

- OK to cite as Kaggle dataset with MIT metadata.
- Still describe source/platform details cautiously because the local controlled file uses only the Hinglish subset from a larger multilingual file.

### CM Code-Mixed / Offensive Dataset

Source:

- https://github.com/shikharras/cm-hate-speech-detection

Check performed:

- GitHub repository page opened.
- GitHub API checked with `curl -k -sS https://api.github.com/repos/shikharras/cm-hate-speech-detection`.

Observed metadata on 2026-10-04:

- repository: `shikharras/cm-hate-speech-detection`
- detected license: `None`
- repository is public.

Current permission stance:

- OK to cite repository and report derived metrics.
- Do not redistribute raw CM files or processed text unless permission/license is clarified.
- In the paper, describe CM as offensive/hate-adjacent, not strict hate speech.

### THAR

Sources:

- https://github.com/aakash-dl/THAR
- DOI: https://doi.org/10.1145/3653017

Checks performed:

- GitHub repository page opened.
- GitHub API checked with `curl -k -sS https://api.github.com/repos/aakash-dl/THAR`.
- THAR paper metadata checked through DOI/CiteDrive-accessible metadata.

Observed metadata on 2026-10-04:

- repository: `aakash-dl/THAR`
- detected license: `None`
- repository is public.
- paper title: `THAR- Targeted Hate Speech Against Religion: A high-quality Hindi-English code-mixed Dataset with the Application of Deep Learning Models for Automatic Detection`
- authors: Deepawali Sharma, Aakash Singh, Vivek Kumar Singh
- DOI: `10.1145/3653017`
- paper description reports 11,549 comments annotated by five independent annotators.

Current permission stance:

- OK to cite THAR paper and repository and report derived metrics.
- Do not redistribute raw THAR CSV or processed text unless permission/license is clarified.
- In the paper, describe THAR as targeted religious hate, not general Hinglish hate.

## Public Draft Cleanup Completed

- Removed public review markers from `paper/application_research_draft.md`.
- Removed the public review marker from `paper/one_page_research_summary.md`.
- Moved unresolved review items into this internal check file.
- Added explicit selection-set caveat to the application draft.

## Remaining Before arXiv

- Decide whether to submit the Markdown draft as-is after converting to PDF/LaTeX, or first convert `paper/application_research_draft.md` into the main PDF builder.
- Add 8-12 anonymized/paraphrased manual error examples if space allows.
- Consider rerunning at least one clean nested-validation or held-out test experiment if the paper needs stronger final-test claims.
- Avoid publishing raw CM/THAR text in the arXiv source bundle or GitHub release unless permissions are clarified.
