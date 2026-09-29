SELECT
    product_category,
    SUM(profit) AS profit
FROM {{ ref('sales_analytics') }}
GROUP BY product_category
ORDER BY profit DESC