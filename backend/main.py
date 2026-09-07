import os
import io
import uuid
from typing import Dict, Any, Optional
from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel
import pandas as pd
from dotenv import load_dotenv

from analyzer import analyze_dataset
from visualizer import generate_automatic_visualizations, generate_custom_chart
from insights import generate_rule_based_insights, generate_llm_insights
from query_engine import answer_data_question
from data_cleaner import clean_dataset

# Load environment variables (e.g. GEMINI_API_KEY)
load_dotenv()

app = FastAPI(
    title="AI Data Analyst API",
    description="Backend for automated dataset profiling, visualization, AI insights, and natural language querying.",
    version="1.0.0"
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for active datasets and cached analyses
# Key: dataset_id -> Dict
datasets_store: Dict[str, Dict[str, Any]] = {}

MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB limit
SAMPLE_DATA_DIR = os.path.join(os.path.dirname(__file__), "sample_data")

class CustomChartRequest(BaseModel):
    chart_type: str
    x_col: str
    y_col: Optional[str] = None
    color_col: Optional[str] = None
    agg_func: Optional[str] = None

class QueryRequest(BaseModel):
    question: str

class CleanRequest(BaseModel):
    drop_duplicates: bool = True
    fill_missing_numerical: str = "none"
    fill_missing_categorical: str = "none"
    drop_na_rows: bool = False
    drop_high_missing_cols_threshold: Optional[float] = None

def load_and_store_dataframe(df: pd.DataFrame, filename: str) -> Dict[str, Any]:
    """Helper to process, analyze and store dataset."""
    if df.empty:
        raise HTTPException(status_code=400, detail="The uploaded file contains no data rows.")
    
    dataset_id = str(uuid.uuid4())
    analysis = analyze_dataset(df)
    rule_insights = generate_rule_based_insights(df, analysis)
    insights = generate_llm_insights(df, analysis, rule_insights)
    visualizations = generate_automatic_visualizations(
        df,
        analysis["column_types"],
        analysis["strong_correlations"]
    )

    datasets_store[dataset_id] = {
        "id": dataset_id,
        "filename": filename,
        "df": df,
        "analysis": analysis,
        "insights": insights,
        "visualizations": visualizations
    }

    return {
        "dataset_id": dataset_id,
        "filename": filename,
        "total_rows": analysis["summary"]["total_rows"],
        "total_columns": analysis["summary"]["total_columns"],
        "columns": list(df.columns)
    }

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "AI Data Analyst API",
        "version": "1.0.0",
        "has_llm_configured": bool(os.environ.get("GEMINI_API_KEY") or os.environ.get("OPENAI_API_KEY"))
    }

@app.post("/api/upload")
async def upload_dataset(file: UploadFile = File(...)):
    """Uploads and validates a CSV or XLSX dataset."""
    filename = file.filename or "dataset.csv"
    ext = filename.lower().split('.')[-1]
    if ext not in ['csv', 'xlsx', 'xls']:
        raise HTTPException(status_code=400, detail="Unsupported file type. Please upload a .csv or .xlsx file.")

    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large. Maximum supported upload size is 50MB.")
    if len(content) == 0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    try:
        if ext == 'csv':
            try:
                df = pd.read_csv(io.BytesIO(content))
            except UnicodeDecodeError:
                df = pd.read_csv(io.BytesIO(content), encoding='latin1')
        else:
            df = pd.read_excel(io.BytesIO(content))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse file: {str(e)}")

    return load_and_store_dataframe(df, filename)

@app.get("/api/samples")
def list_sample_datasets():
    """Lists available sample datasets."""
    samples = []
    if os.path.exists(SAMPLE_DATA_DIR):
        for f in os.listdir(SAMPLE_DATA_DIR):
            if f.endswith(('.csv', '.xlsx')):
                path = os.path.join(SAMPLE_DATA_DIR, f)
                samples.append({
                    "name": f,
                    "size_kb": round(os.path.getsize(path) / 1024, 1),
                    "description": "Enterprise sales & performance metrics across regions, products, and profits." if "sales" in f else "Customer churn and subscription metrics."
                })
    return {"samples": samples}

@app.post("/api/samples/load")
def load_sample_dataset(name: str = Query(..., description="Filename of sample dataset")):
    """Loads one of the bundled sample datasets."""
    file_path = os.path.join(SAMPLE_DATA_DIR, name)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"Sample dataset '{name}' not found.")
    
    if name.endswith('.csv'):
        df = pd.read_csv(file_path)
    else:
        df = pd.read_excel(file_path)

    return load_and_store_dataframe(df, name)

