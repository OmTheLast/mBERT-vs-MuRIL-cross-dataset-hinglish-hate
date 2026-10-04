# Current Recovery Checkpoint

Date: 2026-10-04 19:37 IST

## Request
Prepare arXiv-readiness cleanup: verify dataset citations and permissions, remove public review notes from public draft, and keep checks internally. User also notes reported evaluation splits were used to choose the best epoch, so claims must be honest about this.

## Status
running

## Decisions
- Treat this as documentation/arXiv-readiness work, not new training.
- Keep sensitive verification/checklist details in internal docs.
- Public draft should remove review markers and disclose evaluation-split reuse as a limitation.
- Do not claim untouched final test-set results.

## Completed
- Inspected repo status and searched for public review markers, citation/license, and epoch-selection references.
- Confirmed `paper/application_research_draft.md` still had public review markers at round start.
- Confirmed README already notes that evaluation splits guided best-epoch selection and results are not untouched final-test results.

## Running
- Verify citations/permissions from local docs and web/current sources.
- Edit application draft, internal checks, dataset registry/references if needed.

## Artifacts To Update
- `paper/application_research_draft.md`
- `paper/one_page_research_summary.md`
- `docs/internal_arxiv_checks.md` or similar internal check file
- `docs/dataset_registry.md`
- `paper/references.bib`
- `docs/research_journal.md`

## Blockers
None yet.

## Exact Next Action
Browse/check Kaggle, CM GitHub, THAR GitHub/ACM metadata and then apply scoped documentation edits.
