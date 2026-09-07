# InsightPulse — AI Data Analyst Web Application

An autonomous, full-stack **AI Data Analyst** web application built with React, Vite, Tailwind CSS, Plotly, Python, FastAPI, and Pandas.

Upload any CSV or Excel file, and the application automatically profiles the dataset, detects business data types, checks data quality (nulls, duplicates, outliers), generates interactive Plotly visualizations, produces statistical & AI-synthesized insights, and provides a conversational natural-language Q&A interface powered by safe Pandas operations (**zero arbitrary code execution**).

---

## Architecture Overview

```
ai-data-analyst/
├── backend/
│   ├── analyzer.py          # Data profiling, type inference, IQR outliers, summary stats
│   ├── visualizer.py        # Automatic & custom Plotly chart specifications (JSON)
│   ├── insights.py          # Rule-based statistical engine + optional LLM synthesis
│   ├── query_engine.py      # Natural language query parser to safe Pandas ops (no eval/exec)
│   ├── data_cleaner.py      # Missing value imputation, deduplication, CSV export
│   ├── main.py              # FastAPI application routes, CORS, upload handling
│   ├── test_api.py          # Automated verification test suite
│   ├── sample_data/         # Bundled sample datasets (sales_performance.csv, customer_churn.xlsx)
│   ├── requirements.txt     # Python dependencies
│   └── .env.example         # Optional LLM API key configuration
├── frontend/
│   ├── src/
│   │   ├── api.js           # API client service
│   │   ├── App.jsx          # Main application container & view manager
│   │   └── components/
│   │       ├── Sidebar.jsx           # Dashboard navigation sidebar
│   │       ├── Header.jsx            # Top navbar, demo loader & health badge
│   │       ├── FileUpload.jsx        # Drag-and-drop zone with format validation
│   │       ├── MetricCards.jsx       # 5 KPI metrics & column type badges
│   │       ├── DataPreview.jsx       # Paginated 20-row table & column data dictionary
│   │       ├── Statistics.jsx        # Numerical, categorical & correlation tables
│   │       ├── Visualizations.jsx    # Auto Plotly charts & custom chart builder
│   │       ├── AiInsights.jsx        # Categorized insight cards & severity tags
│   │       ├── ChatInterface.jsx     # Natural language chat stream with charts & tables
│   │       ├── DataCleanerModal.jsx  # Interactive preprocessing & imputation modal
│   │       ├── ExportModal.jsx       # Cleaned CSV & JSON analytical report exporter
│   │       └── PlotlyChart.jsx       # Responsive Plotly.js wrapper
│   ├── package.json
│   ├── vite.config.js       # Vite config with backend API proxy
│   └── tailwind.config.js
├── .env.example
└── README.md
```

---

## Core Implemented Features

1. **File Upload & Validation**:
   - Supports `.csv`, `.xlsx`, `.xls` formats up to 50MB.
   - Validates file type, mime encoding, non-empty dataset, and parse errors.
   - Bundled with 2 sample datasets (`sales_performance.csv` and `customer_churn.xlsx`) for 1-click immediate testing.

2. **Dataset Preview & Quality Profiling**:
   - Interactive preview of first 20 rows with live search filtering.
   - Column schema dictionary with detected business types (`numerical`, `categorical`, `datetime`, `boolean`).
   - Missing value indicators and duplicate row count.

3. **Automated Statistical Analysis**:
   - Computes count, mean, median, minimum, maximum, standard deviation, IQR, skewness, outlier counts, and missing percentages for numerical columns.
   - Computes unique counts, most frequent modes, frequency counts, and top 5 category breakdowns for categorical columns.
   - Computes Pearson correlation matrix and flags strong linear dependencies ($|r| \ge 0.4$).

4. **Interactive Plotly Visualizations**:
   - **Histograms** with box plot marginals for numerical features.
   - **Bar charts** showing frequency distributions for top categories.
   - **Correlation matrix heatmap** with annotated coefficients.
   - **Time series trend lines** when date/time columns are detected.
   - **Scatter plots** for correlated pairs with trendlines.
   - **Interactive Custom Chart Builder**: Allows users to dynamically select chart type (Bar, Line, Scatter, Box, Pie, Histogram), X-axis, Y-axis, Color grouping, and aggregation function.

