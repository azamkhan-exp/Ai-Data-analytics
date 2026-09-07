import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, Tuple, List

def clean_dataset(
    df: pd.DataFrame,
    drop_duplicates: bool = True,
    fill_missing_numerical: str = "none",  # "none", "mean", "median", "zero"
    fill_missing_categorical: str = "none", # "none", "mode", "unknown"
    drop_na_rows: bool = False,
    drop_high_missing_cols_threshold: Optional[float] = None
) -> Tuple[pd.DataFrame, List[str]]:
    """
    Applies data cleaning operations to a dataframe and logs modifications.
    """
    cleaned = df.copy()
    changes_log = []

    # 1. Strip whitespace from string columns
    for col in cleaned.select_dtypes(include=['object']).columns:
        cleaned[col] = cleaned[col].astype(str).str.strip()

    # 2. Drop duplicates
    if drop_duplicates:
        initial_rows = len(cleaned)
        cleaned = cleaned.drop_duplicates()
        dropped = initial_rows - len(cleaned)
        if dropped > 0:
            changes_log.append(f"Removed {dropped:,} duplicate rows.")

    # 3. Drop columns with missing values above threshold
    if drop_high_missing_cols_threshold is not None:
        initial_cols = cleaned.shape[1]
        missing_pcts = cleaned.isna().mean()
        cols_to_drop = missing_pcts[missing_pcts > drop_high_missing_cols_threshold].index.tolist()
        if cols_to_drop:
            cleaned = cleaned.drop(columns=cols_to_drop)
            changes_log.append(f"Dropped {len(cols_to_drop)} columns exceeding {drop_high_missing_cols_threshold*100}% missing values: {', '.join(cols_to_drop)}")

    # 4. Drop NA rows if requested
    if drop_na_rows:
        initial_rows = len(cleaned)
        cleaned = cleaned.dropna()
        dropped = initial_rows - len(cleaned)
        if dropped > 0:
            changes_log.append(f"Dropped {dropped:,} rows containing missing values.")

    # 5. Fill missing numerical values
    if fill_missing_numerical != "none":
        num_cols = cleaned.select_dtypes(include=[np.number]).columns
        for col in num_cols:
            na_count = cleaned[col].isna().sum()
            if na_count > 0:
                if fill_missing_numerical == "mean":
                    val = cleaned[col].mean()
                    cleaned[col] = cleaned[col].fillna(val)
                    changes_log.append(f"Imputed {na_count} missing values in '{col}' with mean ({val:.2f}).")
                elif fill_missing_numerical == "median":
                    val = cleaned[col].median()
                    cleaned[col] = cleaned[col].fillna(val)
                    changes_log.append(f"Imputed {na_count} missing values in '{col}' with median ({val:.2f}).")
                elif fill_missing_numerical == "zero":
                    cleaned[col] = cleaned[col].fillna(0)
                    changes_log.append(f"Imputed {na_count} missing values in '{col}' with 0.")

    # 6. Fill missing categorical values
    if fill_missing_categorical != "none":
        cat_cols = cleaned.select_dtypes(include=['object', 'category']).columns
        for col in cat_cols:
            na_count = cleaned[col].isna().sum()
            if na_count > 0:
                if fill_missing_categorical == "mode":
                    mode_val = cleaned[col].mode()
                    val = mode_val.iloc[0] if not mode_val.empty else "Unknown"
                    cleaned[col] = cleaned[col].fillna(val)
                    changes_log.append(f"Imputed {na_count} missing values in '{col}' with mode ('{val}').")
                elif fill_missing_categorical == "unknown":
                    cleaned[col] = cleaned[col].fillna("Unknown")
                    changes_log.append(f"Imputed {na_count} missing values in '{col}' with 'Unknown'.")

    return cleaned, changes_log
