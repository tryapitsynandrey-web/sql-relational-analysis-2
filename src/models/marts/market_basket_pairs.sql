-- market_basket_pairs.sql
WITH cart_items AS (
    SELECT session_id, product_id
    FROM events
    WHERE event_type = 'purchase'
),
item_pairs AS (
    SELECT 
        a.product_id AS product_a,
        b.product_id AS product_b,
        COUNT(DISTINCT a.session_id) AS co_purchase_count
    FROM cart_items a
    JOIN cart_items b 
        ON a.session_id = b.session_id 
        AND a.product_id < b.product_id
    GROUP BY 1, 2
)
SELECT 
    product_a,
    product_b,
    co_purchase_count,
    RANK() OVER (ORDER BY co_purchase_count DESC) as pair_rank
FROM item_pairs
WHERE co_purchase_count > 1
ORDER BY co_purchase_count DESC
LIMIT 10;
