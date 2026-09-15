#!/usr/bin/env python3
"""Prepare, validate, upload, publish, and verify the 26 research checkpoints.

Run with the project .venv. No credentials are stored by this script.
Original checkpoint files are never edited; large weights are hard-linked into
an ignored staging directory. Uploads use an explicit file allowlist.
"""
from __future__ import annotations

import argparse
import csv
import gc
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import statistics
import subprocess

ROOT = Path(__file__).resolve().parents[1]
STAGE = ROOT / '.cache/hf-release'
MANIFEST = ROOT / 'docs/huggingface_release_manifest.json'
CODE = 'https://github.com/OmTheLast/mBERT-vs-MuRIL-cross-dataset-hinglish-hate'
BASES = {'mbert': 'google-bert/bert-base-multilingual-cased', 'muril': 'google/muril-base-cased'}
DATA = {
    'kaggle_hinglish_hate': ('kaggle', 'Kaggle Hinglish hate speech', ['NON_HATE', 'HATE']),
    'cm_splits_codemixed': ('cm', 'CM code-mixed offensive language', ['NOT_OFFENSIVE', 'OFFENSIVE']),
    'thar_religion': ('thar', 'THAR targeted religious hate', ['NON_ANTI_RELIGION', 'ANTI_RELIGION']),
    'mixed_kaggle_plus_cm': ('mixed-kaggle-cm', 'Kaggle + CM', ['NEGATIVE', 'POSITIVE']),
    'mixed_kaggle_plus_thar': ('mixed-kaggle-thar', 'Kaggle + THAR', ['NEGATIVE', 'POSITIVE']),
    'mixed_cm_plus_thar': ('mixed-cm-thar', 'CM + THAR', ['NEGATIVE', 'POSITIVE']),
    'mixed_all_three': ('mixed-all-three', 'Kaggle + CM + THAR', ['NEGATIVE', 'POSITIVE']),
}
FILES = ['config.json', 'model.safetensors', 'tokenizer.json', 'tokenizer_config.json',
         'special_tokens_map.json', 'vocab.txt', 'eval_metrics.json', 'training_metadata.json',
         'README.md', 'release_metadata.json', 'evaluation_summary.json', 'requirements.txt']
SOURCES = {
    'kaggle': 'https://www.kaggle.com/datasets/sharduldhekane/code-mixed-hinglish-hate-speech-detection-dataset',
    'cm': 'https://github.com/shikharras/cm-hate-speech-detection',
    'thar': 'https://github.com/aakash-dl/THAR',
}


