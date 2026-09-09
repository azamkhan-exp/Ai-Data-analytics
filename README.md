# 🚀 InsightPulse — Autonomous AI Data Analyst

> **Production-Grade, Decoupled Architecture: Python Data Science Engine + Vercel-Ready React Frontend**  
> Instant in-memory profiling, algorithmic Data Quality Scores (0–100), Smart KPI detection, multi-algorithm outlier detection (Tukey IQR, Gaussian Z-Score, and scikit-learn Isolation Forest), interactive Plotly visualizations, parameterized conversational query engine (strictly zero `eval()` / `exec()`), and data preprocessing — with **zero databases required** and **stateless in-memory session management**.

---

## 🌟 Architecture Overview

InsightPulse uses a modern decoupled architecture that keeps **data science in Python** where it belongs (leveraging Pandas, NumPy, SciPy, and scikit-learn) while delivering a lightning-fast, responsive user experience through a **React + Vite** single-page application deployable to **Vercel**.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    CLIENT BROWSER (Vercel-Hosted SPA)                   │
│                                                                         │
│  React 19 + Vite 8 + Tailwind CSS + Plotly.js                           │
│  • 9 Specialized Analytic Views                                         │
│  • Dark Mode & Light Mode support                                       │
│  • Interactive Custom Plotly Chart Builder                              │
│  • Client-side file validation & stream upload                          │
│  • Dynamic API connection via VITE_API_URL                              │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │
                        HTTP REST / JSON Stream
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                 PYTHON BACKEND (FastAPI Analytics Engine)               │
│                                                                         │
│  Deployable to Railway, Render, Fly.io, AWS, or Docker                  │
│                                                                         │
│  ┌───────────────────────────────┐   ┌───────────────────────────────┐  │
│  │ Data Ingestion & Profiling    │   │ Statistical Moments Engine    │  │
│  │ • Pandas & OpenPyXL Loader    │   │ • SciPy Skewness & Kurtosis   │  │
│  │ • Multi-encoding Fallbacks    │   │ • Variance, Std Dev, Quartiles│  │
│  │ • Type & Role Inference       │   │ • Pearson Correlation Matrix  │  │
│  └───────────────────────────────┘   └───────────────────────────────┘  │
│  ┌───────────────────────────────┐   ┌───────────────────────────────┐  │
│  │ Anomaly Detection Center      │   │ Algorithmic Data Quality      │  │
│  │ • Tukey 1.5× IQR Bounds       │   │ • 0–100 Health Score          │  │
│  │ • Gaussian Z-Score (|z| > 3.0)│   │ • Hygiene Deduction Factors   │  │
│  │ • scikit-learn IsolationForest│   │ • Actionable Remediation Tips │  │
│  └───────────────────────────────┘   └───────────────────────────────┘  │
│  ┌───────────────────────────────┐   ┌───────────────────────────────┐  │
│  │ Ask Your Data 2.0 (Safe AST)  │   │ Visualizations & Cleaner      │  │
│  │ • Parameterized Pandas ops    │   │ • Plotly JSON Generators      │  │
│  │ • STRICTLY ZERO eval()/exec() │   │ • In-Memory Deduplication     │  │
│  │ • Top/Bottom/Mean/Group aggreg│   │ • Imputation (Mean/Mode/Zero) │  │
│  └───────────────────────────────┘   └───────────────────────────────┘  │
│  ┌───────────────────────────────┐   ┌───────────────────────────────┐  │
│  │ In-Memory Bounded LRU Store   │   │ Optional Gemini AI Synthesis  │  │
│  │ • Zero Database (No SQL/NoSQL)│   │ • Fallback to 100% offline    │  │
│  │ • Auto-eviction (Cap: 50 items│   │   deterministic algorithms    │  │
│  └───────────────────────────────┘   └───────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## ⚡ Key Architectural Tenets

1. **Python-Native Data Science**: Core analytical workloads remain in Python. No complex mathematical operations or statistical algorithms have been rewritten in JavaScript.
2. **Zero Database Dependency**: Operates 100% database-free. No PostgreSQL, MongoDB, SQLite, Supabase, Redis, or Firebase required. Datasets reside in a bounded in-memory LRU store with automatic eviction.
3. **No Persistent Disk Dependency**: Uploaded files and processing streams are held in memory. The application does not write temporary files to `/uploads` or `/data`, ensuring stateless portability across serverless and container platforms.
4. **Zero Dynamic Code Execution**: The conversational natural language engine translates user queries into safe, parameterized Pandas operations using strict AST parsing and whitelist dispatching. **Strictly zero `eval()`, `exec()`, or shell commands.**
5. **AI Optionality**: Operates 100% offline with deterministic, verifiable statistical heuristics. When `GEMINI_API_KEY` is present, executive summaries are enriched with Google Gemini Pro.
6. **Configurable Endpoints**: No hardcoded `localhost:8000`. The frontend resolves its backend target dynamically via the `VITE_API_URL` environment variable.

---

## 📊 Core Features & 9 Specialized Views

| View / Module | Description |
| :--- | :--- |
| **1. Ingestion Studio** | Drag-and-drop ingestion for CSV and XLSX files up to 50MB. Includes 1-click bundled datasets (*Retail Sales Performance* and *Customer Churn*). |
| **2. Executive Dashboard** | Summary metric cards, algorithmic Data Quality Score, Smart KPI detection (Revenue, Margin, Volume, Churn), and dataset preview. |
| **3. Data Explorer 2.0** | Interactive searchable table with client-side filtering, column visibility toggles, and data dictionary profiling. |
| **4. Visual Analytics** | Automated distribution histograms, categorical bar charts, correlation heatmaps, time-series trends, and an interactive Custom Chart Builder. |
| **5. Descriptive Statistics** | Comprehensive moments table computing Mean, Median, Mode, Standard Deviation, Variance, Min, Max, Range, IQR, Skewness, and Excess Kurtosis. |
| **6. Anomaly Detection Center** | Multi-algorithm outlier identification combining Tukey ($1.5 \times \text{IQR}$), Gaussian Z-Score ($|z| > 3.0$), and scikit-learn's `IsolationForest`. |
| **7. Data Quality & Hygiene** | Algorithmic 0–100 health audit penalizing missing cells, duplicate records, high-cardinality noise, and severe skewness, with automated remediation tips. |
| **8. Automated & AI Insights** | Rule-based statistical pattern extraction coupled with optional Google Gemini Pro synthesis for narrative executive briefings. |
| **9. Ask Your Data 2.0** | Conversational data exploration safely querying Pandas DataFrames with instant response tables and generated Plotly charts. |

---

## 🛠️ Tech Stack

### Frontend
- **Framework**: React 19 + Vite 8
- **Styling**: Tailwind CSS (with full class-based Dark Mode support)
- **Charts**: Plotly.js (`plotly.js-dist-min`)
- **Icons**: Lucide React
- **HTTP Client**: Axios (dynamic `VITE_API_URL` resolution)

### Backend
- **API Framework**: FastAPI + Uvicorn
- **Data Manipulation**: Pandas 3 + NumPy 2 + OpenPyXL
- **Statistical Science**: SciPy + scikit-learn
- **Visualization Specs**: Plotly Python (serializes to JSON specs for the frontend)
- **Validation**: Pydantic v2
- **Optional AI**: Google GenAI SDK (`google-genai`)

---

## 🚀 Running Locally

### 1. Start the Python Backend

```bash
cd backend

# Create and activate virtual environment
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# (Optional) Create .env file for Gemini AI
# echo GEMINI_API_KEY=your_gemini_key > .env

# Run FastAPI server
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

FastAPI will be running at `http://127.0.0.1:8000`. You can inspect the Swagger API documentation at `http://127.0.0.1:8000/docs`.

### 2. Start the React Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start Vite dev server (proxies /api to http://127.0.0.1:8000)
npm run dev
```

Open [http://localhost:5173](http://localhost:5173) in your browser.

---

## ☁️ Deployment Guide

### A. Deploy Frontend to Vercel

1. Push your repository to GitHub.
2. In the [Vercel Dashboard](https://vercel.com/new), select **"Import Project"** and point to your repository.
3. Configure the Project Settings:
   - **Root Directory**: `frontend`
   - **Framework Preset**: `Vite`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
4. Add the Environment Variable in Vercel:
   - `VITE_API_URL`: The public URL of your deployed Python backend (e.g., `https://insightpulse-api.up.railway.app`)
5. Click **Deploy**. Vercel will build and host your production frontend globally with instant edge caching.

### B. Deploy Backend to Python Host (Railway / Render / Fly.io / AWS)

#### Option 1: Railway / Render (Using Dockerfile or Procfile)
1. Point Railway or Render to your GitHub repository.
2. Set the **Root Directory** to `backend`.
3. Set the start command:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```
4. Set Environment Variables:
   - `CORS_ORIGINS`: Your Vercel frontend URL (e.g., `https://insightpulse.vercel.app,http://localhost:5173`)
   - `GEMINI_API_KEY`: *(Optional)* Your Google Gemini API key.
5. Deploy. Copy the assigned public URL and paste it into your Vercel frontend's `VITE_API_URL` setting.

#### Option 2: Docker Container
Build and run the production Docker container:
```bash
cd backend
docker build -t insightpulse-backend .
docker run -p 8000:8000 -e CORS_ORIGINS="*" insightpulse-backend
```

---

## 🛡️ Security & Reliability Audit

- **AST Whitelisting**: Natural language queries are parsed into high-level intent tokens. No arbitrary Python code is ever compiled or evaluated.
- **Payload Limits**: Ingestion strictly enforces a 50MB file ceiling and validates MIME types and file signatures.
- **LRU Session Eviction**: To prevent memory leaks in long-running container instances, the dataset registry automatically discards the least-recently-used datasets once the capacity limit (50 datasets) is reached.
- **Graceful Fallbacks**: If the Gemini API key is omitted, exhausted, or encounters network timeouts, the system seamlessly serves 100% deterministic statistical summaries without crashing.

---

## 📄 License

MIT License © 2026 InsightPulse Team. Built for modern autonomous data intelligence.
