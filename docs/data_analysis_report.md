# Data Analysis Report

Date: 2026-06-25

This report verifies that the processed datasets match the local source files we claim to be using, then profiles the dataset situations that drive the mBERT-vs-MuRIL experiments.

## Source Integrity Checks

| dataset_id           | status   |   expected_rows |   processed_rows |   missing_from_processed |   extra_in_processed | check                                                                                    |
|:---------------------|:---------|----------------:|-----------------:|-------------------------:|---------------------:|:-----------------------------------------------------------------------------------------|
| kaggle_hinglish_hate | pass     |            4780 |             4780 |                        0 |                    0 | processed equals deduplicated raw rows where language == hinglish                        |
| cm_splits_codemixed  | pass     |            3900 |             3900 |                        0 |                    0 | processed equals raw train/val/test rows where codemixed == 1, label mapped from offense |
| thar_religion        | pass     |           11549 |            11549 |                        0 |                    0 | processed equals THAR raw comments with SubTask1 binary label mapping                    |

Interpretation: `pass` means the processed file matches the local raw/source file under the documented filtering and label-mapping rule. This does not by itself prove the external citation metadata is complete; it proves local processing consistency.

## Dataset Profile

| dataset_id                |   rows |   label_0 |   label_1 | positive_rate   |   unique_normalized_texts |   duplicate_normalized_text_rows |   median_words |   p95_words | mention_rate   | hashtag_rate   | emoji_rate   |
|:--------------------------|-------:|----------:|----------:|:----------------|--------------------------:|---------------------------------:|---------------:|------------:|:---------------|:---------------|:-------------|
| kaggle_hinglish_hate      |   4780 |      2914 |      1866 | 39.0%           |                      4772 |                                8 |             19 |          41 | 10.7%          | 6.6%           | 0.1%         |
| cm_splits_codemixed       |   3900 |      2455 |      1445 | 37.1%           |                      3764 |                              136 |             26 |          54 | 76.5%          | 25.3%          | 18.7%        |
| thar_religion             |  11549 |      6095 |      5454 | 47.2%           |                     11546 |                                3 |             17 |          86 | 0.2%           | 0.1%           | 18.1%        |
| existing_79_row_benchmark |     79 |        40 |        39 | 49.4%           |                        75 |                                4 |              5 |           7 | 0.0%           | 0.0%           | 0.0%         |

## Script Composition

| dataset_id                | script_bucket          |   rows | rate   |
|:--------------------------|:-----------------------|-------:|:-------|
| cm_splits_codemixed       | devanagari_only        |     13 | 0.3%   |
| cm_splits_codemixed       | latin_only             |   3458 | 88.7%  |
| cm_splits_codemixed       | mixed_latin_devanagari |    428 | 11.0%  |
| cm_splits_codemixed       | other_or_symbolic      |      1 | 0.0%   |
| existing_79_row_benchmark | latin_only             |     79 | 100.0% |
| kaggle_hinglish_hate      | latin_only             |   4780 | 100.0% |
| thar_religion             | devanagari_only        |   2187 | 18.9%  |
| thar_religion             | latin_only             |   8877 | 76.9%  |
| thar_religion             | mixed_latin_devanagari |    482 | 4.2%   |
| thar_religion             | other_or_symbolic      |      3 | 0.0%   |

Script composition is important because mBERT and MuRIL may not behave the same on Latin-script Hinglish versus Devanagari-heavy Hindi-English text.

## Text Length By Label

