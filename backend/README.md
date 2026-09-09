# 🐍 InsightPulse — Python Analytics Engine & API

Production-grade Python backend for **InsightPulse — Autonomous AI Data Analyst**, powered by **FastAPI, Pandas, NumPy, SciPy, and scikit-learn**.

---

## 🏗️ Architecture

```
backend/
├── app/
│   ├── main.py                     # FastAPI application, CORS, and in-memory LRU session cache
│   ├── api/                        # Modular HTTP routes
│   │   ├── routes_health.py        # /api/health (zero database probe)
│   │   ├── routes_analyze.py       # /api/upload, /api/analysis/{id}, /api/samples
│   │   ├── routes_chart.py         # /api/visualizations/{id}, /custom
│   │   ├── routes_ask.py           # /api/query/{id} (Safe AST natural language engine)
│   │   └── routes_clean.py         # /api/clean/{id}, /api/export/{id}
│   ├── analytics/                  # Core Data Science & Statistical Engines
│   │   ├── profiler.py             # Schema, type inference, role detection, memory usage
│   │   ├── statistics.py           # Moments (Mean, Median, Mode, Variance, Skewness, Kurtosis)
│   │   ├── correlations.py         # Pearson correlation matrix & ranked pairs
│   │   ├── anomalies.py            # Dual IQR + Z-Score + scikit-learn IsolationForest
│   │   ├── trends.py               # Time-series periodicity and growth momentum
│   │   ├── data_quality.py         # 0-100 algorithmic hygiene health score
│   │   ├── kpis.py                 # Smart heuristic business metric detector
│   │   └── insights.py             # Grounded deterministic findings + optional Gemini AI
│   ├── data/                       # Ingestion & Data Hygiene
│   │   ├── loader.py               # CSV (multi-encoding fallback) & Excel (openpyxl)
│   │   ├── cleaner.py              # In-memory deduplication, imputation, column drops/renames
│   │   └── validators.py           # 50MB file size, extension, and MIME validation
│   ├── ai/
│   │   └── gemini.py               # Optional Gemini GenAI client (graceful offline fallback)
│   └── schemas/
│       └── responses.py            # Pydantic models for validation and OpenAPI docs
├── sample_data/                    # Bundled demonstration datasets
│   ├── sales_performance.csv
│   └── customer_churn.xlsx
├── Dockerfile                      # Production container deployment
├── Procfile                        # PaaS web process definition
├── requirements.txt                # Curated Python data-science dependencies
└── test_api.py                     # Comprehensive test suite
```

---

## ⚡ Quick Start

### 1. Prerequisites
- Python 3.10+ (Python 3.11 or 3.12 recommended)
- `pip` or `uv`

### 2. Setup Virtual Environment
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows (PowerShell):
.venv\Scripts\Activate.ps1
# On Linux/macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Variables (Optional)
Copy `.env.example` to `.env`:
```env
# Optional Gemini AI key for strategic briefing (Deterministic engine works 100% without it)
GEMINI_API_KEY=your_gemini_api_key_here

# Allowed CORS origins (comma-separated). Set your Vercel frontend URL in production:
CORS_ORIGINS=https://your-insightpulse.vercel.app,http://localhost:5173
```

### 4. Run Development Server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
- API Base: `http://localhost:8000`
- Interactive Swagger UI: `http://localhost:8000/docs`
- Health Diagnostic: `http://localhost:8000/api/health`

### 5. Run Automated Tests
```bash
python -m unittest test_api.py
```

---

## 🚀 Cloud Deployment

### Deploy to Railway
1. Push your repository to GitHub.
2. In [Railway](https://railway.app), click **"New Project"** $\rightarrow$ **"Deploy from GitHub repo"**.
3. Select your repository.
4. Set **Root Directory** to `backend`.
5. Under **Variables**, add:
   - `CORS_ORIGINS=https://your-frontend.vercel.app`
   - `GEMINI_API_KEY=your_key` (optional)
6. Railway detects `Dockerfile` or `Procfile` and deploys automatically.

### Deploy to Render
1. In [Render](https://render.com), click **"New +"** $\rightarrow$ **"Web Service"**.
2. Select repository, set **Root Directory** to `backend`.
3. Set **Runtime** to `Python 3`.
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
6. Add Environment Variables:
   - `CORS_ORIGINS=https://your-frontend.vercel.app`
