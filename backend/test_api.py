import os
import pandas as pd
from analyzer import analyze_dataset
from visualizer import generate_automatic_visualizations, generate_custom_chart
from insights import generate_rule_based_insights
from query_engine import answer_data_question
from data_cleaner import clean_dataset
from fastapi.testclient import TestClient
from main import app

def run_tests():
    print("=== 1. Testing Analyzer ===")
    sample_csv = os.path.join(os.path.dirname(__file__), "sample_data", "sales_performance.csv")
    df = pd.read_csv(sample_csv)
    analysis = analyze_dataset(df)
    
    assert analysis["summary"]["total_rows"] == 50, f"Expected 50 rows, got {analysis['summary']['total_rows']}"
    assert analysis["summary"]["total_columns"] == 10, f"Expected 10 cols, got {analysis['summary']['total_columns']}"
    assert "Sales" in analysis["numerical_columns"], "Sales should be detected as numerical"
    assert "Category" in analysis["categorical_columns"], "Category should be detected as categorical"
    assert "Date" in analysis["datetime_columns"], "Date should be detected as datetime"
    print(f"[PASS] Analyzer correctly identified {len(analysis['numerical_columns'])} num, {len(analysis['categorical_columns'])} cat, {len(analysis['datetime_columns'])} date cols.")

    print("\n=== 2. Testing Rule-Based Insights ===")
    insights = generate_rule_based_insights(df, analysis)
    assert len(insights) > 0, "Should generate at least one insight"
    for ins in insights:
        print(f"  - [{ins['category']}] {ins['title']}: {ins['description'][:80]}...")
    print(f"[PASS] Generated {len(insights)} statistical insights.")

    print("\n=== 3. Testing Visualizer ===")
    visuals = generate_automatic_visualizations(df, analysis["column_types"], analysis["strong_correlations"])
    assert "histograms" in visuals and len(visuals["histograms"]) > 0
    assert "bar_charts" in visuals and len(visuals["bar_charts"]) > 0
    assert "correlation_heatmap" in visuals
    assert "time_series" in visuals
    print(f"[PASS] Generated automatic Plotly charts: {list(visuals.keys())}")

    print("\n=== 4. Testing Query Engine ===")
    test_questions = [
        "What is the average sales?",
        "Which product generated the highest revenue?",
        "Which month had the highest sales?",
        "Are there missing values?",
        "What are the top 10 customers?"
    ]
    for q in test_questions:
        ans = answer_data_question(df, q, analysis["column_types"])
        print(f"  Q: '{q}'")
        print(f"  A: {ans['answer']}")
        assert ans["answer"] is not None and len(ans["answer"]) > 0
    print("[PASS] All sample questions answered successfully.")

    print("\n=== 5. Testing Data Cleaner ===")
    cleaned_df, log = clean_dataset(df, drop_duplicates=True)
    assert len(cleaned_df) <= len(df)
    print(f"[PASS] Data cleaner finished. Changes: {log or 'No duplicates to drop.'}")

    print("\n=== 6. Testing FastAPI Endpoints with TestClient ===")
    client = TestClient(app)
    
    # Health
    r_health = client.get("/api/health")
    assert r_health.status_code == 200
    print("  - GET /api/health: OK")

    # Samples
    r_samples = client.get("/api/samples")
    assert r_samples.status_code == 200
    print(f"  - GET /api/samples: {len(r_samples.json()['samples'])} sample(s) available")

    # Load sample
    r_load = client.post("/api/samples/load?name=sales_performance.csv")
    assert r_load.status_code == 200
    ds_id = r_load.json()["dataset_id"]
    print(f"  - POST /api/samples/load: loaded with ID {ds_id}")

    # Analysis
    r_analysis = client.get(f"/api/analysis/{ds_id}")
    assert r_analysis.status_code == 200
    print("  - GET /api/analysis/{id}: OK")

    # Visualizations
    r_vis = client.get(f"/api/visualizations/{ds_id}")
    assert r_vis.status_code == 200
    print("  - GET /api/visualizations/{id}: OK")

    # Insights
    r_ins = client.get(f"/api/insights/{ds_id}")
    assert r_ins.status_code == 200
    print("  - GET /api/insights/{id}: OK")

    # Query
    r_q = client.post(f"/api/query/{ds_id}", json={"question": "What is the average sales?"})
    assert r_q.status_code == 200
    assert "average" in r_q.json()["answer"].lower()
    print("  - POST /api/query/{id}: OK")

    # Export CSV
    r_export = client.get(f"/api/export/{ds_id}?format=csv")
    assert r_export.status_code == 200
    assert "text/csv" in r_export.headers.get("content-type", "")
    print("  - GET /api/export/{id}?format=csv: OK")

    print("\nALL BACKEND TESTS PASSED SUCCESSFULLY! [OK]")

if __name__ == "__main__":
    run_tests()