| dataset_id                |   label |   rows |   median_words |   p95_words | url_rate   | mention_rate   | hashtag_rate   | emoji_rate   |
|:--------------------------|--------:|-------:|---------------:|------------:|:-----------|:---------------|:---------------|:-------------|
| kaggle_hinglish_hate      |       0 |   2914 |             18 |          38 | 8.2%       | 11.3%          | 6.9%           | 0.1%         |
| kaggle_hinglish_hate      |       1 |   1866 |             19 |          46 | 6.4%       | 9.7%           | 6.2%           | 0.0%         |
| cm_splits_codemixed       |       0 |   2455 |             24 |          53 | 0.0%       | 73.0%          | 29.2%          | 19.7%        |
| cm_splits_codemixed       |       1 |   1445 |             29 |          55 | 0.1%       | 82.5%          | 18.5%          | 17.2%        |
| thar_religion             |       0 |   6095 |             15 |          80 | 0.0%       | 0.1%           | 0.1%           | 17.0%        |
| thar_religion             |       1 |   5454 |             20 |          89 | 0.0%       | 0.2%           | 0.2%           | 19.4%        |
| existing_79_row_benchmark |       0 |     40 |              6 |           7 | 0.0%       | 0.0%           | 0.0%           | 0.0%         |
| existing_79_row_benchmark |       1 |     39 |              5 |           6 | 0.0%       | 0.0%           | 0.0%           | 0.0%         |

## Cross-Dataset Text Overlap

| dataset_a                 | dataset_b                 |   overlap_normalized_texts |   dataset_a_unique_texts |   dataset_b_unique_texts | overlap_rate_min_side   |
|:--------------------------|:--------------------------|---------------------------:|-------------------------:|-------------------------:|:------------------------|
| kaggle_hinglish_hate      | thar_religion             |                          0 |                     4772 |                    11546 | 0.0%                    |
| cm_splits_codemixed       | kaggle_hinglish_hate      |                          0 |                     3764 |                     4772 | 0.0%                    |
| cm_splits_codemixed       | thar_religion             |                          0 |                     3764 |                    11546 | 0.0%                    |
| cm_splits_codemixed       | existing_79_row_benchmark |                          0 |                     3764 |                       75 | 0.0%                    |
| existing_79_row_benchmark | kaggle_hinglish_hate      |                          0 |                       75 |                     4772 | 0.0%                    |
| existing_79_row_benchmark | thar_religion             |                          0 |                       75 |                    11546 | 0.0%                    |

Low overlap means cross-dataset evaluation is mostly testing domain/definition transfer rather than memorized duplicate text.

## Duplicate Texts

