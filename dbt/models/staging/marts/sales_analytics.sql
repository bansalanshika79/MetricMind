SELECT
    f.order_id,

    -- Date
    d.date_id AS order_date,
    d.year,
    d.quarter,
    d.month,
    d.day_of_week,
    d.season,
    d.holiday_season,

    -- Customer
    c.customer_id,
    c.customer_age,
    c.customer_gender,
    c.customer_segment,
    c.membership_status,
    c.customer_lifetime_value,

    -- Product
    p.product_id,
    p.product_category,
    p.product_subcategory,
    p.brand,

    -- Region
    r.country,
    r.city,
    r.warehouse_region,

    -- Sales measures
    f.quantity,
    f.discount_percent,
    f.discount_amount,
    f.shipping_cost,
    f.tax_amount,
    f.order_amount AS revenue,
    f.profit_amount AS profit,
    f.profit_margin_percent AS margin,

    -- Order information
    f.payment_method,
    f.shipping_method,
    f.traffic_source,
    f.device_type,
    f.delivery_days,
    f.order_status,
    f.returned,
    f.review_rating,
    f.coupon_used,
    f.high_value_order

FROM {{ ref('fct_sales') }} f

LEFT JOIN public.dim_customer c
    ON f.customer_id = c.customer_id

LEFT JOIN public.dim_product p
    ON f.product_id = p.product_id

LEFT JOIN public.dim_region r
    ON f.region_id = r.region_id

LEFT JOIN public.dim_date d
    ON f.order_date = d.date_id