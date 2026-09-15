-- H3 - Platform Performance Compared With Its Own Average
--
-- A post is exceptional when its total engagement is at least
-- two times the average engagement of its own platform.
--
-- Posts with missing platforms are excluded because they cannot
-- be compared with a platform-specific average.
--
-- Missing likes are treated as zero only for total engagement.

WITH post_engagement AS (
    SELECT
        post_id,
        user_id,
        platform,
        timestamp,

        COALESCE(likes, 0) + shares + comments
            AS total_engagement

    FROM posts

    WHERE platform IS NOT NULL
),

platform_averages AS (
    SELECT
        platform,

        AVG(total_engagement)
            AS platform_average_engagement

    FROM post_engagement

    GROUP BY platform
)

SELECT
    post_engagement.platform,
    post_engagement.post_id,
    post_engagement.user_id,
    post_engagement.timestamp,
    post_engagement.total_engagement,

    ROUND(
        platform_averages.platform_average_engagement,
        2
    ) AS platform_average_engagement,

    ROUND(
        post_engagement.total_engagement
        / platform_averages.platform_average_engagement,
        2
    ) AS multiple_of_platform_average

FROM post_engagement

INNER JOIN platform_averages
    ON post_engagement.platform = platform_averages.platform

WHERE post_engagement.total_engagement
      >= 2 * platform_averages.platform_average_engagement

ORDER BY
    post_engagement.platform,
    post_engagement.total_engagement DESC;