| dataset_id          |   duplicate_count | labels_seen   | example_text                                                                                                                                                                            |
|:--------------------|------------------:|:--------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| cm_splits_codemixed |                19 | 0             | @user 😭😭😭😭                                                                                                                                                                              |
| cm_splits_codemixed |                11 | 1             | While talking about the outcome of the Quit India Movement Golwalkar said: Sangh vowed not to do anything directly #RSSQuitIndia                                                        |
| cm_splits_codemixed |                 9 | 1             | The national flag is a matter of pride for us. But, Mr. Savarkar and Mr. Golwalkar had not accepted the national flag. Tiranga Virodhi RSS                                              |
| cm_splits_codemixed |                 9 | 0,1           | The vision of RSS is based on the book "BUNCH OF THOUGHT" by Golwalkar and the ideas of Savarkar who always opposed the freedom struggle of India #RSSBrokeIndia                        |
| cm_splits_codemixed |                 9 | 0,1           | While talking about the outcome of the Quit India Movement Golwalkar said: Sangh vowed not to do anything directly #RSSBrokeIndia                                                       |
| cm_splits_codemixed |                 8 | 0,1           | In 1942, when the Quit India Movement began, Golwalkar issued instructions that the RSS’s routine work should continue and nothing should be done to annoy the British. #RSSBrokeInd... |
| cm_splits_codemixed |                 6 | 1             | Golwalkar as the most important ideologue of the RSS and Hindutva brand of politics forcefully argued for adopting the models of Hitler and Mussolini #RSSBrokeIndia                    |
| cm_splits_codemixed |                 6 | 1             | Golwalkar as the most important ideologue of the RSS and Hindutva brand of politics forcefully argued for adopting the models of Hitler and Mussolini #RSSQuitIndia                     |
| cm_splits_codemixed |                 6 | 0             | @user @user 🙏🙏🙏🙏🙏                                                                                                                                                                       |
| cm_splits_codemixed |                 5 | 0             | #MaritalRape                                                                                                                                                                            |
| cm_splits_codemixed |                 5 | 0             | @user Jai Hind 🇮🇳                                                                                                                                                                       |
| cm_splits_codemixed |                 4 | 0             | From the fishermen of Kerala to the farmers of Karnataka all have been bearing the brunt of inflation with no support from the government. We raised their issues while they walked ... |
| cm_splits_codemixed |                 4 | 1             | In 1942, when the Quit India Movement began, Golwalkar issued instructions that the RSS’s routine work should continue and nothing should be done to annoy the British. #RSSQuitIndi... |
| cm_splits_codemixed |                 3 | 0,1           | The vision of RSS is based on the book "BUNCH OF THOUGHT" by Golwalkar and the ideas of Savarkar who always opposed the freedom struggle of India #RSSQuitIndia                         |
| cm_splits_codemixed |                 3 | 0             | @user @user @user 👏👏👏                                                                                                                                                                   |
| cm_splits_codemixed |                 3 | 0,1           | @user What about bjp scams Coffingate Vyapam Mines scam Jobs scam Rafale scam Scam exposed by S Malik Karnataka cut commission UP police extortion list And Demonetisation Electoral... |
| cm_splits_codemixed |                 2 | 0,1           | A brief timeline: Credit Crunch Panic Tories/LibDems Austerity Blame Game Ukip Referendum Brexit May Soft vs Hard Crisis Johnson Prorogation Withdrawal Agreement NI Protocol Leave ... |
| cm_splits_codemixed |                 2 | 0             | AriGrayson giving very much love o2o couple vibes😭😭😭😭                                                                                                                                   |
| cm_splits_codemixed |                 2 | 0             | Chidambaram: But what about the non-monetary hardships faced by people? The loss of livelihoods, jobs, wages? Justice Nazeer: What should they have done acc to you? #Demonetisation... |
| cm_splits_codemixed |                 2 | 0             | Chidambaram: Did they apply their minds? Was this a decision taken rationally? Let us see the documents then. #Demonetisation #SupremeCourtofIndia                                      |

Full duplicate list saved to `results/data_analysis/duplicate_examples.csv`.

## Label-Associated Terms

These are not explanations by themselves. They are lexical clues showing which words are most associated with the positive or negative class inside each dataset. Strong lexical clues can partly explain why TF-IDF baselines are competitive.

### `kaggle_hinglish_hate`

**Positive-associated terms**

|   rank | token    |   positive_doc_count |   negative_doc_count |   log_odds_score |
|-------:|:---------|---------------------:|---------------------:|-----------------:|
|      1 | rajneeti |                    7 |                    0 |             2.39 |
|      2 | kuttay   |                    7 |                    0 |             2.39 |
|      3 | khattar  |                    7 |                    0 |             2.39 |
|      4 | admi     |                    7 |                    0 |             2.39 |
|      5 | kisano   |                    6 |                    0 |             2.25 |
|      6 | winner   |                    5 |                    0 |             2.1  |
|      7 | vikash   |                    5 |                    0 |             2.1  |
|      8 | muslimo  |                    5 |                    0 |             2.1  |
|      9 | mass     |                    5 |                    0 |             2.1  |
|     10 | bhadwe   |                    5 |                    0 |             2.1  |
|     11 | abay     |                    5 |                    0 |             2.1  |
|     12 | task     |                    9 |                    1 |             1.92 |

**Negative-associated terms**

|   rank | token       |   positive_doc_count |   negative_doc_count |   log_odds_score |
|-------:|:------------|---------------------:|---------------------:|-----------------:|
|      1 | khatm       |                    0 |                   15 |            -2.47 |
|      2 | stop        |                    0 |                   12 |            -2.26 |
|      3 | manzoor     |                    0 |                   10 |            -2.09 |
|      4 | bakri       |                    0 |                    9 |            -2    |
|      5 | hazar       |                    0 |                    9 |            -2    |
|      6 | himachal    |                    0 |                    9 |            -2    |
|      7 | jeeto       |                    0 |                    9 |            -2    |
|      8 | kartey      |                    0 |                    9 |            -2    |
|      9 | ziada       |                    0 |                    9 |            -2    |
|     10 | balochistan |                    0 |                    8 |            -1.89 |
|     11 | episode     |                    0 |                    8 |            -1.89 |
|     12 | kaan        |                    0 |                    8 |            -1.89 |

