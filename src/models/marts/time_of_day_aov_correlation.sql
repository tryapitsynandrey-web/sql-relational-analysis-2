-- time_of_day_aov_correlation.sql
WITH hourly_purchases AS (
    SELECT 
        EXTRACT('hour' FROM timestamp) AS hour_of_day,
        COUNT(DISTINCT session_id) AS total_orders,
        SUM(price) AS total_revenue
    FROM events
    WHERE event_type = 'purchase'
    GROUP BY 1
)
SELECT 
    hour_of_day,
    total_orders,
    total_revenue,
    ROUND(total_revenue / NULLIF(total_orders, 0), 2) AS aov,
    RANK() OVER (ORDER BY (total_revenue / NULLIF(total_orders, 0)) DESC) AS aov_rank
FROM hourly_purchases
ORDER BY hour_of_day;
