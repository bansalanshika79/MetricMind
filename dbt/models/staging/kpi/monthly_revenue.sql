SELECT
    year,
    month,
    SUM(revenue) AS revenue
FROM {{ ref('sales_analytics') }}
GROUP BY year, month
ORDER BY year, month