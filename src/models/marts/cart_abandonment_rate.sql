-- cart_abandonment_rate.sql
WITH session_events AS (
    SELECT 
        DATE_TRUNC('day', timestamp) as act_date,
        session_id,
        MAX(CASE WHEN event_type = 'cart' THEN 1 ELSE 0 END) AS added_to_cart,
        MAX(CASE WHEN event_type = 'purchase' THEN 1 ELSE 0 END) AS purchased
    FROM events
    GROUP BY 1, 2
)
SELECT 
    act_date,
    COUNT(session_id) as total_sessions,
    SUM(added_to_cart) as carts_created,
    SUM(purchased) as successful_purchases,
    SUM(added_to_cart) - SUM(purchased) as abandoned_carts,
    ROUND((SUM(added_to_cart) - SUM(purchased)) * 100.0 / NULLIF(SUM(added_to_cart), 0), 2) AS cart_abandonment_rate,
    ROUND(AVG((SUM(added_to_cart) - SUM(purchased)) * 100.0 / NULLIF(SUM(added_to_cart), 0)) OVER (), 2) AS avg_historical_abandonment
FROM session_events
GROUP BY 1
HAVING SUM(added_to_cart) > 0
ORDER BY act_date DESC;
