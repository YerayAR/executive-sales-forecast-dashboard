from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)


def build_product_catalog() -> pd.DataFrame:
    products = [
        ("Software", "BI", "Power BI Pro", 1200, 720),
        ("Software", "BI", "Power BI Premium", 3200, 1950),
        ("Services", "Consulting", "Analytics Advisory", 4800, 2600),
        ("Services", "Consulting", "Forecast Optimization", 5400, 3000),
        ("Data", "Warehouse", "SQL Warehouse Starter", 2600, 1550),
        ("Data", "Warehouse", "SQL Warehouse Enterprise", 6200, 3600),
        ("Automation", "RPA", "RPA Bot License", 4100, 2500),
        ("Automation", "RPA", "Intelligent Document Processing", 5800, 3550),
        ("Platform", "Cloud", "Data Platform Subscription", 6900, 4300),
        ("Platform", "Cloud", "ML Forecast Add-on", 3600, 2200),
    ]
    return pd.DataFrame(
        products,
        columns=["category", "subcategory", "product_name", "unit_price", "unit_cost"],
    )


def build_region_catalog() -> pd.DataFrame:
    regions = [
        ("North America", "USA", "Ava Brooks"),
        ("Europe", "Spain", "Liam Carter"),
        ("LATAM", "Mexico", "Mia Sanchez"),
        ("Middle East", "UAE", "Noah Hassan"),
    ]
    return pd.DataFrame(regions, columns=["region_name", "country", "sales_manager"])


def generate_sales() -> pd.DataFrame:
    rng = np.random.default_rng(42)
    dates = pd.date_range("2023-01-01", "2025-12-31", freq="D")
    products = build_product_catalog()
    regions = build_region_catalog()
    channels = np.array(["Direct", "Partner", "Online"])
    customers = np.array(
        [
            "Nova Retail",
            "Axis Health",
            "Zenith Logistics",
            "Blue Peak Energy",
            "Vertex Finance",
            "Atlas Telecom",
            "Bright Core Labs",
            "Summit Foods",
            "Urban Mobility Co",
            "Pioneer Manufacturing",
        ]
    )

    records: list[dict[str, object]] = []
    sales_id = 1

    for current_date in dates:
        weekday = current_date.weekday()
        base_orders = 10 if weekday < 5 else 6
        seasonal_uplift = 1.18 if current_date.month in (10, 11, 12) else 1.0
        monthly_factor = 1 + ((current_date.month - 6) / 40)
        daily_orders = max(3, int(rng.poisson(base_orders * seasonal_uplift * monthly_factor)))

        for order_number in range(daily_orders):
            product = products.sample(1, random_state=int(rng.integers(0, 1_000_000))).iloc[0]
            region = regions.sample(1, random_state=int(rng.integers(0, 1_000_000))).iloc[0]
            units_sold = int(rng.integers(1, 9))
            discount_pct = float(rng.choice([0.0, 0.03, 0.05, 0.07, 0.1], p=[0.25, 0.2, 0.25, 0.2, 0.1]))
            demand_multiplier = 1.15 if product["category"] in {"Platform", "Services"} else 1.0
            revenue = product["unit_price"] * units_sold * (1 - discount_pct) * demand_multiplier
            cost = product["unit_cost"] * units_sold
            profit = revenue - cost

            records.append(
                {
                    "sales_id": sales_id,
                    "order_id": f"SO-{current_date:%Y%m%d}-{order_number + 1:03d}",
                    "order_date": current_date.date().isoformat(),
                    "region_name": region["region_name"],
                    "country": region["country"],
                    "sales_manager": region["sales_manager"],
                    "channel_name": str(rng.choice(channels, p=[0.45, 0.3, 0.25])),
                    "category": product["category"],
                    "subcategory": product["subcategory"],
                    "product_name": product["product_name"],
                    "customer_name": str(rng.choice(customers)),
                    "units_sold": units_sold,
                    "unit_price": float(product["unit_price"]),
                    "unit_cost": float(product["unit_cost"]),
                    "discount_pct": round(discount_pct, 2),
                    "revenue": round(revenue, 2),
                    "cost": round(cost, 2),
                    "profit": round(profit, 2),
                }
            )
            sales_id += 1

    sales_df = pd.DataFrame(records).sort_values(["order_date", "order_id"]).reset_index(drop=True)
    return sales_df


def main() -> None:
    sales_df = generate_sales()
    sales_df.to_csv(RAW_DIR / "sales.csv", index=False)
    build_product_catalog().to_csv(RAW_DIR / "products.csv", index=False)
    build_region_catalog().to_csv(RAW_DIR / "regions.csv", index=False)


if __name__ == "__main__":
    main()
