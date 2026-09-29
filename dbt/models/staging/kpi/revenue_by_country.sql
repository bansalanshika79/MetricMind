SELECT
    country,
    SUM(revenue) AS revenue
FROM {{ ref('sales_analytics') }}
GROUP BY country
ORDER BY revenue DESC