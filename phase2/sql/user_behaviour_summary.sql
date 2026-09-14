-- Count how many users belong to each behavioural group

WITH user_metrics AS (
    SELECT
        u.user_id,

        COUNT(p.post_id) AS post_count,

        AVG(
            COALESCE(p.likes, 0)
            + p.shares
            + p.comments
        ) AS average_engagement

    FROM users AS u
    INNER JOIN posts AS p
        ON u.user_id = p.user_id

    GROUP BY u.user_id
),

classified_users AS (
    SELECT
        user_id,
        post_count,
        average_engagement,

        CASE
            WHEN post_count >= 15
                 AND average_engagement >= 5000
                THEN 'high-frequency_high-impact'

            WHEN post_count >= 15
                THEN 'high-frequency'

            WHEN average_engagement >= 5000
                THEN 'high-impact'

            ELSE 'occasional_or_low-impact'
        END AS behaviour_group

    FROM user_metrics
)

SELECT
    behaviour_group,
    COUNT(*) AS user_count,
    ROUND(
        100.0 * COUNT(*) / (SELECT COUNT(*) FROM classified_users),
        2
    ) AS percentage_of_users
FROM classified_users
GROUP BY behaviour_group
ORDER BY user_count DESC;