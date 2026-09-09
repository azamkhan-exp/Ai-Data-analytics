import pandas as pd
import numpy as np
from typing import Dict, List, Any

def detect_column_types(df: pd.DataFrame) -> Dict[str, str]:
    """
    Identifies column types: 'numerical', 'categorical', 'datetime', 'boolean', 'text'.
    """
    col_types = {}
    for col in df.columns:
        series = df[col]
        non_null = series.dropna()

        if non_null.empty:
            col_types[col] = 'text'
            continue

        # 1. Check boolean
        if pd.api.types.is_bool_dtype(series):
            col_types[col] = 'boolean'
            continue
        unique_vals = set(str(v).strip().lower() for v in non_null.head(100))
        if unique_vals.issubset({'true', 'false', 'yes', 'no', '0', '1', 't', 'f'}) and len(unique_vals) <= 2:
            col_types[col] = 'boolean'
            continue

        # 2. Check datetime
        if pd.api.types.is_datetime64_any_dtype(series):
            col_types[col] = 'datetime'
            continue

        if pd.api.types.is_string_dtype(series) or series.dtype in ['object', 'str', 'string']:
            sample = non_null.head(50)
            if not sample.empty:
                try:
                    converted = pd.to_datetime(sample, errors='coerce', format='mixed')
                    if converted.notna().mean() >= 0.8 and not all(str(x).isdigit() and len(str(x)) < 4 for x in sample):
                        col_types[col] = 'datetime'
                        continue
                except Exception:
                    pass

        # 3. Check numerical
        if pd.api.types.is_numeric_dtype(series):
            unique_cnt = non_null.nunique()
            col_lower = str(col).lower()
            if unique_cnt <= 5 and not any(k in col_lower for k in ['rate', 'score', 'discount', 'percent', 'margin']):
                col_types[col] = 'categorical'
            else:
                col_types[col] = 'numerical'
            continue

        # 4. Check categorical vs free-form text
        unique_cnt = non_null.nunique()
        total_cnt = len(non_null)
        ratio = unique_cnt / (total_cnt or 1)
        if ratio < 0.5 or unique_cnt <= 50:
            col_types[col] = 'categorical'
        else:
            col_types[col] = 'text'

    return col_types

def detect_column_roles(df: pd.DataFrame, col_types: Dict[str, str]) -> Dict[str, str]:
    """
    Infers business roles for columns based on nomenclature and distributions.
    """
    roles = {}
    total_rows = len(df) or 1

    for col in df.columns:
        col_lower = str(col).lower().strip()
        t = col_types.get(col, 'text')
        non_null = df[col].dropna()
        unique_cnt = non_null.nunique()

        if col_lower.endswith(('id', '_id', 'code', 'key', 'number')) or (unique_cnt == total_rows and t != 'numerical'):
            roles[col] = 'Identifier'
        elif any(k in col_lower for k in ['churn', 'target', 'label', 'status', 'outcome', 'is_fraud', 'converted', 'approved']):
            roles[col] = 'Target / Label'
        elif any(k in col_lower for k in ['price', 'revenue', 'sales', 'cost', 'charge', 'profit', 'fee', 'amount', 'salary', 'income', 'budget', 'spend']):
            roles[col] = 'Monetary Metric'
        elif any(k in col_lower for k in ['rate', 'pct', 'percent', 'discount', 'ratio', 'margin']):
            roles[col] = 'Percentage / Rate'
        elif t == 'datetime':
            roles[col] = 'Temporal Dimension'
        elif t == 'numerical':
            roles[col] = 'Continuous Measure'
        else:
            roles[col] = 'Categorical Dimension'

    return roles

def profile_dataset(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Profiles the structural hygiene, column details, and preview rows of a DataFrame.
    """
    total_rows, total_cols = df.shape
    duplicate_rows = int(df.duplicated().sum())
    total_cells = total_rows * total_cols if total_rows * total_cols > 0 else 1
    total_missing_cells = int(df.isna().sum().sum())
    overall_missing_pct = round((total_missing_cells / total_cells) * 100, 2)
    memory_bytes = int(df.memory_usage(deep=True).sum())
    memory_str = f"{memory_bytes / 1024:.1f} KB" if memory_bytes < 1024 * 1024 else f"{memory_bytes / (1024 * 1024):.2f} MB"

    col_types = detect_column_types(df)
    col_roles = detect_column_roles(df, col_types)

    numerical_cols = [c for c, t in col_types.items() if t == 'numerical']
    categorical_cols = [c for c, t in col_types.items() if t in ['categorical', 'text']]
    datetime_cols = [c for c, t in col_types.items() if t == 'datetime']
    boolean_cols = [c for c, t in col_types.items() if t == 'boolean']

    column_details = []
    for col in df.columns:
        series = df[col]
        non_null = series.dropna()
        missing_count = int(series.isna().sum())
        missing_pct = round((missing_count / (total_rows or 1)) * 100, 2)
        unique_count = int(series.nunique())
        raw_dtype = str(series.dtype)
        examples = [str(x) for x in non_null.head(3).tolist()]

        column_details.append({
            "name": col,
            "inferred_type": col_types[col],
            "detected_role": col_roles[col],
            "raw_dtype": raw_dtype,
            "missing_count": missing_count,
            "missing_percentage": missing_pct,
            "unique_count": unique_count,
            "examples": examples
        })

    # Safe serializable preview rows (first 20)
    preview_df = df.head(20).copy()
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
        "column_roles": col_roles,
        "column_details": column_details,
        "preview_rows": preview_records,
        "numerical_columns": numerical_cols,
        "categorical_columns": categorical_cols,
        "datetime_columns": datetime_cols,
        "boolean_columns": boolean_cols
    }
