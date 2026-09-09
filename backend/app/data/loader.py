import io
import os
import pandas as pd
from typing import Tuple
from fastapi import HTTPException

COMMON_ENCODINGS = ['utf-8', 'utf-8-sig', 'latin1', 'cp1252', 'iso-8859-1']

def normalize_dataframe_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Cleans column headers: strips whitespace and renames empty/unnamed columns."""
    cleaned_cols = []
    for idx, c in enumerate(df.columns):
        c_str = str(c).strip()
        if not c_str or c_str.lower().startswith('unnamed:'):
            c_str = f"column_{idx + 1}"
        cleaned_cols.append(c_str)
    df.columns = cleaned_cols
    return df

def load_dataframe_from_bytes(content: bytes, ext: str) -> pd.DataFrame:
    """Loads a DataFrame from raw byte stream with automatic encoding detection."""
    if ext == 'csv':
        df = None
        last_err = None
        for enc in COMMON_ENCODINGS:
            try:
                df = pd.read_csv(io.BytesIO(content), encoding=enc)
                break
            except (UnicodeDecodeError, pd.errors.ParserError) as e:
                last_err = e
                continue

        if df is None:
            raise HTTPException(
                status_code=400,
                detail=f"Could not decode CSV file. Please verify encoding: {str(last_err)}"
            )
    else:
        try:
            df = pd.read_excel(io.BytesIO(content), engine='openpyxl')
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to parse Excel workbook: {str(e)}"
            )

    if df.empty:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file contains no data rows."
        )

    return normalize_dataframe_columns(df)

def load_dataframe_from_file(file_path: str) -> pd.DataFrame:
    """Loads a DataFrame directly from a local path (for sample datasets)."""
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"File '{os.path.basename(file_path)}' not found.")

    ext = file_path.lower().split('.')[-1]
    with open(file_path, 'rb') as f:
        content = f.read()

    return load_dataframe_from_bytes(content, ext)
