# Cross-Dataset Evaluation of mBERT and MuRIL for Hinglish and Hindi-English Harmful Speech Detection

Working Paper Draft v0.3: 2026-08-27

This is an application research draft, not a published paper.

Author: Om Patnaik

## Abstract

Hinglish and Hindi-English code-mixed harmful-speech detection is difficult because online text varies across language, script, platform, topic, and annotation policy. This project compares mBERT, a general multilingual BERT model, with MuRIL, an Indian-language-focused model, for binary harmful-speech classification across three dataset situations: a Kaggle Hinglish hate subset, a CM code-mixed offensive dataset, and THAR targeted religious hate. The strongest evidence comes from matched multi-seed experiments using seeds `7`, `13`, and `42`: mBERT outperforms MuRIL on Kaggle Hinglish hate, mBERT narrowly outperforms MuRIL on CM code-mixed/offensive data, and MuRIL outperforms mBERT on THAR targeted religious hate. Cross-dataset, TF-IDF baseline, and mixed-training results show that label definition, platform, topic, and script mix strongly affect model behavior. The central claim is therefore conditional rather than universal: neither mBERT nor MuRIL is globally better for Hinglish harmful-speech detection under the current evidence.

## 1. Introduction

Hindi-English code-mixed text is common in Indian and South Asian online spaces. A single post may combine English, Romanized Hindi, Devanagari, slang, emojis, usernames, hashtags, and platform-specific context. This makes harmful-speech detection harder than ordinary binary text classification because the model must handle noisy multilingual input and unstable definitions of harm.

The project began with a direct question: whether MuRIL, because it is focused on Indian languages, would be better than mBERT for Hinglish hate-speech detection. As more datasets were added, the question became more interesting. The winner changed depending on the dataset. This shifted the project from a simple model comparison into a study of cross-dataset robustness.

The current research claim is not that mBERT is better in general or that MuRIL is better in general. The claim is that model ranking depends on dataset situation. A dataset situation includes the positive-label meaning, platform, topic/domain, script composition, and whether the model is tested in-domain or transferred from another dataset.

## 2. Research Question

The main research question is:

> Does Indian-language-specific pretraining in MuRIL improve hate/offensive speech detection for Hinglish and Hindi-English code-mixed text compared with general multilingual pretraining in mBERT?

The current answer is conditional:

- mBERT performs better on the matched Kaggle Hinglish hate condition.
- mBERT narrowly performs better on the matched CM code-mixed/offensive condition.
- MuRIL performs better on the matched THAR targeted religious-hate condition.
- Cross-dataset and mixed-training results show that label definition and dataset domain strongly affect model behavior.

[OM VERIFY] The final introduction should include Om's own wording for why this question matters personally or academically.

## 3. Related Work / Background

BERT introduced deep bidirectional Transformer pretraining for language understanding tasks and provides the base architecture behind many later text classifiers [@devlin2019bert]. mBERT extends this style of pretraining to many languages and is commonly used as a multilingual baseline.

MuRIL was developed for Indian-language representation learning and includes Indian-language and transliterated signals that make it a natural candidate for Hinglish and Hindi-English code-mixed classification [@khanuja2021muril]. The comparison between mBERT and MuRIL is therefore meaningful because Hinglish sits between English, Hindi, Romanized Hindi, and Indian social media usage.

Prior Hindi-English code-mixed hate-speech work, including Bohra et al., shows that code-mixed harmful-speech detection cannot be treated as ordinary English hate-speech detection [@bohra2018dataset]. This project builds on that idea but focuses specifically on whether the relative ranking of mBERT and MuRIL remains stable across datasets.

The dataset sources used here include the Kaggle Code-Mixed Hinglish Hate Speech Detection Dataset [@dhekane2024kaggle], the CM hate-speech repository [@cmrepo2024], and the THAR targeted religious-hate dataset [@sharma2024thar; @tharrepo2024]. [OM VERIFY] Dataset licenses, full author metadata, and redistribution rules still need final checking before public final release.

## 4. Datasets

The project uses three primary source-backed datasets. The 79-row benchmark is retained only as a diagnostic probe and excluded from primary claims.

| Dataset ID | Rows | Positive label | Platform/domain | Script profile | Paper role |
|---|---:|---|---|---|---|
| `kaggle_hinglish_hate` | 4,780 | hate | mixed/unclear from local metadata | 100% Latin script in processed subset | primary matched Hinglish hate condition |
| `cm_splits_codemixed` | 3,900 | offensive | Indian politics / Twitter/X | mostly Latin with some mixed Latin-Devanagari | external code-mixed offensive condition |
| `thar_religion` | 11,549 | AntiReligion | YouTube religious comments | mostly Latin, meaningful Devanagari portion | targeted religious-hate condition |
| `existing_79_row_benchmark` | 79 | hate | unclear/manual/artificial | 100% Latin script | diagnostic only |

