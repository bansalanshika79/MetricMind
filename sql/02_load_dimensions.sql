INSERT INTO dim_customer (customer_id, customer_age, customer_gender, customer_segment, membership_status, customer_lifetime_value)
SELECT DISTINCT ON (customer_id)
    customer_id,
    customer_age,
    customer_gender,
    customer_segment,
    membership_status,
    customer_lifetime_value
FROM staging_ecommerce_orders
WHERE customer_id IS NOT NULL
ON CONFLICT (customer_id) DO NOTHING;

SELECT COUNT(*) FROM dim_customer;
SELECT * FROM dim_customer LIMIT 10;


INSERT INTO dim_product (product_id, product_category, product_subcategory, brand, unit_price)
SELECT DISTINCT ON (product_id)
    product_id,
    product_category,
    product_subcategory,
    brand,
    unit_price
FROM staging_ecommerce_orders
WHERE product_id IS NOT NULL
ON CONFLICT (product_id) DO NOTHING;

SELECT COUNT(*) FROM dim_product;
SELECT * FROM dim_product LIMIT 10;

INSERT INTO dim_region (country, city, warehouse_region)
SELECT DISTINCT
    country,
    city,
    warehouse_region
FROM staging_ecommerce_orders
WHERE country IS NOT NULL AND city IS NOT NULL
ON CONFLICT (country, city, warehouse_region) DO NOTHING;

SELECT COUNT(*) FROM dim_region;
SELECT * FROM dim_region LIMIT 10;

INSERT INTO dim_date (date_id, year, quarter, month, day, day_of_week, season, holiday_season)
SELECT DISTINCT
    order_date AS date_id,
    year,
    'Q' || quarter::text AS quarter,
    month,
    day,
    day_of_week,
    season,
    CASE 
        WHEN LOWER(holiday_season) IN ('true', 'yes', '1') THEN TRUE 
        ELSE FALSE 
    END AS holiday_season
FROM staging_ecommerce_orders
WHERE order_date IS NOT NULL
ON CONFLICT (date_id) DO NOTHING;

SELECT COUNT(*) FROM dim_date;
SELECT * FROM dim_date LIMIT 10;