### `cm_splits_codemixed`

**Positive-associated terms**

|   rank | token      |   positive_doc_count |   negative_doc_count |   log_odds_score |
|-------:|:-----------|---------------------:|---------------------:|-----------------:|
|      1 | wapasi     |                  136 |                    0 |             5.2  |
|      2 | ghar       |                  149 |                    3 |             3.91 |
|      3 | gharwapasi |                   34 |                    0 |             3.84 |
|      4 | talaq      |                   27 |                    0 |             3.61 |
|      5 | hitler     |                   15 |                    0 |             3.05 |
|      6 | mussolini  |                   14 |                    0 |             2.99 |
|      7 | triple     |                   27 |                    1 |             2.92 |
|      8 | models     |                   13 |                    0 |             2.92 |
|      9 | pride      |                   12 |                    0 |             2.85 |
|     10 | forcefully |                   12 |                    0 |             2.85 |
|     11 | adopting   |                   12 |                    0 |             2.85 |
|     12 | jihad      |                  113 |                    8 |             2.82 |

**Negative-associated terms**

|   rank | token            |   positive_doc_count |   negative_doc_count |   log_odds_score |
|-------:|:-----------------|---------------------:|---------------------:|-----------------:|
|      1 | chidambaram      |                    0 |                  115 |            -4.47 |
|      2 | rbi              |                    0 |                   29 |            -3.12 |
|      3 | worldcup         |                    0 |                   20 |            -2.76 |
|      4 | supremecourt     |                    2 |                   59 |            -2.71 |
|      5 | tomorrow         |                    0 |                   15 |            -2.49 |
|      6 | played           |                    0 |                   13 |            -2.36 |
|      7 | zimbabwe         |                    0 |                   13 |            -2.36 |
|      8 | affecting        |                    0 |                   12 |            -2.28 |
|      9 | azad             |                    0 |                   12 |            -2.28 |
|     10 | flood            |                    3 |                   51 |            -2.28 |
|     11 | genderbiasedlaws |                    0 |                   12 |            -2.28 |
|     12 | million          |                    0 |                   12 |            -2.28 |

### `thar_religion`

**Positive-associated terms**

|   rank | token      |   positive_doc_count |   negative_doc_count |   log_odds_score |
|-------:|:-----------|---------------------:|---------------------:|-----------------:|
|      1 | muharram   |                   12 |                    0 |             2.53 |
|      2 | islami     |                   10 |                    0 |             2.36 |
|      3 | molana     |                  122 |                   11 |             2.29 |
|      4 | अशरफ       |                    9 |                    0 |             2.26 |
|      5 | reference  |                    8 |                    0 |             2.16 |
|      6 | mollana    |                    8 |                    0 |             2.16 |
|      7 | maulanao   |                    8 |                    0 |             2.16 |
|      8 | madharchod |                    8 |                    0 |             2.16 |
|      9 | कमज        |                    7 |                    0 |             2.04 |
|     10 | rehe       |                    7 |                    0 |             2.04 |
|     11 | mullo      |                   31 |                    3 |             2.04 |
|     12 | jgh        |                    7 |                    0 |             2.04 |

**Negative-associated terms**

