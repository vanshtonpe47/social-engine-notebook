-- E3 — Average Engagement by Platform
--
-- Question:
-- Calculate the average likes, shares, and comments for each platform.
-- Which platform generates the highest average total engagement?
--
-- Missing-platform posts are excluded because they cannot be assigned
-- to a named platform.
--
-- AVG(likes) ignores missing likes.
-- COALESCE(likes, 0) is used only for total engagement.

WITH platform_engagement AS (
    SELECT
        platform,

        COUNT(*) AS post_count,

        AVG(likes) AS average_likes,
        AVG(shares) AS average_shares,
        AVG(comments) AS average_comments,

        AVG(
            COALESCE(likes, 0) + shares + comments
        ) AS average_total_engagement

    FROM posts

    WHERE platform IS NOT NULL

    GROUP BY platform
)

SELECT
    platform,
    post_count,
    ROUND(average_likes, 2) AS average_likes,
    ROUND(average_shares, 2) AS average_shares,
    ROUND(average_comments, 2) AS average_comments,
    ROUND(average_total_engagement, 2)
        AS average_total_engagement

FROM platform_engagement

ORDER BY average_total_engagement DESC;