### 4.1 Kaggle Hinglish Hate

The Kaggle dataset is used as the closest dataset to the original project aim: Hinglish hate/non-hate classification. The local processed file contains 4,780 Hinglish rows, with 2,914 negative examples and 1,866 positive examples. Its processed subset is 100% Latin script. This matters because MuRIL's Indian-language pretraining may not automatically help when the task is heavily Romanized and resembles Latin-script social media.

### 4.2 CM Code-Mixed Offensive

The CM dataset contains Indian politics and social-media text from Twitter/X. Its project label is mapped from `offense`, so its positive class is hate-adjacent rather than strict hate speech. The processed file contains 3,900 rows, with 2,455 negatives and 1,445 positives. This dataset is useful because it adds a strong Indian-context code-mixed condition, but it should not be treated as semantically identical to strict hate speech.

### 4.3 THAR Targeted Religious Hate

THAR is a targeted religious-hate dataset from YouTube comments. Its positive class is `AntiReligion`, not general hate or general offensive language. The processed file contains 11,549 rows, with 6,095 negatives and 5,454 positives. THAR is narrower than the other datasets, but that narrowness is methodologically useful because it tests whether MuRIL performs better in a targeted Indian-language harmful-speech situation.

### 4.4 Diagnostic 79-Row Probe

The 79-row benchmark is excluded from primary results because its provenance is uncertain, it may be manually written or AI-generated, it contains duplicate rows, and its labels may not consistently represent targeted hate. It remains useful as a lesson: small unclear benchmarks can produce unstable model rankings and misleading confidence.

## 5. Models And Baselines

The transformer models are:

- mBERT: `bert-base-multilingual-cased`
- MuRIL: `google/muril-base-cased`

Both are fine-tuned as binary sequence classifiers. The project also includes TF-IDF baselines:

- TF-IDF with Logistic Regression
- TF-IDF with Linear SVM

The baselines matter because harmful-speech datasets often contain strong lexical cues: repeated slurs, slogans, target-group terms, political phrases, and platform-specific patterns. If a TF-IDF model performs competitively, then transformer gains should not be exaggerated.

## 6. Methodology

The experiments use binary labels (`0` and `1`) across all datasets, but the meaning of `1` differs. This is intentional and documented: the project tests robustness across harmful-speech dataset situations, not one perfectly harmonized hate-speech ontology.

Transformer training used a controlled first-pass configuration:

| Setting | Value |
|---|---|
| Epochs | 2 |
| Learning rate | 2e-5 |
| Maximum sequence length | 128 |
| Batch size on Mac MPS | 8 |
| Matched multi-seed seeds | 7, 13, 42 |

Two epochs were used as a controlled first-pass setting across model/dataset combinations. The project prioritized comparable coverage across matched, cross-dataset, and mixed-training conditions over extensive hyperparameter tuning. Future work should test validation-based early stopping, additional epoch counts, threshold tuning, and class weighting.

The primary metric is Macro F1 because it averages performance across both classes and is less misleading than accuracy under class imbalance. Positive recall is also tracked because false negatives are harmful examples that the model misses. In harmful-speech detection, a high false-negative rate means the system is too hesitant to flag harmful content.

## 7. Results

### 7.1 Matched Multi-Seed Results

The matched multi-seed results are the strongest evidence in the repository because they repeat the primary matched comparison across seeds `7`, `13`, and `42`.

| Dataset | Better model | mBERT Macro F1 | MuRIL Macro F1 | mBERT positive recall | MuRIL positive recall | Interpretation |
|---|---|---:|---:|---:|---:|---|
| `kaggle_hinglish_hate` | mBERT | 67.5 +/- 2.1 | 58.1 +/- 5.7 | 46.9 +/- 8.5 | 25.1 +/- 8.5 | mBERT has a clear matched advantage; MuRIL misses many positives |
| `cm_splits_codemixed` | mBERT, narrowly | 77.7 +/- 1.9 | 76.1 +/- 2.3 | 70.7 +/- 1.3 | 64.4 +/- 8.3 | both are competitive; mBERT is slightly stronger and more stable |
| `thar_religion` | MuRIL | 74.7 +/- 0.1 | 76.5 +/- 1.3 | 79.3 +/- 2.0 | 79.7 +/- 0.6 | MuRIL wins targeted religious hate across seeds |

These results do not support a universal winner. They show that mBERT is stronger on the Latin-script-heavy Kaggle condition and narrowly stronger on CM, while MuRIL is stronger on targeted religious hate.

### 7.2 Cross-Dataset Results

The cross-dataset results are mostly single-seed evidence and should be treated as weaker than the matched multi-seed table. They are still important because they test whether a model trained on one dataset situation works on another.

The largest generalization gaps occur when models are trained on one positive-label definition and evaluated on another. Examples from the result analysis include:

