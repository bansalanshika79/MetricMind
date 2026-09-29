SELECT
    s.order_id,
    s.customer_id,
    s.product_id,
    r.region_id,
    s.order_date AS date_id,
    s.order_date,
    s.quantity,
    s.unit_price,
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
    s.returned,
    s.review_rating,
    s.coupon_used,
    s.high_value_order

FROM {{ ref('stg_orders') }} s

LEFT JOIN public.dim_region r
    ON s.country = r.country
    AND s.city = r.city
    AND s.warehouse_region = r.warehouse_region