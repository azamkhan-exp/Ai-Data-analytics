import pandas as pd
import numpy as np
from typing import Tuple, List, Dict, Optional

def clean_dataset(
    df: pd.DataFrame,
    drop_duplicates: bool = True,
    fill_missing_numerical: str = "none",   # none, mean, median, zero
    fill_missing_categorical: str = "none", # none, mode, unknown
    drop_na_rows: bool = False,
    drop_high_missing_cols_threshold: Optional[float] = None,
    drop_columns: Optional[List[str]] = None,
    rename_columns: Optional[Dict[str, str]] = None,
    trim_strings: bool = True
) -> Tuple[pd.DataFrame, List[str]]:
    """
    Non-destructively cleans a pandas DataFrame and returns a comprehensive changelog.
    """
    cleaned = df.copy()
    changes_log = []

    # 1. Rename columns if requested
    if rename_columns:
        valid_renames = {k: v.strip() for k, v in rename_columns.items() if k in cleaned.columns and v and v.strip()}
        if valid_renames:
            cleaned = cleaned.rename(columns=valid_renames)
            changes_log.append(f"Renamed column(s): {', '.join(f'{k} -> {v}' for k, v in valid_renames.items())}.")

    # 2. Drop specific columns if requested
    if drop_columns:
        valid_drops = [c for c in drop_columns if c in cleaned.columns]
        if valid_drops:
            cleaned = cleaned.drop(columns=valid_drops)
            changes_log.append(f"Dropped column(s): {', '.join(valid_drops)}.")

    # 3. Trim leading/trailing whitespace from string columns
    if trim_strings:
        str_cols = cleaned.select_dtypes(include=['object', 'string']).columns
        trimmed_count = 0
        for col in str_cols:
            orig = cleaned[col].astype(str)
            trimmed = orig.str.strip()
            diff_mask = orig != trimmed
            if diff_mask.any():
                cleaned[col] = trimmed
                trimmed_count += int(diff_mask.sum())
        if trimmed_count > 0:
            changes_log.append(f"Trimmed whitespace from {trimmed_count:,} text cells.")

    # 4. Remove exact duplicate rows
    if drop_duplicates:
        initial_len = len(cleaned)
        cleaned = cleaned.drop_duplicates()
        dropped_dups = initial_len - len(cleaned)
        if dropped_dups > 0:
            changes_log.append(f"Removed {dropped_dups:,} duplicate row(s).")

    # 5. Drop columns exceeding missing threshold (e.g. > 0.5 for 50%)
    if drop_high_missing_cols_threshold is not None and drop_high_missing_cols_threshold > 0:
        missing_ratios = cleaned.isna().mean()
        high_missing_cols = missing_ratios[missing_ratios > drop_high_missing_cols_threshold].index.tolist()
        if high_missing_cols:
            cleaned = cleaned.drop(columns=high_missing_cols)
            pct_label = int(drop_high_missing_cols_threshold * 100)
            changes_log.append(f"Dropped {len(high_missing_cols)} column(s) exceeding {pct_label}% missingness: {', '.join(high_missing_cols)}.")

    # 6. Drop rows with any missing values if strict mode
    if drop_na_rows:
        initial_len = len(cleaned)
        cleaned = cleaned.dropna()
        dropped_rows = initial_len - len(cleaned)
        if dropped_rows > 0:
            changes_log.append(f"Dropped {dropped_rows:,} incomplete row(s).")

    # 7. Impute missing numerical values
    if fill_missing_numerical != "none":
        num_cols = cleaned.select_dtypes(include=[np.number]).columns
        for col in num_cols:
            missing_count = int(cleaned[col].isna().sum())
            if missing_count > 0:
                if fill_missing_numerical == "mean":
                    val = float(cleaned[col].mean())
                    cleaned[col] = cleaned[col].fillna(val)
                    changes_log.append(f"Imputed {missing_count:,} missing values in '{col}' with mean ({val:.2f}).")
                elif fill_missing_numerical == "median":
                    val = float(cleaned[col].median())
                    cleaned[col] = cleaned[col].fillna(val)
                    changes_log.append(f"Imputed {missing_count:,} missing values in '{col}' with median ({val:.2f}).")
                elif fill_missing_numerical == "zero":
                    cleaned[col] = cleaned[col].fillna(0.0)
                    changes_log.append(f"Imputed {missing_count:,} missing values in '{col}' with 0.")

    # 8. Impute missing categorical values
    if fill_missing_categorical != "none":
        cat_cols = cleaned.select_dtypes(include=['object', 'category', 'string']).columns
        for col in cat_cols:
            missing_count = int(cleaned[col].isna().sum())
            if missing_count > 0:
                if fill_missing_categorical == "mode":
                    mode_series = cleaned[col].mode()
                    val = str(mode_series.iloc[0]) if not mode_series.empty else "Unknown"
                    cleaned[col] = cleaned[col].fillna(val)
                    changes_log.append(f"Imputed {missing_count:,} missing values in '{col}' with mode ('{val}').")
                elif fill_missing_categorical == "unknown":
                    cleaned[col] = cleaned[col].fillna("Unknown")
                    changes_log.append(f"Imputed {missing_count:,} missing values in '{col}' with 'Unknown'.")

    return cleaned, changes_log
