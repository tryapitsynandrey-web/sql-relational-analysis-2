-- aov_trends.sql
WITH daily_purchases AS (
    SELECT 
        DATE_TRUNC('day', timestamp) AS act_date,
        COUNT(DISTINCT session_id) AS total_orders,
        SUM(price) AS total_revenue
    FROM events
    WHERE event_type = 'purchase'
    GROUP BY 1
)
SELECT 
    act_date,
    total_orders,
    total_revenue,
    total_revenue / NULLIF(total_orders, 0) AS aov,
    AVG(total_revenue / NULLIF(total_orders, 0)) OVER (
        ORDER BY act_date 
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS moving_7d_aov
FROM daily_purchases
ORDER BY act_date DESC;
