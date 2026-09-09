import pandas as pd
import numpy as np
from typing import Dict, List, Any
from scipy import stats

def compute_numerical_statistics(df: pd.DataFrame, numerical_cols: List[str]) -> List[Dict[str, Any]]:
    """
    Computes rigorous descriptive moments (Mean, Median, Mode, Variance, Std,
    Range, Quartiles, IQR, Skewness, Kurtosis) using Pandas, NumPy, and SciPy.
    """
    results = []
    total_rows = len(df)

    for col in numerical_cols:
        series = pd.to_numeric(df[col], errors='coerce').dropna()
        if series.empty:
            continue

        count = int(series.count())
        mean_val = float(series.mean())
        median_val = float(series.median())

        # Mode via SciPy / Pandas
        mode_series = series.mode()
        mode_val = float(mode_series.iloc[0]) if not mode_series.empty else median_val

        min_val = float(series.min())
        max_val = float(series.max())
        range_val = max_val - min_val

        variance_val = float(series.var(ddof=1)) if count > 1 else 0.0
        std_val = float(series.std(ddof=1)) if count > 1 else 0.0

        q1 = float(series.quantile(0.25))
        q3 = float(series.quantile(0.75))
        iqr = q3 - q1

        # Skewness & Kurtosis via SciPy
        skew_val = float(stats.skew(series, bias=False)) if count > 2 else 0.0
        kurt_val = float(stats.kurtosis(series, bias=False)) if count > 3 else 0.0

        # Outlier counts (Tukey 1.5x IQR)
        lower_iqr_bound = q1 - 1.5 * iqr
        upper_iqr_bound = q3 + 1.5 * iqr
        outliers_iqr = int(((series < lower_iqr_bound) | (series > upper_iqr_bound)).sum())

        # Z-Score outliers (|z| > 3.0)
        if std_val > 0:
            z_scores = np.abs((series - mean_val) / std_val)
            outliers_zscore = int((z_scores > 3.0).sum())
        else:
            outliers_zscore = 0

        missing_count = int(df[col].isna().sum())
        missing_pct = round((missing_count / (total_rows or 1)) * 100, 2)

        results.append({
            "column": col,
            "count": count,
            "sum": round(float(series.sum()), 2),
            "mean": round(mean_val, 3),
            "median": round(median_val, 3),
            "mode": round(mode_val, 3),
            "min": round(min_val, 3),
            "max": round(max_val, 3),
            "range": round(range_val, 3),
            "std": round(std_val, 3),
            "variance": round(variance_val, 3),
            "q25": round(q1, 3),
            "q75": round(q3, 3),
            "iqr": round(iqr, 3),
            "skewness": round(skew_val, 3),
            "kurtosis": round(kurt_val, 3),
            "outliers_count": outliers_iqr,
            "zscore_outliers_count": outliers_zscore,
            "missing_count": missing_count,
            "missing_percentage": missing_pct
        })

    return results

def compute_categorical_statistics(df: pd.DataFrame, categorical_cols: List[str]) -> List[Dict[str, Any]]:
    """
    Computes frequency distributions, modal dominance, and cardinality for categorical features.
    """
    results = []
    total_rows = len(df)

    for col in categorical_cols:
        series = df[col].dropna().astype(str)
        if series.empty:
            continue

        val_counts = series.value_counts()
        top_val = str(val_counts.index[0]) if not val_counts.empty else "N/A"
        top_freq = int(val_counts.iloc[0]) if not val_counts.empty else 0
        top_pct = round((top_freq / len(series) * 100), 2) if len(series) > 0 else 0

        top_breakdown = [
            {
                "value": str(k),
                "count": int(v),
                "percentage": round(v / len(series) * 100, 1)
            }
            for k, v in val_counts.head(5).items()
        ]

        missing_count = int(df[col].isna().sum())
        missing_pct = round((missing_count / (total_rows or 1)) * 100, 2)

        results.append({
            "column": col,
            "count": int(series.count()),
            "unique_count": int(series.nunique()),
            "top_value": top_val,
            "top_frequency": top_freq,
            "top_percentage": top_pct,
            "top_breakdown": top_breakdown,
            "missing_count": missing_count,
            "missing_percentage": missing_pct
        })

    return results
