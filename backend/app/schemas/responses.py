from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field

class HealthResponse(BaseModel):
    status: str = "ok"
    service: str = "insightpulse-analytics"
    database: bool = False
    ai: str = "optional"
    version: str = "2.0.0"

class UploadResponse(BaseModel):
    dataset_id: str
    filename: str
    total_rows: int
    total_columns: int
    columns: List[str]

class SampleItem(BaseModel):
    name: str
    size_kb: float
    description: str

class SamplesResponse(BaseModel):
    samples: List[SampleItem]

class CustomChartRequest(BaseModel):
    chart_type: str = Field(..., description="bar, line, scatter, box, pie, histogram, area")
    x_col: str
    y_col: Optional[str] = None
    color_col: Optional[str] = None
    agg_func: Optional[str] = Field(None, description="sum, mean, count, median, min, max")

class QueryRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=500)

class QueryResponse(BaseModel):
    question: str
    answer: str
    data: Optional[List[Dict[str, Any]]] = None
    chart: Optional[Dict[str, Any]] = None
    suggestions: Optional[List[str]] = None

class CleanRequest(BaseModel):
    drop_duplicates: bool = True
    fill_missing_numerical: str = "none"  # none, mean, median, zero
    fill_missing_categorical: str = "none"  # none, mode, unknown
    drop_na_rows: bool = False
    drop_high_missing_cols_threshold: Optional[float] = None
    drop_columns: Optional[List[str]] = None
    rename_columns: Optional[Dict[str, str]] = None
    trim_strings: bool = True

class CleanResponse(BaseModel):
    message: str
    changes_log: List[str]
    analysis: Dict[str, Any]
