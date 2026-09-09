import pandas as pd
from typing import Dict, List, Any
from ..ai.gemini import synthesize_executive_insights

def generate_grounded_insights(df: pd.DataFrame, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Produces deterministic statistical discoveries grounded strictly in computed facts.
    """
    insights = []
    summary = analysis.get("summary", {})
    total_rows = summary.get("total_rows", len(df)) or 1
    num_stats = {s["column"]: s for s in analysis.get("numerical_stats", [])}
    cat_stats = {s["column"]: s for s in analysis.get("categorical_stats", [])}

    # 1. Data Quality: Duplicates
    dup_rows = summary.get("duplicate_rows", 0)
    if dup_rows > 0:
        dup_pct = round((dup_rows / total_rows) * 100, 1)
        insights.append({
            "id": "dq-duplicates",
            "category": "Data Quality",
            "importance": "high" if dup_pct > 5 else "medium",
            "title": f"Duplicate Records Detected ({dup_rows:,} rows)",
            "description": f"Found {dup_rows:,} duplicate row(s) representing {dup_pct}% of the dataset. Deduplication is advised before downstream reporting.",
            "recommendation": "Launch the Data Cleaner tool to remove exact duplicate rows.",
            "type": "warning"
        })

    # 2. Data Quality: Completeness
    missing_cols = [c for c in analysis.get("column_details", []) if c["missing_count"] > 0]
    if missing_cols:
        for c in missing_cols:
            pct = c["missing_percentage"]
            if pct >= 15:
                insights.append({
                    "id": f"dq-missing-high-{c['name']}",
                    "category": "Data Quality",
                    "importance": "high",
                    "title": f"High Missingness in '{c['name']}' ({pct}%)",
                    "description": f"Column '{c['name']}' has {c['missing_count']:,} empty cells ({pct}% of total records).",
                    "recommendation": "Evaluate whether to impute values (mean/median/mode) or drop rows to avoid biased aggregations.",
                    "type": "warning"
                })
            elif pct >= 5:
                insights.append({
                    "id": f"dq-missing-mod-{c['name']}",
                    "category": "Data Quality",
                    "importance": "medium",
                    "title": f"Moderate Missingness in '{c['name']}' ({pct}%)",
                    "description": f"Column '{c['name']}' contains {c['missing_count']:,} empty cells ({pct}%).",
                    "recommendation": "Mean or median imputation can fill missing cells without distorting sample moments.",
                    "type": "info"
                })
    else:
        insights.append({
            "id": "dq-complete",
            "category": "Data Quality",
            "importance": "info",
            "title": "Complete Dataset (Zero Missing Values)",
            "description": "All records across every column contain complete values with zero null or undefined cells.",
            "recommendation": "Data completeness is optimal for immediate statistical and machine learning modeling.",
            "type": "success"
        })

    # 3. Correlations
    strong_corrs = analysis.get("strong_correlations", [])
    for sc in strong_corrs[:3]:
        r = sc["correlation"]
        rel = sc["relationship"]
        c1, c2 = sc["col1"], sc["col2"]
        dir_text = "When one increases, the other tends to increase proportionally." if r > 0 else "When one increases, the other tends to decrease inversely."

        insights.append({
            "id": f"corr-{c1}-{c2}",
            "category": "Correlations",
            "importance": "high" if abs(r) >= 0.7 else "medium",
            "title": f"{rel} Correlation: {c1} & {c2}",
            "description": f"Columns '{c1}' and '{c2}' have a Pearson correlation coefficient of {r:.2f}. {dir_text}",
            "recommendation": f"Investigate business causality or multicollinearity between '{c1}' and '{c2}'. Note: correlation does not imply causation.",
            "type": "trend"
        })

    # 4. Outliers & Skewness
    for col, stat in num_stats.items():
        outliers = stat.get("outliers_count", 0)
        outlier_pct = round((outliers / total_rows) * 100, 1)
        if outliers > 0 and outlier_pct >= 2:
            insights.append({
                "id": f"anomaly-outliers-{col}",
                "category": "Anomalies",
                "importance": "medium",
                "title": f"Distribution Outliers in '{col}' ({outliers} records)",
                "description": f"{outliers} points ({outlier_pct}% of records) fall outside the 1.5× IQR boundary. Maximum reaches {stat['max']:,} compared to median {stat['median']:,}.",
                "recommendation": f"Inspect high-magnitude records in '{col}' to verify if they reflect genuine business peaks or recording errors.",
                "type": "alert"
            })

        skew = stat.get("skewness", 0)
        if abs(skew) > 1.2:
            direction = "right-skewed (positive tail)" if skew > 0 else "left-skewed (negative tail)"
            insights.append({
                "id": f"dist-skew-{col}",
                "category": "Distribution",
                "importance": "info",
                "title": f"Distribution Skewness in '{col}'",
                "description": f"'{col}' is heavily {direction} (skewness = {skew:.2f}). The median ({stat['median']:,}) provides a more robust measure of central tendency than the mean ({stat['mean']:,}).",
                "recommendation": "Use median instead of mean when reporting central trends for this feature.",
                "type": "info"
            })

    # 5. Categorical Concentration (Pareto Principle)
    for col, stat in cat_stats.items():
        top_pct = stat.get("top_percentage", 0)
        top_val = stat.get("top_value", "")
        if top_pct >= 40 and stat.get("unique_count", 0) > 1:
            insights.append({
                "id": f"cat-dominance-{col}",
                "category": "Patterns",
                "importance": "high" if top_pct >= 60 else "medium",
                "title": f"Dominant Category in '{col}': '{top_val}'",
                "description": f"'{top_val}' represents {top_pct}% ({stat['top_frequency']:,} rows) of all records in '{col}'.",
                "recommendation": f"Assess whether operational strategy is overly dependent on segment '{top_val}'.",
                "type": "trend"
            })

    # 6. Timeline Trend
    trend = analysis.get("trend_analysis")
    if trend:
        verb = "increased" if trend["percentage_change"] > 0 else "decreased"
        insights.append({
            "id": f"trend-time-{trend['metric_column']}",
            "category": "Trends",
            "importance": "high",
            "title": f"Timeline Trend for '{trend['metric_column']}'",
            "description": f"'{trend['metric_column']}' {verb} by approximately {abs(trend['percentage_change'])}% between the early and late periods tracked across '{trend['date_column']}'.",
            "recommendation": f"Forecast trajectory for '{trend['metric_column']}' anticipating continuation of current {trend['direction']} momentum.",
            "type": "trend"
        })

    # Optional Gemini executive synthesis
    ai_insights = synthesize_executive_insights(analysis)
    return ai_insights + insights
