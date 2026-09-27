CREATE TABLE staging_ecommerce_orders (
    order_id INT,
    customer_id VARCHAR(20),
    order_date DATE,
    year INT,
    month INT,
    day INT,
    day_of_week VARCHAR(15),
    quarter INT,
    customer_age INT,
    customer_gender VARCHAR(10),
    country VARCHAR(50),
    city VARCHAR(100),
    customer_segment VARCHAR(30),
    product_id VARCHAR(20),
    product_category VARCHAR(50),
    product_subcategory VARCHAR(50),
    brand VARCHAR(50),
    unit_price DECIMAL(10,2),
    quantity INT,
    discount_percent DECIMAL(5,2),
    discount_amount DECIMAL(10,2),
    coupon_used VARCHAR(10),
    shipping_cost DECIMAL(10,2),
    tax_amount DECIMAL(10,2),
    order_amount DECIMAL(12,2),
    payment_method VARCHAR(30),
    device_type VARCHAR(30),
    traffic_source VARCHAR(30),
    membership_status VARCHAR(20),
    shipping_method VARCHAR(30),
    warehouse_region VARCHAR(30),
    delivery_days INT,
    order_status VARCHAR(20),
    returned VARCHAR(10),
    review_rating DECIMAL(2,1),
    customer_lifetime_value DECIMAL(12,2),
    profit_margin_percent DECIMAL(5,2),
    profit_amount DECIMAL(12,2),
    season VARCHAR(20),
    holiday_season VARCHAR(10),
    high_value_order VARCHAR(10)
);

\copy staging_ecommerce_orders FROM 'C:/path_to_file/ecommerce_orders_dataset' WITH (FORMAT csv, HEADER true, DELIMITER ',');



CREATE TABLE dim_customer (
    customer_id VARCHAR(20) PRIMARY KEY,
    customer_age INT,
    customer_gender VARCHAR(10),
    customer_segment VARCHAR(30),
    membership_status VARCHAR(20),
    customer_lifetime_value DECIMAL(12,2)
);

CREATE TABLE dim_product (
    product_id VARCHAR(20) PRIMARY KEY,
    product_category VARCHAR(50),
    product_subcategory VARCHAR(50),
    brand VARCHAR(50),
    unit_price DECIMAL(10,2)
);


CREATE TABLE dim_region (
    region_id SERIAL PRIMARY KEY,
    country VARCHAR(50),
    city VARCHAR(100),
    warehouse_region VARCHAR(30),
    UNIQUE(country, city, warehouse_region)
);

CREATE TABLE dim_date (
    date_id DATE PRIMARY KEY,
    year INT,
    quarter VARCHAR(5),
    month INT,
    day INT,
    day_of_week VARCHAR(15),
    season VARCHAR(20),
    holiday_season BOOLEAN
);

CREATE TABLE fact_sales (
    order_id VARCHAR(20) PRIMARY KEY,

    customer_id VARCHAR(20),
    product_id VARCHAR(20),
    region_id INT,
    date_id DATE,

    quantity INT,
    discount_percent DECIMAL(5,2),
    discount_amount DECIMAL(10,2),
    shipping_cost DECIMAL(10,2),
    tax_amount DECIMAL(10,2),

    order_amount DECIMAL(12,2),
    profit_amount DECIMAL(12,2),
    profit_margin_percent DECIMAL(5,2),

    payment_method VARCHAR(30),
    shipping_method VARCHAR(30),
    traffic_source VARCHAR(30),
    device_type VARCHAR(30),

    delivery_days INT,
    order_status VARCHAR(20),
    returned BOOLEAN,
    review_rating DECIMAL(2,1),
    coupon_used BOOLEAN,
    high_value_order BOOLEAN,

    CONSTRAINT fk_customer
        FOREIGN KEY (customer_id)
        REFERENCES dim_customer(customer_id),

    CONSTRAINT fk_product
        FOREIGN KEY (product_id)
        REFERENCES dim_product(product_id),

    CONSTRAINT fk_region
        FOREIGN KEY (region_id)
        REFERENCES dim_region(region_id),

    CONSTRAINT fk_date
        FOREIGN KEY (date_id)
        REFERENCES dim_date(date_id)
);
