# Data Directory

This directory separates raw downloaded datasets from processed CSV files used by experiments.

## Layout

```text
data/
  raw/          # Downloaded or cloned datasets; ignored by Git.
  processed/    # Standardized CSVs; generated locally and ignored by Git.
```

## Standard Processed Schema

Every dataset used in experiments should eventually be converted to:

```text
text,label,dataset,source,language
```

Required fields:

- `text`: the text/comment/tweet/post.
- `label`: `0` for non-hate/non-offensive, `1` for hate/offensive after documented mapping.
- `dataset`: short dataset identifier.

Useful optional fields:

- `source`: source platform or original source file.
- `language`: `english`, `hindi`, `hinglish`, `mixed`, or `unknown`.

## GitHub Safety

Raw datasets and generated processed files are ignored by `.gitignore` because:

- some datasets have redistribution restrictions;
- some files may contain social-media text with licensing constraints;
- generated files can be recreated from scripts.

Dataset provenance and access notes should be documented in:

- `docs/dataset_registry.md` for datasets used in experiments.
- `docs/dataset_acquisition_log.md` for download/contact/access attempts.
- `docs/dataset_candidates.md` for candidate datasets and research leads.