def read(path):
    return json.loads(path.read_text())


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + '.tmp')
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')
    temporary.replace(path)


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(8 * 1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def clean(text):
    text = re.sub(r'http\S+|www\S+|https\S+', ' URL ', str(text))
    text = re.sub(r'@\w+', ' USER ', text)
    return re.sub(r'\s+', ' ', text).strip()


def prepare():
    if MANIFEST.exists() and any(r.get('uploaded_commit') for r in read(MANIFEST)['checkpoints']):
        raise RuntimeError('This manifest contains uploaded checkpoints. Resume with upload/verify; preparation would erase release history.')
    commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    rows = []
    for src in sorted((ROOT / 'Models').glob('*__train-*__seed*__e2')):
        family, dataset, seed, _ = src.name.split('__')
        dataset, seed = dataset.removeprefix('train-'), int(seed.removeprefix('seed'))
        short, title, labels = DATA[dataset]
        dest = STAGE / src.name
        dest.mkdir(parents=True, exist_ok=True)
        for name in FILES[:8]:
            p = src / name
            if not p.exists():
                if name == 'training_metadata.json':
                    continue
                raise FileNotFoundError(p)
            target = dest / name
            if target.exists():
                target.unlink()
            if name == 'model.safetensors':
                os.link(p, target)
            else:
                shutil.copy2(p, target)
        config = read(dest / 'config.json')
        config['id2label'] = {str(i): label for i, label in enumerate(labels)}
        config['label2id'] = {label: i for i, label in enumerate(labels)}
        write(dest / 'config.json', config)
        if (src / 'training_metadata.json').exists():
            metadata = read(src / 'training_metadata.json')
        else:
            assert dataset == 'kaggle_hinglish_hate' and seed == 42
            metadata = {
                'model': family, 'base_checkpoint': BASES[family], 'seed': 42,
                'epochs': 2, 'batch_size': 8, 'split_policy': 'stratified_80_20_seed42',
                'train_csv': 'data/processed/kaggle_hinglish_hate.csv',
                'train_rows': 3824, 'eval_rows': 956,
                'cleaning': 'minimal', 'max_length': 128, 'learning_rate': 2e-5, 'weight_decay': 0.01,
                'metadata_status': 'Reconstructed; original run did not save this file.',
                'evidence': ['docs/research_journal.md: Local Training Run On 2026-06-24',
                             'experiments/train_mac_mps.py', 'experiments/train_transformer.py at 7a85bd1'],
                'uncertainty': 'Seed, epochs, batch size, dataset and split are journal-backed. Cleaning is wrapper-backed; max length, learning rate and weight decay are historical defaults, not recovered CLI arguments.',
            }
        write(dest / 'training_metadata.json', metadata)
        rows.append({'source': str(src.relative_to(ROOT)), 'stage': str(dest.relative_to(ROOT)),
                     'repo_id': f'OmTheLast/{family}-hinglish-{short}', 'family': family,
                     'dataset': dataset, 'seed': seed, 'weights_sha256': sha(src / 'model.safetensors'),
                     'weights_bytes': (src / 'model.safetensors').stat().st_size})
    assert len(rows) == 26
    cross = list(csv.DictReader((ROOT / 'results/result_analysis/mixed_training_macro_f1_summary.csv').open()))
    for row in rows:
        dest = ROOT / row['stage']
        peers = [r for r in rows if r['repo_id'] == row['repo_id']]
        metrics = [{'seed': r['seed'], **read(ROOT / r['stage'] / 'eval_metrics.json')} for r in peers]
        summary = {'evaluation_role': 'Evaluation split also used for best-epoch selection; not an untouched final test.',
                   'per_seed': metrics}
        if len(peers) == 3:
            summary['aggregate'] = {key: {'mean': statistics.mean(m[key] for m in metrics),
                                         'sample_std': statistics.stdev(m[key] for m in metrics)}
                                    for key in ['eval_accuracy', 'eval_f1_macro', 'eval_f1_hate', 'eval_recall_hate']}
        summary['mixed_external_evaluation'] = [r for r in cross if r['model'] == row['family'] and r['train_dataset'] == row['dataset']]
        write(dest / 'evaluation_summary.json', summary)
        write(dest / 'release_metadata.json', {
            **{k: row[k] for k in ['source', 'repo_id', 'family', 'dataset', 'seed', 'weights_sha256', 'weights_bytes']},
            'research_code_commit': commit, 'weight_modifications': 'None; config label names added in export only.',
            'release_status': 'Private research archive; public release license review pending.',
        })
        (dest / 'requirements.txt').write_text('transformers==4.57.6\ntorch>=2.2\nsafetensors>=0.4\nhuggingface-hub>=0.36\n')
        (dest / 'README.md').write_text(card(row, peers, metrics, summary, commit))
        from huggingface_hub import ModelCard
        ModelCard.load(str(dest / 'README.md'))  # Parse YAML before remote writes.
    write(MANIFEST, {'owner': 'OmTheLast', 'private': True, 'research_code_commit': commit,
                     'checkpoints': rows, 'excluded': ['Models/mbert_model', 'Models/muril_model', 'Models/smoke_mbert_model']})
    print(f'PREPARED {len(rows)} checkpoints in {len(set(r["repo_id"] for r in rows))} repos', flush=True)


def card(row, peers, metrics, summary, commit):
    ds = row['dataset']; short, title, labels = DATA[ds]
    mixed = ds.startswith('mixed')
    table = '\n'.join(f"| {m['seed']} | {m['eval_accuracy']:.4f} | {m['eval_f1_macro']:.4f} | {m['eval_f1_hate']:.4f} | {m['eval_recall_hate']:.4f} |" for m in sorted(metrics, key=lambda m:m['seed']))
    aggregate = ''
    if 'aggregate' in summary:
        a = summary['aggregate']['eval_f1_macro']
        aggregate = f"\nAcross seeds 7, 13, 42: Macro F1 **{a['mean']:.4f} ± {a['sample_std']:.4f}** (sample standard deviation, not a confidence interval). This describes the group, not one checkpoint.\n"
    split = ('CM uses source train+val for training and source test for evaluation, with the same split across seeds.'
             if ds == 'cm_splits_codemixed' else
             'Kaggle and THAR use stratified 80/20 splits whose membership changes with the seed. Variation includes split changes as well as training randomness.' if not mixed else
             'The mixture is built from source training partitions at seed 42, then internally split 80/20 for training and evaluation. This condition has only one seed.')
    warning = ''
    if row['family'] == 'muril' and ds in ['mixed_kaggle_plus_cm', 'mixed_cm_plus_thar']:
        warning = '\n**Known failure:** this checkpoint produced all-negative predictions at the default decision rule on the reported primary external evaluations. It is preserved as a research failure case. See the project model registry and collapse diagnostics.\n'
    external = ''
    if mixed:
        external = '\n### Separate external evaluations (seed 42)\n\n| Evaluation dataset | Rows | Macro F1 | Positive recall |\n|---|---:|---:|---:|\n'
        external += '\n'.join(f"| {r['test_dataset']} | {r['test_rows']} | {float(r['f1_macro']):.4f} | {float(r['recall_positive']):.4f} |" for r in summary['mixed_external_evaluation'])
        external += '\n\nThese use the project evaluation harness and its cleaning/deduplication policy; CM has 415 evaluation rows here versus 424 in matched training evaluation. They are distinct from the internal mixture scores.\n'
    return f'''---
language:
- hi
- en
library_name: transformers
pipeline_tag: text-classification
base_model: {BASES[row['family']]}
tags:
- hinglish
- code-mixed
- research
- hate-speech-detection
---
# {row['family']} — {title}

Research checkpoint by Om Patnaik comparing mBERT and MuRIL across Hinglish hate/offensive-language datasets. Fine-tuned BERT sequence classifier with two labels.

**This revision contains seed {row['seed']}.** `main` defaults to seed 42 for consistency, not because it has the best test score. Available seed revisions: {', '.join('`seed-'+str(p['seed'])+'`' for p in sorted(peers,key=lambda p:p['seed']))}.
{warning}
## Task and labels

- Class 0: `{labels[0]}`
- Class 1: `{labels[1]}`

Kaggle positives mean hate; CM positives mean offensive language; THAR positives mean AntiReligion content (targeted religious hate). {'This mixture combines these numeric labels; POSITIVE is not a single consistent definition of hate.' if mixed else 'Interpret this classifier using its own training dataset definition.'} Scores are model softmax outputs, not calibrated certainty or judgments about a person.

## Data and attribution

- [Kaggle dataset by Shardul Dhekane]({SOURCES['kaggle']}) — processed Hinglish subset, 4,780 rows; source platform/provenance needs further review.
- [CM source repository]({SOURCES['cm']}) — Hindi-English political/social Twitter/X offensive-language data, 3,900 processed rows.
- [THAR source repository]({SOURCES['thar']}) and [paper](https://doi.org/10.1145/3653017) — religious hate in Hindi-English YouTube comments, 11,549 rows.

The training condition for this repository is **{title}** (`{ds}`). Sources above describe the overall study; only the source(s) named in this condition were used for this checkpoint. No dataset text is included in this model repository.

## Training and evaluation

See `training_metadata.json` for this run's settings, row counts, split policy and any reconstructed fields. Runs used two training epochs; the script restores the epoch with the highest evaluation Macro F1. The exported weights may therefore come from an earlier epoch.

{split}

**Evaluation limitation:** the training script evaluates each epoch on this evaluation split and uses it to choose the checkpoint. In CM this includes the source test split. The following scores are therefore selection-set results, not an untouched final test estimate. The training seed was supplied to Trainer; exact reproduction of classifier initialization and device behavior is not guaranteed.

### Internal / matched evaluation recorded with checkpoints

| Seed | Accuracy | Macro F1 | Positive F1 | Positive recall |
|---:|---:|---:|---:|---:|
{table}
{aggregate}
All scores above come directly from the saved `eval_metrics.json` files. Historical `*_hate` keys mean the dataset-specific positive class. The 79-row diagnostic probe is excluded from these claims.
{external}
## Usage

Install packages from `requirements.txt`. While this repository is private, sign in with `hf auth login` as an authorized account before loading.

```python
import re
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

repo = "{row['repo_id']}"
revision = "seed-{row['seed']}"  # use "main" for the default seed 42
tokenizer = AutoTokenizer.from_pretrained(repo, revision=revision)
model = AutoModelForSequenceClassification.from_pretrained(repo, revision=revision)
model.eval()

def clean(text):
    text = re.sub(r"http\\S+|www\\S+|https\\S+", " URL ", str(text))
    text = re.sub(r"@\\w+", " USER ", text)
    return re.sub(r"\\s+", " ", text).strip()

text = clean("Aaj ka din accha tha.")
inputs = tokenizer(text, return_tensors="pt", padding="max_length",
                   truncation=True, max_length=128)
with torch.inference_mode():
    scores = model(**inputs).logits.softmax(dim=-1)[0]
print({{model.config.id2label[i]: float(score) for i, score in enumerate(scores)}})
```

Preprocessing preserves case, replaces URLs with `URL`, handles with `USER`, and collapses whitespace. Truncation is 128 tokens including special tokens.

## Intended use and limitations

Use for research, comparison and error analysis. Cross-dataset generalization is limited; label definitions and platforms differ, duplicates exist in CM, and annotation/source uncertainties remain. Identity words, transliteration, quoted abuse and missing conversation context can cause errors. These checkpoints have not been validated for autonomous moderation or decisions about individuals. Single-seed mixed results do not establish seed robustness.

## Release status and licensing

Private research archive. Both base-model cards declare Apache-2.0 ([mBERT](https://huggingface.co/google-bert/bert-base-multilingual-cased), [MuRIL](https://huggingface.co/google/muril-base-cased)). A license for these fine-tuned releases has not yet been assigned: training-source terms and public redistribution conditions still need review, including the unresolved CM license. The base-model license is not a license grant for the datasets. No public reuse or commercial-use permission is asserted by this private draft.

## Reproducibility and project

- [Research code]({CODE}), source snapshot `{commit}`.
- [Working paper draft]({CODE}/blob/{commit}/paper/application_research_draft.md).
- [Dataset registry]({CODE}/blob/{commit}/docs/dataset_registry.md).
- [Model registry and failure cases]({CODE}/blob/{commit}/docs/model_registry.md).
- `release_metadata.json` records original checkpoint identity and SHA-256. Weights are unmodified; label names were added to the exported configuration.
- Seeds 42 for the two Kaggle models have reconstructed metadata, with provenance and uncertainty recorded in their metadata files.

### Tools Note

AI tools were used for coding, debugging, and documentation assistance; the research direction, result interpretation, and final claims were reviewed and owned by Om Patnaik.
'''


def validate():
    import torch
    from transformers import AutoTokenizer, AutoModelForSequenceClassification
    torch.set_num_threads(4)
    manifest = read(MANIFEST)
    for row in manifest['checkpoints']:
        folder = ROOT / row['stage']
        tok = AutoTokenizer.from_pretrained(folder, local_files_only=True)
        model, info = AutoModelForSequenceClassification.from_pretrained(folder, local_files_only=True, output_loading_info=True)
        assert not any(info[k] for k in ['missing_keys', 'unexpected_keys', 'mismatched_keys', 'error_msgs']), info
        model.eval()
        inputs = tok([clean('Aaj ka din accha tha.'), clean('@friend https://example.com Kal milte hain.')],
                     padding='max_length', truncation=True, max_length=128, return_tensors='pt')
        with torch.inference_mode():
            scores = model(**inputs).logits.softmax(-1)
        assert scores.shape == (2, 2) and torch.isfinite(scores).all()
        assert torch.allclose(scores.sum(-1), torch.ones(2), atol=1e-6)
        row['local_validation'] = {'status': 'passed', 'probabilities': scores.tolist()}
        row['file_sha256'] = {p.name: sha(p) for p in folder.iterdir() if p.name in FILES}
        assert row['file_sha256']['model.safetensors'] == row['weights_sha256']
        write(MANIFEST, manifest)
        print('VALIDATED', row['repo_id'], row['seed'], flush=True)
        del model, tok
        gc.collect()


def upload():
    from huggingface_hub import HfApi
    api = HfApi()
    assert api.whoami()['name'] == 'OmTheLast'
    manifest = read(MANIFEST)
    assert all(r.get('local_validation', {}).get('status') == 'passed' for r in manifest['checkpoints'])
    for repo in sorted({r['repo_id'] for r in manifest['checkpoints']}):
        api.create_repo(repo_id=repo, private=True, exist_ok=True)
        assert api.model_info(repo).private, f'Refusing to write a public repository: {repo}'
        rows = sorted([r for r in manifest['checkpoints'] if r['repo_id'] == repo], key=lambda r:(r['seed'] != 42, r['seed']))
        for row in rows:
            revision = 'main' if row['seed'] == 42 else f"seed-{row['seed']}"
            if row.get('uploaded_commit'):
                assert api.model_info(repo, revision=revision).sha == row['uploaded_commit']
                continue
            if revision != 'main':
                api.create_branch(repo_id=repo, branch=revision, exist_ok=True)
            print('UPLOADING', repo, revision, flush=True)
            result = api.upload_folder(repo_id=repo, folder_path=ROOT / row['stage'], revision=revision,
                                       allow_patterns=FILES, commit_message=f"Archive validated research checkpoint, seed {row['seed']}")
            if row['seed'] == 42:
                api.create_branch(repo_id=repo, branch='seed-42', revision=result.oid, exist_ok=True)
            row['uploaded_commit'] = result.oid
            row['uploaded_revision'] = revision
            write(MANIFEST, manifest)
            print('UPLOADED', repo, revision, result.oid, flush=True)


def publish():
    """Publish existing archives after an explicit request; transfer metadata only."""
    import requests
    from huggingface_hub import HfApi, CommitOperationAdd
    api = HfApi()
    assert api.whoami()['name'] == 'OmTheLast'
    manifest = read(MANIFEST)
    response = requests.get('https://www.apache.org/licenses/LICENSE-2.0.txt', timeout=30)
    response.raise_for_status()
    license_text = response.text
    assert 'Apache License' in license_text and 'Version 2.0' in license_text
    rows = sorted(manifest['checkpoints'], key=lambda r: (r['repo_id'], r['seed'] != 42, r['seed']))
    for row in rows:
        repo = row['repo_id']; dest = ROOT / row['stage']
        revision = row['uploaded_revision']
        if not row.get('public_metadata_commit'):
            card_path = dest / 'README.md'
            card_text = card_path.read_text()
            card_text = card_text.replace(
                'While this repository is private, sign in with `hf auth login` as an authorized account before loading.',
                'This repository is public and can be loaded without a Hugging Face login.')
            card_text = card_text.replace('Private research archive.', 'Public research checkpoint release.')
            card_text = card_text.replace(
                'training-source terms and public redistribution conditions still need review, including the unresolved CM license.',
                'training-source terms remain under review, including the unresolved CM and THAR licenses.')
            card_text = card_text.replace(
                'No public reuse or commercial-use permission is asserted by this private draft.',
                'Public access does not assign a new license to the fine-tuned releases or their training data. '
                'The upstream Apache-2.0 license is included in `BASE_MODEL_LICENSE.txt`; see `BASE_MODEL_NOTICE.md` for attribution.')
            assert 'private draft' not in card_text and 'Private research archive' not in card_text
            card_path.write_text(card_text)
            metadata = read(dest / 'release_metadata.json')
            metadata['release_status'] = 'Public research release; fine-tuned-model license unspecified; dataset terms under review.'
            write(dest / 'release_metadata.json', metadata)
            (dest / 'BASE_MODEL_LICENSE.txt').write_text(license_text)
            (dest / 'BASE_MODEL_NOTICE.md').write_text(
                f"# Base model attribution\n\nBase model: [{BASES[row['family']]}](https://huggingface.co/{BASES[row['family']]}).\n\n"
                "The upstream model card declares Apache-2.0. The accompanying license text is reproduced from "
                "https://www.apache.org/licenses/LICENSE-2.0.txt.\n\n"
                "Om Patnaik fine-tuned the base model for the dataset condition described in README.md. "
                "Weights differ from the base model, and descriptive classifier labels were added to the exported configuration. "
                "This notice does not license the third-party datasets or assign a separate fine-tuned-model license.\n")
            names = ['README.md', 'release_metadata.json', 'BASE_MODEL_LICENSE.txt', 'BASE_MODEL_NOTICE.md']
            result = api.create_commit(repo_id=repo, revision=revision, parent_commit=row['uploaded_commit'],
                operations=[CommitOperationAdd(path_in_repo=n, path_or_fileobj=dest / n) for n in names],
                commit_message='Document public research release and upstream attribution')
            row.setdefault('archive_commit', row['uploaded_commit'])
            row['uploaded_commit'] = row['public_metadata_commit'] = result.oid
            row['file_sha256'].update({n: sha(dest / n) for n in names})
            row['remote_verification'] = 'pending public-release verification'
            write(MANIFEST, manifest)
        if row['seed'] == 42:
            refs = {b.name: b.target_commit for b in api.list_repo_refs(repo).branches}
            if refs.get('seed-42') != row['uploaded_commit']:
                if 'seed-42' in refs:
                    api.delete_branch(repo_id=repo, branch='seed-42')
                api.create_branch(repo_id=repo, branch='seed-42', revision=row['uploaded_commit'])
        print('PUBLIC CARD READY', repo, revision, flush=True)
    for repo in sorted({r['repo_id'] for r in rows}):
        api.update_repo_settings(repo_id=repo, private=False, gated=False)
        assert api.model_info(repo, token=False).private is False
        print('PUBLIC', repo, flush=True)
    collection_path = ROOT / 'docs/huggingface_collection.json'
    collection = read(collection_path)
    api.update_collection_metadata(collection['slug'], private=False)
    assert api.get_collection(collection['slug'], token=False).private is False
    collection['private'] = False
    write(collection_path, collection)
    manifest['private'] = False
    manifest['release_status'] = 'public_release_pending_verification'
    write(MANIFEST, manifest)


def polish():
    """Apply a concise public overview while retaining detailed model documentation."""
    from huggingface_hub import HfApi, CommitOperationAdd, ModelCard
    api = HfApi()
    assert api.whoami()['name'] == 'OmTheLast'
    manifest = read(MANIFEST)
    assert manifest['private'] is False
    for row in manifest['checkpoints']:
        dest = ROOT / row['stage']; path = dest / 'README.md'
        if not row.get('presentation_commit'):
            original = path.read_text()
            # Keep the previous card as a local recovery copy, outside the upload allowlist.
            backup = dest / 'README.before-presentation.md'
            if not backup.exists():
                backup.write_text(original)
            original = backup.read_text()
            frontmatter = original.split('---', 2)[1]
            sections = dict(re.findall(r'^## ([^\n]+)\n\n(.*?)(?=^## |\Z)', original, re.M | re.S))
            family = {'mbert': 'mBERT', 'muril': 'MuRIL'}[row['family']]
            short, title, labels = DATA[row['dataset']]
            peers = sorted(r['seed'] for r in manifest['checkpoints'] if r['repo_id'] == row['repo_id'])
            revisions = ', '.join(f'`seed-{s}`' for s in peers)
            condition = row['dataset']
            source_keys = ['kaggle', 'cm', 'thar'] if short == 'mixed-all-three' else [s for s in SOURCES if s in short.split('-')]
            sources = ' · '.join(f'[{s.upper() if s != "kaggle" else "Kaggle"}]({SOURCES[s]})' for s in source_keys)
            warning = ''
            if row['family'] == 'muril' and condition in ['mixed_kaggle_plus_cm', 'mixed_cm_plus_thar']:
                warning = '\n**Known failure:** all-negative predictions on the reported primary external evaluations. Preserved for error analysis.\n'
            mixed_note = ' Mixture labels combine different source definitions of hate and offense.' if condition.startswith('mixed') else ''
            overview = f'''---{frontmatter}---
# {family}: {title}

{family} fine-tuned for binary classification of Hindi–English code-mixed text on **{title}**. Part of a comparative study of dataset transfer, training mixtures and seed variation.

[Research code]({CODE}) · [Results]({CODE}/blob/main/docs/matched_multiseed_results.md)

- **Labels:** `0 = {labels[0]}`, `1 = {labels[1]}`.{mixed_note}
- **Revision:** seed {row['seed']}; `main` defaults to seed 42. Available: {revisions}.
- **Training sources:** {sources}. No dataset text is included.
{warning}
## Evaluation

Evaluation splits also guided checkpoint selection; the recorded internal scores are not untouched final-test estimates. Cross-dataset results and label definitions should be interpreted separately.

'''
            summary = read(dest / 'evaluation_summary.json')
            overview += '| Seed | Macro F1 | Positive recall |\n|---:|---:|---:|\n'
            for metric in sorted(summary['per_seed'], key=lambda m: m['seed']):
                overview += f"| {metric['seed']} | {metric['eval_f1_macro']:.4f} | {metric['eval_recall_hate']:.4f} |\n"
            if 'aggregate' in summary:
                a = summary['aggregate']['eval_f1_macro']
                overview += f"\nMean Macro F1: **{a['mean']:.4f} ± {a['sample_std']:.4f}** (sample standard deviation).\n"
            overview += '\n## Limitations\n\n' + sections['Intended use and limitations'].strip() + '\n\n'
            for heading, body in [
                ('Loading and preprocessing', sections['Usage']),
                ('Training details and full evaluation', sections['Training and evaluation']),
                ('Licensing and provenance', sections['Release status and licensing'] + '\n' + sections['Reproducibility and project']),
            ]:
                body = body.replace('project evaluation harness', 'evaluation harness').replace('project model registry', 'model registry')
                overview += f'<details>\n<summary>{heading}</summary>\n\n{body.strip()}\n\n</details>\n\n'
            assert not re.search(r'\b(college|applications|projects?)\b', overview, re.I)
            path.write_text(overview)
            ModelCard.load(str(path))
            result = api.create_commit(repo_id=row['repo_id'], revision=row['uploaded_revision'],
                parent_commit=row['uploaded_commit'],
                operations=[CommitOperationAdd(path_in_repo='README.md', path_or_fileobj=path)],
                commit_message='Clarify research overview, results and reproducibility details')
            row['uploaded_commit'] = row['presentation_commit'] = result.oid
            row['file_sha256']['README.md'] = sha(path)
            row['remote_verification'] = 'pending presentation verification'
            write(MANIFEST, manifest)
        if row['seed'] == 42:
            refs = {b.name: b.target_commit for b in api.list_repo_refs(row['repo_id']).branches}
            if refs.get('seed-42') != row['uploaded_commit']:
                if 'seed-42' in refs:
                    api.delete_branch(repo_id=row['repo_id'], branch='seed-42')
                api.create_branch(repo_id=row['repo_id'], branch='seed-42', revision=row['uploaded_commit'])
        print('PRESENTATION UPDATED', row['repo_id'], row['seed'], flush=True)
    collection_path = ROOT / 'docs/huggingface_collection.json'
    collection = read(collection_path)
    collection['title'] = 'Hinglish Hate Speech: mBERT vs MuRIL'
    collection['description'] = '26 research checkpoints comparing mBERT and MuRIL across Hinglish datasets, training mixtures, and random seeds.'
    api.update_collection_metadata(collection['slug'], title=collection['title'],
                                   description=collection['description'], private=False)
    write(collection_path, collection)


def verify():
    from huggingface_hub import HfApi, hf_hub_download
    api = HfApi(); manifest = read(MANIFEST)
    for row in manifest['checkpoints']:
        repo = row['repo_id']; rev = f"seed-{row['seed']}"
        token = None if manifest['private'] else False
        info = api.model_info(repo, revision=rev, files_metadata=True, token=token)
        assert info.private == manifest['private'] and info.sha == row['uploaded_commit']
        siblings = {f.rfilename: f for f in info.siblings}
        names = set(row['file_sha256'])
        assert names.issubset(siblings)
        assert set(siblings).issubset(names | {'.gitattributes'}), (repo, rev, 'unexpected remote files')
        for name in sorted(names):
            remote = siblings[name]
            if remote.lfs:
                assert remote.lfs.sha256 == row['file_sha256'][name], (repo, rev, name)
            elif row.get('presentation_commit') and name != 'README.md':
                # Unchanged small artifacts were downloaded during initial verification.
                # Compare both the staged SHA-256 and Git content hash on later card edits.
                contents = (ROOT / row['stage'] / name).read_bytes()
                assert hashlib.sha256(contents).hexdigest() == row['file_sha256'][name]
                blob = hashlib.sha1(f'blob {len(contents)}\0'.encode() + contents).hexdigest()
                assert remote.blob_id == blob, (repo, rev, name)
            else:
                path = Path(hf_hub_download(repo, name, revision=info.sha, token=token))
                assert sha(path) == row['file_sha256'][name], (repo, rev, name)
        if row['seed'] == 42:
            assert api.model_info(repo, revision='main', token=token).sha == info.sha
        visibility = 'private' if manifest['private'] else 'public (anonymous access verified)'
        row['remote_verification'] = f'passed: all file hashes and seed revision match; repository {visibility}'
        write(MANIFEST, manifest)
        print('VERIFIED', repo, rev, flush=True)
    manifest['release_status'] = 'verified_private_archive' if manifest['private'] else 'verified_public_release'
    write(MANIFEST, manifest)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['prepare', 'validate', 'upload', 'publish', 'polish', 'verify'])
    args = parser.parse_args()
    globals()[args.action]()
