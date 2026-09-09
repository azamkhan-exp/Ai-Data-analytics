from fastapi import APIRouter, HTTPException
from ..schemas.responses import QueryRequest, QueryResponse
from ..analytics.query_engine import answer_data_question

router = APIRouter()

def get_store():
    from ..main import datasets_store
    return datasets_store

@router.post("/query/{dataset_id}", response_model=QueryResponse)
def ask_question(dataset_id: str, req: QueryRequest):
    """
    Answers natural language dataset queries using safe, parameterized Pandas aggregations.
    Guaranteed zero eval(), exec(), or arbitrary code execution.
    """
    store = get_store()
    if dataset_id not in store:
        raise HTTPException(status_code=404, detail="Dataset not found or session expired.")

    item = store[dataset_id]
    df = item["df"]
    col_types = item["analysis"]["column_types"]

    try:
        result = answer_data_question(df, req.question, col_types)
        return QueryResponse(
            question=result["question"],
            answer=result["answer"],
            data=result.get("data"),
            chart=result.get("chart"),
            suggestions=result.get("suggestions")
        )
    except Exception as e:
        return QueryResponse(
            question=req.question,
            answer=f"Could not compute an answer for '{req.question}': {str(e)}",
            data=None,
            chart=None,
            suggestions=["What is the average of the primary numeric column?", "Show top 5 categories", "Are there missing values?"]
        )
