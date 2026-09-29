SELECT
    SUM(revenue) AS total_revenue,
    SUM(profit) AS total_profit,
    ROUND(AVG(margin), 2) AS average_margin,
    COUNT(DISTINCT order_id) AS total_orders
FROM {{ ref('sales_analytics') }}