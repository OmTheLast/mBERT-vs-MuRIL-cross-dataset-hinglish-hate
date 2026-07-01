# Manual Error Analysis Report

Date: 2026-06-27

This report is a first-pass qualitative coding of `results/error_analysis/manual_error_annotation_template.csv`. It should be treated as a structured reading aid, not as final human-ground-truth annotation.

## Coding Codebook

| Code | Meaning |
|---|---|
| `cross_dataset_label_mismatch` | Training and test datasets use different label meanings or domains. |
| `target_group_or_religion_cue` | Text contains religion or target-group cues that may drive hate/offense decisions. |
| `political_context_or_slogan` | Text depends on political entities, slogans, or platform-specific political context. |
| `generic_profanity_or_abuse` | Text contains abuse/profanity or violent terms. |
| `non_hateful_lexical_trigger` | Text contains words such as hate/profanity but appears not to be targeted hate. |
| `script_mismatch_devanagari` | Devanagari-only row; may stress tokenizer/script handling. |
| `mixed_script_complexity` | Row mixes Latin and Devanagari scripts. |
| `short_or_contextless_text` | Example is too short or context-poor to interpret confidently. |
| `implicit_context_or_unclear_signal` | No obvious surface cue; likely requires conversation/context. |

## Overall First-Pass Code Counts

| manual_reason                      |   rows | share   |
|:-----------------------------------|-------:|:--------|
| cross_dataset_label_mismatch       |    191 | 67.0%   |
| generic_profanity_or_abuse         |     78 | 27.4%   |
| target_group_or_religion_cue       |     64 | 22.5%   |
| political_context_or_slogan        |     47 | 16.5%   |
| implicit_context_or_unclear_signal |     37 | 13.0%   |
| non_hateful_lexical_trigger        |     27 | 9.5%    |
| short_or_contextless_text          |     26 | 9.1%    |
| mixed_script_complexity            |      9 | 3.2%    |
| script_mismatch_devanagari         |      8 | 2.8%    |

## Primary Reason By Train/Test Pair

| train_dataset        | test_dataset         | primary_reason                     |   rows |
|:---------------------|:---------------------|:-----------------------------------|-------:|
| cm_splits_codemixed  | cm_splits_codemixed  | political_context_or_slogan        |     12 |
| cm_splits_codemixed  | cm_splits_codemixed  | implicit_context_or_unclear_signal |     11 |
| cm_splits_codemixed  | cm_splits_codemixed  | target_group_or_religion_cue       |      4 |
| cm_splits_codemixed  | cm_splits_codemixed  | mixed_script_complexity            |      3 |
| cm_splits_codemixed  | cm_splits_codemixed  | short_or_contextless_text          |      1 |
| kaggle_hinglish_hate | cm_splits_codemixed  | cross_dataset_label_mismatch       |     33 |
| thar_religion        | cm_splits_codemixed  | cross_dataset_label_mismatch       |     29 |
| cm_splits_codemixed  | kaggle_hinglish_hate | cross_dataset_label_mismatch       |     31 |
| kaggle_hinglish_hate | kaggle_hinglish_hate | generic_profanity_or_abuse         |     26 |
| kaggle_hinglish_hate | kaggle_hinglish_hate | implicit_context_or_unclear_signal |      4 |
| kaggle_hinglish_hate | kaggle_hinglish_hate | political_context_or_slogan        |      3 |
| kaggle_hinglish_hate | kaggle_hinglish_hate | target_group_or_religion_cue       |      1 |
| thar_religion        | kaggle_hinglish_hate | cross_dataset_label_mismatch       |     28 |
| cm_splits_codemixed  | thar_religion        | cross_dataset_label_mismatch       |     34 |
| kaggle_hinglish_hate | thar_religion        | cross_dataset_label_mismatch       |     36 |
| thar_religion        | thar_religion        | implicit_context_or_unclear_signal |     22 |
| thar_religion        | thar_religion        | political_context_or_slogan        |      4 |
| thar_religion        | thar_religion        | target_group_or_religion_cue       |      2 |
| thar_religion        | thar_religion        | script_mismatch_devanagari         |      1 |

## Main Qualitative Reason Under Cross-Dataset Transfer

This table ignores `cross_dataset_label_mismatch` when another code is present, so it shows the more specific reason underneath transfer failure.

