import re
import json
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
import plotly.express as px

SYNONYM_MAP = {
    'product': ['sub_category', 'category', 'product_name', 'product', 'item', 'item_name'],
    'revenue': ['sales', 'total_charges', 'revenue', 'amount', 'turnover', 'income'],
    'sales': ['revenue', 'sales', 'total_sales', 'amount'],
    'profit': ['profit', 'net_profit', 'margin', 'earnings'],
    'customer': ['customer', 'customer_name', 'customer_id', 'client', 'account'],
    'region': ['region', 'territory', 'area', 'zone', 'country', 'state', 'city'],
    'discount': ['discount', 'discount_rate', 'rebate'],
    'quantity': ['quantity', 'units', 'volume', 'qty', 'count'],
    'charges': ['monthly_charges', 'total_charges', 'charges', 'cost', 'fee'],
    'tenure': ['tenure_months', 'tenure', 'months', 'duration'],
    'churn': ['churn', 'churn_rate', 'churned', 'status']
}

def fig_to_spec(fig) -> Dict[str, Any]:
    return json.loads(fig.to_json())

def extract_columns_from_query(query: str, columns: List[str]) -> List[str]:
    """Identifies mentioned columns from query string, incorporating semantic synonyms."""
    query_lower = query.lower()
    matched = []

    # Check direct name matches
    sorted_cols = sorted(columns, key=lambda c: len(c), reverse=True)
    for col in sorted_cols:
        col_clean = col.lower().replace('_', ' ')
        if col_clean in query_lower:
            matched.append(col)

    # Check semantic synonyms
    for syn_key, target_keys in SYNONYM_MAP.items():
        if re.search(rf'\b{syn_key}\w*\b', query_lower):
            for target in target_keys:
                for col in columns:
                    clean = col.lower().replace('_', ' ')
                    if target in clean and col not in matched:
                        matched.append(col)
                        break

    return matched

def format_number(val: Any) -> str:
    """Formats numeric values with standard thousand separators."""
    if pd.isna(val):
        return "N/A"
    if isinstance(val, (int, np.integer)):
        return f"{val:,}"
    if isinstance(val, (float, np.floating)):
        return f"{val:,.2f}" if abs(val) >= 1000 else f"{val:.2f}"
    return str(val)

