import os
from fastapi import APIRouter
from ..schemas.responses import HealthResponse

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
def health_check():
    """
    Health diagnostic probe. Confirms zero database requirement and optional AI status.
    """
    has_gemini = bool(os.environ.get("GEMINI_API_KEY"))
    return HealthResponse(
        status="ok",
        service="insightpulse-analytics",
        database=False,
        ai="connected" if has_gemini else "optional",
        version="2.0.0"
    )
