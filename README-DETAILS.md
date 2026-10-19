# mBERT vs MuRIL: Cross-Dataset Hinglish Hate Speech

A comparative study of multilingual and Indian-language pretraining for Hinglish hate and offensive-language detection.

[Models on Hugging Face](https://huggingface.co/collections/OmTheLast/hinglish-research-mbert-vs-muril-6aa96a16ed03bba0e89e9408) · [Working paper](paper/application_research_draft.md) · [One-page summary](output/pdf/one_page_research_summary.pdf) · [Detailed results](docs/matched_multiseed_results.md)

## Research question

Does MuRIL outperform mBERT consistently when the dataset, label definition, and evaluation domain change?

## Main finding

Model ranking depends on the dataset. mBERT scores higher on Kaggle and narrowly on CM; MuRIL scores higher on THAR. Cross-dataset results show limited generalization, with hate, offense, and targeted religious hate representing different classification tasks.

| Dataset | Positive label | mBERT Macro F1 | MuRIL Macro F1 |
|---|---|---:|---:|
| Kaggle Hinglish | Hate | 67.5% ± 2.1% | 58.1% ± 5.7% |
| CM code-mixed | Offensive | 77.7% ± 1.9% | 76.1% ± 2.3% |
| THAR | AntiReligion | 74.7% ± 0.1% | 76.5% ± 1.3% |

Values are matched evaluation means ± sample standard deviations across seeds **7, 13, and 42**. Macro F1 gives each class equal weight. These evaluation splits also guided best-epoch selection, so the figures are **not results on an untouched final test set**. Kaggle and THAR seeds change split membership as well as training randomness.

## Method

- Fine-tune **mBERT** and **MuRIL** on three datasets with distinct label definitions.
- Compare matched multi-seed runs, cross-dataset transfer, four training mixtures, and TF-IDF baselines.
- Analyze positive-class recall, errors, duplicate text, and collapsed prediction behavior.

Dataset sources and mappings are documented in the [dataset registry](docs/dataset_registry.md). The [results analysis](docs/result_analysis_report.md) covers transfer and mixed training; the table above uses the newer multi-seed summary.

## Released models

**26 checkpoints across 14 public Hugging Face repositories.** Seeds 7, 13, and 42 are preserved where available; `main` defaults to seed 42. Each model card includes training details, per-seed scores, label definitions, loading code, and limitations.

[Browse the collection](https://huggingface.co/collections/OmTheLast/hinglish-research-mbert-vs-muril-6aa96a16ed03bba0e89e9408) · [Model index and verification](docs/huggingface_release.md)

## Limitations

The label definitions differ across datasets. Matched evaluation data was reused for epoch selection; mixed-training and transfer evidence is mostly single-seed. Two MuRIL mixtures produced all-negative external predictions. The 79-row diagnostic probe is excluded from primary conclusions. Fine-tuned-model licensing and training-source terms are documented in the model cards.

## Reproduce and inspect

- [Setup and experiment commands](docs/running_experiments.md)
- [Training runner](experiments/train_transformer.py) · [Evaluation harness](experiments/run_model_harness.py)
- [Per-seed results](results/multiseed/matched_multiseed_per_seed.csv) · [Aggregate results](results/multiseed/matched_multiseed_summary.csv)
- [Research roadmap](docs/research_rigor_roadmap.md) · [Research journal](docs/research_journal.md)
- [Internal arXiv readiness checks](docs/internal_arxiv_checks.md)
- [Earlier single-dataset study](https://github.com/OmTheLast/mBERT-vs-MuRIL-in-detecting-hatespeech)

Code and analysis by **Om Patnaik**. This is an ongoing research study; the linked manuscript is a working draft.

### Tools Note

AI tools were used for coding, debugging, and documentation assistance; the research direction, result interpretation, and final claims were reviewed and owned by Om Patnaik.
