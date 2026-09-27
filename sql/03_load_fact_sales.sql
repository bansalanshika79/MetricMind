INSERT INTO fact_sales (
    order_id,
    customer_id,
    product_id,
    region_id,
    date_id,
    quantity,
    discount_percent,
    discount_amount,
    shipping_cost,
    tax_amount,
    order_amount,
    profit_amount,
    profit_margin_percent,
    payment_method,
    shipping_method,
    traffic_source,
    device_type,
    delivery_days,
    order_status,
    returned,
    review_rating,
    coupon_used,
    high_value_order
)
SELECT
    s.order_id::VARCHAR(20),
    s.customer_id,
    s.product_id,
    r.region_id,
    s.order_date,
    s.quantity,
    s.discount_percent,
    s.discount_amount,
    s.shipping_cost,
    s.tax_amount,
    s.order_amount,
    s.profit_amount,
    s.profit_margin_percent,
    s.payment_method,
    s.shipping_method,
    s.traffic_source,
    s.device_type,
    s.delivery_days,
    s.order_status,

    CASE
        WHEN LOWER(s.returned) IN ('true', 'yes', '1') THEN TRUE
        ELSE FALSE
    END,

    s.review_rating,

    CASE
        WHEN LOWER(s.coupon_used) IN ('true', 'yes', '1') THEN TRUE
        ELSE FALSE
    END,

    CASE
        WHEN LOWER(s.high_value_order) IN ('true', 'yes', '1') THEN TRUE
        ELSE FALSE
    END

FROM staging_ecommerce_orders s

JOIN dim_region r
    ON s.country = r.country
    AND s.city = r.city
    AND s.warehouse_region = r.warehouse_region;



SELECT COUNT(*)
FROM fact_sales;

SELECT *
FROM fact_sales
LIMIT 10;

/* Add check for foreign keys works or not */

SELECT
    f.order_id,
    f.customer_id,
    c.customer_segment,
    f.product_id,
    p.product_category,
    f.region_id,
    r.country,
    f.order_amount,
    f.profit_amount
FROM fact_sales f
JOIN dim_customer c
    ON f.customer_id = c.customer_id
JOIN dim_product p
    ON f.product_id = p.product_id
JOIN dim_region r
    ON f.region_id = r.region_id
LIMIT 10;
