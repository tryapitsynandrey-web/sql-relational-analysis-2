-- cohort_retention.sql
WITH user_first_purchase AS (
    SELECT 
        user_id,
        MIN(DATE_TRUNC('day', timestamp)) AS cohort_date
    FROM events
    WHERE event_type = 'purchase'
    GROUP BY user_id
),
retention_data AS (
    SELECT 
        u.cohort_date,
        e.user_id,
        DATE_DIFF('day', u.cohort_date, DATE_TRUNC('day', e.timestamp)) AS days_since_first_purchase
    FROM events e
    JOIN user_first_purchase u ON e.user_id = u.user_id
    WHERE e.event_type = 'purchase'
)
SELECT 
    cohort_date,
    COUNT(DISTINCT user_id) AS cohort_size,
    COUNT(DISTINCT CASE WHEN days_since_first_purchase BETWEEN 1 AND 7 THEN user_id END) AS retained_7_days,
    COUNT(DISTINCT CASE WHEN days_since_first_purchase BETWEEN 8 AND 14 THEN user_id END) AS retained_14_days,
    COUNT(DISTINCT CASE WHEN days_since_first_purchase BETWEEN 15 AND 30 THEN user_id END) AS retained_30_days,
    ROUND(COUNT(DISTINCT CASE WHEN days_since_first_purchase BETWEEN 1 AND 7 THEN user_id END) * 100.0 / NULLIF(COUNT(DISTINCT user_id), 0), 2) AS retention_rate_7d,
    ROUND(COUNT(DISTINCT CASE WHEN days_since_first_purchase BETWEEN 8 AND 14 THEN user_id END) * 100.0 / NULLIF(COUNT(DISTINCT user_id), 0), 2) AS retention_rate_14d,
    ROUND(COUNT(DISTINCT CASE WHEN days_since_first_purchase BETWEEN 15 AND 30 THEN user_id END) * 100.0 / NULLIF(COUNT(DISTINCT user_id), 0), 2) AS retention_rate_30d
FROM retention_data
GROUP BY cohort_date
ORDER BY cohort_date DESC;
