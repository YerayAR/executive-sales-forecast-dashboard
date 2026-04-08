DROP VIEW IF EXISTS vw_dashboard_sales;
DROP VIEW IF EXISTS vw_monthly_sales;
DROP VIEW IF EXISTS vw_kpi_summary;

CREATE VIEW vw_dashboard_sales AS
SELECT
    fs.sales_id,
    fs.order_id,
    dd.full_date,
    dd.year,
    dd.quarter,
    dd.month,
    dd.month_name,
    dr.region_name,
    dr.country,
    dr.sales_manager,
    dc.channel_name,
    dp.category,
    dp.subcategory,
    dp.product_name,
    fs.customer_name,
    fs.units_sold,
    fs.revenue,
    fs.cost,
    fs.profit,
    fs.discount_pct
FROM fact_sales fs
INNER JOIN dim_date dd ON fs.date_id = dd.date_id
INNER JOIN dim_region dr ON fs.region_id = dr.region_id
INNER JOIN dim_channel dc ON fs.channel_id = dc.channel_id
INNER JOIN dim_product dp ON fs.product_id = dp.product_id;

CREATE VIEW vw_monthly_sales AS
SELECT
    dd.year,
    dd.month,
    printf('%04d-%02d-01', dd.year, dd.month) AS month_start,
    SUM(fs.revenue) AS revenue,
    SUM(fs.profit) AS profit,
    SUM(fs.units_sold) AS units_sold,
    COUNT(DISTINCT fs.order_id) AS orders
FROM fact_sales fs
INNER JOIN dim_date dd ON fs.date_id = dd.date_id
GROUP BY dd.year, dd.month
ORDER BY month_start;

CREATE VIEW vw_kpi_summary AS
SELECT
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    SUM(units_sold) AS total_units,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(revenue) / COUNT(DISTINCT order_id), 2) AS average_order_value,
    ROUND(SUM(profit) / SUM(revenue), 4) AS profit_margin_pct
FROM fact_sales;
