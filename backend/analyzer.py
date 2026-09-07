import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional

def detect_column_types(df: pd.DataFrame) -> Dict[str, str]:
    """
    Detects business data types for each column:
    'numerical', 'categorical', 'datetime', 'boolean', 'text'
    """
    col_types = {}
    for col in df.columns:
        series = df[col]
        # Check boolean
        if pd.api.types.is_bool_dtype(series) or set(series.dropna().unique()).issubset({True, False, 0, 1}) and len(series.dropna().unique()) <= 2 and series.dtype == 'bool':
            col_types[col] = 'boolean'
            continue
        
        # Check datetime
        if pd.api.types.is_datetime64_any_dtype(series):
            col_types[col] = 'datetime'
            continue
        
        # Try datetime conversion if string or object
        if pd.api.types.is_string_dtype(series) or series.dtype in ['object', 'str', 'string']:
            sample = series.dropna().head(50)
            if not sample.empty:
                try:
                    converted = pd.to_datetime(sample, errors='coerce', format='mixed')
                    if converted.notna().mean() > 0.8 and not all(str(x).isdigit() and len(str(x)) < 4 for x in sample):
                        col_types[col] = 'datetime'
                        continue
                except Exception:
                    pass

        # Check numerical
        if pd.api.types.is_numeric_dtype(series):
            # If numeric but very few unique values and integers, could be categorical, but we treat as numerical if >= 10 unique or float
            unique_cnt = series.nunique()
            if unique_cnt <= 5 and series.dtype in ['int64', 'int32'] and not col.lower().endswith(('id', 'code', 'zip')):
                col_types[col] = 'categorical'
            else:
                col_types[col] = 'numerical'
            continue

        # Check categorical vs free text
        unique_cnt = series.nunique()
        total_non_null = series.count()
        if total_non_null > 0 and (unique_cnt / total_non_null < 0.5 or unique_cnt <= 50):
            col_types[col] = 'categorical'
        else:
            col_types[col] = 'text'

    return col_types


