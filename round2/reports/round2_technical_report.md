# Data Vortex 2026 - Round 2 Technical Report

## 1. Problem Definition

The Social Engine requires a semantic layer capable of interpreting short human-language posts.

This project builds two classifiers:

```text
post_text -> sentiment_label
post_text -> topic_category
```

The sentiment model predicts Positive, Negative, or Neutral. The topic model predicts the category of the post.

## 2. Dataset Overview

The dataset contains 9,000 records and four source columns:

```text
text_id
post_text
sentiment_label
topic_category
```

The inspection found no missing values, blank text values, duplicate complete rows, or duplicate text IDs.

There are 7,900 unique text values and 987 repeated text values. Repeated texts have no conflicting labels.

The sentiment labels are balanced with 3,000 records per class. The topic labels are strongly imbalanced.

## 3. Preprocessing Pipeline

The preprocessing pipeline:

1. Decodes HTML entities.
2. Decodes escaped Unicode sequences where possible.
3. Replaces URLs with `URLTOKEN`.
4. Replaces mentions with `USERTOKEN`.
5. Normalizes whitespace.
6. Converts text to lowercase.
7. Creates TF-IDF unigram and bigram features.

TF-IDF used minimum document frequency 2, sublinear term frequency, and a maximum of 100,000 features.

## 4. Model Selection

Two models were compared:

- Logistic Regression.
- Linear Support Vector Machine.

Both used the same TF-IDF representation and balanced class weights.

Models were selected using validation macro F1-score because macro F1 gives equal importance to every class.

Selected sentiment model: **logistic_regression**

Selected topic model: **logistic_regression**

Final models were saved as:

```text
round2/models/sentiment_model.pkl
round2/models/topic_model.pkl
```

## 5. Training Methodology

| Split | Records |
|---|---:|
| Training | 5382 |
| Validation | 1805 |
| Testing | 1813 |

A group-aware split used the original text as the group. Therefore identical texts could not cross dataset splits.

Train/validation overlap: 0

Train/test overlap: 0

Validation/test overlap: 0

The selected model was retrained on training plus validation records and evaluated once on the untouched test set.

## 6. Evaluation Metrics

### Sentiment classification

| Metric | Score |
|---|---:|
| Accuracy | 0.5885 |
| Macro precision | 0.5913 |
| Macro recall | 0.5887 |
| Macro F1-score | 0.5897 |
| Weighted F1-score | 0.5894 |

Per-class results:

| Class | Precision | Recall | F1-score | Support |
|---|---:|---:|---:|---:|
| Negative | 0.6481 | 0.6385 | 0.6433 | 603 |
| Neutral | 0.5138 | 0.5474 | 0.5301 | 612 |
| Positive | 0.6120 | 0.5803 | 0.5957 | 598 |

### Topic classification

| Metric | Score |
|---|---:|
| Accuracy | 0.9073 |
| Macro precision | 0.7890 |
| Macro recall | 0.5091 |
| Macro F1-score | 0.5875 |
| Weighted F1-score | 0.8948 |

Per-class results:

| Class | Precision | Recall | F1-score | Support |
|---|---:|---:|---:|---:|
| Account_Security | 1.0000 | 0.3077 | 0.4706 | 26 |
| Community_Discussion | 0.9184 | 0.9839 | 0.9500 | 1555 |
| Feature_Feedback | 0.3056 | 0.1667 | 0.2157 | 66 |
| Technical_Issues | 0.9320 | 0.5783 | 0.7138 | 166 |

## 7. Confusion Matrices

### Sentiment

![Sentiment confusion matrix](../figures/sentiment_confusion_matrix.png)

### Topic

![Topic confusion matrix](../figures/topic_confusion_matrix.png)

The matrices show strong majority-class performance and more difficulty with neutral sentiment and minority topics.

## 8. Error Analysis

The error files were generated from final test predictions:

```text
round2/reports/sentiment_errors.csv
round2/reports/topic_errors.csv
```

### Sentiment error examples

| Text ID | Actual label | Predicted label | Text |
|---|---|---|---|
| TXT_00003 | Positive | Neutral | Would you like to join us at our annual gala at the Sandman Signature Resort on Oct 25? Contact our centre at 6042773100 for tickets! |
| TXT_00006 | Negative | Positive | @user @user aaaah. Nokia used to make the Best Phone Cameras Ever.  Sadly I think those days may be past. |
| TXT_00010 | Neutral | Positive | "1st game played under Solar Powered floodlights in the world happened in MYSA,Nairobi Kenya. #PhilipsLED" |
| TXT_00033 | Positive | Negative | The game 1st album 1 song he say he rap like Eazy-E then Nas then 50 cent then dr Dre then Jay-Z then Eazy-E again then like his dead bro |
| TXT_00108 | Negative | Neutral | November 21 in the lonely hour tour.. OKAY SAM SMITH OKAY!!!! :-(((( TAPOS SOLD OUT PA OKAY!!!!! OKAY LANG TALAGA |

Typical causes include sarcasm, slang, mixed sentiment, short text, and neutral language containing emotional words.

### Topic error examples

| Text ID | Actual label | Predicted label | Text |
|---|---|---|---|
| TXT_00079 | Account_Security | Community_Discussion | bloodymary - hackers nirvana - smell like teen spirit butterfingers - nicotine feeder - 7 days in the sun smashing pumpkins - bullets with.. |
| TXT_00190 | Feature_Feedback | Community_Discussion | What's the requirement to work at Dunkin? Complete up to 8th grade? Reasons I hate going there. No people skills. |
| TXT_00261 | Technical_Issues | Feature_Feedback | "Kendrick Lamar may just be the greatest rapper of this generation, and maybe many more to come" |
| TXT_00296 | Technical_Issues | Community_Discussion | SUN UPDATE: UFC 191, Beyonce with Ronda Rousey, Jimmy Snuka, TUF, New WWE stable, CHIKARA King of Trios |
| TXT_00402 | Feature_Feedback | Community_Discussion | Fuck a Saturday class I just wanna go home and play with our squirrel and watch Jurassic Park |

Topic errors are concentrated in minority categories because those categories contain fewer training examples and share vocabulary with other topics.

## 9. Limitations

The topic dataset is highly imbalanced. The model performs better on Community Discussion than on the smallest classes.

TF-IDF cannot fully understand sarcasm, outside context, world knowledge, or subtle meaning.

Future improvements could include character features, transformer embeddings, cross-validation, hyperparameter tuning, and additional minority-class data.

## 10. Reproducibility

Run these commands from the project root:

```powershell
python "round2\src\inspect_dataset.py"
python "round2\src\check_text_duplicates.py"
python "round2\src\train_models.py"
python "round2\src\generate_reports.py"
```

## 11. Conclusion

This project rebuilds the Social Engine semantic layer using text normalization, duplicate-aware splitting, TF-IDF features, model comparison, final test evaluation, confusion matrices, and error analysis.

The resulting system performs sentiment recognition and topic classification with transparent evaluation and documented limitations.