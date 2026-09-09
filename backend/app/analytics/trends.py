import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional

def analyze_temporal_trends(df: pd.DataFrame, datetime_cols: List[str], numerical_cols: List[str]) -> Optional[Dict[str, Any]]:
    """
    Evaluates chronological trends, periodicity, momentum, and peak/drop patterns.
    """
    if not datetime_cols or not numerical_cols:
        return None

    date_col = datetime_cols[0]
    metric_col = numerical_cols[0]

    temp = df.copy()
    temp[date_col] = pd.to_datetime(temp[date_col], errors='coerce')
    temp[metric_col] = pd.to_numeric(temp[metric_col], errors='coerce')
    temp = temp.dropna(subset=[date_col, metric_col]).sort_values(by=date_col)

    if len(temp) < 6:
        return None

    # Determine optimal aggregation cadence based on span
    min_date = temp[date_col].min()
    max_date = temp[date_col].max()
    day_span = (max_date - min_date).days

    if day_span > 730:
        cadence = 'YE'
        cadence_label = 'Yearly'
    elif day_span > 90:
        cadence = 'ME'
        cadence_label = 'Monthly'
    elif day_span > 21:
        cadence = 'W'
        cadence_label = 'Weekly'
    else:
        cadence = 'D'
        cadence_label = 'Daily'

    # Compute period aggregations
    try:
        grouped = temp.set_index(date_col).resample(cadence)[metric_col].sum().reset_index()
    except Exception:
        grouped = temp.groupby(temp[date_col].dt.to_period('M'))[metric_col].sum().reset_index()
        grouped[date_col] = grouped[date_col].dt.to_timestamp()

    grouped = grouped.dropna()
    if len(grouped) < 2:
        return None

    # Calculate overall early vs late period momentum
    n_sample = max(2, int(len(temp) * 0.25))
    early_mean = float(temp.head(n_sample)[metric_col].mean())
    late_mean = float(temp.tail(n_sample)[metric_col].mean())

    pct_change = round(((late_mean - early_mean) / abs(early_mean)) * 100, 1) if early_mean != 0 else 0.0
    direction = "increasing" if pct_change > 0 else ("decreasing" if pct_change < 0 else "stable")

    # Peak and trough detection
    peak_row = grouped.loc[grouped[metric_col].idxmax()]
    drop_row = grouped.loc[grouped[metric_col].idxmin()]

    return {
        "date_column": date_col,
        "metric_column": metric_col,
        "cadence": cadence_label,
        "first_date": str(min_date.date()),
        "last_date": str(max_date.date()),
        "total_days_span": day_span,
        "early_average": round(early_mean, 2),
        "late_average": round(late_mean, 2),
        "percentage_change": pct_change,
        "direction": direction,
        "peak_period": str(peak_row[date_col].date() if hasattr(peak_row[date_col], 'date') else peak_row[date_col]),
        "peak_value": round(float(peak_row[metric_col]), 2),
        "trough_period": str(drop_row[date_col].date() if hasattr(drop_row[date_col], 'date') else drop_row[date_col]),
        "trough_value": round(float(drop_row[metric_col]), 2)
    }
