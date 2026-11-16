# LaTeX Paper Round Completion

Date: 2026-11-16
Status: completed and verified locally

Request: prepare the paper in LaTeX and remove the v0.5 manuscript.

Completed:
- Edited the existing open paper/main.tex in place as the authoritative source.
- Added proper paper structure, inline bibliography, six result/data tables,
  four existing figures, methods, threshold findings and explicit limitations.
- Removed application_research_draft.md and obsolete generated paper PDF;
  earlier versions remain recoverable from Git history.
- Converted overleaf_self_contained.tex into a main.tex compatibility include.
- Replaced Markdown generator with read-only table/reference/asset checks.
- Updated active project map, README links and experiment instructions.

Checks:
- Desktop compile_latex_document returned kind=success for paper/main.tex.
- 31 result rows matched saved CSVs; citations/references/figure paths passed.
- No separate PDF was generated or exported. Existing editor stays open.
- No model training, inference, result CSV changes or dependency installs.

No running jobs or blockers. Exact next action: commit and push the verified
paper update and check remote HEAD. Future experimental work requires an
independent final-evaluation protocol and repeated exploratory conditions.

Publication integration: initial push found newer origin/main work through
992a8c1 (README house style and portfolio links). Fetched and merged those
changes, preserving the upstream README, plot script, chart, portfolio link
and work logs. Resolved the README opening conflict by retaining the new
opening and placing the LaTeX paper link with its final pointers. Updated the
upstream README-DETAILS.md paper link as well. No remote commits were discarded.