@app.get("/api/analysis/{dataset_id}")
def get_analysis(dataset_id: str):
    """Returns dataset summary, column types, missing values, and preview rows."""
    if dataset_id not in datasets_store:
        raise HTTPException(status_code=404, detail="Dataset not found. Please upload a dataset first.")
    
    data = datasets_store[dataset_id]
    return {
        "dataset_id": dataset_id,
        "filename": data["filename"],
        "analysis": data["analysis"]
    }

@app.get("/api/visualizations/{dataset_id}")
def get_visualizations(dataset_id: str):
    """Returns automatic Plotly charts for the dataset."""
    if dataset_id not in datasets_store:
        raise HTTPException(status_code=404, detail="Dataset not found.")
    
    return {
        "dataset_id": dataset_id,
        "visualizations": datasets_store[dataset_id]["visualizations"]
    }

@app.post("/api/visualizations/{dataset_id}/custom")
def create_custom_visualization(dataset_id: str, req: CustomChartRequest):
    """Generates a user-configured Plotly chart."""
    if dataset_id not in datasets_store:
        raise HTTPException(status_code=404, detail="Dataset not found.")
    
    df = datasets_store[dataset_id]["df"]
    try:
        spec = generate_custom_chart(
            df=df,
            chart_type=req.chart_type,
            x_col=req.x_col,
            y_col=req.y_col,
            color_col=req.color_col,
            agg_func=req.agg_func
        )
        return {"spec": spec}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/insights/{dataset_id}")
def get_insights(dataset_id: str):
    """Returns AI and statistical insights."""
    if dataset_id not in datasets_store:
        raise HTTPException(status_code=404, detail="Dataset not found.")
    
    return {
        "dataset_id": dataset_id,
        "insights": datasets_store[dataset_id]["insights"]
    }

@app.post("/api/query/{dataset_id}")
def ask_question(dataset_id: str, req: QueryRequest):
    """Answers natural language data questions using safe Pandas operations."""
    if dataset_id not in datasets_store:
        raise HTTPException(status_code=404, detail="Dataset not found.")
    
    data = datasets_store[dataset_id]
    df = data["df"]
    col_types = data["analysis"]["column_types"]

    try:
        result = answer_data_question(df, req.question, col_types)
        return result
    except Exception as e:
        return {
            "question": req.question,
            "answer": f"An error occurred while answering your question: {str(e)}",
            "data": [],
            "chart": None,
            "suggestions": ["What is the average sales?", "Show top 5 products", "Are there missing values?"]
        }

@app.post("/api/clean/{dataset_id}")
def clean_dataset_endpoint(dataset_id: str, req: CleanRequest):
    """Cleans dataset (drop duplicates, fill missing values) and updates analysis."""
    if dataset_id not in datasets_store:
        raise HTTPException(status_code=404, detail="Dataset not found.")
    
    data = datasets_store[dataset_id]
    df = data["df"]

    cleaned_df, changes_log = clean_dataset(
        df=df,
        drop_duplicates=req.drop_duplicates,
        fill_missing_numerical=req.fill_missing_numerical,
        fill_missing_categorical=req.fill_missing_categorical,
        drop_na_rows=req.drop_na_rows,
        drop_high_missing_cols_threshold=req.drop_high_missing_cols_threshold
    )

    # Re-run analysis & visuals
    analysis = analyze_dataset(cleaned_df)
    rule_insights = generate_rule_based_insights(cleaned_df, analysis)
    insights = generate_llm_insights(cleaned_df, analysis, rule_insights)
    visualizations = generate_automatic_visualizations(
        cleaned_df,
        analysis["column_types"],
        analysis["strong_correlations"]
    )

    datasets_store[dataset_id]["df"] = cleaned_df
    datasets_store[dataset_id]["analysis"] = analysis
    datasets_store[dataset_id]["insights"] = insights
    datasets_store[dataset_id]["visualizations"] = visualizations

    return {
        "message": "Dataset cleaned successfully.",
        "changes_log": changes_log,
        "analysis": analysis
    }

@app.get("/api/export/{dataset_id}")
def export_dataset(dataset_id: str, format: str = Query("csv", pattern="^(csv|json)$")):
    """Exports cleaned dataset as CSV or summary as JSON."""
    if dataset_id not in datasets_store:
        raise HTTPException(status_code=404, detail="Dataset not found.")
    
    data = datasets_store[dataset_id]
    df = data["df"]
    base_name = os.path.splitext(data["filename"])[0]

    if format == "csv":
        stream = io.StringIO()
        df.to_csv(stream, index=False)
        stream.seek(0)
        return StreamingResponse(
            io.BytesIO(stream.getvalue().encode('utf-8')),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename=cleaned_{base_name}.csv"}
        )
    else:
        export_payload = {
            "dataset": data["filename"],
            "analysis": data["analysis"],
            "insights": data["insights"]
        }
        return JSONResponse(
            content=export_payload,
            headers={"Content-Disposition": f"attachment; filename=report_{base_name}.json"}
        )
