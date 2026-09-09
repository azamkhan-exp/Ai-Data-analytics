import os
import sys
import unittest
import pandas as pd
import numpy as np

# Ensure backend package is in python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.data.validators import validate_uploaded_file
from app.data.loader import load_dataframe_from_file
from app.data.cleaner import clean_dataset
from app.analytics.profiler import profile_dataset, detect_column_types, detect_column_roles
from app.analytics.statistics import compute_numerical_statistics, compute_categorical_statistics
from app.analytics.correlations import compute_correlation_matrix
from app.analytics.anomalies import detect_anomalies
from app.analytics.trends import analyze_temporal_trends
from app.analytics.data_quality import calculate_data_quality_score
from app.analytics.kpis import detect_smart_kpis
from app.analytics.insights import generate_grounded_insights
from app.analytics.query_engine import answer_data_question
from app.analytics import run_full_analysis

SAMPLE_DIR = os.path.join(os.path.dirname(__file__), "sample_data")
SALES_CSV = os.path.join(SAMPLE_DIR, "sales_performance.csv")
CHURN_XLSX = os.path.join(SAMPLE_DIR, "customer_churn.xlsx")

class TestPythonAnalyticsEngine(unittest.TestCase):

    def setUp(self):
        self.sales_df = load_dataframe_from_file(SALES_CSV)
        self.churn_df = load_dataframe_from_file(CHURN_XLSX)

    def test_data_loader(self):
        self.assertEqual(len(self.sales_df), 50)
        self.assertEqual(len(self.sales_df.columns), 10)
        self.assertIn("Sales", self.sales_df.columns)
        self.assertIn("Profit", self.sales_df.columns)

        self.assertEqual(len(self.churn_df), 40)
        self.assertEqual(len(self.churn_df.columns), 9)
        self.assertIn("Monthly_Charges", self.churn_df.columns)
        self.assertIn("Churn", self.churn_df.columns)

    def test_file_validator(self):
        ext = validate_uploaded_file("data.csv", 1024)
        self.assertEqual(ext, "csv")
        ext_xlsx = validate_uploaded_file("report.XLSX", 2048)
        self.assertEqual(ext_xlsx, "xlsx")

    def test_profiler_and_types(self):
        col_types = detect_column_types(self.sales_df)
        self.assertEqual(col_types["Sales"], "numerical")
        self.assertEqual(col_types["Profit"], "numerical")
        self.assertEqual(col_types["Category"], "categorical")
        self.assertEqual(col_types["Date"], "datetime")

        profile = profile_dataset(self.sales_df)
        self.assertEqual(profile["summary"]["total_rows"], 50)
        self.assertEqual(profile["summary"]["total_columns"], 10)
        self.assertEqual(len(profile["preview_rows"]), 20)

    def test_statistics_moments(self):
        num_stats = compute_numerical_statistics(self.sales_df, ["Sales", "Profit", "Discount"])
        stats_map = {s["column"]: s for s in num_stats}

        sales_stat = stats_map["Sales"]
        self.assertGreater(sales_stat["mean"], 0)
        self.assertGreater(sales_stat["median"], 0)
        self.assertGreater(sales_stat["variance"], 0)
        self.assertIn("skewness", sales_stat)
        self.assertIn("kurtosis", sales_stat)
        self.assertIn("iqr", sales_stat)

    def test_correlations(self):
        matrix, ranked = compute_correlation_matrix(self.sales_df, ["Sales", "Profit", "Quantity", "Discount"])
        self.assertEqual(len(matrix["columns"]), 4)
        self.assertTrue(len(ranked) > 0)
        # Sales and Profit should have a strong positive correlation
        top_corr = ranked[0]
        self.assertTrue(abs(top_corr["correlation"]) > 0.5)

    def test_anomaly_detection(self):
        anomalies = detect_anomalies(self.sales_df, ["Sales", "Profit"])
        self.assertIn("total_anomalies", anomalies)
        self.assertIn("affected_columns", anomalies)
        self.assertIn("affected_rows_count", anomalies)
        self.assertIn("anomaly_percentage", anomalies)

    def test_temporal_trends(self):
        trend = analyze_temporal_trends(self.sales_df, ["Date"], ["Sales"])
        self.assertIsNotNone(trend)
        self.assertIn("percentage_change", trend)
        self.assertIn("direction", trend)

    def test_data_quality_score(self):
        profile = profile_dataset(self.sales_df)
        quality = calculate_data_quality_score(self.sales_df, profile["summary"], profile["column_types"])
        self.assertGreaterEqual(quality["score"], 10)
        self.assertLessEqual(quality["score"], 100)
        self.assertIn("rating", quality)

    def test_smart_kpis(self):
        num_stats = compute_numerical_statistics(self.sales_df, ["Sales", "Profit", "Discount"])
        kpis = detect_smart_kpis(self.sales_df, num_stats)
        self.assertTrue(len(kpis) >= 2)
        labels = [k["label"] for k in kpis]
        self.assertTrue(any("Revenue" in l or "Sales" in l for l in labels))

    def test_grounded_insights(self):
        analysis = run_full_analysis(self.sales_df)
        self.assertIn("insights", analysis)
        self.assertTrue(len(analysis["insights"]) >= 3)
        categories = set(i["category"] for i in analysis["insights"])
        self.assertTrue(len(categories) >= 2)

    def test_natural_language_query_engine(self):
        col_types = detect_column_types(self.sales_df)

        # 1. Average Sales query
        res1 = answer_data_question(self.sales_df, "What is the average sales?", col_types)
        self.assertIn("average", res1["answer"].lower())
        self.assertIsNotNone(res1["data"])

        # 2. Highest sales category query
        res2 = answer_data_question(self.sales_df, "Which Category has the highest Sales?", col_types)
        self.assertIn("highest", res2["answer"].lower())
        self.assertIsNotNone(res2["chart"])

        # 3. Missing values query
        res3 = answer_data_question(self.sales_df, "Are there missing values?", col_types)
        self.assertIn("missing", res3["answer"].lower())

    def test_data_cleaner(self):
        cleaned, log = clean_dataset(
            self.sales_df,
            drop_duplicates=True,
            fill_missing_numerical="mean",
            trim_strings=True
        )
        self.assertEqual(len(cleaned), len(self.sales_df))
        self.assertIsInstance(log, list)

    def test_fastapi_endpoints(self):
        import asyncio
        from httpx import AsyncClient, ASGITransport
        from app.main import app

        async def run_endpoint_tests():
            transport = ASGITransport(app=app)
            async with AsyncClient(transport=transport, base_url="http://test") as client:
                # 1. Health check
                res = await client.get("/api/health")
                self.assertEqual(res.status_code, 200)
                data = res.json()
                self.assertEqual(data["status"], "ok")
                self.assertEqual(data["database"], False)

                # 2. Samples list
                res = await client.get("/api/samples")
                self.assertEqual(res.status_code, 200)
                samples = res.json()["samples"]
                self.assertTrue(len(samples) >= 1)

                # 3. Load sample
                res = await client.post("/api/samples/load?name=sales_performance.csv")
                self.assertEqual(res.status_code, 200)
                dataset_id = res.json()["dataset_id"]

                # 4. Get analysis
                res = await client.get(f"/api/analysis/{dataset_id}")
                self.assertEqual(res.status_code, 200)

                # 5. Get visualizations
                res = await client.get(f"/api/visualizations/{dataset_id}")
                self.assertEqual(res.status_code, 200)

                # 6. Ask question
                res = await client.post(f"/api/query/{dataset_id}", json={"question": "What is total sales?"})
                self.assertEqual(res.status_code, 200)
                self.assertIn("total", res.json()["answer"].lower())

                # 7. Clean dataset
                res = await client.post(f"/api/clean/{dataset_id}", json={"drop_duplicates": True})
                self.assertEqual(res.status_code, 200)

                # 8. Export dataset
                res = await client.get(f"/api/export/{dataset_id}?format=csv")
                self.assertEqual(res.status_code, 200)
                self.assertIn("text/csv", res.headers.get("content-type", ""))

                res = await client.get(f"/api/export/{dataset_id}?format=json")
                self.assertEqual(res.status_code, 200)

        asyncio.run(run_endpoint_tests())

if __name__ == "__main__":
    unittest.main()
