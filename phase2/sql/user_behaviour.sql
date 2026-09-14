-- Group users by posting frequency and average engagement

WITH user_metrics AS (
    SELECT
        u.user_id,
        u.location,
        u.language,
        u.follower_count,

        COUNT(p.post_id) AS post_count,

        ROUND(
            AVG(
                COALESCE(p.likes, 0)
                + p.shares
                + p.comments
            ),
            2
        ) AS average_engagement

    FROM users AS u
    INNER JOIN posts AS p
        ON u.user_id = p.user_id

    GROUP BY
        u.user_id,
        u.location,
        u.language,
        u.follower_count
)

SELECT
    user_id,
    location,
    language,
    follower_count,
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

ORDER BY
    average_engagement DESC;