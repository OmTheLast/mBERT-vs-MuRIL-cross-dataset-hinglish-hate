# Hugging Face research checkpoint archive

Owner: `OmTheLast`.

[Open the public Hugging Face collection](https://huggingface.co/collections/OmTheLast/hinglish-research-mbert-vs-muril-6aa96a16ed03bba0e89e9408).
The collection contains all 14 model repositories.

The release workflow preserves 26 experiment checkpoints in 14 public model
repositories. `huggingface_release_manifest.json` records the status, original
weight hashes, local inference checks, uploaded commits and remote verification
for each checkpoint. Consult that manifest for completion status.

## Repositories

| Training condition | mBERT | MuRIL | Seeds |
|---|---|---|---|
| Kaggle Hinglish hate | [Model](https://huggingface.co/OmTheLast/mbert-hinglish-kaggle) | [Model](https://huggingface.co/OmTheLast/muril-hinglish-kaggle) | 7, 13, 42 |
| CM offensive language | [Model](https://huggingface.co/OmTheLast/mbert-hinglish-cm) | [Model](https://huggingface.co/OmTheLast/muril-hinglish-cm) | 7, 13, 42 |
| THAR religious hate | [Model](https://huggingface.co/OmTheLast/mbert-hinglish-thar) | [Model](https://huggingface.co/OmTheLast/muril-hinglish-thar) | 7, 13, 42 |
| Kaggle + CM | [Model](https://huggingface.co/OmTheLast/mbert-hinglish-mixed-kaggle-cm) | [Model](https://huggingface.co/OmTheLast/muril-hinglish-mixed-kaggle-cm) | 42 |
| Kaggle + THAR | [Model](https://huggingface.co/OmTheLast/mbert-hinglish-mixed-kaggle-thar) | [Model](https://huggingface.co/OmTheLast/muril-hinglish-mixed-kaggle-thar) | 42 |
| CM + THAR | [Model](https://huggingface.co/OmTheLast/mbert-hinglish-mixed-cm-thar) | [Model](https://huggingface.co/OmTheLast/muril-hinglish-mixed-cm-thar) | 42 |
| All three | [Model](https://huggingface.co/OmTheLast/mbert-hinglish-mixed-all-three) | [Model](https://huggingface.co/OmTheLast/muril-hinglish-mixed-all-three) | 42 |

The collection and all model repositories are publicly accessible without a
Hugging Face login. Public visibility does not assign a separate license to the
fine-tuned models or their training datasets; see the licensing notes below.

## Seed organization

`main` contains seed 42, chosen as a consistent default rather than selected for
its test score. Named branches `seed-7`, `seed-13` and `seed-42` preserve each
available run. The manifest also contains exact commit IDs for immutable loading.
Pass the same `revision` to the tokenizer and model.

The three initial/debug directories (`mbert_model`, `muril_model` and
`smoke_mbert_model`) are excluded. All 26 named experiment weights have distinct
SHA-256 hashes.

## Packaging and validation

The export script leaves original checkpoint files unchanged. Staging lives in
the ignored `.cache/hf-release/` directory. Weight files are hard-linked to avoid
duplicating 21.6 GB locally; never edit staged weight files in place.

Exports contain weights, configuration, tokenizers, saved evaluation metrics,
training metadata, model cards, dependency requirements and provenance. Only an
explicit allowlist of these files is uploaded. Dataset text, tokens, caches,
optimizer state and prediction dumps are excluded.

Readable class names are added to exported configurations. Mixtures use
`NEGATIVE`/`POSITIVE` because their component datasets have different definitions.

Each checkpoint is loaded locally with Transformers and checked for missing,
unexpected or mismatched tensors. Inference on two synthetic inputs must yield
finite two-class probabilities summing to one. Remote verification checks file
hashes, revision identities and the recorded visibility. Public releases are
verified without authentication. This validates packaging and
transfer; it does not rerun the full research benchmark.

One seed-42 CM checkpoint per model family was also downloaded through the
normal Hugging Face `from_pretrained` path. Both reproduced the local inference
outputs within `1e-6`. `huggingface_validation.json` records those checks and
the installed runtime versions.

Transformers 4.57.6 emits a spurious local Mistral-regex warning for these saved
BERT configurations: its local detection logic does not exclude BERT in the
4.57.3–4.x version interval. The files use WordPiece with `BertPreTokenizer`.
Fast and slow BERT tokenizers agreed on Latin, Devanagari, punctuation and
identity-term samples. No Mistral tokenizer patch was applied.

## Research details preserved in the cards

- Kaggle and THAR seeds change the stratified train/evaluation split as well as
  training randomness. CM uses a fixed source split.
- The Trainer seed is recorded, but the model is instantiated before Trainer;
  exact classifier-head initialization reproducibility is not guaranteed.
- The training script chooses the best epoch using evaluation Macro F1. Those
  internal/matched scores are selection-set scores. For CM, the source test
  split was used in this selection; it is not an untouched final test.
- Per-seed scores and means/sample standard deviations are separated. Mixed
  conditions have only seed 42.
- The two MuRIL mixtures Kaggle+CM and CM+THAR retain their documented
  all-negative external-evaluation failure cases.
- The 79-row diagnostic probe is excluded from primary results.
- The two seed-42 Kaggle metadata files are reconstructed in the exports only.
  Journal-backed settings and inferred historical defaults are distinguished.

## Commands

From the research directory:

```bash
.venv/bin/python scripts/release_huggingface.py prepare
.venv/bin/python scripts/release_huggingface.py validate
HF_XET_HIGH_PERFORMANCE=1 .venv/bin/python scripts/release_huggingface.py upload
.venv/bin/python scripts/release_huggingface.py verify
```

To resume a partial upload, run only `upload`, followed by `verify`. Preparation
regenerates staging and resets the manifest; it refuses to run once the manifest
contains uploaded checkpoints, to preserve release history.
The initial upload step checks account identity and refuses to write public
repositories. After an explicit public-release request, `publish` updates the
cards and upstream attribution, preserves weight files and seed aliases, then
makes the models and collection public. Run `verify` after publication. The
current release has already been published; `upload` is for private staging.

## Licensing status

The models are public, with a separate fine-tuned-model license still unspecified.
Both base-model cards declare Apache-2.0, and each released revision includes
`BASE_MODEL_LICENSE.txt` and `BASE_MODEL_NOTICE.md`. Dataset terms are separate;
CM and THAR source licenses remain unresolved in the project registry. The cards
record this status rather than assigning an unsupported license.

The 2026-09-15 source check found `MIT` in the Kaggle dataset's public metadata.
GitHub's repository metadata reports no detected license for either CM or THAR,
and neither repository page displayed a license. These observations are recorded
with source URLs in `huggingface_source_license_check.json`; they do not by
themselves settle the terms for releasing fine-tuned weights.

## Public presentation

Both GitHub repositories link to the public collection. Model cards lead with the
training condition, label meanings, seed revisions and recorded scores. Loading
code, full evaluation details, licensing and provenance remain in expandable
sections. The collection title is **Hinglish Hate Speech: mBERT vs MuRIL**.

After an authorized public release, `publish` updates attribution and visibility.
`polish` applies the concise model-card layout, and `verify` checks the resulting
public revisions. These actions preserve the original checkpoint weights.
