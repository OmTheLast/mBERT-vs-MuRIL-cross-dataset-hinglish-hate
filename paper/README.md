# Research Paper

**Read and edit the research paper in [main.tex](main.tex), then compile it in
the LaTeX editor to view the typeset paper.**

The paper includes three-seed matched results, exploratory transfer and mixed
training, TF-IDF baselines, threshold diagnostics, figures and source citations.
Its limitations explain where evaluation data was reused for epoch selection.
Prepared by Om Patnaik; LaTeX source updated November 16, 2026.

## Edit And Compile

Keep `main.tex` as the authoritative source. The desktop LaTeX editor compiles
it with the project's supporting figure files. For another LaTeX environment,
preserve the repository layout so the four PNG figures in
`results/result_analysis/` remain available. Citations are included directly in
the source; a separate BibTeX run is not required.

## Verify The Results

Run from the repository root:

```bash
.venv/bin/python paper/build_manuscript.py
```

This checks 31 table rows against saved result CSVs, citation keys, cross
references and figure paths. It does not write paper files or compile LaTeX.
Compilation was verified in the desktop editor on November 16, 2026.

## Historical Files

The superseded v0.5 Markdown manuscript and its generated PDF were removed;
their earlier contents remain in Git history. `overleaf_self_contained.tex`
is a compatibility entry point that includes `main.tex`, not a separate paper.
`build_paper_pdf.py` now runs the same checks as `build_manuscript.py` and
does not overwrite the source or generate a separate PDF.

The one-page summary and `paper_draft.md` are historical companion documents.
Dataset, model and paper citations are listed in `main.tex`; `references.bib`
retains earlier structured citation metadata.

[Experiment commands](../docs/running_experiments.md) · [Research journal](../docs/research_journal.md) · [Saved tables](../results/result_analysis/)
