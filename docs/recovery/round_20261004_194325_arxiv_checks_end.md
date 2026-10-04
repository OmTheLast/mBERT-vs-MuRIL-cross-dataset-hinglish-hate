# Current Recovery Checkpoint

Date: 2026-10-04 20:15 IST

## Request
Prepare arXiv-readiness cleanup: verify dataset citations and permissions, remove public review notes from the public draft, and keep checks internally. User also noted reported evaluation splits were used to choose the best epoch, so claims must be honest about this.

## Status
completed

## Decisions
- Treat this as documentation/arXiv-readiness work, not new training.
- Public-facing paper files should not contain review markers.
- Keep citation/permission and evaluation-protocol checks in `docs/internal_arxiv_checks.md`.
- Disclose that matched results are selection-set scores because the evaluation split was used for best-epoch selection.
- Do not claim untouched final-test results.
- Do not redistribute raw CM/THAR text unless permissions are clarified.

## Completed
- Created durable start checkpoint and preserved it at `docs/recovery/round_20261004_193811_arxiv_checks_start.md`.
- Verified training script uses `load_best_model_at_end=True` with `metric_for_best_model="f1_macro"`.
- Checked public metadata:
  - Kaggle API reports MIT for `sharduldhekane/code-mixed-hinglish-hate-speech-detection-dataset`.
  - GitHub API reports no detected license for `shikharras/cm-hate-speech-detection`.
  - GitHub API reports no detected license for `aakash-dl/THAR`.
  - THAR metadata lists Deepawali Sharma, Aakash Singh, and Vivek Kumar Singh; DOI `10.1145/3653017`.
- Added `docs/internal_arxiv_checks.md`.
- Removed public review markers from `paper/application_research_draft.md` and `paper/one_page_research_summary.md`.
- Updated dataset registry and BibTeX for checked citation/permission status.
- Updated PDF builder scripts and regenerated:
  - `output/pdf/one_page_research_summary.pdf`
  - `output/pdf/hinglish_mbert_muril_research_paper_draft.pdf`
- Verified generated PDFs contain v0.4 date, selection-set caveat, Kaggle MIT note, and no public review markers/stale final-verification language.
- Rendered and visually checked one-page summary PDF.

## Checks And Results
- `rg` found no public review-marker or stale final-verification wording in `paper`, `docs`, or `README.md` after edits.
- `pypdf` text extraction confirmed both regenerated PDFs contain `Working Paper Draft v0.4`, `October 4, 2026`, `selection-set`, and `Kaggle metadata lists MIT`.
- `pypdf` text extraction confirmed both regenerated PDFs do not contain the old public review marker or stale final-verification wording.
- `pdfinfo` confirmed one-page summary has 1 page and paper draft has 10 pages.
- `pdftoppm` rendered previews; local Fontconfig warning did not block rendering.

## Unfinished Work
- Decide whether to convert `paper/application_research_draft.md` into the primary LaTeX/PDF source for arXiv submission.
- Add 8-12 anonymized manual error examples if desired.
- Consider a clean nested-validation or held-out-test rerun if stronger final-test claims are needed.

## Blockers
None.

## Exact Next Action
Commit and push the arXiv-readiness documentation and regenerated PDFs.
