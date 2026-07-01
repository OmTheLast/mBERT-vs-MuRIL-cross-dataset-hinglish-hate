# Error Analysis Report

Date: 2026-06-26

This report analyzes transformer prediction errors on the three primary source-backed datasets. The 79-row diagnostic probe is excluded from this primary error analysis because its provenance is uncertain.

## Error Rate Summary

| train_dataset        | test_dataset         |   rows |   positive_rows |   negative_rows | mbert_accuracy   | muril_accuracy   | mbert_false_negative_rate   | muril_false_negative_rate   | mbert_false_positive_rate   | muril_false_positive_rate   |
|:---------------------|:---------------------|-------:|----------------:|----------------:|:-----------------|:-----------------|:----------------------------|:----------------------------|:----------------------------|:----------------------------|
| cm_splits_codemixed  | cm_splits_codemixed  |    415 |             147 |             268 | 80.5%            | 78.8%            | 31.3%                       | 44.9%                       | 13.1%                       | 8.2%                        |
| kaggle_hinglish_hate | cm_splits_codemixed  |    415 |             147 |             268 | 63.1%            | 65.8%            | 80.3%                       | 85.7%                       | 13.1%                       | 6.0%                        |
| thar_religion        | cm_splits_codemixed  |    415 |             147 |             268 | 65.3%            | 68.4%            | 59.9%                       | 46.9%                       | 20.9%                       | 23.1%                       |
| cm_splits_codemixed  | kaggle_hinglish_hate |    956 |             373 |             583 | 52.5%            | 54.5%            | 49.9%                       | 50.1%                       | 46.0%                       | 42.5%                       |
| kaggle_hinglish_hate | kaggle_hinglish_hate |    956 |             373 |             583 | 71.4%            | 67.5%            | 61.4%                       | 77.7%                       | 7.5%                        | 3.6%                        |
| thar_religion        | kaggle_hinglish_hate |    956 |             373 |             583 | 52.9%            | 52.5%            | 79.4%                       | 76.7%                       | 26.4%                       | 28.8%                       |
| cm_splits_codemixed  | thar_religion        |   2310 |            1091 |            1219 | 59.6%            | 59.7%            | 55.4%                       | 40.5%                       | 27.1%                       | 40.0%                       |
| kaggle_hinglish_hate | thar_religion        |   2310 |            1091 |            1219 | 52.6%            | 53.1%            | 84.1%                       | 91.8%                       | 14.6%                       | 6.8%                        |
| thar_religion        | thar_religion        |   2310 |            1091 |            1219 | 74.8%            | 77.9%            | 22.3%                       | 19.7%                       | 27.8%                       | 24.3%                       |

False negatives are especially important because they are hate/offensive examples predicted as non-hate/non-offensive. High false-negative rates indicate a conservative model under that dataset condition.

## Outcome Summary