5. **AI & Statistical Insights Engine**:
   - Works **100% offline out-of-the-box** without requiring any API keys.
   - Generates verifiable, grounded findings for data quality, skewness, outliers, dominant categories, and timeline trends.
   - Optionally enhances insights with executive takeaways if `GEMINI_API_KEY` is provided in `backend/.env`.

6. **Ask Questions About Data (Safe Natural Language Q&A)**:
   - Chat interface with prompt suggestion pills.
   - Supports questions like:
     - *"What is the average sales?"*
     - *"Which product generated the highest revenue?"*
     - *"Which month had the highest sales?"*
     - *"Are there missing values?"*
     - *"What are the top 10 customers?"*
   - Maps questions into safe, parameterized Pandas operations (`groupby`, `agg`, `nlargest`, `corr`, `isna`).
   - **Strictly zero arbitrary code execution (`eval()` / `exec()` are forbidden).**
   - Returns markdown text, tabular result subsets, and auto-generated Plotly charts inside the chat bubble.

7. **Data Cleaning & Export**:
   - Deduplicate rows.
   - Impute missing numerical values (Mean, Median, Zero).
   - Impute missing categorical values (Mode, "Unknown").
   - Drop rows or high-null columns.
   - Export cleaned dataset as CSV and full analysis report as JSON.

---

## Quickstart Guide

### Prerequisites
- Python 3.10+ (Tested on Python 3.14)
- Node.js 18+ (Tested on Node 24)
- npm 9+

---

### 1. Start the Backend

Open a terminal in the `backend` directory:

```powershell
cd backend

# If not already created, create a virtual environment:
python -m venv venv

# Activate virtual environment (Windows PowerShell):
.\venv\Scripts\Activate.ps1
# Or on macOS/Linux:
# source venv/bin/activate

# Install dependencies:
pip install -r requirements.txt

# (Optional) Copy .env.example to .env and add GEMINI_API_KEY if desired:
# cp .env.example .env

# Run automated tests to verify:
python test_api.py

# Start the FastAPI server:
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

- **Backend API**: `http://127.0.0.1:8000`
- **Interactive Swagger Docs**: `http://127.0.0.1:8000/docs`
- **API Health Check**: `http://127.0.0.1:8000/api/health`

---

### 2. Start the Frontend

In a separate terminal in the `frontend` directory:

```powershell
cd frontend

# Install dependencies:
npm install

# Start Vite development server:
npm run dev
```

- **Frontend Application**: `http://localhost:5173`

---

## Security Safeguards

- **No Arbitrary Code Execution**: User and LLM queries are never executed using Python `eval()` or `exec()`. The query engine exclusively translates recognized intents into pre-programmed, parameterized Pandas methods (`df.groupby()`, `df.agg()`, `df.nlargest()`).
- **File Validation**: Mime types, extensions (`.csv`, `.xlsx`, `.xls`), and file size limits (50MB) are strictly validated before parsing.
- **Safe Parsing**: CSV parsing includes encoding fallbacks (`utf-8` with `latin1` fallback) and error boundaries to prevent server crashes.

---

## Known Limitations

- In-memory dataset storage: Datasets are cached in memory for the active server session. Multi-user enterprise scaling would benefit from Redis or SQLite persistent session caching.
- Very large files (>500,000 rows) may take several seconds for complex correlation matrix calculations or full browser-side Plotly rendering.

---

## Suggested Next Improvements

1. **Persistent Project History**: Add SQLite/PostgreSQL storage to save historical uploaded datasets and previous chat conversations across browser refreshes.
2. **Advanced ML Forecasting**: Integrate Prophet or Scikit-learn for automated time-series forecasting and anomaly score calculation.
3. **Multi-File Joins**: Allow users to upload multiple related relational tables and define join keys.
