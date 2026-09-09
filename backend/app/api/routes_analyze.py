import os
import uuid
from typing import Dict, Any
from fastapi import APIRouter, UploadFile, File, HTTPException, Query

from ..data.validators import validate_uploaded_file
from ..data.loader import load_dataframe_from_bytes, load_dataframe_from_file
from ..analytics import run_full_analysis
from ..schemas.responses import UploadResponse, SamplesResponse, SampleItem

router = APIRouter()

SAMPLE_DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "sample_data"))

def get_store() -> Dict[str, Any]:
    # Lazily import store from main app module
    from ..main import datasets_store
    return datasets_store

@router.post("/upload", response_model=UploadResponse)
async def upload_dataset(file: UploadFile = File(...)):
    """Uploads, validates, and profiles a CSV or Excel dataset."""
    filename = file.filename or "dataset.csv"
    content = await file.read()
    ext = validate_uploaded_file(filename, len(content))

    df = load_dataframe_from_bytes(content, ext)
    analysis = run_full_analysis(df)
    dataset_id = str(uuid.uuid4())

    store = get_store()
    store[dataset_id] = {
        "id": dataset_id,
        "filename": filename,
        "df": df,
        "analysis": analysis
    }

    return UploadResponse(
        dataset_id=dataset_id,
        filename=filename,
        total_rows=analysis["summary"]["total_rows"],
        total_columns=analysis["summary"]["total_columns"],
        columns=list(df.columns)
    )

@router.get("/samples", response_model=SamplesResponse)
def list_sample_datasets():
    """Lists bundled demonstration datasets."""
    samples = []
    if os.path.exists(SAMPLE_DATA_DIR):
        for f in os.listdir(SAMPLE_DATA_DIR):
            if f.endswith(('.csv', '.xlsx', '.xls')):
                path = os.path.join(SAMPLE_DATA_DIR, f)
                size_kb = round(os.path.getsize(path) / 1024, 1)
                desc = "Enterprise sales performance metrics across regions, products, discounts, and profits." if "sales" in f.lower() else "Subscription customer churn metrics across tenure, contracts, charges, and churn status."
                samples.append(SampleItem(name=f, size_kb=size_kb, description=desc))
    return SamplesResponse(samples=samples)

@router.post("/samples/load", response_model=UploadResponse)
def load_sample(name: str = Query(..., description="Filename of sample dataset")):
    """Loads a bundled sample dataset immediately."""
    file_path = os.path.join(SAMPLE_DATA_DIR, name)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"Sample dataset '{name}' not found.")

    df = load_dataframe_from_file(file_path)
    analysis = run_full_analysis(df)
    dataset_id = str(uuid.uuid4())

    store = get_store()
    store[dataset_id] = {
        "id": dataset_id,
        "filename": name,
        "df": df,
        "analysis": analysis
    }

    return UploadResponse(
        dataset_id=dataset_id,
        filename=name,
        total_rows=analysis["summary"]["total_rows"],
        total_columns=analysis["summary"]["total_columns"],
        columns=list(df.columns)
    )

@router.get("/analysis/{dataset_id}")
def get_analysis(dataset_id: str):
    """Returns dataset summary, quality score, moments, and correlations."""
    store = get_store()
    if dataset_id not in store:
        raise HTTPException(status_code=404, detail="Dataset not found or session expired. Please re-upload.")

    item = store[dataset_id]
    return {
        "dataset_id": dataset_id,
        "filename": item["filename"],
        "analysis": item["analysis"]
    }

@router.get("/insights/{dataset_id}")
def get_insights(dataset_id: str):
    """Returns grounded statistical and optional AI insights."""
    store = get_store()
    if dataset_id not in store:
        raise HTTPException(status_code=404, detail="Dataset not found.")

    item = store[dataset_id]
    return {
        "dataset_id": dataset_id,
        "insights": item["analysis"].get("insights", [])
    }
