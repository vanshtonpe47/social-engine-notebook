-- M2 - Do High Follower Users Get More Engagement?
--
-- High follower users: follower_count >= 25000
-- Low follower users: follower_count < 25000
--
-- Total engagement = likes + shares + comments.
-- Missing likes are treated as zero only for this calculation.

WITH post_engagement AS (
    SELECT
        post_id,
        user_id,
        COALESCE(likes, 0) + shares + comments
            AS total_engagement
    FROM posts
),

user_groups AS (
    SELECT
        user_id,
        CASE
            WHEN follower_count >= 25000
                THEN 'High follower (>=25000)'
            ELSE 'Low follower (<25000)'
        END AS follower_group
    FROM users
),

group_summary AS (
    SELECT
        user_groups.follower_group,
        COUNT(post_engagement.post_id) AS post_count,
        COUNT(DISTINCT user_groups.user_id) AS user_count,
        AVG(post_engagement.total_engagement)
            AS average_engagement_per_post
    FROM user_groups
    LEFT JOIN post_engagement
        ON user_groups.user_id = post_engagement.user_id
    GROUP BY user_groups.follower_group
)

SELECT
    follower_group,
    post_count,
    user_count,
    ROUND(average_engagement_per_post, 2)
        AS average_engagement_per_post
FROM group_summary
ORDER BY average_engagement_per_post DESC;