| train_dataset        | test_dataset         | non_cross_primary_reason           |   rows |
|:---------------------|:---------------------|:-----------------------------------|-------:|
| cm_splits_codemixed  | cm_splits_codemixed  | political_context_or_slogan        |     12 |
| cm_splits_codemixed  | cm_splits_codemixed  | implicit_context_or_unclear_signal |     11 |
| cm_splits_codemixed  | cm_splits_codemixed  | target_group_or_religion_cue       |      4 |
| cm_splits_codemixed  | cm_splits_codemixed  | mixed_script_complexity            |      3 |
| cm_splits_codemixed  | cm_splits_codemixed  | short_or_contextless_text          |      1 |
| kaggle_hinglish_hate | cm_splits_codemixed  | political_context_or_slogan        |      8 |
| kaggle_hinglish_hate | cm_splits_codemixed  | cross_dataset_label_mismatch_only  |      7 |
| kaggle_hinglish_hate | cm_splits_codemixed  | short_or_contextless_text          |      7 |
| kaggle_hinglish_hate | cm_splits_codemixed  | target_group_or_religion_cue       |      5 |
| kaggle_hinglish_hate | cm_splits_codemixed  | mixed_script_complexity            |      4 |
| kaggle_hinglish_hate | cm_splits_codemixed  | generic_profanity_or_abuse         |      2 |
| thar_religion        | cm_splits_codemixed  | cross_dataset_label_mismatch_only  |     12 |
| thar_religion        | cm_splits_codemixed  | political_context_or_slogan        |      8 |
| thar_religion        | cm_splits_codemixed  | target_group_or_religion_cue       |      6 |
| thar_religion        | cm_splits_codemixed  | short_or_contextless_text          |      2 |
| thar_religion        | cm_splits_codemixed  | mixed_script_complexity            |      1 |
| cm_splits_codemixed  | kaggle_hinglish_hate | generic_profanity_or_abuse         |     20 |
| cm_splits_codemixed  | kaggle_hinglish_hate | short_or_contextless_text          |      5 |
| cm_splits_codemixed  | kaggle_hinglish_hate | cross_dataset_label_mismatch_only  |      2 |
| cm_splits_codemixed  | kaggle_hinglish_hate | political_context_or_slogan        |      2 |
| cm_splits_codemixed  | kaggle_hinglish_hate | target_group_or_religion_cue       |      2 |
| kaggle_hinglish_hate | kaggle_hinglish_hate | generic_profanity_or_abuse         |     26 |
| kaggle_hinglish_hate | kaggle_hinglish_hate | implicit_context_or_unclear_signal |      4 |
| kaggle_hinglish_hate | kaggle_hinglish_hate | political_context_or_slogan        |      3 |
| kaggle_hinglish_hate | kaggle_hinglish_hate | target_group_or_religion_cue       |      1 |
| thar_religion        | kaggle_hinglish_hate | generic_profanity_or_abuse         |     15 |
| thar_religion        | kaggle_hinglish_hate | short_or_contextless_text          |      5 |
| thar_religion        | kaggle_hinglish_hate | cross_dataset_label_mismatch_only  |      3 |
| thar_religion        | kaggle_hinglish_hate | political_context_or_slogan        |      3 |
| thar_religion        | kaggle_hinglish_hate | target_group_or_religion_cue       |      2 |
| cm_splits_codemixed  | thar_religion        | target_group_or_religion_cue       |     19 |
| cm_splits_codemixed  | thar_religion        | cross_dataset_label_mismatch_only  |     11 |
| cm_splits_codemixed  | thar_religion        | generic_profanity_or_abuse         |      1 |
| cm_splits_codemixed  | thar_religion        | mixed_script_complexity            |      1 |
| cm_splits_codemixed  | thar_religion        | political_context_or_slogan        |      1 |
| cm_splits_codemixed  | thar_religion        | script_mismatch_devanagari         |      1 |
| kaggle_hinglish_hate | thar_religion        | target_group_or_religion_cue       |     18 |
| kaggle_hinglish_hate | thar_religion        | cross_dataset_label_mismatch_only  |      9 |
| kaggle_hinglish_hate | thar_religion        | script_mismatch_devanagari         |      6 |
| kaggle_hinglish_hate | thar_religion        | political_context_or_slogan        |      2 |
| kaggle_hinglish_hate | thar_religion        | generic_profanity_or_abuse         |      1 |
| thar_religion        | thar_religion        | implicit_context_or_unclear_signal |     22 |
| thar_religion        | thar_religion        | political_context_or_slogan        |      4 |
| thar_religion        | thar_religion        | target_group_or_religion_cue       |      2 |
| thar_religion        | thar_religion        | script_mismatch_devanagari         |      1 |

