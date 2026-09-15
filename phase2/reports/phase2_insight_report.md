# Data Vortex 2026 - Phase 2 Insight Report

## 1. Selected questions

This report presents one solved question from each required difficulty level:

| Difficulty | Selected question |
|---|---|
| Easy | E3 - Average Engagement by Platform |
| Medium | M2 - Do High Follower Users Get More Engagement? |
| Hard | H3 - Platform Performance Compared With Its Own Average |

The analysis uses 1,500 users and 12,000 cleaned posts.

---

## 2. Executive summary

The selected analyses show three main findings:

1. **Reddit has the highest average total engagement per post** among the named platforms.
2. **Low-follower users have slightly higher average engagement per post** than high-follower users in this dataset.
3. **139 posts perform at least twice as well as the average post on their own platform.**

These results are descriptive findings from the cleaned competition dataset. They do not establish causal relationships.

---

## 3. E3 insight - Average Engagement by Platform

The E3 query compares average likes, shares, comments, and total engagement for each platform.

The platform results were:

| Platform | Average total engagement |
|---|---:|
| Reddit | 3,550.43 |
| YouTube | 3,545.70 |
| Facebook | 3,543.78 |
| Instagram | 3,543.53 |
| Twitter | 3,454.84 |

### Finding

**Reddit generated the highest average total engagement**, at approximately **3,550.43 interactions per post**.

YouTube, Facebook, and Instagram were close to Reddit. Twitter had the lowest average total engagement among the named platforms.

### Interpretation

The difference between Reddit and the other leading platforms is relatively small. Therefore, platform alone should not be treated as a complete explanation for engagement performance. Other factors, such as post topic, timing, audience composition, and content quality, may also influence engagement.

---

## 4. M2 insight - Follower Groups and Engagement

The M2 query divides users according to the questionnaire thresholds:

- High follower users: at least 25,000 followers.
- Low follower users: fewer than 25,000 followers.

The results were:

| Follower group | Users | Posts | Average engagement per post |
|---|---:|---:|---:|
| Low follower users | 758 | 6,075 | 3,535.84 |
| High follower users | 742 | 5,925 | 3,508.45 |

### Finding

The low-follower group had the higher average engagement per post:

```text
3,535.84 - 3,508.45 = 27.39
```

The difference is approximately **27.39 interactions per post**.

### Interpretation

In this dataset, having at least 25,000 followers did not correspond to higher average engagement per post. This does not mean that lower follower counts cause higher engagement. It only describes the difference observed between the two predefined groups.

---

## 5. H3 insight - Platform-relative Exceptional Posts

The H3 query identifies posts whose total engagement is at least twice the average engagement of their own platform.

The query identified:

```text
139 exceptional posts
```

### Finding

These 139 posts performed at least two times better than the average post on their respective platforms.

The comparison is platform-relative. For example, a Facebook post is compared with the Facebook average, while a Reddit post is compared with the Reddit average.

### Interpretation

This approach is more informative than comparing every post with one global average. It identifies unusually strong posts within each platform and avoids automatically favoring platforms with higher overall engagement.

The result can support further investigation into:

- Content characteristics.
- Posting time.
- Hashtags.
- Products or topics.
- User characteristics.
- Possible engagement anomalies.

---

## 6. Data-handling assumptions

The analysis follows these assumptions:

1. Total engagement is calculated as:
   ```text
   likes + shares + comments
   ```

2. Missing likes are treated as zero only for total-engagement calculations.

3. Average likes use SQL `AVG(likes)`, which ignores missing likes rather than treating them as zero.

4. Posts with missing platform values are excluded from platform-specific comparisons.

5. The cleaned datasets are not modified during SQL analysis.

6. No missing values are fabricated or manually invented.

These assumptions preserve the available records while making the treatment of missing values explicit.

---

## 7. Limitations

The analysis has several limitations:

- Treating missing likes as zero may underestimate total engagement for affected posts.
- The two-times-average threshold is specified by the questionnaire and is not a formal statistical significance test.
- The data does not establish that platform or follower count causes engagement differences.
- Average values can be influenced by unusually high-performing posts.
- The results are limited to the recovered competition dataset.

A sensitivity analysis could compare results using only posts with observed likes and could also compare means with medians.

---

## 8. Conclusion

The three selected queries provide results across all required difficulty levels.

- **E3** identifies Reddit as the platform with the highest average total engagement.
- **M2** shows that the low-follower group has slightly higher average engagement per post than the high-follower group.
- **H3** identifies 139 posts with engagement at least twice their platform-specific average.

The SQL queries, generated results, JPEG screenshots, logic explanation, and this insight report are maintained as separate reproducible deliverables in the `phase2` directory.
