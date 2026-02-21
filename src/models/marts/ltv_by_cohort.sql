-- ltv_by_cohort.sql
WITH user_first_purchase AS (
    SELECT 
        user_id,
        MIN(DATE_TRUNC('month', timestamp)) AS cohort_month
    FROM events
    WHERE event_type = 'purchase'
    GROUP BY user_id
),
revenue_by_user_month AS (
    SELECT 
        e.user_id,
        u.cohort_month,
        DATE_TRUNC('month', e.timestamp) AS revenue_month,
        DATE_DIFF('month', u.cohort_month, DATE_TRUNC('month', e.timestamp)) AS months_since_first_purchase,
        SUM(e.price) AS total_revenue
    FROM events e
    JOIN user_first_purchase u ON e.user_id = u.user_id
    WHERE e.event_type = 'purchase'
    GROUP BY 1, 2, 3, 4
)
SELECT 
    cohort_month,
    months_since_first_purchase,
    COUNT(DISTINCT user_id) as active_users,
    SUM(total_revenue) AS cohort_revenue,
    SUM(total_revenue) / COUNT(DISTINCT user_id) AS arpu,
    SUM(SUM(total_revenue)) OVER (PARTITION BY cohort_month ORDER BY months_since_first_purchase) AS cumulative_revenue,
    SUM(SUM(total_revenue)) OVER (PARTITION BY cohort_month ORDER BY months_since_first_purchase) / MAX(COUNT(DISTINCT user_id)) OVER (PARTITION BY cohort_month) AS cumulative_ltv
FROM revenue_by_user_month
GROUP BY 1, 2
ORDER BY 1 DESC, 2 ASC;