| Model | Train dataset | Test dataset | Matched Macro F1 | Transfer Macro F1 | Gap |
|---|---|---|---:|---:|---:|
| MuRIL | `thar_religion` | `kaggle_hinglish_hate` | 77.9 | 46.2 | 31.7 |
| mBERT | `thar_religion` | `kaggle_hinglish_hate` | 74.8 | 45.5 | 29.3 |
| mBERT | `cm_splits_codemixed` | `kaggle_hinglish_hate` | 78.3 | 51.6 | 26.6 |
| mBERT | `kaggle_hinglish_hate` | `thar_religion` | 65.6 | 44.8 | 20.8 |

This is the main evidence that cross-dataset robustness is weak. THAR-trained models do not become general Hinglish hate detectors, and Kaggle-trained models do not transfer cleanly to targeted religious hate.

[OM VERIFY] Cross-dataset rows in `docs/result_analysis_report.md` use the earlier seed-42 matched/cross-dataset matrix. They should be described as single-seed transfer evidence unless rerun under the multi-seed harness.

### 7.3 TF-IDF Baseline Comparison

TF-IDF baselines are competitive in several settings. For example:

| Train dataset | Test dataset | Best transformer Macro F1 | Best TF-IDF Macro F1 | Transformer minus baseline |
|---|---|---:|---:|---:|
| `cm_splits_codemixed` | `cm_splits_codemixed` | 78.3 | 77.6 | +0.7 |
| `kaggle_hinglish_hate` | `thar_religion` | 44.8 | 49.9 | -5.2 |
| `thar_religion` | `kaggle_hinglish_hate` | 46.2 | 51.0 | -4.9 |
| `thar_religion` | `thar_religion` | 77.9 | 70.6 | +7.3 |

These results matter because they prevent overclaiming. Transformers are strongest in matched conditions, but simple lexical models can beat them in some transfer settings. This suggests that dataset-specific lexical cues, slogans, and target terms play a large role.

### 7.4 Mixed-Dataset Training Results

Mixed-training results are currently single-seed evidence. They should be presented as exploratory robustness tests, not as final settled claims.

| Mixed train condition | Main mBERT behavior | Main MuRIL behavior | Interpretation |
|---|---|---|---|
| Kaggle + CM | mBERT improves Kaggle over Kaggle-only seed-42 and remains usable on CM, but weak on THAR | MuRIL collapses to all-negative predictions | related datasets can still produce model-specific instability |
| CM + THAR | mBERT remains strong on CM and THAR, weak on Kaggle | MuRIL collapses to all-negative predictions | MuRIL collapse is serious under this mixture |
| Kaggle + THAR | both models learn; mBERT slightly wins Kaggle, MuRIL wins THAR and CM | MuRIL does not collapse | collapse is condition-dependent, not universal |
| Kaggle + CM + THAR | both models learn; mBERT leads Kaggle/CM, MuRIL leads THAR | MuRIL stable and strong on THAR | broader mixing helps but does not solve robustness |

The key result is not simply that mixed data helps. Mixed data can help, hurt, or destabilize training depending on source balance and label compatibility.

## 8. Error Analysis

The error analysis shows that many failures are not random. They are linked to label mismatch, script, topic, and missing context.

Quantitative error analysis shows that:

- Kaggle-trained models miss many THAR positives, so broad Hinglish hate training does not transfer cleanly to targeted religious hate.
- THAR-trained models miss many Kaggle positives, so targeted religious hate training does not create a general Hinglish hate detector.
- mBERT tends to have lower false-negative rates on matched Kaggle and CM conditions.
- MuRIL tends to have lower false-negative rates on matched THAR and THAR-to-CM transfer.
- Devanagari-only rows show high false-negative rates, which supports further script-specific analysis.

First-pass manual coding found that many sampled errors involve cross-dataset label mismatch. The largest manual category was `cross_dataset_label_mismatch`, appearing in 191 coded rows, or 67.0% of the coded sample. Other recurring categories included generic profanity or abuse, target-group/religion cues, political context or slogans, short/contextless text, and script complexity.

The qualitative lesson is that hate, offensive, and AntiReligion labels are not interchangeable. A text may be offensive but not targeted hate, or religious in topic but not anti-religion hate. Models trained on one label policy often fail when evaluated under another.

[OM VERIFY] Before a final professor-facing version, choose 8-12 anonymized or paraphrased error examples that Om has personally reviewed. Do not include offensive examples verbatim unless necessary and safely masked.

## 9. Discussion

The central result is conditional model ranking. mBERT does better on the Kaggle and CM matched settings, while MuRIL does better on THAR. This is not a contradiction to hide. It is the research finding.

