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
| logistic_regression | 0.5961 | 0.5972 | 0.5971 |
| linear_svm | 0.5801 | 0.5806 | 0.5806 |

Selected model: **logistic_regression**

## Final test metrics

| Metric | Score |
|---|---:|
| Accuracy | 0.5885 |
| Macro precision | 0.5913 |
| Macro recall | 0.5887 |
| Macro F1-score | 0.5897 |
| Weighted F1-score | 0.5894 |

## Per-class metrics

| Class | Precision | Recall | F1-score | Support |
|---|---:|---:|---:|---:|
| Negative | 0.6481 | 0.6385 | 0.6433 | 603 |
| Neutral | 0.5138 | 0.5474 | 0.5301 | 612 |
| Positive | 0.6120 | 0.5803 | 0.5957 | 598 |

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
| logistic_regression | 0.9114 | 0.6049 | 0.8961 |
| linear_svm | 0.9158 | 0.5884 | 0.8961 |

Selected model: **logistic_regression**

## Final test metrics

| Metric | Score |
|---|---:|
| Accuracy | 0.9073 |
| Macro precision | 0.7890 |
| Macro recall | 0.5091 |
| Macro F1-score | 0.5875 |
| Weighted F1-score | 0.8948 |

## Per-class metrics

| Class | Precision | Recall | F1-score | Support |
|---|---:|---:|---:|---:|
| Account_Security | 1.0000 | 0.3077 | 0.4706 | 26 |
| Community_Discussion | 0.9184 | 0.9839 | 0.9500 | 1555 |
| Feature_Feedback | 0.3056 | 0.1667 | 0.2157 | 66 |
| Technical_Issues | 0.9320 | 0.5783 | 0.7138 | 166 |

## Confusion matrix

![Topic confusion matrix](../figures/topic_confusion_matrix.png)

---

# 3. Interpretation

The sentiment classifier achieved a macro F1-score of **0.5897**.

The topic classifier achieved accuracy of **0.9073** and macro F1-score of **0.5875**.

The topic accuracy is high partly because `Community_Discussion` is the dominant class. Macro F1 is therefore also reported.