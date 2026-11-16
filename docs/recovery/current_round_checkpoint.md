# Current Recovery Checkpoint

Date: 2026-11-16
Status: completed and verified locally

Request: prepare the research paper in LaTeX and remove the v0.5 manuscript.

Authoritative artifact: paper/main.tex, edited in the existing document tab.
Removed superseded paper/application_research_draft.md and its generated PDF;
earlier versions remain in Git history. Historical Overleaf entry point now
includes main.tex. Current paper uses inline citations and four saved figures.

Verified: desktop editor compiler returned success; paper/build_manuscript.py
matched 31 result rows to saved CSVs, resolved citations/cross-references and
found all figure assets. Old build commands no longer overwrite paper sources.

Git integration: fetched newer origin/main changes through 992a8c1 and merged
them, retaining upstream README styling, portfolio links, chart/script and logs.
Updated paper links in both README files; no remote work was discarded.

Research boundaries: matched evaluation data still selects epochs; transfer,
mixed and threshold results are exploratory single-seed evidence. No new
training, annotations or result metrics were created. No separate PDF export.

Round details: round_20261116_latex_paper_start.md and
round_20261116_latex_paper_end.md. No running jobs or blockers.

Exact next action: verify Git publication against origin/main after the paper
commit. Future research priority remains independent final evaluation and
human-reviewed error examples; no new training is authorized by this log.