One likely explanation is script/domain alignment. The processed Kaggle dataset is entirely Latin script, and CM is mostly Latin-script political/social media text. mBERT may handle these Latin-script, English-adjacent subword patterns better. MuRIL's Indian-language-focused pretraining does not automatically help when the task is heavily Romanized and broad.

THAR is different. It is targeted religious hate, includes a meaningful Devanagari portion, and focuses on Indian religious group references. MuRIL's stronger THAR performance may reflect better alignment with Indian-language cues and target-domain signals. However, this should remain a cautious interpretation, not a causal proof.

The mixed-training results deepen the story. MuRIL collapses under some mixtures but not others, especially recovering when THAR is included with Kaggle or all three datasets. This suggests that model behavior depends on label compatibility, source balance, threshold/decision boundary behavior, and the training mixture, not only on model architecture.

The TF-IDF results show that lexical cues remain powerful. A transformer that beats another transformer by a few points should still be compared against lexical baselines, especially when cross-dataset transfer rewards simple keyword overlap.

## 10. Limitations

The main limitation is label comparability. `hate`, `offensive`, and `AntiReligion` are related harmful-speech labels, but they do not define the same task. This limits any universal claim about model superiority.

Other limitations:

- Mixed-training and cross-dataset transformer results are mostly single-seed evidence.
- Only the main matched settings currently have three-seed means and standard deviations.
- Hyperparameters were controlled rather than extensively tuned.
- No confidence intervals or bootstrap intervals have been added yet.
- Threshold tuning and class weighting need further investigation, especially for MuRIL collapse conditions.
- Dataset license and citation details still need final verification.
- The Kaggle dataset's exact source metadata and Indian-context status need additional review.
- The CM dataset includes duplicates and some duplicate-label conflicts.
- The 79-row probe is excluded from primary conclusions because its provenance is uncertain.
- Manual error examples need more human review and careful anonymization.

These limitations do not invalidate the project. They define the correct strength of the claim: this is an application research draft with meaningful evidence, not a final peer-reviewed conclusion.

## 11. AI Assistance And Student Responsibility Statement

This project was developed with substantial assistance from AI tools, including Codex, which helped with coding, debugging, experiment organization, documentation, result summarization, and drafting support. Om Patnaik used AI as a technical and writing assistant throughout the project. The research direction, dataset choices, interpretation of results, comparison of model behavior, and final claims were reviewed and directed by Om. Om is responsible for understanding and defending the project's methodology, results, limitations, and conclusions. The project should therefore be understood as AI-assisted independent student research, not as unaided work and not as work independently authored by AI.

### Student Role

Om's role was to guide the project's research direction, review and interpret experiment outputs, compare dataset situations, refine the central claim, and connect the technical results to the broader question of cross-dataset robustness in Hinglish harmful-speech detection. The project evolved from a simple mBERT-vs-MuRIL comparison into a cross-dataset robustness study after Om reviewed evidence showing that model ranking changed across datasets.

### AI/Codex Role

AI/Codex assisted with implementation, debugging, running and organizing experiments, writing scripts, producing documentation, summarizing results, and structuring the paper. Any code or prose produced with AI assistance should be reviewed by Om before being treated as final.

## 12. Conclusion

This project shows that the mBERT-vs-MuRIL comparison cannot be answered with a single score. In matched multi-seed evaluation, mBERT is stronger on Kaggle Hinglish hate and narrowly stronger on CM code-mixed/offensive data, while MuRIL is stronger on THAR targeted religious hate. Cross-dataset and mixed-training experiments show that harmful-speech detection is strongly shaped by dataset situation: label definition, platform, topic, script composition, and source balance.

The most defensible conclusion is that model choice and dataset definition must be studied together. For Hinglish and Hindi-English harmful-speech detection, cross-dataset robustness is weak, and that weakness is a core finding rather than a failure to hide.

## References

- Devlin, J., Chang, M.-W., Lee, K., and Toutanova, K. BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding. NAACL-HLT, 2019.
- Khanuja, S., et al. MuRIL: Multilingual Representations for Indian Languages. arXiv:2103.10730, 2021.
- Bohra, A., Vijay, D., Singh, V., Akhtar, S. S., and Shrivastava, M. A Dataset of Hindi-English Code-Mixed Social Media Text for Hate Speech Detection. W18-1105, 2018.
- Dhekane, S. Code-Mixed Hinglish Hate Speech Detection Dataset. Kaggle. [OM VERIFY license and exact source metadata]
- cm-hate-speech-detection contributors. `cm-hate-speech-detection` GitHub repository. [OM VERIFY license and preferred citation]
- Sharma, D., et al. THAR: Targeted Hate Speech Against Religion: A High-Quality Hindi-English Code-Mixed Dataset with the Application of Deep Learning Models for Automatic Detection. ACM Digital Library, 2024. [OM VERIFY full author list]
- THAR contributors. THAR GitHub repository. [OM VERIFY repository license and citation]

