from __future__ import annotations

from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


ROOT = Path(__file__).resolve().parents[1]
EXPORT_DIR = ROOT / "exports"
MODEL_DIR = ROOT / "models"


def build_feature_frame(monthly_sales: pd.DataFrame) -> pd.DataFrame:
    df = monthly_sales.copy()
    df["month_start"] = pd.to_datetime(df["month_start"])
    df["month_number"] = df["month_start"].dt.month
    df["quarter"] = df["month_start"].dt.quarter
    df["year"] = df["month_start"].dt.year
    df["time_index"] = np.arange(len(df))
    df["lag_1"] = df["revenue"].shift(1)
    df["lag_2"] = df["revenue"].shift(2)
    df["lag_3"] = df["revenue"].shift(3)
    df["rolling_mean_3"] = df["revenue"].shift(1).rolling(3).mean()
    df["rolling_std_3"] = df["revenue"].shift(1).rolling(3).std()
    return df


def train_model(feature_frame: pd.DataFrame) -> Pipeline:
    train_df = feature_frame.dropna().copy()
    feature_columns = ["month_number", "quarter", "year", "time_index", "lag_1", "lag_2", "lag_3", "rolling_mean_3", "rolling_std_3"]
    categorical_columns = ["quarter"]

    preprocessing = ColumnTransformer(
        transformers=[
            (
                "num",
                Pipeline(steps=[("imputer", SimpleImputer(strategy="median"))]),
                [column for column in feature_columns if column not in categorical_columns],
            ),
            (
                "cat",
                Pipeline(
                    steps=[
                        ("imputer", SimpleImputer(strategy="most_frequent")),
                        ("encoder", OneHotEncoder(handle_unknown="ignore")),
                    ]
                ),
                categorical_columns,
            ),
        ]
    )

    model = Pipeline(
        steps=[
            ("preprocess", preprocessing),
            ("regressor", RandomForestRegressor(n_estimators=400, random_state=42, max_depth=8)),
        ]
    )
    model.fit(train_df[feature_columns], train_df["revenue"])
    return model


def recursive_forecast(feature_frame: pd.DataFrame, model: Pipeline, horizon: int = 3) -> pd.DataFrame:
    history = feature_frame.copy().reset_index(drop=True)
    forecasts: list[dict[str, object]] = []

    for _ in range(horizon):
        next_month = history["month_start"].max() + pd.offsets.MonthBegin(1)
        revenue_series = history["revenue"].tolist()
        lag_1 = revenue_series[-1]
        lag_2 = revenue_series[-2]
        lag_3 = revenue_series[-3]
        rolling_window = revenue_series[-3:]
        row = pd.DataFrame(
            [
                {
                    "month_start": next_month,
                    "month_number": next_month.month,
                    "quarter": next_month.quarter,
                    "year": next_month.year,
                    "time_index": len(history),
                    "lag_1": lag_1,
                    "lag_2": lag_2,
                    "lag_3": lag_3,
                    "rolling_mean_3": float(np.mean(rolling_window)),
                    "rolling_std_3": float(np.std(rolling_window)),
                }
            ]
        )
        prediction = float(model.predict(row.drop(columns=["month_start"]))[0])
        row["revenue"] = round(prediction, 2)
        history = pd.concat([history, row], ignore_index=True, sort=False)
        forecasts.append({"month_start": next_month.date().isoformat(), "forecast_revenue": round(prediction, 2)})

    return pd.DataFrame(forecasts)


def expand_to_daily(forecast_monthly: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for _, row in forecast_monthly.iterrows():
        month_start = pd.to_datetime(row["month_start"])
        next_month = month_start + pd.offsets.MonthBegin(1)
        month_days = pd.date_range(month_start, next_month - pd.Timedelta(days=1), freq="D")
        daily_revenue = row["forecast_revenue"] / len(month_days)
        for current_day in month_days:
            rows.append(
                {
                    "forecast_date": current_day.date().isoformat(),
                    "forecast_revenue": round(daily_revenue, 2),
                    "forecast_month": month_start.strftime("%Y-%m-01"),
                }
            )
    return pd.DataFrame(rows).head(90)


def main() -> None:
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    monthly_sales = pd.read_csv(EXPORT_DIR / "monthly_sales.csv")
    feature_frame = build_feature_frame(monthly_sales)
    model = train_model(feature_frame)
    forecast_monthly = recursive_forecast(feature_frame, model, horizon=3)
    forecast_daily = expand_to_daily(forecast_monthly)

    joblib.dump(model, MODEL_DIR / "sales_forecast_model.joblib")
    forecast_daily.to_csv(EXPORT_DIR / "sales_forecast.csv", index=False)


if __name__ == "__main__":
    main()
