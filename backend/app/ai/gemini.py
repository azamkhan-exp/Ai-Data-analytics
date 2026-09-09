import os
import json
from typing import Dict, List, Any

def synthesize_executive_insights(analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Synthesizes strategic executive takeaways using Google Gemini if GEMINI_API_KEY is configured.
    Falls back gracefully to an empty list if key is missing or offline.
    """
    gemini_key = os.environ.get("GEMINI_API_KEY")
    if not gemini_key:
        return []

    summary = analysis.get("summary", {})
    kpis = analysis.get("smart_kpis", [])
    corrs = analysis.get("strong_correlations", [])[:3]
    quality = analysis.get("quality_score", {})
    anomalies = analysis.get("anomaly_summary", {})

    kpi_text = ", ".join([f"{k['label']}: {k['value']}" for k in kpis]) or "Standard enterprise dataset"
    corr_text = ", ".join([f"{c['col1']} & {c['col2']} (r={c['correlation']})" for c in corrs]) or "No high linear correlations"

    prompt = f"""You are an executive Chief Data Officer reviewing dataset metrics.
Summary: {summary.get('total_rows', 0):,} rows, {summary.get('total_columns', 0)} columns.
Data Quality Health Score: {quality.get('score', 100)}/100 ({quality.get('rating', 'Good')}).
Identified KPIs: {kpi_text}
Strong Correlations: {corr_text}
Detected Anomalies: {anomalies.get('total_anomalies', 0)} outliers across {len(anomalies.get('affected_columns', []))} columns.

Synthesize exactly 3 concise, high-value executive recommendations.
Format: return a strict JSON array of objects with keys:
[
  {{
    "category": "Executive Strategy",
    "importance": "high",
    "title": "Clear headline",
    "description": "Evidence-backed finding grounded in these exact metrics",
    "recommendation": "Actionable business recommendation",
    "type": "opportunity"
  }}
]
Return ONLY raw JSON without markdown code fences."""

    try:
        from google import genai
        client = genai.Client(api_key=gemini_key)
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        text = response.text.strip()
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        data = json.loads(text.strip())
        if isinstance(data, list):
            for i, item in enumerate(data):
                item["id"] = f"gemini-exec-{i}"
            return data
    except Exception as e:
        print(f"[Gemini AI] Optional executive synthesis bypassed: {e}")

    return []