| train_dataset        | test_dataset         | outcome                    |   rows | share   |
|:---------------------|:---------------------|:---------------------------|-------:|:--------|
| cm_splits_codemixed  | cm_splits_codemixed  | both_correct               |    303 | 73.0%   |
| cm_splits_codemixed  | cm_splits_codemixed  | both_wrong_same_prediction |     57 | 13.7%   |
| cm_splits_codemixed  | cm_splits_codemixed  | mbert_only_correct         |     31 | 7.5%    |
| cm_splits_codemixed  | cm_splits_codemixed  | muril_only_correct         |     24 | 5.8%    |
| cm_splits_codemixed  | kaggle_hinglish_hate | both_correct               |    385 | 40.3%   |
| cm_splits_codemixed  | kaggle_hinglish_hate | both_wrong_same_prediction |    318 | 33.3%   |
| cm_splits_codemixed  | kaggle_hinglish_hate | mbert_only_correct         |    117 | 12.2%   |
| cm_splits_codemixed  | kaggle_hinglish_hate | muril_only_correct         |    136 | 14.2%   |
| cm_splits_codemixed  | thar_religion        | both_correct               |   1081 | 46.8%   |
| cm_splits_codemixed  | thar_religion        | both_wrong_same_prediction |    635 | 27.5%   |
| cm_splits_codemixed  | thar_religion        | mbert_only_correct         |    295 | 12.8%   |
| cm_splits_codemixed  | thar_religion        | muril_only_correct         |    299 | 12.9%   |
| kaggle_hinglish_hate | cm_splits_codemixed  | both_correct               |    241 | 58.1%   |
| kaggle_hinglish_hate | cm_splits_codemixed  | both_wrong_same_prediction |    121 | 29.2%   |
| kaggle_hinglish_hate | cm_splits_codemixed  | mbert_only_correct         |     21 | 5.1%    |
| kaggle_hinglish_hate | cm_splits_codemixed  | muril_only_correct         |     32 | 7.7%    |
| kaggle_hinglish_hate | kaggle_hinglish_hate | both_correct               |    601 | 62.9%   |
| kaggle_hinglish_hate | kaggle_hinglish_hate | both_wrong_same_prediction |    229 | 24.0%   |
| kaggle_hinglish_hate | kaggle_hinglish_hate | mbert_only_correct         |     82 | 8.6%    |
| kaggle_hinglish_hate | kaggle_hinglish_hate | muril_only_correct         |     44 | 4.6%    |
| kaggle_hinglish_hate | thar_religion        | both_correct               |   1103 | 47.7%   |
| kaggle_hinglish_hate | thar_religion        | both_wrong_same_prediction |    973 | 42.1%   |
| kaggle_hinglish_hate | thar_religion        | mbert_only_correct         |    111 | 4.8%    |
| kaggle_hinglish_hate | thar_religion        | muril_only_correct         |    123 | 5.3%    |
| thar_religion        | cm_splits_codemixed  | both_correct               |    233 | 56.1%   |
| thar_religion        | cm_splits_codemixed  | both_wrong_same_prediction |     93 | 22.4%   |
| thar_religion        | cm_splits_codemixed  | mbert_only_correct         |     38 | 9.2%    |
| thar_religion        | cm_splits_codemixed  | muril_only_correct         |     51 | 12.3%   |
| thar_religion        | kaggle_hinglish_hate | both_correct               |    438 | 45.8%   |
| thar_religion        | kaggle_hinglish_hate | both_wrong_same_prediction |    386 | 40.4%   |
| thar_religion        | kaggle_hinglish_hate | mbert_only_correct         |     68 | 7.1%    |
| thar_religion        | kaggle_hinglish_hate | muril_only_correct         |     64 | 6.7%    |
| thar_religion        | thar_religion        | both_correct               |   1639 | 71.0%   |
| thar_religion        | thar_religion        | both_wrong_same_prediction |    422 | 18.3%   |
| thar_religion        | thar_religion        | mbert_only_correct         |     89 | 3.9%    |
| thar_religion        | thar_religion        | muril_only_correct         |    160 | 6.9%    |

## Feature-Level Error Signals

| feature             | value                  |   rows |   positive_rows | mbert_error_rate   | muril_error_rate   | mbert_false_negative_rate   | muril_false_negative_rate   |
|:--------------------|:-----------------------|-------:|----------------:|:-------------------|:-------------------|:----------------------------|:----------------------------|
| has_abuse_terms     | 0                      |   8643 |            3837 | 37.2%              | 35.7%              | 55.4%                       | 52.7%                       |
| has_abuse_terms     | 1                      |   2400 |             996 | 39.6%              | 41.6%              | 60.3%                       | 66.1%                       |
| has_political_terms | 0                      |   9804 |            4233 | 37.3%              | 36.5%              | 57.6%                       | 56.1%                       |
| has_political_terms | 1                      |   1239 |             600 | 41.1%              | 41.0%              | 48.3%                       | 51.2%                       |
| has_religion_terms  | 0                      |   7731 |            2718 | 34.2%              | 34.0%              | 66.3%                       | 65.5%                       |
| has_religion_terms  | 1                      |   3312 |            2115 | 45.9%              | 44.0%              | 43.8%                       | 42.6%                       |
| script_bucket       | latin_only             |   9303 |            4032 | 37.5%              | 37.0%              | 54.6%                       | 54.8%                       |
| script_bucket       | devanagari_only        |   1287 |             600 | 40.1%              | 37.6%              | 68.0%                       | 60.2%                       |
| script_bucket       | mixed_latin_devanagari |    453 |             201 | 36.4%              | 34.4%              | 59.7%                       | 56.2%                       |

