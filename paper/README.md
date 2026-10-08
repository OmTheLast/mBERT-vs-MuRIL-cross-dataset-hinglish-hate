# Manuscript Source

`application_research_draft.md` is the authoritative manuscript. Edit it, then run:

```bash
.venv/bin/python -m pip install -r paper/requirements.txt
.venv/bin/python paper/build_manuscript.py
```

This generates `main.tex`, `overleaf_self_contained.tex`, and
`output/pdf/hinglish_mbert_muril_research_paper_draft.pdf` from the same text,
tables, and figure references. Both LaTeX exports require the referenced image
files; the historical `overleaf_self_contained.tex` filename does not imply
embedded figures. Run LaTeX with `paper/` as the working directory.

The PDF uses ReportLab; the LaTeX exports use Pandoc. Reference numbers follow
the reference list in the source. `references.bib` retains structured citation
metadata for future journal formatting. `paper_draft.md` is a historical draft;
the one-page summary is a separate overview, not the manuscript source.
