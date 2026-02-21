-- view_to_cart_funnel.sql
WITH session_events AS (
    SELECT 
        session_id,
        MAX(CASE WHEN event_type = 'view' THEN 1 ELSE 0 END) AS has_view,
        MAX(CASE WHEN event_type = 'cart' THEN 1 ELSE 0 END) AS has_cart,
        MAX(CASE WHEN event_type = 'purchase' THEN 1 ELSE 0 END) AS has_purchase
    FROM events
    GROUP BY session_id
)
SELECT 
    COUNT(session_id) AS total_sessions,
    SUM(has_view) AS viewed_product,
    SUM(has_cart) AS added_to_cart,
    SUM(has_purchase) AS purchased,
    ROUND(SUM(CASE WHEN has_view = 1 AND has_cart = 1 THEN 1 ELSE 0 END) * 100.0 / NULLIF(SUM(has_view), 0), 2) AS view_to_cart_rate,
    ROUND(SUM(CASE WHEN has_cart = 1 AND has_purchase = 1 THEN 1 ELSE 0 END) * 100.0 / NULLIF(SUM(has_cart), 0), 2) AS cart_to_purchase_rate,
    ROUND(SUM(CASE WHEN has_view = 1 AND has_purchase = 1 THEN 1 ELSE 0 END) * 100.0 / NULLIF(SUM(has_view), 0), 2) AS overall_conversion_rate
FROM session_events;
