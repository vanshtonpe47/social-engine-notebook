-- Calculate the correlation between follower count
-- and average engagement per user.

WITH user_engagement AS (
    SELECT
        u.user_id,
        u.follower_count,

        AVG(
            COALESCE(p.likes, 0)
            + p.shares
            + p.comments
        ) AS average_engagement

    FROM users AS u
    INNER JOIN posts AS p
        ON u.user_id = p.user_id

    GROUP BY
        u.user_id,
        u.follower_count
),

means AS (
    SELECT
        AVG(follower_count) AS mean_followers,
        AVG(average_engagement) AS mean_engagement
    FROM user_engagement
)

SELECT
    COUNT(*) AS users_in_sample,

    ROUND(
        SUM(
            (follower_count - mean_followers)
            * (average_engagement - mean_engagement)
        )
        /
        NULLIF(
            SQRT(
                SUM(
                    (follower_count - mean_followers)
                    * (follower_count - mean_followers)
                )
                *
                SUM(
                    (average_engagement - mean_engagement)
                    * (average_engagement - mean_engagement)
                )
            ),
            0
        ),
        4
    ) AS pearson_correlation

FROM user_engagement
CROSS JOIN means;