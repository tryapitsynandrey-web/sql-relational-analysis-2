-- anomaly_detection.sql
WITH daily_conversion AS (
    SELECT 
        DATE_TRUNC('day', timestamp) AS act_date,
        SUM(CASE WHEN event_type = 'purchase' THEN 1 ELSE 0 END) AS daily_purchases,
        SUM(CASE WHEN event_type = 'view' THEN 1 ELSE 0 END) AS daily_views
    FROM events
    GROUP BY 1
),
conversion_rates AS (
    SELECT 
        act_date,
        daily_purchases,
        daily_views,
        ROUND((daily_purchases * 100.0) / NULLIF(daily_views, 0), 2) AS daily_cv_rate
    FROM daily_conversion
),
moving_metrics AS (
    SELECT 
        act_date,
        daily_cv_rate,
        AVG(daily_cv_rate) OVER (
            ORDER BY act_date 
            ROWS BETWEEN 7 PRECEDING AND 1 PRECEDING
        ) AS moving_7d_avg_cv_rate
    FROM conversion_rates
)
SELECT 
    act_date,
    daily_cv_rate,
    moving_7d_avg_cv_rate,
    ROUND((daily_cv_rate - moving_7d_avg_cv_rate) * 100.0 / NULLIF(moving_7d_avg_cv_rate, 0), 2) AS drop_percentage
FROM moving_metrics
WHERE moving_7d_avg_cv_rate IS NOT NULL
  AND ROUND((daily_cv_rate - moving_7d_avg_cv_rate) * 100.0 / NULLIF(moving_7d_avg_cv_rate, 0), 2) < -20.0
ORDER BY drop_percentage ASC, act_date DESC;
