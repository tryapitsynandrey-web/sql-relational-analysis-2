-- dau_mau_ratio.sql
WITH date_boundaries AS (
    SELECT UNNEST(GENERATE_SERIES(
        (SELECT MIN(DATE_TRUNC('day', timestamp)) FROM events),
        (SELECT MAX(DATE_TRUNC('day', timestamp)) FROM events),
        INTERVAL 1 DAY
    )) AS act_date
),
daily_active AS (
    SELECT 
        DATE_TRUNC('day', timestamp) AS act_date,
        COUNT(DISTINCT user_id) AS dau
    FROM events
    GROUP BY 1
),
monthly_active AS (
    SELECT 
        d.act_date,
        COUNT(DISTINCT e.user_id) AS mau
    FROM date_boundaries d
    LEFT JOIN events e ON DATE_TRUNC('day', e.timestamp) BETWEEN d.act_date - INTERVAL 29 DAY AND d.act_date
    GROUP BY 1
)
SELECT 
    d.act_date,
    COALESCE(da.dau, 0) AS dau,
    m.mau,
    ROUND(COALESCE(da.dau, 0) * 100.0 / NULLIF(m.mau, 0), 2) AS dau_mau_ratio_pct
FROM date_boundaries d
LEFT JOIN daily_active da ON d.act_date = da.act_date
JOIN monthly_active m ON d.act_date = m.act_date
ORDER BY d.act_date DESC;
