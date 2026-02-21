-- revenue_degradation.sql
WITH daily_revenue AS (
    SELECT 
        DATE_TRUNC('day', timestamp) AS report_date,
        SUM(price) AS daily_revenue
    FROM events
    WHERE event_type = 'purchase'
    GROUP BY 1
),
revenue_with_lag AS (
    SELECT 
        report_date,
        daily_revenue,
        LAG(daily_revenue, 7) OVER (ORDER BY report_date) AS prev_week_revenue,
        LAG(daily_revenue, 30) OVER (ORDER BY report_date) AS prev_month_revenue
    FROM daily_revenue
)
SELECT 
    report_date,
    daily_revenue,
    prev_week_revenue,
    prev_month_revenue,
    ROUND((daily_revenue - prev_week_revenue) * 100.0 / NULLIF(prev_week_revenue, 0), 2) AS wow_growth_pct,
    ROUND((daily_revenue - prev_month_revenue) * 100.0 / NULLIF(prev_month_revenue, 0), 2) AS mom_growth_pct
FROM revenue_with_lag
ORDER BY report_date DESC;