These feature signals are heuristic, not final causal explanations. They tell us where to focus manual reading.

## High-Confidence Disagreement And Error Samples

Full sample table: `results/error_analysis/error_samples.csv`.

Manual annotation template: `results/error_analysis/manual_error_annotation_template.csv`.

| train_dataset       | test_dataset         | outcome                    | prediction_pattern     | script_bucket          |   has_religion_terms |   has_political_terms |   has_abuse_terms | text                                                                                                                                                                                    |
|:--------------------|:---------------------|:---------------------------|:-----------------------|:-----------------------|---------------------:|----------------------:|------------------:|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| cm_splits_codemixed | cm_splits_codemixed  | both_wrong_same_prediction | true=1;mbert=0;muril=0 | mixed_latin_devanagari |                    0 |                     0 |                 0 | इसलिए तो अपन इसको सुप्रीम कोठा नाम दिया है। #SupremeCourtOfIndia #सुप्रीम_कोठा #MaritalRape                                                                                             |
| cm_splits_codemixed | cm_splits_codemixed  | both_wrong_same_prediction | true=1;mbert=0;muril=0 | latin_only             |                    0 |                     0 |                 0 | USER Smh. 🤕                                                                                                                                                                             |
| cm_splits_codemixed | cm_splits_codemixed  | both_wrong_same_prediction | true=0;mbert=1;muril=1 | latin_only             |                    1 |                     0 |                 0 | USER USER Ye love jihad nhi lag rha...ye gharelu utpeedan Ka case hai....ladke ne dharm nhi chhipaya tha, jhut nhi Bola tha....to ye love jihad nhi h....                               |
| cm_splits_codemixed | cm_splits_codemixed  | both_wrong_same_prediction | true=0;mbert=1;muril=1 | latin_only             |                    0 |                     0 |                 0 | USER USER USER USER Hathras mdhe in the dark of the night ek mulila forcibly jalal gele tichya family la ghari bandist karun,…ashya kiti tari ghatna hotana yanche sentiments hurt h... |
| cm_splits_codemixed | cm_splits_codemixed  | both_wrong_same_prediction | true=1;mbert=0;muril=0 | latin_only             |                    0 |                     0 |                 0 | USER USER Rathiye.adivasi me sikha du                                                                                                                                                   |
| cm_splits_codemixed | cm_splits_codemixed  | both_wrong_same_prediction | true=0;mbert=1;muril=1 | latin_only             |                    1 |                     0 |                 0 | Give the concepts of terms like 'love jihad' or the shutting of doors of education on hijabi women, a thought. Not allowing women to choose their life partners, or denying them edu... |
| cm_splits_codemixed | cm_splits_codemixed  | both_wrong_same_prediction | true=1;mbert=0;muril=0 | latin_only             |                    0 |                     0 |                 0 | USER O gyyani, first reconsider their performance... playing IPL                                                                                                                        |
| cm_splits_codemixed | cm_splits_codemixed  | both_wrong_same_prediction | true=1;mbert=0;muril=0 | latin_only             |                    0 |                     1 |                 0 | USER Hope #mialords didn’t lose any money during demonetisation #SupremeCourt 😉                                                                                                         |
| cm_splits_codemixed | cm_splits_codemixed  | mbert_only_correct         | true=1;mbert=1;muril=0 | latin_only             |                    0 |                     0 |                 0 | USER people who are jihadi apologists are shedding tears for undertrials                                                                                                                |
| cm_splits_codemixed | cm_splits_codemixed  | mbert_only_correct         | true=1;mbert=1;muril=0 | latin_only             |                    0 |                     1 |                 0 | USER USER Hum to 2015 me bank join kiye MUDRA aur Jan Dhan account dekh K hi samajh gya ki bande ne dhang se 'C' kaat diya hai. Phir demonetisation ne aur chaar chaand lga diya.       |
| cm_splits_codemixed | cm_splits_codemixed  | mbert_only_correct         | true=1;mbert=1;muril=0 | latin_only             |                    0 |                     0 |                 0 | USER Indian Army is also sending Kashmiri Islamic jihadist to loose their virginity with 72 hoors in heaven with bullets🤣🤣                                                              |
| cm_splits_codemixed | cm_splits_codemixed  | mbert_only_correct         | true=1;mbert=1;muril=0 | latin_only             |                    0 |                     0 |                 0 | Elnaz Rekabi, Iranian climber, competed oversees with the mandatory hijab. Reports coming from Seoul are worrying. The Iranian delegation has confiscated her phone &amp; passport. ... |
| cm_splits_codemixed | cm_splits_codemixed  | mbert_only_correct         | true=1;mbert=1;muril=0 | latin_only             |                    0 |                     1 |                 0 | USER That man lost a lot of money when the demonetisation happened, and he is still carrying a grudge against Modi ji ? Investigate him for money laundering                            |
| cm_splits_codemixed | cm_splits_codemixed  | mbert_only_correct         | true=0;mbert=0;muril=1 | latin_only             |                    0 |                     0 |                 0 | USER USER wa beta ji moz kar rahe ho to tiwadi jo jati h usko chhod karke dalit ban jao Ye jatipratha banai kisne tum jaise pakhandiyo ne Chale h aarkshan ko kham kar ne aap khatm ... |
| cm_splits_codemixed | cm_splits_codemixed  | mbert_only_correct         | true=0;mbert=0;muril=1 | latin_only             |                    0 |                     1 |                 0 | USER USER What about bjp scams Coffingate Vyapam Mines scam Jobs scam Scam exposed by S Malik Karnataka cut commission UP police extortion list And Demonetisation Electoral bonds H... |
| cm_splits_codemixed | cm_splits_codemixed  | mbert_only_correct         | true=1;mbert=1;muril=0 | latin_only             |                    0 |                     1 |                 0 | USER USER USER 😂😂😂😂😂 nice joke. Beta 1948 se RSS k hi headquarters pr Tiranga lga hua h. Mujhe sikha rhi h jinke khud ke logon ko pta nhi ki Golwalkar Ji ke kya vichaar the ve khud... |
| cm_splits_codemixed | cm_splits_codemixed  | muril_only_correct         | true=0;mbert=1;muril=0 | latin_only             |                    0 |                     0 |                 0 | USER You deserve this embarrassment as u blamed the umpires of the last as puppets of IPL. Jaisi karni waisi bharni                                                                     |
| cm_splits_codemixed | cm_splits_codemixed  | muril_only_correct         | true=0;mbert=1;muril=0 | latin_only             |                    0 |                     1 |                 0 | USER USER First you look behind ur Modi Model of india. Intolerance. How many are tortured. Not too far the disintegration of this nation built by Sardar Patel ji..                    |
| cm_splits_codemixed | cm_splits_codemixed  | muril_only_correct         | true=0;mbert=1;muril=0 | latin_only             |                    0 |                     1 |                 0 | USER Arun Jaitley didn't knew about demonetisation who was the FM that time. Infact no one in the Govt knew about it except Shah, Doval and BJP. Manohar Parikar didn't knew about n... |
| cm_splits_codemixed | cm_splits_codemixed  | muril_only_correct         | true=0;mbert=1;muril=0 | latin_only             |                    0 |                     1 |                 0 | USER USER Are bro even Aamir supported demonetisation. I don't agree with that support of Aamir too.                                                                                    |
| cm_splits_codemixed | cm_splits_codemixed  | muril_only_correct         | true=0;mbert=1;muril=0 | mixed_latin_devanagari |                    0 |                     0 |                 0 | USER USER USER सय्यद मुश्ताक अली ट्रॉफी साठी खूप खूप शुभेच्छा श्रेयस......❣️                                                                                                            |
| cm_splits_codemixed | cm_splits_codemixed  | muril_only_correct         | true=0;mbert=1;muril=0 | latin_only             |                    0 |                     0 |                 0 | USER USER USER tirangey ka apmaan nahi hua, tu divert mat kar, farmers protests aur anti-farmer's bill pe dhyaan de                                                                     |
| cm_splits_codemixed | cm_splits_codemixed  | muril_only_correct         | true=0;mbert=1;muril=0 | latin_only             |                    0 |                     0 |                 0 | USER Ye aaj kiske vanshaj hain? Bhagat singh, Rana Pratap or Sardar Patel or Gandhiji.                                                                                                  |
| cm_splits_codemixed | cm_splits_codemixed  | muril_only_correct         | true=0;mbert=1;muril=0 | latin_only             |                    0 |                     1 |                 0 | USER India is a vibrant democracy, it's people are lashing out against 60 years old corrupt governance. Whem Modi will not fit the bill, they vote him out too. If you are talking K... |
| cm_splits_codemixed | kaggle_hinglish_hate | both_wrong_same_prediction | true=1;mbert=0;muril=0 | latin_only             |                    0 |                     0 |                 1 | SuChai TO Ye Hai Ks Ki ArMy Rape kRti Hai Ab KhNa Ye B JOoTh hai                                                                                                                        |
| cm_splits_codemixed | kaggle_hinglish_hate | both_wrong_same_prediction | true=1;mbert=0;muril=0 | latin_only             |                    0 |                     0 |                 1 | Dalit ladki ka rape Kiya tere bhai ne USER ?? URL …                                                                                                                                     |
| cm_splits_codemixed | kaggle_hinglish_hate | both_wrong_same_prediction | true=1;mbert=0;muril=0 | latin_only             |                    0 |                     0 |                 0 | rundi                                                                                                                                                                                   |
| cm_splits_codemixed | kaggle_hinglish_hate | both_wrong_same_prediction | true=0;mbert=1;muril=1 | latin_only             |                    0 |                     0 |                 1 | Abe gandu... Hum baap log hi hain!! Gawar saale pehle apna terrorism wala desh ko sambhalo                                                                                              |
| cm_splits_codemixed | kaggle_hinglish_hate | both_wrong_same_prediction | true=1;mbert=0;muril=0 | latin_only             |                    0 |                     0 |                 1 | I hate Yuvraj URL …                                                                                                                                                                     |
| cm_splits_codemixed | kaggle_hinglish_hate | both_wrong_same_prediction | true=0;mbert=1;muril=1 | latin_only             |                    0 |                     0 |                 1 | mahajiron se kisi ko bhe nafrat nahe hai,mostly log mohajiron ki tragedy ko samjhte hain.aur ,but altaf husain ne qatal o gharatkar ke mohajir cause ko badnaam kar dia hai.            |