def answer_data_question(df: pd.DataFrame, question: str, col_types: Dict[str, str]) -> Dict[str, Any]:
    """
    Interprets natural language queries using safe, deterministic Pandas operations.
    Strictly zero eval(), exec(), or arbitrary dynamic execution.
    """
    q = question.strip().lower()
    cols = list(df.columns)
    num_cols = [c for c, t in col_types.items() if t == 'numerical']
    cat_cols = [c for c, t in col_types.items() if t in ['categorical', 'text']]
    date_cols = [c for c, t in col_types.items() if t == 'datetime']

    mentioned_cols = extract_columns_from_query(q, cols)

    # 1. Missing Values Intent
    if any(w in q for w in ["missing", "null", "empty", "na values", "blanks", "completeness"]):
        if mentioned_cols:
            target_col = mentioned_cols[0]
            missing_cnt = int(df[target_col].isna().sum())
            pct = round((missing_cnt / len(df)) * 100, 2) if len(df) > 0 else 0
            answer = f"Column **'{target_col}'** has **{missing_cnt:,} missing values** ({pct}% of {len(df):,} rows)." if missing_cnt > 0 else f"Column **'{target_col}'** has **0 missing values** (100% complete)."
            return {
                "question": question,
                "answer": answer,
                "data": [{"column": target_col, "missing_count": missing_cnt, "missing_percentage": f"{pct}%"}],
                "chart": None
            }
        else:
            missing_list = []
            for c in cols:
                mc = int(df[c].isna().sum())
                if mc > 0:
                    pct = round((mc / len(df)) * 100, 2)
                    missing_list.append({"column": c, "missing_count": mc, "percentage": f"{pct}%"})

            answer = f"Found missing values across **{len(missing_list)} column(s)**:" if missing_list else "There are **zero missing values** across all columns in this dataset!"
            return {
                "question": question,
                "answer": answer,
                "data": missing_list if missing_list else [{"status": "100% complete across all columns"}],
                "chart": None
            }

    # 2. Duplicate Rows Intent
    if any(w in q for w in ["duplicate", "repeated", "copies"]):
        dup_cnt = int(df.duplicated().sum())
        pct = round((dup_cnt / len(df)) * 100, 2) if len(df) > 0 else 0
        return {
            "question": question,
            "answer": f"The dataset contains **{dup_cnt:,} duplicate rows** ({pct}% of records).",
            "data": [{"metric": "Duplicate Rows", "count": dup_cnt, "percentage": f"{pct}%"}],
            "chart": None
        }

    # 3. Dimensions / Size Intent
    if any(w in q for w in ["how many rows", "number of rows", "dataset size", "how many columns", "total records"]):
        r, c = df.shape
        return {
            "question": question,
            "answer": f"The dataset contains **{r:,} records** across **{c} columns**.",
            "data": [{"total_rows": r, "total_columns": c}],
            "chart": None
        }

    # 4. Timeline / Monthly Trend Intent
    if (("month" in q or "year" in q or "trend" in q or "over time" in q) and date_cols):
        date_col = date_cols[0]
        metric_col = next((c for c in mentioned_cols if c in num_cols), num_cols[0] if num_cols else None)

        if metric_col:
            temp = df.copy()
            temp[date_col] = pd.to_datetime(temp[date_col], errors='coerce')
            temp[metric_col] = pd.to_numeric(temp[metric_col], errors='coerce')
            temp = temp.dropna(subset=[date_col, metric_col])

            if "year" in q:
                temp['Period'] = temp[date_col].dt.year.astype(str)
                period_label = "Year"
            else:
                temp['Period'] = temp[date_col].dt.strftime('%b %Y')
                period_label = "Month"

            agg_res = temp.groupby('Period')[metric_col].sum().reset_index()
            is_lowest = any(w in q for w in ["lowest", "least", "minimum", "min", "bottom"])
            sorted_res = agg_res.sort_values(by=metric_col, ascending=is_lowest)

            if not sorted_res.empty:
                top_row = sorted_res.iloc[0]
                descriptor = "lowest" if is_lowest else "highest"
                answer = f"The {period_label.lower()} with the **{descriptor}** {metric_col} was **{top_row['Period']}** with **{format_number(top_row[metric_col])}**."

                fig = px.bar(
                    sorted_res.head(10),
                    x='Period',
                    y=metric_col,
                    title=f"{metric_col} by {period_label}",
                    color=metric_col,
                    color_continuous_scale='Blues'
                )
                fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=30, r=20, t=40, b=30))

                table_data = sorted_res.head(8).to_dict(orient='records')
                for r in table_data:
                    r[metric_col] = format_number(r[metric_col])

                return {
                    "question": question,
                    "answer": answer,
                    "data": table_data,
                    "chart": fig_to_spec(fig)
                }

    # 5. Top N / Lowest Group Aggregation Intent
    top_match = re.search(r'\btop\s+(\d+)\b', q)
    limit = int(top_match.group(1)) if top_match else (5 if any(w in q for w in ["which", "highest", "most", "lowest"]) else 10)
    is_grouping = any(w in q for w in ["which", "top", "highest", "best", "lowest", "least", "worst", "by", "per"])

    if is_grouping and cat_cols and num_cols:
        group_col = next((c for c in mentioned_cols if c in cat_cols), cat_cols[0])
        metric_col = next((c for c in mentioned_cols if c in num_cols), num_cols[0])

        agg_func = 'mean' if any(w in q for w in ["average", "avg", "mean"]) else 'sum'
        ascending = any(w in q for w in ["lowest", "least", "bottom", "worst"])

        temp = df.copy()
        temp[metric_col] = pd.to_numeric(temp[metric_col], errors='coerce')
        grouped = temp.groupby(group_col)[metric_col].agg(agg_func).reset_index()
        grouped = grouped.sort_values(by=metric_col, ascending=ascending).dropna().head(limit)

        if not grouped.empty:
            leader = grouped.iloc[0]
            val_str = format_number(leader[metric_col])
            adj = "lowest" if ascending else "highest"
            answer = f"The **{group_col}** with the **{adj}** {agg_func} {metric_col} is **'{leader[group_col]}'** with **{val_str}**."

            fig = px.bar(
                grouped,
                x=group_col,
                y=metric_col,
                title=f"{agg_func.capitalize()} {metric_col} by {group_col}",
                color=metric_col,
                color_continuous_scale='Teal' if not ascending else 'Reds'
            )
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=30, r=20, t=40, b=30))

            table_data = grouped.to_dict(orient='records')
            for r in table_data:
                r[metric_col] = format_number(r[metric_col])

            return {
                "question": question,
                "answer": answer,
                "data": table_data,
                "chart": fig_to_spec(fig)
            }

    # 6. Direct Metric Aggregation Intent
    metric_col = next((c for c in mentioned_cols if c in num_cols), num_cols[0] if num_cols else None)
    if metric_col:
        series = pd.to_numeric(df[metric_col], errors='coerce').dropna()
        if not series.empty:
            if any(w in q for w in ["average", "mean", "avg"]):
                avg_val = float(series.mean())
                return {
                    "question": question,
                    "answer": f"The **average {metric_col}** is **{format_number(avg_val)}** (Min: {format_number(series.min())}, Max: {format_number(series.max())}).",
                    "data": [{
                        "metric": f"Average {metric_col}",
                        "mean": format_number(avg_val),
                        "median": format_number(series.median()),
                        "std_dev": format_number(series.std()),
                        "records": len(series)
                    }],
                    "chart": None
                }
            elif any(w in q for w in ["total", "sum", "overall"]):
                sum_val = float(series.sum())
                return {
                    "question": question,
                    "answer": f"The **total {metric_col}** is **{format_number(sum_val)}** across {len(series):,} records.",
                    "data": [{"metric": f"Total {metric_col}", "total": format_number(sum_val), "records": len(series)}],
                    "chart": None
                }
            elif any(w in q for w in ["max", "maximum", "highest"]):
                max_val = float(series.max())
                return {
                    "question": question,
                    "answer": f"The **maximum {metric_col}** recorded is **{format_number(max_val)}**.",
                    "data": [{"metric": f"Max {metric_col}", "max": format_number(max_val)}],
                    "chart": None
                }
            elif any(w in q for w in ["min", "minimum", "lowest"]):
                min_val = float(series.min())
                return {
                    "question": question,
                    "answer": f"The **minimum {metric_col}** recorded is **{format_number(min_val)}**.",
                    "data": [{"metric": f"Min {metric_col}", "min": format_number(min_val)}],
                    "chart": None
                }

    # 7. Correlation Inquiries
    if any(w in q for w in ["correlation", "correlate", "relationship"]):
        if len(num_cols) >= 2:
            c1, c2 = (mentioned_cols[:2] if len(mentioned_cols) >= 2 else (num_cols[0], num_cols[1]))
            sub_df = df[[c1, c2]].apply(pd.to_numeric, errors='coerce').dropna()
            r_val = float(sub_df.corr().iloc[0, 1]) if len(sub_df) > 2 else 0.0
            return {
                "question": question,
                "answer": f"The Pearson correlation coefficient between **'{c1}'** and **'{c2}'** is **{r_val:.3f}**.",
                "data": [{"column_1": c1, "column_2": c2, "correlation": round(r_val, 3)}],
                "chart": None
            }

    # Fallback with guided questions
    suggestions = []
    if num_cols:
        suggestions.append(f"What is the average {num_cols[0]}?")
    if cat_cols and num_cols:
        suggestions.append(f"Which {cat_cols[0]} has the highest {num_cols[0]}?")
    if date_cols:
        suggestions.append("Which month had the highest sales?")
    suggestions.append("Are there missing values in the dataset?")

    return {
        "question": question,
        "answer": f"I analyzed your question regarding '{question}', but need a bit more context. Try asking one of these guided questions:",
        "data": [{"hint": "Select a guided question below"}],
        "suggestions": suggestions[:4],
        "chart": None
    }
