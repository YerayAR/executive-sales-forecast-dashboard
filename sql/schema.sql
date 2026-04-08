DROP TABLE IF EXISTS fact_sales;
DROP TABLE IF EXISTS dim_date;
DROP TABLE IF EXISTS dim_region;
DROP TABLE IF EXISTS dim_channel;
DROP TABLE IF EXISTS dim_product;

CREATE TABLE dim_date (
    date_id INTEGER PRIMARY KEY,
    full_date TEXT NOT NULL UNIQUE,
    year INTEGER NOT NULL,
    quarter INTEGER NOT NULL,
    month INTEGER NOT NULL,
    month_name TEXT NOT NULL,
    week_of_year INTEGER NOT NULL,
    day_of_month INTEGER NOT NULL,
    is_weekend INTEGER NOT NULL
);

CREATE TABLE dim_region (
    region_id INTEGER PRIMARY KEY,
    region_name TEXT NOT NULL,
    country TEXT NOT NULL,
    sales_manager TEXT NOT NULL
);

CREATE TABLE dim_channel (
    channel_id INTEGER PRIMARY KEY,
    channel_name TEXT NOT NULL UNIQUE
);

CREATE TABLE dim_product (
    product_id INTEGER PRIMARY KEY,
    category TEXT NOT NULL,
    subcategory TEXT NOT NULL,
    product_name TEXT NOT NULL UNIQUE,
    unit_price REAL NOT NULL,
    unit_cost REAL NOT NULL
);

CREATE TABLE fact_sales (
    sales_id INTEGER PRIMARY KEY,
    order_id TEXT NOT NULL,
    date_id INTEGER NOT NULL,
    region_id INTEGER NOT NULL,
    channel_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    customer_name TEXT NOT NULL,
    units_sold INTEGER NOT NULL,
    revenue REAL NOT NULL,
    cost REAL NOT NULL,
    profit REAL NOT NULL,
    discount_pct REAL NOT NULL,
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id),
    FOREIGN KEY (region_id) REFERENCES dim_region(region_id),
    FOREIGN KEY (channel_id) REFERENCES dim_channel(channel_id),
    FOREIGN KEY (product_id) REFERENCES dim_product(product_id)
);

CREATE INDEX idx_fact_sales_date ON fact_sales (date_id);
CREATE INDEX idx_fact_sales_region ON fact_sales (region_id);
CREATE INDEX idx_fact_sales_channel ON fact_sales (channel_id);
CREATE INDEX idx_fact_sales_product ON fact_sales (product_id);
