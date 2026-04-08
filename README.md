# Executive Sales & Forecast Dashboard

Portfolio project that combines Python, SQL, forecasting, and BI-ready outputs to simulate an executive sales analytics workflow.

## What This Project Demonstrates

- Building a synthetic but realistic sales dataset with daily granularity.
- Modeling a small analytical warehouse in SQLite using fact and dimension tables.
- Creating KPI and reporting exports for Power BI.
- Training a forecasting model with `scikit-learn` and exporting a 90-day revenue forecast.

## Business Scenario

The use case represents a sales leadership dashboard designed to answer:

- How much revenue, profit, and volume are we generating?
- Which regions, channels, and product categories perform best?
- How are sales evolving over time?
- What revenue should we expect over the next 90 days?

## Tech Stack

- Python
- Pandas
- SQL
- SQLite
- Scikit-Learn
- Power BI

## Pipeline Outputs

Current generated results:

- 10,205 synthetic orders
- 46,155 units sold
- 207.8M total revenue
- 87.6M total profit
- 90-day forecast exported for BI consumption

## Repository Structure

```text
executive-sales-forecast-dashboard/
|-- data/
|   |-- raw/
|   `-- processed/
|-- exports/
|-- models/
|-- scripts/
|-- sql/
|-- requirements.txt
`-- README.md
```

## Key Files

- [scripts/run_pipeline.py](./scripts/run_pipeline.py): runs the full pipeline end to end.
- [scripts/generate_sample_data.py](./scripts/generate_sample_data.py): builds the synthetic sales dataset.
- [scripts/build_warehouse.py](./scripts/build_warehouse.py): creates the warehouse and exports reporting views.
- [scripts/train_forecast.py](./scripts/train_forecast.py): trains the forecast model and generates predictions.
- [sql/schema.sql](./sql/schema.sql): warehouse schema.
- [sql/analytics_views.sql](./sql/analytics_views.sql): analytical SQL views.

## How to Run

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python scripts/run_pipeline.py
```

## BI Deliverables

The `exports/` folder contains files ready to import into Power BI:

- `dashboard_sales.csv`
- `kpi_summary.csv`
- `monthly_sales.csv`
- `sales_forecast.csv`

## Why It Matters

This project shows a practical mix of analytics engineering and business reporting: data preparation, warehouse modeling, forecasting, and BI handoff in one reproducible workflow.