def analyze_dataset(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Performs comprehensive automated analysis of the dataset.
    """
    total_rows, total_cols = df.shape
    duplicate_rows = int(df.duplicated().sum())
    total_cells = total_rows * total_cols if total_rows * total_cols > 0 else 1
    total_missing_cells = int(df.isna().sum().sum())
    overall_missing_pct = round((total_missing_cells / total_cells) * 100, 2)
    memory_bytes = int(df.memory_usage(deep=True).sum())
    memory_str = f"{memory_bytes / 1024:.1f} KB" if memory_bytes < 1024 * 1024 else f"{memory_bytes / (1024 * 1024):.2f} MB"

    col_types = detect_column_types(df)

    numerical_cols = [col for col, t in col_types.items() if t == 'numerical']
    categorical_cols = [col for col, t in col_types.items() if t in ['categorical', 'text']]
    datetime_cols = [col for col, t in col_types.items() if t == 'datetime']
    boolean_cols = [col for col, t in col_types.items() if t == 'boolean']

    # Column details table
    column_details = []
    for col in df.columns:
        series = df[col]
        missing_count = int(series.isna().sum())
        missing_pct = round((missing_count / total_rows * 100), 2) if total_rows > 0 else 0
        unique_count = int(series.nunique())
        raw_dtype = str(series.dtype)
        inferred_type = col_types[col]

        column_details.append({
            "name": col,
            "inferred_type": inferred_type,
            "raw_dtype": raw_dtype,
            "missing_count": missing_count,
            "missing_percentage": missing_pct,
            "unique_count": unique_count
        })

    # Numerical statistics
    numerical_stats = []
    for col in numerical_cols:
        series = pd.to_numeric(df[col], errors='coerce').dropna()
        if series.empty:
            continue
        
        q1 = float(series.quantile(0.25))
        q3 = float(series.quantile(0.75))
        iqr = q3 - q1
        outliers_count = int(((series < (q1 - 1.5 * iqr)) | (series > (q3 + 1.5 * iqr))).sum())
        skewness = float(series.skew()) if len(series) > 2 else 0.0

        numerical_stats.append({
            "column": col,
            "count": int(series.count()),
            "mean": round(float(series.mean()), 3),
            "median": round(float(series.median()), 3),
            "min": round(float(series.min()), 3),
            "max": round(float(series.max()), 3),
            "std": round(float(series.std()), 3) if len(series) > 1 else 0.0,
            "q25": round(q1, 3),
            "q75": round(q3, 3),
            "iqr": round(iqr, 3),
            "skewness": round(skewness, 3),
            "outliers_count": outliers_count,
            "missing_count": int(df[col].isna().sum()),
            "missing_percentage": round((df[col].isna().sum() / total_rows * 100), 2) if total_rows > 0 else 0
        })

    # Categorical statistics
    categorical_stats = []
    for col in categorical_cols:
        series = df[col].dropna().astype(str)
        if series.empty:
            continue
        
        val_counts = series.value_counts()
        top_val = str(val_counts.index[0]) if not val_counts.empty else "N/A"
        top_freq = int(val_counts.iloc[0]) if not val_counts.empty else 0
        top_pct = round((top_freq / len(series) * 100), 2) if len(series) > 0 else 0

        # top 5 breakdown
        top_breakdown = [
            {"value": str(k), "count": int(v), "percentage": round(v / len(series) * 100, 1)}
            for k, v in val_counts.head(5).items()
        ]

        categorical_stats.append({
            "column": col,
            "count": int(series.count()),
            "unique_count": int(series.nunique()),
            "top_value": top_val,
            "top_frequency": top_freq,
            "top_percentage": top_pct,
            "top_breakdown": top_breakdown,
            "missing_count": int(df[col].isna().sum()),
            "missing_percentage": round((df[col].isna().sum() / total_rows * 100), 2) if total_rows > 0 else 0
        })

    # Correlation Matrix for numerical columns
    corr_matrix = {}
    strong_correlations = []
    if len(numerical_cols) >= 2:
        num_df = df[numerical_cols].apply(pd.to_numeric, errors='coerce')
        corr = num_df.corr().round(3)
        corr_matrix = {
            "columns": numerical_cols,
            "values": corr.fillna(0).values.tolist()
        }
        # Find strongest correlations (excluding diagonal)
        for i in range(len(numerical_cols)):
            for j in range(i + 1, len(numerical_cols)):
                col1, col2 = numerical_cols[i], numerical_cols[j]
                val = corr.iloc[i, j]
                if pd.notna(val) and abs(val) >= 0.4:
                    strong_correlations.append({
                        "col1": col1,
                        "col2": col2,
                        "correlation": float(val),
                        "relationship": "Strong Positive" if val >= 0.7 else ("Moderate Positive" if val >= 0.4 else ("Strong Negative" if val <= -0.7 else "Moderate Negative"))
                    })
        strong_correlations.sort(key=lambda x: abs(x["correlation"]), reverse=True)

    # 20 rows preview safely formatted
    preview_df = df.head(20).copy()
    # Convert datetimes and NaNs to serializable
    preview_records = []
    for _, row in preview_df.iterrows():
        rec = {}
        for col in df.columns:
            val = row[col]
            if pd.isna(val):
                rec[col] = None
            elif isinstance(val, (pd.Timestamp, np.datetime64)):
                rec[col] = str(val)
            elif isinstance(val, (np.integer, np.int64, np.int32)):
                rec[col] = int(val)
            elif isinstance(val, (np.floating, np.float64, np.float32)):
                rec[col] = round(float(val), 4)
            else:
                rec[col] = str(val)
        preview_records.append(rec)

    return {
        "summary": {
            "total_rows": total_rows,
            "total_columns": total_cols,
            "duplicate_rows": duplicate_rows,
            "overall_missing_cells": total_missing_cells,
            "overall_missing_percentage": overall_missing_pct,
            "memory_usage": memory_str,
            "numerical_columns_count": len(numerical_cols),
            "categorical_columns_count": len(categorical_cols),
            "datetime_columns_count": len(datetime_cols),
            "boolean_columns_count": len(boolean_cols),
        },
        "column_types": col_types,
        "column_details": column_details,
        "preview_rows": preview_records,
        "numerical_stats": numerical_stats,
        "categorical_stats": categorical_stats,
        "correlation_matrix": corr_matrix,
        "strong_correlations": strong_correlations,
        "numerical_columns": numerical_cols,
        "categorical_columns": categorical_cols,
        "datetime_columns": datetime_cols
    }
