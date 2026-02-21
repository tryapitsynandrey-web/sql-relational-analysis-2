-- weekend_degradation.sql
WITH daily_metrics AS (
    SELECT 
        DATE_TRUNC('day', timestamp) AS act_date,
        EXTRACT('dow' FROM timestamp) AS day_of_week,
        CASE WHEN EXTRACT('dow' FROM timestamp) IN (0, 6) THEN 'Weekend' ELSE 'Weekday' END AS day_type,
        COUNT(DISTINCT session_id) as sessions,
        SUM(CASE WHEN event_type = 'purchase' THEN price ELSE 0 END) AS daily_revenue
    FROM events
    GROUP BY 1, 2, 3
)
SELECT 
    day_type,
    ROUND(AVG(sessions), 0) AS avg_daily_sessions,
    ROUND(AVG(daily_revenue), 2) AS avg_daily_revenue,
    ROUND(AVG(daily_revenue) / NULLIF(AVG(sessions), 0), 2) AS revenue_per_session
FROM daily_metrics
GROUP BY 1;
