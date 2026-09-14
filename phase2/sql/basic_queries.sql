-- Query 1: View the first five posts
SELECT *
FROM posts
LIMIT 5;


-- Query 2: Count posts by platform
SELECT
    platform,
    COUNT(*) AS post_count
FROM posts
GROUP BY platform
ORDER BY post_count DESC;


-- Query 3: Count users by language
SELECT
    language,
    COUNT(*) AS user_count
FROM users
GROUP BY language
ORDER BY user_count DESC;


-- Query 4: Calculate average engagement
SELECT
    AVG(likes) AS average_likes,
    AVG(shares) AS average_shares,
    AVG(comments) AS average_comments
FROM posts;