## Main Qualitative Findings

- Many sampled errors are cross-dataset failures. This supports the central claim that a model trained on one dataset situation does not automatically transfer to another.
- Religion and target-group cues are frequent in the error sample, especially whenever THAR is involved. This explains why THAR changes the mBERT-vs-MuRIL story.
- Kaggle examples often contain generic uses of `hate`, celebrity/sports dislikes, or profanity. This helps explain why a model can learn lexical triggers without learning strict targeted hate.
- CM examples often require political context or source-specific offense definitions. Some positives are subtle or slogan-like, and some negatives still contain religious/political terms.
- Devanagari and mixed-script examples appear as recurring difficult cases, especially in THAR and CM transfer.
- Short/contextless examples are genuinely hard to judge without surrounding thread context, so these should be treated carefully in the paper.

## Example Coded Rows

| train_dataset       | test_dataset         | outcome                    | prediction_pattern     | manual_reason                                                                       | label_quality_note                                                                                                                                                                                                                   | text                                                                                                                                                                                                                                                                                          |
|:--------------------|:---------------------|:---------------------------|:-----------------------|:------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| cm_splits_codemixed | cm_splits_codemixed  | both_wrong_same_prediction | true=1;mbert=0;muril=0 | mixed_script_complexity                                                             | Hard positive miss by both transformers under this condition. CM positive label is offense/hate-adjacent, not necessarily strict hate.                                                                                               | इसलिए तो अपन इसको सुप्रीम कोठा नाम दिया है। #SupremeCourtOfIndia #सुप्रीम_कोठा #MaritalRape                                                                                                                                                                                                   |
| cm_splits_codemixed | cm_splits_codemixed  | both_wrong_same_prediction | true=1;mbert=0;muril=0 | short_or_contextless_text                                                           | Very short/context-poor example; label may depend on missing conversation context. Hard positive miss by both transformers under this condition. CM positive label is offense/hate-adjacent, not necessarily strict hate.            | USER Smh. 🤕                                                                                                                                                                                                                                                                                   |
| cm_splits_codemixed | cm_splits_codemixed  | both_wrong_same_prediction | true=0;mbert=1;muril=1 | target_group_or_religion_cue                                                        | Both transformers mark this negative example as positive. CM negative examples can still contain political or religious discussion.                                                                                                  | USER USER Ye love jihad nhi lag rha...ye gharelu utpeedan Ka case hai....ladke ne dharm nhi chhipaya tha, jhut nhi Bola tha....to ye love jihad nhi h....                                                                                                                                     |
| cm_splits_codemixed | cm_splits_codemixed  | both_wrong_same_prediction | true=0;mbert=1;muril=1 | implicit_context_or_unclear_signal                                                  | Both transformers mark this negative example as positive. CM negative examples can still contain political or religious discussion. No obvious lexical/script cue; likely needs conversation context or human domain knowledge.      | USER USER USER USER Hathras mdhe in the dark of the night ek mulila forcibly jalal gele tichya family la ghari bandist karun,…ashya kiti tari ghatna hotana yanche sentiments hurt hote nahit… Rajasthan mdhe Dalit mulanvar attack jhala teva kiti protest kele yani ? Two days?             |
| cm_splits_codemixed | cm_splits_codemixed  | both_wrong_same_prediction | true=1;mbert=0;muril=0 | implicit_context_or_unclear_signal                                                  | Hard positive miss by both transformers under this condition. CM positive label is offense/hate-adjacent, not necessarily strict hate. No obvious lexical/script cue; likely needs conversation context or human domain knowledge.   | USER USER Rathiye.adivasi me sikha du                                                                                                                                                                                                                                                         |
| cm_splits_codemixed | cm_splits_codemixed  | both_wrong_same_prediction | true=0;mbert=1;muril=1 | target_group_or_religion_cue                                                        | Both transformers mark this negative example as positive. CM negative examples can still contain political or religious discussion.                                                                                                  | Give the concepts of terms like 'love jihad' or the shutting of doors of education on hijabi women, a thought. Not allowing women to choose their life partners, or denying them education due to their religious beliefs or caste.... Hypocrisy ki seema                                     |
| cm_splits_codemixed | cm_splits_codemixed  | both_wrong_same_prediction | true=1;mbert=0;muril=0 | implicit_context_or_unclear_signal                                                  | Hard positive miss by both transformers under this condition. CM positive label is offense/hate-adjacent, not necessarily strict hate. No obvious lexical/script cue; likely needs conversation context or human domain knowledge.   | USER O gyyani, first reconsider their performance... playing IPL                                                                                                                                                                                                                              |
| cm_splits_codemixed | cm_splits_codemixed  | both_wrong_same_prediction | true=1;mbert=0;muril=0 | political_context_or_slogan                                                         | Hard positive miss by both transformers under this condition. CM positive label is offense/hate-adjacent, not necessarily strict hate.                                                                                               | USER Hope #mialords didn’t lose any money during demonetisation #SupremeCourt 😉                                                                                                                                                                                                               |
| cm_splits_codemixed | cm_splits_codemixed  | mbert_only_correct         | true=1;mbert=1;muril=0 | target_group_or_religion_cue                                                        | CM positive label is offense/hate-adjacent, not necessarily strict hate.                                                                                                                                                             | USER people who are jihadi apologists are shedding tears for undertrials                                                                                                                                                                                                                      |
| cm_splits_codemixed | cm_splits_codemixed  | mbert_only_correct         | true=1;mbert=1;muril=0 | political_context_or_slogan                                                         | CM positive label is offense/hate-adjacent, not necessarily strict hate.                                                                                                                                                             | USER USER Hum to 2015 me bank join kiye MUDRA aur Jan Dhan account dekh K hi samajh gya ki bande ne dhang se 'C' kaat diya hai. Phir demonetisation ne aur chaar chaand lga diya.                                                                                                             |
| cm_splits_codemixed | cm_splits_codemixed  | mbert_only_correct         | true=1;mbert=1;muril=0 | implicit_context_or_unclear_signal                                                  | CM positive label is offense/hate-adjacent, not necessarily strict hate. No obvious lexical/script cue; likely needs conversation context or human domain knowledge.                                                                 | USER Indian Army is also sending Kashmiri Islamic jihadist to loose their virginity with 72 hoors in heaven with bullets🤣🤣                                                                                                                                                                    |
| cm_splits_codemixed | cm_splits_codemixed  | mbert_only_correct         | true=1;mbert=1;muril=0 | target_group_or_religion_cue                                                        | CM positive label is offense/hate-adjacent, not necessarily strict hate.                                                                                                                                                             | Elnaz Rekabi, Iranian climber, competed oversees with the mandatory hijab. Reports coming from Seoul are worrying. The Iranian delegation has confiscated her phone &amp; passport. Athletes are scheduled to fly to Iran on Wednesday. Be her voice. #مهسا_امینی                             |
| cm_splits_codemixed | cm_splits_codemixed  | mbert_only_correct         | true=1;mbert=1;muril=0 | political_context_or_slogan                                                         | CM positive label is offense/hate-adjacent, not necessarily strict hate.                                                                                                                                                             | USER That man lost a lot of money when the demonetisation happened, and he is still carrying a grudge against Modi ji ? Investigate him for money laundering                                                                                                                                  |
| cm_splits_codemixed | cm_splits_codemixed  | mbert_only_correct         | true=0;mbert=0;muril=1 | implicit_context_or_unclear_signal                                                  | CM negative examples can still contain political or religious discussion. No obvious lexical/script cue; likely needs conversation context or human domain knowledge.                                                                | USER USER wa beta ji moz kar rahe ho to tiwadi jo jati h usko chhod karke dalit ban jao Ye jatipratha banai kisne tum jaise pakhandiyo ne Chale h aarkshan ko kham kar ne aap khatm ho jaoge magar aarkshan nahi Or ha 10% to tumhe bhi to mila huaa h                                        |
| cm_splits_codemixed | cm_splits_codemixed  | mbert_only_correct         | true=0;mbert=0;muril=1 | political_context_or_slogan                                                         | CM negative examples can still contain political or religious discussion.                                                                                                                                                            | USER USER What about bjp scams Coffingate Vyapam Mines scam Jobs scam Scam exposed by S Malik Karnataka cut commission UP police extortion list And Demonetisation Electoral bonds Horse trading                                                                                              |
| cm_splits_codemixed | cm_splits_codemixed  | mbert_only_correct         | true=1;mbert=1;muril=0 | political_context_or_slogan                                                         | CM positive label is offense/hate-adjacent, not necessarily strict hate.                                                                                                                                                             | USER USER USER 😂😂😂😂😂 nice joke. Beta 1948 se RSS k hi headquarters pr Tiranga lga hua h. Mujhe sikha rhi h jinke khud ke logon ko pta nhi ki Golwalkar Ji ke kya vichaar the ve khud yahan bdbd krne aa gye 🤣🤣🤣                                                                               |
| cm_splits_codemixed | cm_splits_codemixed  | muril_only_correct         | true=0;mbert=1;muril=0 | implicit_context_or_unclear_signal                                                  | CM negative examples can still contain political or religious discussion. No obvious lexical/script cue; likely needs conversation context or human domain knowledge.                                                                | USER You deserve this embarrassment as u blamed the umpires of the last as puppets of IPL. Jaisi karni waisi bharni                                                                                                                                                                           |
| cm_splits_codemixed | cm_splits_codemixed  | muril_only_correct         | true=0;mbert=1;muril=0 | political_context_or_slogan                                                         | CM negative examples can still contain political or religious discussion.                                                                                                                                                            | USER USER First you look behind ur Modi Model of india. Intolerance. How many are tortured. Not too far the disintegration of this nation built by Sardar Patel ji..                                                                                                                          |
| cm_splits_codemixed | cm_splits_codemixed  | muril_only_correct         | true=0;mbert=1;muril=0 | political_context_or_slogan                                                         | CM negative examples can still contain political or religious discussion.                                                                                                                                                            | USER Arun Jaitley didn't knew about demonetisation who was the FM that time. Infact no one in the Govt knew about it except Shah, Doval and BJP. Manohar Parikar didn't knew about new Rafale deal. Sushma Swaraj as EAM was unaware that Modi is heading to Pakistan without telling anyone. |
| cm_splits_codemixed | cm_splits_codemixed  | muril_only_correct         | true=0;mbert=1;muril=0 | political_context_or_slogan                                                         | CM negative examples can still contain political or religious discussion.                                                                                                                                                            | USER USER Are bro even Aamir supported demonetisation. I don't agree with that support of Aamir too.                                                                                                                                                                                          |
| cm_splits_codemixed | cm_splits_codemixed  | muril_only_correct         | true=0;mbert=1;muril=0 | mixed_script_complexity                                                             | CM negative examples can still contain political or religious discussion.                                                                                                                                                            | USER USER USER सय्यद मुश्ताक अली ट्रॉफी साठी खूप खूप शुभेच्छा श्रेयस......❣️                                                                                                                                                                                                                  |
| cm_splits_codemixed | cm_splits_codemixed  | muril_only_correct         | true=0;mbert=1;muril=0 | political_context_or_slogan                                                         | CM negative examples can still contain political or religious discussion.                                                                                                                                                            | USER USER USER tirangey ka apmaan nahi hua, tu divert mat kar, farmers protests aur anti-farmer's bill pe dhyaan de                                                                                                                                                                           |
| cm_splits_codemixed | cm_splits_codemixed  | muril_only_correct         | true=0;mbert=1;muril=0 | implicit_context_or_unclear_signal                                                  | CM negative examples can still contain political or religious discussion. No obvious lexical/script cue; likely needs conversation context or human domain knowledge.                                                                | USER Ye aaj kiske vanshaj hain? Bhagat singh, Rana Pratap or Sardar Patel or Gandhiji.                                                                                                                                                                                                        |
| cm_splits_codemixed | cm_splits_codemixed  | muril_only_correct         | true=0;mbert=1;muril=0 | political_context_or_slogan                                                         | CM negative examples can still contain political or religious discussion.                                                                                                                                                            | USER India is a vibrant democracy, it's people are lashing out against 60 years old corrupt governance. Whem Modi will not fit the bill, they vote him out too. If you are talking Kashmir, CAA, Farmer's Bill with broad strokes, you cannot be more wrong. Trust people's intellect.        |
| cm_splits_codemixed | kaggle_hinglish_hate | both_wrong_same_prediction | true=1;mbert=0;muril=0 | cross_dataset_label_mismatch;generic_profanity_or_abuse                             | Hard positive miss by both transformers under this condition.                                                                                                                                                                        | SuChai TO Ye Hai Ks Ki ArMy Rape kRti Hai Ab KhNa Ye B JOoTh hai                                                                                                                                                                                                                              |
| cm_splits_codemixed | kaggle_hinglish_hate | both_wrong_same_prediction | true=1;mbert=0;muril=0 | cross_dataset_label_mismatch;generic_profanity_or_abuse                             | Hard positive miss by both transformers under this condition.                                                                                                                                                                        | Dalit ladki ka rape Kiya tere bhai ne USER ?? URL …                                                                                                                                                                                                                                           |
| cm_splits_codemixed | kaggle_hinglish_hate | both_wrong_same_prediction | true=1;mbert=0;muril=0 | cross_dataset_label_mismatch;generic_profanity_or_abuse;short_or_contextless_text   | Very short/context-poor example; label may depend on missing conversation context. Hard positive miss by both transformers under this condition. Kaggle positive label may include generic hate/profanity rather than targeted hate. | rundi                                                                                                                                                                                                                                                                                         |
| cm_splits_codemixed | kaggle_hinglish_hate | both_wrong_same_prediction | true=0;mbert=1;muril=1 | cross_dataset_label_mismatch;generic_profanity_or_abuse                             | Both transformers mark this negative example as positive. Kaggle negative label may include abusive words used non-targetedly or conversationally.                                                                                   | Abe gandu... Hum baap log hi hain!! Gawar saale pehle apna terrorism wala desh ko sambhalo                                                                                                                                                                                                    |
| cm_splits_codemixed | kaggle_hinglish_hate | both_wrong_same_prediction | true=1;mbert=0;muril=0 | cross_dataset_label_mismatch;generic_profanity_or_abuse;non_hateful_lexical_trigger | The text contains a lexical cue such as 'hate' but may not be targeted hate. Hard positive miss by both transformers under this condition. Kaggle positive label may include generic hate/profanity rather than targeted hate.       | I hate Yuvraj URL …                                                                                                                                                                                                                                                                           |
| cm_splits_codemixed | kaggle_hinglish_hate | both_wrong_same_prediction | true=0;mbert=1;muril=1 | cross_dataset_label_mismatch;generic_profanity_or_abuse                             | Both transformers mark this negative example as positive. Kaggle negative label may include abusive words used non-targetedly or conversationally.                                                                                   | mahajiron se kisi ko bhe nafrat nahe hai,mostly log mohajiron ki tragedy ko samjhte hain.aur ,but altaf husain ne qatal o gharatkar ke mohajir cause ko badnaam kar dia hai.                                                                                                                  |

