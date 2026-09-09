import pandas as pd
from typing import Dict, List, Any

def calculate_data_quality_score(df: pd.DataFrame, summary: Dict[str, Any], col_types: Dict[str, str]) -> Dict[str, Any]:
    """
    Computes a deterministic 0–100 Data Quality Health Score based on completeness,
    duplicate rates, zero-variance columns, and cardinality entropy.
    """
    score = 100
    issues = []
    recommendations = []
    total_rows = summary.get("total_rows", len(df)) or 1

    # 1. Missing Values Deduction (up to -25 pts)
    missing_pct = summary.get("overall_missing_percentage", 0.0)
    if missing_pct > 0:
        deduction = min(25, max(2, int(missing_pct * 0.8)))
        score -= deduction
        issues.append({
            "title": f"{missing_pct}% Overall Missing Values",
            "description": f"{summary.get('overall_missing_cells', 0):,} empty or unpopulated cells detected across records.",
            "deduction": f"-{deduction} pts"
        })
        recommendations.append("Execute mean/median imputation for numericals or mode for categoricals to restore completeness.")

    # 2. Duplicate Rows Deduction (up to -20 pts)
    dup_rows = summary.get("duplicate_rows", 0)
    if dup_rows > 0:
        dup_pct = (dup_rows / total_rows) * 100
        deduction = min(20, max(2, int(dup_pct * 1.5) + 2))
        score -= deduction
        issues.append({
            "title": f"{dup_rows:,} Duplicate Row(s) Detected",
            "description": f"{dup_pct:.1f}% of records are exact duplicates across all columns.",
            "deduction": f"-{deduction} pts"
        })
        recommendations.append("Run deduplication in the Data Cleaner tool to ensure non-redundant metrics.")

    # 3. Constant Columns Deduction (-5 pts per column, max -15 pts)
    constant_cols = []
    for col in df.columns:
        non_null_vals = df[col].dropna()
        if not non_null_vals.empty and non_null_vals.nunique() == 1:
            constant_cols.append(col)

    if constant_cols:
        deduction = min(15, len(constant_cols) * 5)
        score -= deduction
        issues.append({
            "title": f"Zero-Variance Column(s): {', '.join(constant_cols)}",
            "description": "Columns containing a single constant value provide no analytical signal.",
            "deduction": f"-{deduction} pts"
        })
        recommendations.append(f"Consider dropping constant columns ({', '.join(constant_cols)}) to reduce noise.")

    # 4. High-Cardinality Categorical Warning (-5 pts)
    high_card_cols = []
    for col in df.columns:
        if col_types.get(col) == 'categorical' and not col.lower().endswith(('id', 'code', 'key')):
            non_null = df[col].dropna()
            u_count = non_null.nunique()
            if u_count > 100 and (u_count / total_rows) > 0.6:
                high_card_cols.append(col)

    if high_card_cols:
        score -= 5
        issues.append({
            "title": f"High Cardinality Categoricals: {', '.join(high_card_cols)}",
            "description": "Columns have high distinct values relative to dataset size and may function as free text.",
            "deduction": "-5 pts"
        })

    # Bounded [10, 100]
    score = max(10, min(100, int(score)))

    if score >= 90:
        rating = "Excellent"
        badge_color = "emerald"
    elif score >= 75:
        rating = "Good Quality"
        badge_color = "blue"
    elif score >= 50:
        rating = "Moderate Quality"
        badge_color = "amber"
    else:
        rating = "Needs Immediate Attention"
        badge_color = "rose"

    if not recommendations:
        recommendations.append("Dataset structure satisfies all high-integrity data hygiene standards.")

    return {
        "score": score,
        "rating": rating,
        "badge_color": badge_color,
        "issues": issues,
        "recommendations": recommendations,
        "constant_columns": constant_cols
    }