## Hard False Negatives

Hard false negatives are positive examples that both mBERT and MuRIL predicted as negative for the same train/test condition. Full table: `results/error_analysis/hard_false_negative_samples.csv`.

| train_dataset       | test_dataset         | prediction_pattern     | script_bucket          |   has_religion_terms |   has_political_terms |   has_abuse_terms | text                                                                                                                                                                                    |
|:--------------------|:---------------------|:-----------------------|:-----------------------|---------------------:|----------------------:|------------------:|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| cm_splits_codemixed | cm_splits_codemixed  | true=1;mbert=0;muril=0 | mixed_latin_devanagari |                    0 |                     0 |                 0 | इसलिए तो अपन इसको सुप्रीम कोठा नाम दिया है। #SupremeCourtOfIndia #सुप्रीम_कोठा #MaritalRape                                                                                             |
| cm_splits_codemixed | cm_splits_codemixed  | true=1;mbert=0;muril=0 | latin_only             |                    0 |                     0 |                 0 | USER Smh. 🤕                                                                                                                                                                             |
| cm_splits_codemixed | cm_splits_codemixed  | true=1;mbert=0;muril=0 | latin_only             |                    0 |                     0 |                 0 | USER USER Rathiye.adivasi me sikha du                                                                                                                                                   |
| cm_splits_codemixed | cm_splits_codemixed  | true=1;mbert=0;muril=0 | latin_only             |                    0 |                     0 |                 0 | USER O gyyani, first reconsider their performance... playing IPL                                                                                                                        |
| cm_splits_codemixed | cm_splits_codemixed  | true=1;mbert=0;muril=0 | latin_only             |                    0 |                     1 |                 0 | USER Hope #mialords didn’t lose any money during demonetisation #SupremeCourt 😉                                                                                                         |
| cm_splits_codemixed | cm_splits_codemixed  | true=1;mbert=0;muril=0 | latin_only             |                    0 |                     0 |                 0 | Undertrials can't vote but can contest polls: SC Underrail can't vote but the can be elected representatives "Mera Desh Mahan" #LokSabhaElections2019                                   |
| cm_splits_codemixed | cm_splits_codemixed  | true=1;mbert=0;muril=0 | latin_only             |                    0 |                     0 |                 0 | USER As proclaimed by the neighbors, PSL is the no.1 Cricket league in the world. Why would they play in the IPL.. C'mon man!!!                                                         |
| cm_splits_codemixed | cm_splits_codemixed  | true=1;mbert=0;muril=0 | latin_only             |                    0 |                     0 |                 0 | For our society every man is like Ravana and every woman is Sita, so as per supreme court verdict on #MaritalRape                                                                       |
| cm_splits_codemixed | cm_splits_codemixed  | true=1;mbert=0;muril=0 | latin_only             |                    0 |                     0 |                 0 | USER USER USER changing your vocab 👀 haha                                                                                                                                               |
| cm_splits_codemixed | cm_splits_codemixed  | true=1;mbert=0;muril=0 | latin_only             |                    1 |                     0 |                 0 | Triple Talaq is back in the Republic. #AgneepathRecruitmentScheme is like 4 years of marriage and then #Talaq #Talaq #Talaq to the 75% of the recruits... Which selection process go... |
| cm_splits_codemixed | cm_splits_codemixed  | true=1;mbert=0;muril=0 | mixed_latin_devanagari |                    0 |                     0 |                 0 | भारत में पत्नी पड़ोसी के साथ सो सकती है, पति को आपत्ति हो तो पति पर #MaritalRape फाइल कर सकती है! #MarriageStrike #BoycottMarriage                                                      |
| cm_splits_codemixed | cm_splits_codemixed  | true=1;mbert=0;muril=0 | latin_only             |                    0 |                     1 |                 0 | Priyanka Gandhi(Vadra), is she even knows what the farmer's bill is ? if she has real concerns for farmers then let her husband Mr Robert Vadra to release all illegal acquisition o... |
| cm_splits_codemixed | kaggle_hinglish_hate | true=1;mbert=0;muril=0 | latin_only             |                    0 |                     0 |                 1 | SuChai TO Ye Hai Ks Ki ArMy Rape kRti Hai Ab KhNa Ye B JOoTh hai                                                                                                                        |
| cm_splits_codemixed | kaggle_hinglish_hate | true=1;mbert=0;muril=0 | latin_only             |                    0 |                     0 |                 1 | Dalit ladki ka rape Kiya tere bhai ne USER ?? URL …                                                                                                                                     |
| cm_splits_codemixed | kaggle_hinglish_hate | true=1;mbert=0;muril=0 | latin_only             |                    0 |                     0 |                 1 | I hate Yuvraj URL …                                                                                                                                                                     |
| cm_splits_codemixed | kaggle_hinglish_hate | true=1;mbert=0;muril=0 | latin_only             |                    0 |                     0 |                 0 | rundi                                                                                                                                                                                   |
| cm_splits_codemixed | kaggle_hinglish_hate | true=1;mbert=0;muril=0 | latin_only             |                    0 |                     0 |                 1 | Aaj Deepu Form me hai I hate u                                                                                                                                                          |
| cm_splits_codemixed | kaggle_hinglish_hate | true=1;mbert=0;muril=0 | latin_only             |                    0 |                     0 |                 0 | soover                                                                                                                                                                                  |
| cm_splits_codemixed | kaggle_hinglish_hate | true=1;mbert=0;muril=0 | latin_only             |                    0 |                     0 |                 1 | We hate naam sethi                                                                                                                                                                      |
| cm_splits_codemixed | kaggle_hinglish_hate | true=1;mbert=0;muril=0 | latin_only             |                    0 |                     0 |                 0 | soower                                                                                                                                                                                  |
| cm_splits_codemixed | kaggle_hinglish_hate | true=1;mbert=0;muril=0 | latin_only             |                    0 |                     0 |                 0 | khatmal                                                                                                                                                                                 |
| cm_splits_codemixed | kaggle_hinglish_hate | true=1;mbert=0;muril=0 | latin_only             |                    0 |                     0 |                 1 | I hate manu rohan KO priyanka se compare karta hai. Kuch bhi URL …                                                                                                                      |
| cm_splits_codemixed | kaggle_hinglish_hate | true=1;mbert=0;muril=0 | latin_only             |                    0 |                     0 |                 0 | makhanchudai                                                                                                                                                                            |
| cm_splits_codemixed | kaggle_hinglish_hate | true=1;mbert=0;muril=0 | latin_only             |                    0 |                     0 |                 0 | bum                                                                                                                                                                                     |
| cm_splits_codemixed | thar_religion        | true=1;mbert=0;muril=0 | latin_only             |                    1 |                     0 |                 0 | JO ISLAM KA NHI WO KISI KAAM KA NHI ❌                                                                                                                                                   |
| cm_splits_codemixed | thar_religion        | true=1;mbert=0;muril=0 | latin_only             |                    1 |                     0 |                 0 | Gullat fut gyi h mulla ki                                                                                                                                                               |
| cm_splits_codemixed | thar_religion        | true=1;mbert=0;muril=0 | latin_only             |                    0 |                     0 |                 0 | Nice ab Pooja bhi road pr hoge                                                                                                                                                          |
| cm_splits_codemixed | thar_religion        | true=1;mbert=0;muril=0 | latin_only             |                    1 |                     0 |                 0 | Jadatar Mandir road pe hi hai😀                                                                                                                                                          |
| cm_splits_codemixed | thar_religion        | true=1;mbert=0;muril=0 | latin_only             |                    1 |                     0 |                 0 | Aur Islam ko chodo yahi hal hoga                                                                                                                                                        |
| cm_splits_codemixed | thar_religion        | true=1;mbert=0;muril=0 | latin_only             |                    0 |                     1 |                 0 | Q bahi pakistan t sshirt aur jeans ban he kya                                                                                                                                           |

