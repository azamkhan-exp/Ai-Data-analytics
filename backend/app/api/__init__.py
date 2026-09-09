from fastapi import APIRouter
from .routes_health import router as health_router
from .routes_analyze import router as analyze_router
from .routes_chart import router as chart_router
from .routes_ask import router as ask_router
from .routes_clean import router as clean_router

api_router = APIRouter(prefix="/api")
api_router.include_router(health_router, tags=["Health"])
api_router.include_router(analyze_router, tags=["Analyze"])
api_router.include_router(chart_router, tags=["Visualizations"])
api_router.include_router(ask_router, tags=["Ask Your Data"])
api_router.include_router(clean_router, tags=["Cleaning & Export"])

__all__ = ["api_router"]
