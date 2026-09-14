-- Analyze missing text and likes by platform

SELECT
    COALESCE(platform, 'Missing') AS platform,
    COUNT(*) AS post_count,

    SUM(
        CASE
            WHEN text_content IS NULL THEN 1
            ELSE 0
        END
    ) AS missing_text,

    SUM(
        CASE
            WHEN likes IS NULL THEN 1
            ELSE 0
        END
    ) AS missing_likes,

    ROUND(
        100.0 * SUM(
            CASE
                WHEN text_content IS NULL THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS missing_text_percentage,

    ROUND(
        100.0 * SUM(
            CASE
                WHEN likes IS NULL THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS missing_likes_percentage

FROM posts
GROUP BY platform
ORDER BY missing_likes_percentage DESC;