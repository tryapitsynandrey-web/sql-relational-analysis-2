-- time_to_first_purchase.sql
WITH user_first_events AS (
    SELECT 
        user_id,
        MIN(CASE WHEN event_type = 'view' THEN timestamp END) AS first_view,
        MIN(CASE WHEN event_type = 'purchase' THEN timestamp END) AS first_purchase
    FROM events
    GROUP BY user_id
),
purchase_times AS (
    SELECT 
        user_id,
        first_view,
        first_purchase,
        DATE_DIFF('minute', first_view, first_purchase) AS minutes_to_purchase
    FROM user_first_events
    WHERE first_purchase IS NOT NULL AND first_view IS NOT NULL AND first_purchase >= first_view
)
SELECT 
    CASE 
        WHEN minutes_to_purchase <= 10 THEN '0-10 mins'
        WHEN minutes_to_purchase <= 30 THEN '11-30 mins'
        WHEN minutes_to_purchase <= 60 THEN '31-60 mins'
        WHEN minutes_to_purchase <= 1440 THEN '1-24 hours'
        ELSE '1+ days'
    END AS time_segment,
    COUNT(user_id) AS user_count,
    ROUND(COUNT(user_id) * 100.0 / SUM(COUNT(user_id)) OVER (), 2) AS pct_of_purchasers,
    ROUND(SUM(CASE WHEN MIN(minutes_to_purchase) <= 60 THEN COUNT(user_id) ELSE 0 END) OVER () * 100.0 / SUM(COUNT(user_id)) OVER (), 2) AS fast_buyers_pct
FROM purchase_times
GROUP BY 1
ORDER BY MIN(minutes_to_purchase);
