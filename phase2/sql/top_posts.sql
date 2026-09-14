-- Find the top 5 posts within each platform
-- Missing likes are treated as zero only for ranking.

WITH ranked_posts AS (
    SELECT
        post_id,
        user_id,
        COALESCE(platform, 'Missing') AS platform,
        timestamp,
        likes,
        shares,
        comments,

        COALESCE(likes, 0) + shares + comments
            AS total_engagement,

        ROW_NUMBER() OVER (
            PARTITION BY COALESCE(platform, 'Missing')
            ORDER BY
                COALESCE(likes, 0) + shares + comments DESC,
                post_id
        ) AS platform_rank

    FROM posts
)

SELECT
    platform,
    platform_rank,
    post_id,
    user_id,
    timestamp,
    likes,
    shares,
    comments,
    total_engagement
FROM ranked_posts
WHERE platform_rank <= 5
ORDER BY platform, platform_rank;