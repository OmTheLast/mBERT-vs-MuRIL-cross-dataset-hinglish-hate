# LaTeX Paper Round

Date: 2026-11-16
Status: running

Request: prepare the research paper in LaTeX and remove the v0.5 manuscript.

Starting state: clean worktree. Read current checkpoint, Markdown manuscript,
LaTeX source, saved mixed-training and baseline tables, threshold report and
mix-builder implementation.

Decisions: edit the existing open paper/main.tex in place; make it authoritative.
Remove superseded application_research_draft.md, with its history retained in
Git. Keep quantitative claims tied to saved results. Preserve selection-set,
three-seed versus single-seed, automated-tagging and license caveats. No training.
Do not generate a separate PDF or open another editor tab. Compile with the
built-in editor and record the returned diagnostics.

Next action: write structured LaTeX, update source pointers and prevent the old
Markdown builder from overwriting the paper, then validate and compile.
