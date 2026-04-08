from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"
SQL_DIR = ROOT / "sql"
EXPORT_DIR = ROOT / "exports"

DB_PATH = PROCESSED_DIR / "sales_warehouse.db"


def build_date_dimension(sales_df: pd.DataFrame) -> pd.DataFrame:
    dates = pd.DataFrame({"full_date": pd.to_datetime(sales_df["order_date"]).sort_values().unique()})
    iso_calendar = dates["full_date"].dt.isocalendar()
    dates["date_id"] = dates["full_date"].dt.strftime("%Y%m%d").astype(int)
    dates["year"] = dates["full_date"].dt.year
    dates["quarter"] = dates["full_date"].dt.quarter
    dates["month"] = dates["full_date"].dt.month
    dates["month_name"] = dates["full_date"].dt.strftime("%B")
    dates["week_of_year"] = iso_calendar.week.astype(int)
    dates["day_of_month"] = dates["full_date"].dt.day
    dates["is_weekend"] = (dates["full_date"].dt.weekday >= 5).astype(int)
    dates["full_date"] = dates["full_date"].dt.date.astype(str)
    return dates[
        ["date_id", "full_date", "year", "quarter", "month", "month_name", "week_of_year", "day_of_month", "is_weekend"]
    ]


def create_tables(connection: sqlite3.Connection) -> None:
    schema_sql = (SQL_DIR / "schema.sql").read_text(encoding="utf-8")
    connection.executescript(schema_sql)


def create_views(connection: sqlite3.Connection) -> None:
    views_sql = (SQL_DIR / "analytics_views.sql").read_text(encoding="utf-8")
    connection.executescript(views_sql)


def export_views(connection: sqlite3.Connection) -> None:
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    dashboard_sales = pd.read_sql_query("SELECT * FROM vw_dashboard_sales", connection)
    monthly_sales = pd.read_sql_query("SELECT * FROM vw_monthly_sales", connection)
    kpi_summary = pd.read_sql_query("SELECT * FROM vw_kpi_summary", connection)

    dashboard_sales.to_csv(EXPORT_DIR / "dashboard_sales.csv", index=False)
    monthly_sales.to_csv(EXPORT_DIR / "monthly_sales.csv", index=False)
    kpi_summary.to_csv(EXPORT_DIR / "kpi_summary.csv", index=False)


def main() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    sales_df = pd.read_csv(RAW_DIR / "sales.csv")

    date_dim = build_date_dimension(sales_df)
    region_dim = (
        sales_df[["region_name", "country", "sales_manager"]]
        .drop_duplicates()
        .sort_values(["region_name", "country"])
        .reset_index(drop=True)
    )
    region_dim.insert(0, "region_id", range(1, len(region_dim) + 1))

    channel_dim = (
        sales_df[["channel_name"]].drop_duplicates().sort_values("channel_name").reset_index(drop=True)
    )
    channel_dim.insert(0, "channel_id", range(1, len(channel_dim) + 1))

    product_dim = (
        sales_df[["category", "subcategory", "product_name", "unit_price", "unit_cost"]]
        .drop_duplicates()
        .sort_values(["category", "subcategory", "product_name"])
        .reset_index(drop=True)
    )
    product_dim.insert(0, "product_id", range(1, len(product_dim) + 1))

    fact_sales = (
        sales_df.merge(region_dim, on=["region_name", "country", "sales_manager"], how="left")
        .merge(channel_dim, on="channel_name", how="left")
        .merge(product_dim, on=["category", "subcategory", "product_name", "unit_price", "unit_cost"], how="left")
    )
    fact_sales["date_id"] = pd.to_datetime(fact_sales["order_date"]).dt.strftime("%Y%m%d").astype(int)
    fact_sales = fact_sales[
        [
            "sales_id",
            "order_id",
            "date_id",
            "region_id",
            "channel_id",
            "product_id",
            "customer_name",
            "units_sold",
            "revenue",
            "cost",
            "profit",
            "discount_pct",
        ]
    ]

    with sqlite3.connect(DB_PATH) as connection:
        create_tables(connection)
        date_dim.to_sql("dim_date", connection, if_exists="append", index=False)
        region_dim.to_sql("dim_region", connection, if_exists="append", index=False)
        channel_dim.to_sql("dim_channel", connection, if_exists="append", index=False)
        product_dim.to_sql("dim_product", connection, if_exists="append", index=False)
        fact_sales.to_sql("fact_sales", connection, if_exists="append", index=False)
        create_views(connection)
        export_views(connection)


if __name__ == "__main__":
    main()
