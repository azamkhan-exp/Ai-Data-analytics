import pandas as pd
import numpy as np
from typing import Dict, List, Any

def compute_correlation_matrix(df: pd.DataFrame, numerical_cols: List[str]) -> TupleDict:
    """
    Computes full Pearson correlation matrix and ranks strongest inter-variable correlations.
    """
    if len(numerical_cols) < 2:
        return {"columns": numerical_cols, "values": []}, []

    num_df = df[numerical_cols].apply(pd.to_numeric, errors='coerce')
    corr_df = num_df.corr(method='pearson').round(3)

    matrix = {
        "columns": numerical_cols,
        "values": corr_df.fillna(0.0).values.tolist()
    }

    ranked_correlations = []
    n = len(numerical_cols)

    for i in range(n):
        for j in range(i + 1, n):
            col_a, col_b = numerical_cols[i], numerical_cols[j]
            r_val = corr_df.iloc[i, j]

            if pd.notna(r_val):
                abs_r = abs(r_val)
                if abs_r >= 0.35:
                    if abs_r >= 0.70:
                        strength = "Strong"
                    elif abs_r >= 0.50:
                        strength = "Moderate"
                    else:
                        strength = "Weak-to-Moderate"

                    direction = "Positive" if r_val > 0 else "Negative"
                    rel_label = f"{strength} {direction}"

                    ranked_correlations.append({
                        "col1": col_a,
                        "col2": col_b,
                        "column_a": col_a,
                        "column_b": col_b,
                        "correlation": round(float(r_val), 3),
                        "strength": strength.lower(),
                        "direction": direction.lower(),
                        "relationship": rel_label,
                        "disclaimer": "Correlation reflects statistical association and does not imply causation."
                    })

    ranked_correlations.sort(key=lambda x: abs(x["correlation"]), reverse=True)
    return matrix, ranked_correlations

TupleDict = Any
