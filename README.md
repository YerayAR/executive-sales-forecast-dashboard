# Executive Sales & Forecast Dashboard

Proyecto end-to-end para portfolio orientado a analitica comercial. Incluye:

- Generacion de ventas sinteticas con granularidad diaria.
- Modelo en estrella en SQLite para analitica SQL.
- Pipeline en Python con `pandas`.
- Forecast de ventas con `scikit-learn`.
- Exportables listos para consumir desde Power BI.

## Stack

- Python
- SQL
- SQLite
- Pandas
- Scikit-Learn
- Power BI

## Estructura

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

## Objetivo del caso

Construir un dashboard ejecutivo con visibilidad casi en tiempo real sobre:

- Revenue total y unidades vendidas.
- Evolucion mensual de ventas y margen.
- Rendimiento por region, canal y categoria.
- Top productos y clientes.
- Forecast de revenue para los proximos 90 dias.

## Como ejecutarlo

1. Crear entorno virtual.
2. Instalar dependencias.
3. Ejecutar el pipeline.

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python scripts/run_pipeline.py
```

## Salidas generadas

- `data/raw/sales.csv`: dataset base.
- `data/processed/sales_warehouse.db`: data warehouse SQLite.
- `exports/dashboard_sales.csv`: tabla denormalizada para Power BI.
- `exports/kpi_summary.csv`: resumen ejecutivo.
- `exports/monthly_sales.csv`: serie historica agregada.
- `exports/sales_forecast.csv`: forecast para los proximos 90 dias.
- `models/sales_forecast_model.joblib`: modelo entrenado.

## Resultado del pipeline

Tras ejecutar el pipeline actual se generan:

- 10,205 pedidos sinteticos.
- 46,155 unidades vendidas.
- 207.8M de revenue acumulado.
- 87.6M de profit acumulado.
- 90 dias de forecast exportados para visualizacion.

## Uso en Power BI

Importa estos CSV desde la carpeta `exports/`:

- `dashboard_sales.csv`
- `kpi_summary.csv`
- `monthly_sales.csv`
- `sales_forecast.csv`

Visuales sugeridos:

- KPI cards para revenue, profit, units y average order value.
- Line chart para revenue mensual.
- Clustered bar chart por region y categoria.
- Map por region.
- Forecast chart comparando historico y prediccion.

## Entidades del modelo

- `dim_date`
- `dim_region`
- `dim_channel`
- `dim_product`
- `fact_sales`

## Consultas SQL

El esquema y las vistas analiticas estan en:

- `sql/schema.sql`
- `sql/analytics_views.sql`

## Nota

Los datos son sinteticos, pero la estructura esta pensada para parecerse a un flujo real de analitica comercial conectado a un warehouse.
