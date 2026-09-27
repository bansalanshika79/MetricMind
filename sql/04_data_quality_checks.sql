/* Check duplicate orders */
SELECT
    order_id,
    COUNT(*)
FROM staging_ecommerce_orders
GROUP BY order_id
HAVING COUNT(*) > 1;

/* Check missing customers */
SELECT COUNT(*)
FROM staging_ecommerce_orders
WHERE customer_id IS NULL;

/* Check missing products */
SELECT COUNT(*)
FROM staging_ecommerce_orders
WHERE product_id IS NULL;

/* Check missing dates */
SELECT COUNT(*)
FROM staging_ecommerce_orders
WHERE order_date IS NULL;

/* Check negative revenue */
SELECT COUNT(*)
FROM fact_sales
WHERE order_amount < 0;

/* Check negative quantity */
SELECT COUNT(*)
FROM fact_sales
WHERE quantity < 0;

