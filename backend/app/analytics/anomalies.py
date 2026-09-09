import pandas as pd
import numpy as np
from typing import Dict, List, Any

def detect_anomalies(df: pd.DataFrame, numerical_cols: List[str]) -> Dict[str, Any]:
    """
    Dual-method statistical outlier detection (IQR + Z-Score) supplemented by
    scikit-learn IsolationForest when multidimensional feature space permits.
    """
    total_rows = len(df)
    if total_rows == 0 or not numerical_cols:
        return {
            "total_anomalies": 0,
            "affected_columns": [],
            "affected_rows_count": 0,
            "anomaly_percentage": 0.0,
            "ml_anomalies_detected": 0
        }

    affected_columns = []
    anomalous_row_indices = set()
    total_anomalies_count = 0

    # 1. Feature-by-feature univariate diagnostics
    for col in numerical_cols:
        series = pd.to_numeric(df[col], errors='coerce').dropna()
        if len(series) < 5:
            continue

        q1 = float(series.quantile(0.25))
        q3 = float(series.quantile(0.75))
        iqr = q3 - q1

        # Tukey 1.5x IQR boundaries
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        iqr_mask = (series < lower_bound) | (series > upper_bound)
        iqr_outliers = series[iqr_mask]
        iqr_count = len(iqr_outliers)

        # Z-Score boundaries (|z| > 3.0)
        mean_val = float(series.mean())
        std_val = float(series.std(ddof=1)) if len(series) > 1 else 0.0

        if std_val > 0:
            z_mask = np.abs((series - mean_val) / std_val) > 3.0
            z_count = int(z_mask.sum())
        else:
            z_count = 0

        # Mark affected rows
        for idx in series[iqr_mask].index:
            anomalous_row_indices.add(idx)

        if iqr_count > 0 or z_count > 0:
            total_anomalies_count += iqr_count
            affected_columns.append({
                "column": col,
                "iqr_count": iqr_count,
                "zscore_count": z_count,
                "lower_bound": round(lower_bound, 2),
                "upper_bound": round(upper_bound, 2),
                "max_value": round(float(series.max()), 2),
                "min_value": round(float(series.min()), 2),
                "explanation": f"{iqr_count} record(s) diverge beyond the 1.5× IQR threshold [{lower_bound:.2f}, {upper_bound:.2f}]; {z_count} diverge beyond 3 standard deviations."
            })

    # 2. Advanced Multi-dimensional Anomaly Detection via scikit-learn IsolationForest
    ml_outliers_count = 0
    if len(numerical_cols) >= 2 and total_rows >= 15:
        try:
            from sklearn.ensemble import IsolationForest
            clean_num_df = df[numerical_cols].apply(pd.to_numeric, errors='coerce').fillna(0)
            iso = IsolationForest(contamination=0.05, random_state=42, n_estimators=50)
            preds = iso.fit_predict(clean_num_df)
            ml_outliers_count = int((preds == -1).sum())
        except Exception:
            ml_outliers_count = 0

    affected_rows_count = len(anomalous_row_indices)
    anomaly_pct = round((affected_rows_count / (total_rows or 1)) * 100, 1)

    return {
        "total_anomalies": total_anomalies_count,
        "affected_columns": affected_columns,
        "affected_rows_count": affected_rows_count,
        "anomaly_percentage": anomaly_pct,
        "ml_anomalies_detected": ml_outliers_count
    }