## How To Use This File

The output CSV is `results/error_analysis/manual_error_annotation_first_pass.csv`. Review it row by row and edit the three qualitative columns if you disagree:

- `manual_reason`
- `label_quality_note`
- `paper_relevance`

For paper writing, do not treat every code as final. Use these annotations to select examples and justify broader patterns already supported by quantitative metrics.

## How To Manually Review It Yourself

1. Open `results/error_analysis/manual_error_annotation_first_pass.csv` in Excel, Numbers, Google Sheets, or VS Code.
2. Filter one train/test pair at a time. Start with matched datasets first because they are easier to interpret.
3. Read `prediction_pattern`: `true=1;mbert=0;muril=0` means both models missed a positive example; `true=0;mbert=1;muril=1` means both models produced a false positive.
4. Read the text and ask: is the gold label obvious, or does it need missing thread/context?
5. Check whether the current `manual_reason` fits. If not, replace it with a better code from the codebook.
6. Use `label_quality_note` to record doubts such as `label seems ambiguous`, `generic dislike not hate`, `religion mention but not attack`, or `needs conversation context`.
7. Use `paper_relevance` only when the row teaches a broader point, such as script failure, label mismatch, or a clear mBERT/MuRIL disagreement.
8. Do not overuse examples containing slurs in the paper. Prefer paraphrased examples or short excerpts when possible.

A good manual-coding habit: if you are unsure, write `uncertain` in `label_quality_note` rather than forcing a confident interpretation.
