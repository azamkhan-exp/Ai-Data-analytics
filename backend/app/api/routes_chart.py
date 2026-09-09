from fastapi import APIRouter, HTTPException
from ..schemas.responses import CustomChartRequest
from ..analytics.visualizer import generate_automatic_visualizations, generate_custom_chart

router = APIRouter()

def get_store():
    from ..main import datasets_store
    return datasets_store

@router.get("/visualizations/{dataset_id}")
def get_visualizations(dataset_id: str):
    """Returns the full suite of automated Plotly visualizations."""
    store = get_store()
    if dataset_id not in store:
        raise HTTPException(status_code=404, detail="Dataset not found.")

    item = store[dataset_id]
    df = item["df"]
    analysis = item["analysis"]

    charts = generate_automatic_visualizations(
        df=df,
        col_types=analysis["column_types"],
        strong_corrs=analysis["strong_correlations"]
    )

    return {
        "dataset_id": dataset_id,
        "visualizations": charts
    }

@router.post("/visualizations/{dataset_id}/custom")
def create_custom_chart(dataset_id: str, req: CustomChartRequest):
    """Generates a user-configured Plotly chart specification."""
    store = get_store()
    if dataset_id not in store:
        raise HTTPException(status_code=404, detail="Dataset not found.")

    df = store[dataset_id]["df"]
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
