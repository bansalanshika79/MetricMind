SELECT *
FROM {{ source('ecommerce', 'staging_ecommerce_orders') }}