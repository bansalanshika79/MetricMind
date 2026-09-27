/* Total Revenue */
SELECT
    SUM(revenue) AS total_revenue
FROM sales_analytics;


/* Total Profit */
SELECT
    SUM(profit) AS total_profit
FROM sales_analytics;


/* Average Margin */
SELECT
    ROUND(AVG(margin), 2) AS average_margin
FROM sales_analytics;


/* Total Orders */
SELECT
    COUNT(DISTINCT order_id) AS total_orders
FROM sales_analytics;


/* Revenue by Country */
SELECT
    country,
    SUM(revenue) AS revenue
FROM sales_analytics
GROUP BY country
ORDER BY revenue DESC;


/* Profit by Product Category */
SELECT
    product_category,
    SUM(profit) AS profit
FROM sales_analytics
GROUP BY product_category
ORDER BY profit DESC;


/* Monthly Revenue */
SELECT
    year,
    month,
    SUM(revenue) AS revenue
FROM sales_analytics
GROUP BY year, month
ORDER BY year, month;


