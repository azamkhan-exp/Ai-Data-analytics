import io
import os
import pandas as pd
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse, JSONResponse

from ..schemas.responses import CleanRequest, CleanResponse
from ..data.cleaner import clean_dataset
from ..analytics import run_full_analysis

router = APIRouter()

def get_store():
    from ..main import datasets_store
    return datasets_store

@router.post("/clean/{dataset_id}", response_model=CleanResponse)
def clean_dataset_endpoint(dataset_id: str, req: CleanRequest):
    """
    Applies non-destructive cleaning transformations and re-runs statistical profiling.
    """
    store = get_store()
    if dataset_id not in store:
        raise HTTPException(status_code=404, detail="Dataset not found.")

    item = store[dataset_id]
    original_df = item["df"]

    cleaned_df, changes_log = clean_dataset(
        df=original_df,
        drop_duplicates=req.drop_duplicates,
        fill_missing_numerical=req.fill_missing_numerical,
        fill_missing_categorical=req.fill_missing_categorical,
        drop_na_rows=req.drop_na_rows,
        drop_high_missing_cols_threshold=req.drop_high_missing_cols_threshold,
        drop_columns=req.drop_columns,
        rename_columns=req.rename_columns,
        trim_strings=req.trim_strings
    )

    new_analysis = run_full_analysis(cleaned_df)

    # Update in-memory session store
    store[dataset_id]["df"] = cleaned_df
    store[dataset_id]["analysis"] = new_analysis

    return CleanResponse(
        message="Dataset cleaned successfully.",
        changes_log=changes_log,
        analysis=new_analysis
    )

@router.get("/export/{dataset_id}")
def export_dataset(dataset_id: str, format: str = Query("csv", pattern="^(csv|json)$")):
    """
    Exports the current dataset as a CSV file or full analysis report as a formatted JSON document.
    """
    store = get_store()
    if dataset_id not in store:
        raise HTTPException(status_code=404, detail="Dataset not found.")

    item = store[dataset_id]
    df = item["df"]
    base_name = os.path.splitext(item["filename"])[0]

    if format == "csv":
        stream = io.StringIO()
        df.to_csv(stream, index=False)
        stream.seek(0)
        return StreamingResponse(
            io.BytesIO(stream.getvalue().encode('utf-8')),
            media_type="text/csv",
            headers={"Content-Disposition": f'attachment; filename="cleaned_{base_name}.csv"'}
        )
    else:
        export_payload = {
            "dataset": item["filename"],
            "exported_at": pd.Timestamp.now().isoformat(),
            "total_rows": len(df),
            "total_columns": len(df.columns),
            "analysis": item["analysis"]
        }
        return JSONResponse(
            content=export_payload,
            headers={"Content-Disposition": f'attachment; filename="report_{base_name}.json"'}
        )
