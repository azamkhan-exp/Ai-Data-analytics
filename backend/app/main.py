import os
import time
from collections import OrderedDict
from typing import Dict, Any
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

from .api import api_router

# Load environment variables
load_dotenv()

# Bounded LRU in-memory store for active datasets (Stateless, zero database required)
MAX_STORE_CAPACITY = 50

class DatasetStore(OrderedDict):
    """LRU in-memory cache for loaded datasets and their analytical caches."""
    def __setitem__(self, key, value):
        if key in self:
            del self[key]
        elif len(self) >= MAX_STORE_CAPACITY:
            oldest_key, _ = self.popitem(last=False)
            print(f"[Store Eviction] Evicted oldest dataset session: {oldest_key}")
        value["last_accessed"] = time.time()
        super().__setitem__(key, value)

    def __getitem__(self, key):
        value = super().__getitem__(key)
        value["last_accessed"] = time.time()
        self.move_to_end(key)
        return value

datasets_store: Dict[str, Dict[str, Any]] = DatasetStore()

def create_app() -> FastAPI:
    app = FastAPI(
        title="InsightPulse Autonomous AI Data Analyst API",
        description="Production-ready Python FastAPI analytics engine with Pandas, NumPy, SciPy, and scikit-learn.",
        version="2.0.0"
    )

    # CORS Configuration
    # In production, set CORS_ORIGINS="https://your-app.vercel.app,https://another-domain.com"
    raw_cors = os.environ.get("CORS_ORIGINS", "")
    if raw_cors.strip():
        allowed_origins = [o.strip() for o in raw_cors.split(",") if o.strip()]
    else:
        # Default development origins
        allowed_origins = [
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "*"
        ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins if "*" not in allowed_origins else ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Mount API routers
    app.include_router(api_router)

    # Global Exception Handlers
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        import traceback
        traceback.print_exc()
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "Internal Analytics Engine Error",
                "detail": str(exc),
                "path": request.url.path
            }
        )

    return app

app = create_app()
