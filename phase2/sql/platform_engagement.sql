-- Compare average engagement by platform

SELECT
    COALESCE(platform, 'Missing') AS platform,
    COUNT(*) AS post_count,
    ROUND(AVG(likes), 2) AS average_likes,
    ROUND(AVG(shares), 2) AS average_shares,
    ROUND(AVG(comments), 2) AS average_comments,
    ROUND(
        AVG(
            COALESCE(likes, 0)
            + shares
            + comments
        ),
        2
    ) AS average_total_engagement
FROM posts
GROUP BY platform
ORDER BY average_total_engagement DESC;