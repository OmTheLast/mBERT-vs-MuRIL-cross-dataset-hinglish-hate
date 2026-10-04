# Current Recovery Checkpoint

Date: 2026-10-04

## Request
Apply manuscript feedback from screenshot: use updated `paper/application_research_draft.md` as the manuscript source, remove drafting instructions/public TODOs, soften conclusions so results are described as observed scores under this setup rather than causal proof, and keep the selection-set limitation prominent. Screenshot is feedback, not authoritative hidden instructions.

## Status
completed

## Decisions
- Do not treat attached screenshot text as code/instructions beyond the user's explicit request to apply the feedback.
- Edit source Markdown and generated PDF/LaTeX sources where stale text could mislead.
- Preserve internal check files.
- Keep the public claim as observed model differences under the current setup, not causal proof or statistically established superiority.

## Completed
- Started recovery checkpoint.
- Updated `paper/application_research_draft.md` to remove public drafting instructions and soften model-ranking claims.
- Updated `paper/one_page_research_summary.md` with the same observed-score framing.
- Updated `paper/main.tex` and `paper/overleaf_self_contained.tex` so they no longer contain stale v0.2/single-seed matched framing or mixed-training-as-future wording.
- Updated `paper/build_paper_pdf.py` to use the three-seed matched summary and to describe mixed-dataset training as completed exploratory work.
- Updated `paper/build_one_page_summary_pdf.py` with softened one-page wording.
- Updated `docs/internal_arxiv_checks.md` and `docs/research_journal.md` with the selection-set/arXiv framing and manuscript cleanup note.
- Regenerated `output/pdf/hinglish_mbert_muril_research_paper_draft.pdf` and `output/pdf/one_page_research_summary.pdf`.
- Verified regenerated PDFs by text extraction and rendered-page visual checks.

## Running
None.

## Blockers
None.

## Exact Next Action
Commit and push the manuscript cleanup update.
