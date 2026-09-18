# Round 2 Evaluation Metrics Report

## Dataset and evaluation design

The dataset contains 9,000 labelled text records. Two supervised NLP tasks were evaluated:

1. Sentiment classification.
2. Topic-category classification.

A group-aware split prevented identical text values from appearing in more than one data split.

| Split | Records |
|---|---:|
| Training | 5382 |
| Validation | 1805 |
| Testing | 1813 |

Final metrics were calculated only on the untouched test set.

---

# 1. Sentiment classification

## Target

```text
post_text -> sentiment_label
```

The classes are Negative, Neutral, and Positive.

## Model selection

| Candidate model | Accuracy | Macro F1 | Weighted F1 |
|---|---:|---:|---:|
| word_C1.0_cwNone | 0.6183 | 0.6169 | 0.6170 |
| word_C2.0_cwbalanced | 0.6127 | 0.6119 | 0.6119 |
| char_C1.0_cwbalanced | 0.6039 | 0.6031 | 0.6031 |
| combined_C0.5_cwNone | 0.6133 | 0.6120 | 0.6121 |
| combined_C1.0_cwNone | 0.6183 | 0.6169 | 0.6170 |
| combined_C2.0_cwNone | 0.6133 | 0.6125 | 0.6125 |

Selected model: **combined_tfidf_logistic_regression**

## Final test metrics

| Metric | Score |
|---|---:|
| Accuracy | 0.6062 |
| Macro precision | 0.6069 |
| Macro recall | 0.6065 |
| Macro F1-score | 0.6067 |
| Weighted F1-score | 0.6063 |

## Per-class metrics

| Class | Precision | Recall | F1-score | Support |
|---|---:|---:|---:|---:|
| Negative | 0.6622 | 0.6501 | 0.6561 | 603 |
| Neutral | 0.5456 | 0.5474 | 0.5465 | 612 |
| Positive | 0.6129 | 0.6221 | 0.6174 | 598 |

## Confusion matrix

![Sentiment confusion matrix](../figures/sentiment_confusion_matrix.png)

---

# 2. Topic classification

## Target

```text
post_text -> topic_category
```

The topic classes are Account Security, Community Discussion, Feature Feedback, and Technical Issues.

## Model selection

| Candidate model | Accuracy | Macro F1 | Weighted F1 |
|---|---:|---:|---:|
| word_C1.0_cwbalanced | 0.9291 | 0.6294 | 0.9138 |
| char_C0.5_cwbalanced | 0.9490 | 0.7315 | 0.9407 |
| char_C1.0_cwbalanced | 0.9457 | 0.6933 | 0.9344 |
| combined_C1.0_cwbalanced | 0.9291 | 0.6294 | 0.9138 |
| combined_C2.0_cwbalanced | 0.9307 | 0.6325 | 0.9155 |

Selected model: **char_tfidf_logistic_regression**

## Final test metrics

| Metric | Score |
|---|---:|
| Accuracy | 0.9619 |
| Macro precision | 0.9157 |
| Macro recall | 0.7607 |
| Macro F1-score | 0.8241 |
| Weighted F1-score | 0.9597 |

## Per-class metrics

| Class | Precision | Recall | F1-score | Support |
|---|---:|---:|---:|---:|
| Account_Security | 0.8750 | 0.5385 | 0.6667 | 26 |
| Community_Discussion | 0.9663 | 0.9942 | 0.9800 | 1555 |
| Feature_Feedback | 0.8627 | 0.6667 | 0.7521 | 66 |
| Technical_Issues | 0.9589 | 0.8434 | 0.8974 | 166 |

## Confusion matrix

![Topic confusion matrix](../figures/topic_confusion_matrix.png)

---

# 3. Interpretation

The sentiment classifier achieved a macro F1-score of **0.6067**.

The topic classifier achieved accuracy of **0.9619** and macro F1-score of **0.8241**.

The topic accuracy is high partly because `Community_Discussion` is the dominant class. Macro F1 is therefore also reported.