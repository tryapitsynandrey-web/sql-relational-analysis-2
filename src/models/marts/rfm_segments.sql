-- rfm_segments.sql
WITH user_metrics AS (
    SELECT 
        user_id,
        DATE_DIFF('day', MAX(timestamp), now()::TIMESTAMP) AS recency_days,
        COUNT(DISTINCT session_id) AS frequency_orders,
        SUM(price) AS monetary_value
    FROM events
    WHERE event_type = 'purchase'
    GROUP BY user_id
),
percentiles AS (
    SELECT 
        user_id,
        recency_days,
        frequency_orders,
        monetary_value,
        NTILE(4) OVER (ORDER BY recency_days DESC) AS r_score,
        NTILE(4) OVER (ORDER BY frequency_orders ASC) AS f_score,
        NTILE(4) OVER (ORDER BY monetary_value ASC) AS m_score
    FROM user_metrics
)
SELECT 
    CASE 
        WHEN r_score >= 3 AND f_score >= 3 AND m_score >= 3 THEN 'Champions'
        WHEN r_score >= 2 AND f_score >= 2 AND m_score >= 2 THEN 'Loyal Customers'
        WHEN r_score >= 3 AND f_score <= 2 THEN 'Recent Buyers'
        WHEN r_score <= 2 AND f_score >= 3 THEN 'At Risk'
        ELSE 'Hibernating'
    END AS rfm_segment,
    COUNT(user_id) AS customer_count,
    ROUND(AVG(recency_days), 1) AS avg_recency,
    ROUND(AVG(frequency_orders), 1) AS avg_frequency,
    ROUND(AVG(monetary_value), 2) AS avg_monetary
FROM percentiles
GROUP BY 1
ORDER BY avg_monetary DESC;
