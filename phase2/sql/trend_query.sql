-- Monthly post volume and month-to-month change

WITH monthly_posts AS (
    SELECT
        strftime('%Y-%m', timestamp) AS month,
        COUNT(*) AS post_count
    FROM posts
    GROUP BY strftime('%Y-%m', timestamp)
),

monthly_with_previous AS (
    SELECT
        month,
        post_count,

        LAG(post_count) OVER (
            ORDER BY month
        ) AS previous_month_count

    FROM monthly_posts
)

SELECT
    month,
    post_count,
    previous_month_count,

    ROUND(
        100.0 * (post_count - previous_month_count)
        / NULLIF(previous_month_count, 0),
        2
    ) AS percentage_change

FROM monthly_with_previous
ORDER BY month;