## Top Error Terms

Full term table: `results/error_analysis/top_error_terms.csv`.

### `mbert` False-Negative Terms

| train_dataset       | test_dataset        |   rank | token       |   count |
|:--------------------|:--------------------|-------:|:------------|--------:|
| cm_splits_codemixed | cm_splits_codemixed |      1 | can         |       7 |
| cm_splits_codemixed | cm_splits_codemixed |      2 | में         |       7 |
| cm_splits_codemixed | cm_splits_codemixed |      3 | like        |       6 |
| cm_splits_codemixed | cm_splits_codemixed |      4 | talaq       |       6 |
| cm_splits_codemixed | cm_splits_codemixed |      5 | man         |       5 |
| cm_splits_codemixed | cm_splits_codemixed |      6 | uapa        |       5 |
| cm_splits_codemixed | cm_splits_codemixed |      7 | gandhi      |       4 |
| cm_splits_codemixed | cm_splits_codemixed |      8 | what        |       4 |
| cm_splits_codemixed | cm_splits_codemixed |      9 | nehru       |       4 |
| cm_splits_codemixed | cm_splits_codemixed |     10 | सुप्रीम     |       4 |
| cm_splits_codemixed | cm_splits_codemixed |     11 | bill        |       4 |
| cm_splits_codemixed | cm_splits_codemixed |     12 | right       |       4 |
| cm_splits_codemixed | cm_splits_codemixed |     13 | ipl         |       4 |
| cm_splits_codemixed | cm_splits_codemixed |     14 | back        |       4 |
| cm_splits_codemixed | cm_splits_codemixed |     15 | india       |       3 |
| cm_splits_codemixed | cm_splits_codemixed |     16 | about       |       3 |
| cm_splits_codemixed | cm_splits_codemixed |     17 | which       |       3 |
| cm_splits_codemixed | cm_splits_codemixed |     18 | maritalrape |       3 |
| cm_splits_codemixed | cm_splits_codemixed |     19 | every       |       3 |
| cm_splits_codemixed | cm_splits_codemixed |     20 | hijab       |       3 |

