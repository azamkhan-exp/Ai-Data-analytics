import os
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional

def generate_rule_based_insights(df: pd.DataFrame, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Generates genuine, rich statistical insights computed directly from dataset facts.
    """
    insights = []
    summary = analysis.get("summary", {})
    total_rows = summary.get("total_rows", len(df))
    num_stats = {s["column"]: s for s in analysis.get("numerical_stats", [])}
    cat_stats = {s["column"]: s for s in analysis.get("categorical_stats", [])}
    col_types = analysis.get("column_types", {})

    # 1. Data Quality: Duplicates
    dup_rows = summary.get("duplicate_rows", 0)
    if dup_rows > 0:
        dup_pct = round((dup_rows / total_rows) * 100, 1) if total_rows > 0 else 0
        insights.append({
            "id": "dq-duplicates",
            "category": "Data Quality",
            "importance": "high" if dup_pct > 5 else "medium",
            "title": f"Duplicate Records Detected ({dup_rows} rows)",
            "description": f"Found {dup_rows:,} duplicate row(s) representing {dup_pct}% of the dataset. Consider removing duplicates before final reporting to avoid skewed metrics.",
            "type": "warning"
        })

    # 2. Data Quality: Missing Values
    missing_cols = [c for c in analysis.get("column_details", []) if c["missing_count"] > 0]
    if missing_cols:
        for c in missing_cols:
            pct = c["missing_percentage"]
            if pct >= 15:
                insights.append({
                    "id": f"dq-missing-high-{c['name']}",
                    "category": "Data Quality",
                    "importance": "high",
                    "title": f"High Missing Data in '{c['name']}' ({pct}%)",
                    "description": f"Column '{c['name']}' has {c['missing_count']:,} missing values ({pct}% of rows). Imputation or deletion strategy should be evaluated.",
                    "type": "warning"
                })
            elif pct >= 5:
                insights.append({
                    "id": f"dq-missing-mod-{c['name']}",
                    "category": "Data Quality",
                    "importance": "medium",
                    "title": f"Moderate Missing Data in '{c['name']}' ({pct}%)",
                    "description": f"Column '{c['name']}' has {c['missing_count']:,} missing entries ({pct}%).",
                    "type": "info"
                })
    else:
        insights.append({
            "id": "dq-complete",
            "category": "Data Quality",
            "importance": "info",
            "title": "Complete Dataset (Zero Missing Values)",
            "description": "All columns have 100% data completeness with zero null or empty cells detected.",
            "type": "success"
        })

    # 3. Correlation Findings
    strong_corrs = analysis.get("strong_correlations", [])
    for sc in strong_corrs[:3]:
        corr_val = sc["correlation"]
        rel = sc["relationship"]
        c1, c2 = sc["col1"], sc["col2"]
        insights.append({
            "id": f"corr-{c1}-{c2}",
            "category": "Correlations",
            "importance": "high" if abs(corr_val) >= 0.7 else "medium",
            "title": f"{rel} Correlation: {c1} & {c2}",
            "description": f"Columns '{c1}' and '{c2}' exhibit a {rel.lower()} correlation coefficient of {corr_val:.2f}. " + 
                           ("When one increases, the other tends to increase proportionally." if corr_val > 0 else "When one increases, the other tends to decrease inversely."),
            "type": "trend"
        })

    # 4. Outliers & Skewness
    for col, stat in num_stats.items():
        outliers = stat.get("outliers_count", 0)
        outlier_pct = round((outliers / total_rows) * 100, 1) if total_rows > 0 else 0
        if outliers > 0 and outlier_pct >= 2:
            insights.append({
                "id": f"anomaly-outliers-{col}",
                "category": "Anomalies",
                "importance": "medium",
                "title": f"Potential Outliers in '{col}' ({outliers} detected)",
                "description": f"{outliers} points ({outlier_pct}% of entries) fall outside 1.5× IQR boundaries for '{col}'. Maximum value reaches {stat['max']:,} compared to median of {stat['median']:,}.",
                "type": "alert"
            })
        
        # Check skewness
        skew = stat.get("skewness", 0)
        if abs(skew) > 1.2:
            direction = "right-skewed (positive tail)" if skew > 0 else "left-skewed (negative tail)"
            insights.append({
                "id": f"dist-skew-{col}",
                "category": "Distribution",
                "importance": "info",
                "title": f"Distribution Skewness in '{col}'",
                "description": f"Column '{col}' is heavily {direction} (skewness = {skew:.2f}). The mean ({stat['mean']:,}) deviates significantly from median ({stat['median']:,}).",
                "type": "info"
            })

    # 5. Categorical Concentrations
    for col, stat in cat_stats.items():
        top_pct = stat.get("top_percentage", 0)
        top_val = stat.get("top_value", "")
        if top_pct >= 40 and stat.get("unique_count", 0) > 1:
            insights.append({
                "id": f"cat-dominance-{col}",
                "category": "Patterns",
                "importance": "medium",
                "title": f"Dominant Category in '{col}': '{top_val}'",
                "description": f"'{top_val}' represents {top_pct}% ({stat['top_frequency']:,} rows) of all records in '{col}'. The column has {stat['unique_count']} distinct categories in total.",
                "type": "info"
            })

    # 6. Temporal Growth / Trends (if datetime column exists)
    datetime_cols = analysis.get("datetime_columns", [])
    numerical_cols = analysis.get("numerical_columns", [])
    if datetime_cols and numerical_cols:
        dcol = datetime_cols[0]
        mcol = numerical_cols[0]
        try:
            temp = df.copy()
            temp[dcol] = pd.to_datetime(temp[dcol], errors='coerce')
            temp = temp.dropna(subset=[dcol]).sort_values(dcol)
            if len(temp) >= 10:
                n_chunk = max(3, int(len(temp) * 0.2))
                start_val = temp.head(n_chunk)[mcol].mean()
                end_val = temp.tail(n_chunk)[mcol].mean()
                if start_val and start_val != 0:
                    pct_change = round(((end_val - start_val) / abs(start_val)) * 100, 1)
                    verb = "increased" if pct_change > 0 else "decreased"
                    insights.append({
                        "id": f"trend-time-{mcol}",
                        "category": "Trends",
                        "importance": "high",
                        "title": f"Timeline Trend for '{mcol}'",
                        "description": f"'{mcol}' {verb} by approximately {abs(pct_change)}% between the early and late stages of the analyzed period (tracking across {dcol}).",
                        "type": "trend"
                    })
        except Exception:
            pass

    return insights


def generate_llm_insights(df: pd.DataFrame, analysis: Dict[str, Any], rule_insights: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    If GEMINI_API_KEY or OPENAI_API_KEY is configured, synthesizes executive insights using LLM.
    Otherwise, returns rule-based insights.
    """
    gemini_key = os.environ.get("GEMINI_API_KEY")
    openai_key = os.environ.get("OPENAI_API_KEY")

    if not gemini_key and not openai_key:
        return rule_insights

    summary_str = f"Dataset has {analysis['summary']['total_rows']} rows and {analysis['summary']['total_columns']} columns. "
    num_summaries = [f"{s['column']} (mean={s['mean']}, median={s['median']}, min={s['min']}, max={s['max']})" for s in analysis.get("numerical_stats", [])[:5]]
    cat_summaries = [f"{s['column']} (top={s['top_value']} with {s['top_percentage']}%)" for s in analysis.get("categorical_stats", [])[:5]]
    corrs = [f"{c['col1']} and {c['col2']} (r={c['correlation']})" for c in analysis.get("strong_correlations", [])[:3]]

    prompt = f"""You are an expert AI Data Analyst. Analyze this dataset summary and produce 3-5 concise, high-value executive insights.
Summary: {summary_str}
Numerical columns: {', '.join(num_summaries)}
Categorical columns: {', '.join(cat_summaries)}
Strong Correlations: {', '.join(corrs)}

Return a valid JSON array of objects with the exact keys:
[
  {{"category": "Executive", "importance": "high", "title": "Brief title", "description": "Specific insight grounded in these numbers", "type": "trend"}}
]
Return ONLY JSON without markdown fences."""

    # Try Gemini API if key is set
    if gemini_key:
        try:
            from google import genai
            client = genai.Client(api_key=gemini_key)
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt
            )
            import json
            text = response.text.strip()
            if text.startswith("```"):
                text = text.split("```")[1]
                if text.startswith("json"):
                    text = text[4:]
            llm_insights = json.loads(text.strip())
            for idx, item in enumerate(llm_insights):
                item["id"] = f"ai-executive-{idx}"
            return llm_insights + rule_insights
        except Exception as e:
            print(f"Gemini insights generation fallback: {e}")

    return rule_insights
