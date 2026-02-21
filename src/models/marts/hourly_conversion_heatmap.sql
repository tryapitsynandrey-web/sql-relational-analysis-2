-- hourly_conversion_heatmap.sql
WITH hourly_events AS (
    SELECT 
        EXTRACT('dow' FROM timestamp) AS day_of_week,
        EXTRACT('hour' FROM timestamp) AS hour_of_day,
        COUNT(CASE WHEN event_type = 'view' THEN 1 END) AS views,
        COUNT(CASE WHEN event_type = 'purchase' THEN 1 END) AS purchases
    FROM events
    GROUP BY 1, 2
)
SELECT 
    day_of_week,
    hour_of_day,
    views,
    purchases,
    ROUND(purchases * 100.0 / NULLIF(views, 0), 2) AS conversion_rate
FROM hourly_events
ORDER BY day_of_week, hour_of_day;