### `muril` False-Negative Terms

| train_dataset       | test_dataset        |   rank | token          |   count |
|:--------------------|:--------------------|-------:|:---------------|--------:|
| cm_splits_codemixed | cm_splits_codemixed |      1 | demonetisation |       7 |
| cm_splits_codemixed | cm_splits_codemixed |      2 | can            |       7 |
| cm_splits_codemixed | cm_splits_codemixed |      3 | what           |       6 |
| cm_splits_codemixed | cm_splits_codemixed |      4 | rss            |       6 |
| cm_splits_codemixed | cm_splits_codemixed |      5 | में            |       6 |
| cm_splits_codemixed | cm_splits_codemixed |      6 | man            |       6 |
| cm_splits_codemixed | cm_splits_codemixed |      7 | like           |       6 |
| cm_splits_codemixed | cm_splits_codemixed |      8 | uapa           |       6 |
| cm_splits_codemixed | cm_splits_codemixed |      9 | who            |       6 |
| cm_splits_codemixed | cm_splits_codemixed |     10 | ipl            |       6 |
| cm_splits_codemixed | cm_splits_codemixed |     11 | nehru          |       5 |
| cm_splits_codemixed | cm_splits_codemixed |     12 | golwalkar      |       5 |
| cm_splits_codemixed | cm_splits_codemixed |     13 | hijab          |       5 |
| cm_splits_codemixed | cm_splits_codemixed |     14 | right          |       5 |
| cm_splits_codemixed | cm_splits_codemixed |     15 | bill           |       5 |
| cm_splits_codemixed | cm_splits_codemixed |     16 | talaq          |       5 |
| cm_splits_codemixed | cm_splits_codemixed |     17 | muslim         |       4 |
| cm_splits_codemixed | cm_splits_codemixed |     18 | india          |       4 |
| cm_splits_codemixed | cm_splits_codemixed |     19 | gandhi         |       4 |
| cm_splits_codemixed | cm_splits_codemixed |     20 | about          |       4 |

## Figures

- `results/error_analysis/false_negative_rates.png`
- `results/error_analysis/false_negative_rates.svg`
- `results/error_analysis/model_disagreement_advantage.png`
- `results/error_analysis/model_disagreement_advantage.svg`

## Initial Interpretation

- Kaggle-trained models miss many positive examples on THAR, confirming that broad Hinglish hate training does not transfer cleanly to targeted religious hate.
- THAR-trained models still miss many Kaggle positives, confirming that targeted religious hate training does not become a general Hinglish hate detector.
- mBERT tends to have lower false-negative rates on matched Kaggle and CM conditions, while MuRIL has lower false-negative rates on matched THAR and THAR-to-CM transfer.
- Disagreement rows are the most useful manual-reading set: they show where model pretraining and dataset situation produce different decisions on the same text.
- The next manual step is to annotate sampled errors with human-readable reasons such as label ambiguity, target-group cue, political context, transliteration, Devanagari/script issue, generic profanity, or missing context.