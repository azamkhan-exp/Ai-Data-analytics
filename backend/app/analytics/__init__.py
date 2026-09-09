import pandas as pd
from typing import Dict, Any

from .profiler import profile_dataset, detect_column_types, detect_column_roles
from .statistics import compute_numerical_statistics, compute_categorical_statistics
from .correlations import compute_correlation_matrix
from .anomalies import detect_anomalies
from .trends import analyze_temporal_trends
from .data_quality import calculate_data_quality_score
from .kpis import detect_smart_kpis
from .insights import generate_grounded_insights

def run_full_analysis(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Executes end-to-end deterministic Python statistical profiling across the entire dataset.
    """
    # 1. Base Profiling & Type Inference
    profile = profile_dataset(df)
    summary = profile["summary"]
    col_types = profile["column_types"]
    col_roles = profile["column_roles"]
    numerical_cols = profile["numerical_columns"]
    categorical_cols = profile["categorical_columns"]
    datetime_cols = profile["datetime_columns"]

    # 2. Descriptive Moments (SciPy + Pandas)
    numerical_stats = compute_numerical_statistics(df, numerical_cols)
    categorical_stats = compute_categorical_statistics(df, categorical_cols)

    # 3. Pearson Correlation Matrix
    corr_matrix, strong_corrs = compute_correlation_matrix(df, numerical_cols)

    # 4. Outlier & Anomaly Detection (IQR + Z-score + IsolationForest)
    anomaly_summary = detect_anomalies(df, numerical_cols)

    # 5. Chronological Trends
    trend_analysis = analyze_temporal_trends(df, datetime_cols, numerical_cols)

    # 6. Data Quality Score (0-100)
    quality_score = calculate_data_quality_score(df, summary, col_types)

    # 7. Smart Business KPIs
    smart_kpis = detect_smart_kpis(df, numerical_stats)

    analysis_result = {
        "summary": summary,
        "quality_score": quality_score,
        "smart_kpis": smart_kpis,
        "anomaly_summary": anomaly_summary,
        "trend_analysis": trend_analysis,
        "column_types": col_types,
        "column_roles": col_roles,
        "column_details": profile["column_details"],
        "preview_rows": profile["preview_rows"],
        "numerical_stats": numerical_stats,
        "categorical_stats": categorical_stats,
        "correlation_matrix": corr_matrix,
        "strong_correlations": strong_corrs,
        "numerical_columns": numerical_cols,
        "categorical_columns": categorical_cols,
        "datetime_columns": datetime_cols
    }

    # 8. Grounded Business Insights
    insights = generate_grounded_insights(df, analysis_result)
    analysis_result["insights"] = insights

    return analysis_result

__all__ = [
    "run_full_analysis",
    "profile_dataset",
    "detect_column_types",
    "detect_column_roles",
    "compute_numerical_statistics",
    "compute_categorical_statistics",
    "compute_correlation_matrix",
    "detect_anomalies",
    "analyze_temporal_trends",
    "calculate_data_quality_score",
    "detect_smart_kpis",
    "generate_grounded_insights",
]