|   rank | token      |   positive_doc_count |   negative_doc_count |   log_odds_score |
|-------:|:-----------|---------------------:|---------------------:|-----------------:|
|      1 | waisi      |                    0 |                   10 |            -2.44 |
|      2 | parmeshvar |                    0 |                    9 |            -2.34 |
|      3 | huya       |                    0 |                    8 |            -2.24 |
|      4 | according  |                    0 |                    7 |            -2.12 |
|      5 | asish      |                    0 |                    7 |            -2.12 |
|      6 | bhugto     |                    0 |                    7 |            -2.12 |
|      7 | kan        |                    0 |                    7 |            -2.12 |
|      8 | shok       |                    0 |                    7 |            -2.12 |
|      9 | marji      |                    2 |                   21 |            -2.03 |
|     10 | ajj        |                    0 |                    6 |            -1.98 |
|     11 | data       |                    0 |                    6 |            -1.98 |
|     12 | dikhate    |                    0 |                    6 |            -1.98 |

### `existing_79_row_benchmark`

**Positive-associated terms**

|   rank | token   |   positive_doc_count |   negative_doc_count |   log_odds_score |
|-------:|:--------|---------------------:|---------------------:|-----------------:|
|      1 | koi     |                   12 |                    0 |             2.69 |
|      2 | nahi    |                   10 |                    0 |             2.53 |
|      3 | ganda   |                    7 |                    0 |             2.21 |
|      4 | galat   |                   12 |                    1 |             2    |
|      5 | tum     |                    3 |                    0 |             1.52 |
|      6 | sabko   |                    3 |                    0 |             1.52 |
|      7 | nafrat  |                    3 |                    0 |             1.52 |
|      8 | iska    |                    3 |                    0 |             1.52 |
|      9 | sab     |                   16 |                    4 |             1.35 |
|     10 | samajh  |                    2 |                    0 |             1.23 |
|     11 | mein    |                    2 |                    0 |             1.23 |
|     12 | kutte   |                    2 |                    0 |             1.23 |

**Negative-associated terms**

|   rank | token   |   positive_doc_count |   negative_doc_count |   log_odds_score |
|-------:|:--------|---------------------:|---------------------:|-----------------:|
|      1 | main    |                    0 |                   18 |            -2.81 |
|      2 | achhe   |                    0 |                   15 |            -2.64 |
|      3 | pasand  |                    0 |                    9 |            -2.17 |
|      4 | hun     |                    1 |                   17 |            -2.07 |
|      5 | lagta   |                    0 |                    7 |            -1.95 |
|      6 | mera    |                    0 |                    7 |            -1.95 |
|      7 | mujhe   |                    1 |                   11 |            -1.66 |
|      8 | dost    |                    0 |                    4 |            -1.48 |
|      9 | meri    |                    0 |                    4 |            -1.48 |
|     10 | family  |                    0 |                    3 |            -1.26 |
|     11 | ghar    |                    0 |                    3 |            -1.26 |
|     12 | khana   |                    0 |                    3 |            -1.26 |

## Figures

- `results/data_analysis/label_balance.png`
- `results/data_analysis/label_balance.svg`
- `results/data_analysis/script_composition.png`
- `results/data_analysis/script_composition.svg`
- `results/data_analysis/word_count_by_label.png`
- `results/data_analysis/word_count_by_label.svg`

## Analysis Takeaways

- The local processed datasets match their documented local sources and label mappings.
- The datasets are not the same task under different names: Kaggle is general Hinglish hate, CM is political offensive/hate-adjacent Twitter/X text, and THAR is targeted religious hate in YouTube comments.
- Script composition differs sharply across datasets, especially between Latin-heavy Kaggle/CM text and Devanagari-heavy THAR text.
- Cross-dataset text overlap is negligible, so transfer results are not duplicate-driven.
- The 79-row diagnostic probe is balanced but manually assembled/provenance-uncertain, has duplicates, and has no direct text overlap with the current source datasets.
- Lexical class cues are visible in every dataset, which helps explain why TF-IDF baselines can be competitive and why dataset-specific models may fail to transfer.

## Local Raw Data Not Yet Included In These Results

The workspace also contains raw candidate data under `data/raw/HASOC2021`, `data/raw/Hinglish_Hate_Detection`, and `data/raw/HateSpeech-Hindi-English-Code-Mixed-Social-Media-Text`. These are not part of the current reported training/evaluation matrix because they have not yet been converted into the project schema, audited, and registered as experiment datasets.