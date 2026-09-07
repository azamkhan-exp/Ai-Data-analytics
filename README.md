# ⚡ InsightPulse — Autonomous AI Data Analyst

[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://python.org)
[![React](https://img.shields.io/badge/React-18%2B-61DAFB.svg?logo=react&logoColor=black)](https://react.dev)
[![Vite](https://img.shields.io/badge/Vite-5%2B-646CFF.svg?logo=vite&logoColor=white)](https://vitejs.dev)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.4%2B-38B2AC.svg?logo=tailwind-css&logoColor=white)](https://tailwindcss.com)
[![Plotly](https://img.shields.io/badge/Plotly.js-2.30%2B-3F4F75.svg?logo=plotly&logoColor=white)](https://plotly.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **InsightPulse** is an autonomous, full-stack AI Data Analyst web application. Upload any CSV or Excel file, and it instantly profiles your data, detects types, calculates statistics, detects anomalies, builds interactive Plotly dashboards, generates statistical insights, and allows you to chat with your dataset using safe, deterministic Pandas queries.

---

## 🌟 Key Features

### 1. 📁 Frictionless File Upload & Validation
* Supports `.csv`, `.xlsx`, and `.xls` files up to 50MB.
* Automatic encoding fallback (`utf-8` and `latin-1`).
* Includes **1-click bundled sample datasets** (`sales_performance.csv` and `customer_churn.xlsx`) for immediate out-of-the-box exploration.

### 2. 🔍 Automated Profiling & Data Dictionary
* **Type Inference**: Identifies numerical, categorical, date/time, and boolean columns.
* **Health Metrics**: Displays total rows, columns, memory usage, duplicate row count, and missing-value percentages.
* **Interactive Table**: Paginated preview of the first 20 rows with live keyword search filtering.

### 3. 📊 Interactive Plotly Visualizations
* **Automated Visuals**:
  * Distribution histograms with box-plot marginals for numerical features.
  * Category frequency bar charts with color scales.
  * Annotated Pearson correlation heatmaps.
  * Time-series trendlines when date columns are detected.
  * Correlation scatter plots with trendline options.
* **Custom Chart Builder**: Choose chart type (Bar, Line, Scatter, Box, Pie, Histogram), configure X/Y axes, add color groupings, and apply aggregate functions (`SUM`, `AVG`, `COUNT`, `MIN`, `MAX`).

### 4. 🧠 Hybrid AI & Statistical Insights Engine
* **100% Offline Capability**: Runs comprehensive statistical heuristics without requiring any external LLM or API keys.
* **Grounded Findings**: Pinpoints data quality issues, distribution skewness, IQR-based outliers ($1.5 \times \text{IQR}$), categorical concentrations, and timeline trends.
* **Optional LLM Integration**: Set `GEMINI_API_KEY` to enrich findings with executive summaries and business takeaways.

### 5. 💬 Safe Natural Language Q&A ("Ask Your Data")
* Chat-style interface with suggested query chips.
* Converts natural language questions directly into **parameterized Pandas operations**:
  * *"What is the average sales?"*
  * *"Which product generated the highest revenue?"*
  * *"Which month had the highest sales?"*
  * *"Are there missing values?"*
  * *"What are the top 10 customers?"*
* **Zero Arbitrary Code Execution**: No `eval()` or `exec()` is ever used, preventing prompt-injection attacks.
* Returns natural language explanations, formatted data tables, and dynamic Plotly charts inside the conversation stream.

### 6. 🧹 Preprocessing & Export
* **Interactive Data Cleaner**: Remove duplicate rows, impute numerical values (Mean, Median, Zero), and impute categorical values (Mode, "Unknown").
* **Exporting**: Download the cleaned dataset as CSV or the complete analytical report as JSON.

---

## 🛠️ Tech Stack

| Layer | Technologies |
| :--- | :--- |
| **Frontend** | React 18, Vite, Tailwind CSS, Lucide React, Plotly.js |
| **Backend** | Python 3.10+, FastAPI, Uvicorn, Pydantic |
| **Data Processing** | Pandas 2.2+, NumPy, OpenPyXL |
| **Visualizations** | Plotly Python (`plotly.express` & `plotly.graph_objects`) |
| **AI / LLM (Optional)**| Google GenAI SDK (`gemini-2.5-flash`) |

---

## 📂 Repository Structure
ai-data-analyst/ ├── backend/ │ ├── main.py # FastAPI application, routes, and CORS setup │ ├── analyzer.py # Data type inference, summary stats, IQR outlier detection │ ├── visualizer.py # Automated & custom Plotly specifications (JSON) │ ├── insights.py # Rule-based statistical engine + LLM adapter │ ├── query_engine.py # Natural language to safe Pandas query translator │ ├── data_cleaner.py # Imputation, deduplication, and cleaning pipeline │ ├── test_api.py # Automated backend integration test suite │ ├── sample_data/ # Demo datasets (sales_performance.csv, customer_churn.xlsx) │ ├── requirements.txt # Python dependencies │ └── .env.example # Optional API key configuration ├── frontend/ │ ├── src/ │ │ ├── api.js # Axios API client │ │ ├── App.jsx # Main application dashboard │ │ └── components/ │ │ ├── Sidebar.jsx # Navigation & active dataset status │ │ ├── Header.jsx # Demo loader & engine health badge │ │ ├── FileUpload.jsx # Drag-and-drop upload zone │ │ ├── MetricCards.jsx # KPI summaries & type pills │ │ ├── DataPreview.jsx # 20-row table & data dictionary │ │ ├── Statistics.jsx # Numerical & categorical stats tables │ │ ├── Visualizations.jsx # Automated charts & custom chart builder │ │ ├── AiInsights.jsx # Categorized insight cards │ │ ├── ChatInterface.jsx # Conversational Q&A stream │ │ ├── DataCleanerModal.jsx # Preprocessing & imputation modal │ │ ├── ExportModal.jsx # CSV & JSON export modal │ │ └── PlotlyChart.jsx # Plotly.js React wrapper │ ├── package.json │ ├── vite.config.js # Vite configuration with backend proxy │ └── tailwind.config.js ├── README.md └── .env.example



---
## 🚀 Quickstart Guide
### Prerequisites
* Python 3.10 or higher
* Node.js 18 or higher
* npm 9 or higher
---
### 1. Start the Backend
```bash
# Navigate to backend directory
cd backend
# Create and activate virtual environment
python -m venv venv
# On Windows:
.\venv\Scripts\Activate.ps1
# On macOS/Linux:
source venv/bin/activate
# Install dependencies
pip install -r requirements.txt
# (Optional) Configure Gemini API key for LLM-enhanced summaries
cp .env.example .env
# Run automated tests to verify setup
python test_api.py
# Start the FastAPI server
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
API URL: http://127.0.0.1:8000
Interactive API Docs (Swagger): http://127.0.0.1:8000/docs
2. Start the Frontend
In a second terminal window:

bash


# Navigate to frontend directory
cd frontend
# Install frontend dependencies
npm install
# Start the Vite development server
npm run dev
Frontend Web App: http://localhost:5173
🛡️ Security & Privacy
Strict Sandboxing: User and LLM questions are never executed via eval() or exec(). The query engine exclusively translates recognized intents into verified Pandas aggregations.
Zero External Dependencies Required: Operates completely on your local machine without sending data to third-party endpoints unless an optional Gemini key is configured.
Input Sanitization: File headers, file sizes, mime types, and query inputs are strictly validated.
🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the 
issues page
.

📝 License
Distributed under the MIT License. See LICENSE for more information.



***
### How to use this:
1. You can save this directly as `README.md` in the root of your GitHub repository.
2. In your repo description, you can use:
   > *"Autonomous full-stack AI Data Analyst web app built with React, Vite, FastAPI, Pandas, and Plotly. Upload CSV/Excel datasets for automated profiling, interactive dashboards, statistical insights, and safe conversational Q&A."*
4:06 AM
