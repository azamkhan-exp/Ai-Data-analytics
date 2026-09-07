import re
import os
import json
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
import plotly.express as px

def fig_to_spec(fig) -> Dict[str, Any]:
    """Safely converts Plotly figure to standard JSON dict."""
    return json.loads(fig.to_json())

def find_best_column_match(token: str, columns: List[str]) -> Optional[str]:
    """Finds exact or fuzzy column match for a token or phrase."""
    token_clean = re.sub(r'[^a-zA-Z0-9]', '', token.lower())
    if not token_clean:
        return None
        
    for col in columns:
        col_clean = re.sub(r'[^a-zA-Z0-9]', '', col.lower())
        if token_clean == col_clean:
            return col
    
    # Substring match
    for col in columns:
        col_clean = re.sub(r'[^a-zA-Z0-9]', '', col.lower())
        if token_clean in col_clean or col_clean in token_clean:
            return col
            
    return None

SYNONYM_MAP = {
    'product': ['sub_category', 'category', 'product_name', 'product', 'item', 'item_name'],
    'revenue': ['sales', 'total_charges', 'revenue', 'amount', 'turnover', 'income'],
    'sales': ['revenue', 'sales', 'total_sales', 'amount'],
    'profit': ['profit', 'net_profit', 'margin', 'earnings'],
    'customer': ['customer', 'customer_name', 'customer_id', 'client', 'account'],
    'region': ['region', 'territory', 'area', 'zone', 'country', 'state', 'city'],
    'discount': ['discount', 'discount_rate', 'rebate'],
    'quantity': ['quantity', 'units', 'volume', 'qty', 'count']
}

def extract_columns_from_query(query: str, columns: List[str]) -> List[str]:
    """Identifies mentioned columns from query string, including semantic synonyms."""
    query_lower = query.lower()
    matched = []
    
    # Check multi-word columns first, then single word
    sorted_cols = sorted(columns, key=lambda c: len(c), reverse=True)
    for col in sorted_cols:
        col_lower = col.lower().replace('_', ' ')
        if col_lower in query_lower:
            matched.append(col)
        else:
            words = re.findall(r'\b\w+\b', col.lower())
            for w in words:
                if len(w) > 3 and re.search(rf'\b{w}\b', query_lower):
                    if col not in matched:
                        matched.append(col)
                    break

    # If no direct matches, check synonyms
    cols_by_clean = {re.sub(r'[^a-zA-Z0-9]', '', c.lower()): c for c in columns}
    for syn_key, target_keys in SYNONYM_MAP.items():
        if re.search(rf'\b{syn_key}\w*\b', query_lower):
            for target in target_keys:
                for clean_name, orig_col in cols_by_clean.items():
                    if target in clean_name and orig_col not in matched:
                        matched.append(orig_col)
                        break
                if any(m in [cols_by_clean.get(t) for t in target_keys if t in cols_by_clean] for m in matched):
                    break

    return matched

def format_number(val: Any) -> str:
    """Formats float or integer nicely."""
    if pd.isna(val):
        return "N/A"
    if isinstance(val, (int, np.integer)):
        return f"{val:,}"
    if isinstance(val, (float, np.floating)):
        if abs(val) >= 1000:
            return f"{val:,.2f}"
        return f"{val:.2f}"
    return str(val)

def answer_data_question(df: pd.DataFrame, question: str, col_types: Dict[str, str]) -> Dict[str, Any]:
    """
    Safely interprets user questions and computes answers using parameterized Pandas operations.
    Guaranteed zero execution of arbitrary code (no eval/exec).
    """
    q = question.strip().lower()
    cols = list(df.columns)
    num_cols = [c for c, t in col_types.items() if t == 'numerical']
    cat_cols = [c for c, t in col_types.items() if t in ['categorical', 'text']]
    date_cols = [c for c, t in col_types.items() if t == 'datetime']

    mentioned_cols = extract_columns_from_query(q, cols)

    # 1. Check Missing Values intent
    if any(w in q for w in ["missing", "null", "empty", "na values", "blanks"]):
        if mentioned_cols:
            target_col = mentioned_cols[0]
            missing_cnt = int(df[target_col].isna().sum())
            pct = round((missing_cnt / len(df)) * 100, 2) if len(df) > 0 else 0
            if missing_cnt == 0:
                answer_text = f"Column **'{target_col}'** has **0 missing values** (100% complete)."
            else:
                answer_text = f"Column **'{target_col}'** has **{missing_cnt:,} missing values** ({pct}% of the {len(df):,} total rows)."
            return {
                "question": question,
                "answer": answer_text,
                "data": [{"column": target_col, "missing_count": missing_cnt, "missing_percentage": f"{pct}%"}],
                "chart": None
            }
        else:
            missing_data = []
            for col in cols:
                mc = int(df[col].isna().sum())
                if mc > 0:
                    pct = round((mc / len(df)) * 100, 2)
                    missing_data.append({"column": col, "missing_count": mc, "percentage": f"{pct}%"})
            
            if not missing_data:
                answer_text = "There are **zero missing values** across all columns in this dataset!"
            else:
                answer_text = f"Found missing values in **{len(missing_data)} column(s)**. Here is the breakdown:"
            
            return {
                "question": question,
                "answer": answer_text,
                "data": missing_data if missing_data else [{"status": "Zero missing values"}],
                "chart": None
            }

    # 2. Check Duplicates intent
    if any(w in q for w in ["duplicate", "repeated", "copies"]):
        dup_cnt = int(df.duplicated().sum())
        pct = round((dup_cnt / len(df)) * 100, 2) if len(df) > 0 else 0
        answer_text = f"The dataset contains **{dup_cnt:,} duplicate rows** ({pct}% of all records)."
        return {
            "question": question,
            "answer": answer_text,
            "data": [{"metric": "Duplicate Rows", "count": dup_cnt, "percentage": f"{pct}%"}],
            "chart": None
        }

    # 3. Check Row count / Column count / Dimensions
    if any(w in q for w in ["how many rows", "number of rows", "dataset size", "how many columns", "total records"]):
        rows, cols_cnt = df.shape
        answer_text = f"The dataset contains **{rows:,} rows** and **{cols_cnt} columns**."
        return {
            "question": question,
            "answer": answer_text,
            "data": [{"rows": rows, "columns": cols_cnt}],
            "chart": None
        }

    # 4. Check Date / Monthly Aggregation ("Which month had highest sales?", etc.)
    if (("month" in q or "year" in q or "quarter" in q) and date_cols) or ("over time" in q and date_cols):
        date_col = date_cols[0]
        # Pick metric column: either mentioned or first numerical
        metric_col = next((c for c in mentioned_cols if c in num_cols), num_cols[0] if num_cols else None)
        if metric_col:
            temp_df = df.copy()
            temp_df[date_col] = pd.to_datetime(temp_df[date_col], errors='coerce')
            temp_df = temp_df.dropna(subset=[date_col])
            
            if "year" in q:
                temp_df['Period'] = temp_df[date_col].dt.year.astype(str)
                period_name = "Year"
            else:
                temp_df['Period'] = temp_df[date_col].dt.strftime('%B %Y')
                period_name = "Month"
            
            agg_result = temp_df.groupby('Period')[metric_col].sum().reset_index()
            # Sort chronologically or by value
            is_highest = any(w in q for w in ["highest", "top", "most", "peak", "maximum", "max"])
            is_lowest = any(w in q for w in ["lowest", "least", "minimum", "min"])
            
            if is_lowest:
                sorted_res = agg_result.sort_values(by=metric_col, ascending=True)
                top_period = sorted_res.iloc[0]
                answer_text = f"The {period_name.lower()} with the lowest total **{metric_col}** was **{top_period['Period']}** with **{format_number(top_period[metric_col])}**."
            else:
                sorted_res = agg_result.sort_values(by=metric_col, ascending=False)
                top_period = sorted_res.iloc[0]
                answer_text = f"The {period_name.lower()} with the highest total **{metric_col}** was **{top_period['Period']}** with **{format_number(top_period[metric_col])}**."
                
            fig = px.bar(
                sorted_res.head(12),
                x='Period',
                y=metric_col,
                title=f"{metric_col} by {period_name}",
                color=metric_col,
                color_continuous_scale='Viridis'
            )
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=30, r=20, t=40, b=30))
            
            # format table
            table_data = sorted_res.head(10).to_dict(orient='records')
            for r in table_data:
                r[metric_col] = format_number(r[metric_col])
                
            return {
                "question": question,
                "answer": answer_text,
                "data": table_data,
                "chart": fig_to_spec(fig)
            }

    # 5. Check "Top N" / "Highest" / "Lowest" group aggregation
    # e.g. "Which product generated the highest revenue?", "What are the top 10 customers?"
    top_match = re.search(r'\btop\s+(\d+)\b', q)
    limit = int(top_match.group(1)) if top_match else (5 if any(w in q for w in ["which", "highest", "most", "lowest", "least"]) else 10)
    
    is_grouping = any(w in q for w in ["which", "top", "highest", "best", "lowest", "least", "worst", "by", "per", "grouped by"])
    if is_grouping and (cat_cols or len(cols) > 1):
        # Identify group column
        group_col = None
        for c in mentioned_cols:
            if c in cat_cols:
                group_col = c
                break
        if not group_col:
            for c in cat_cols:
                # Check singular or plural form
                singular = c.lower().rstrip('s')
                if singular in q or c.lower() in q:
                    group_col = c
                    break
        if not group_col and cat_cols:
            group_col = cat_cols[0]

        # Identify metric column
        metric_col = None
        for c in mentioned_cols:
            if c in num_cols:
                metric_col = c
                break
        if not metric_col and num_cols:
            metric_col = num_cols[0]

        # Identify aggregation function
        agg_func = 'sum'
        if any(w in q for w in ["average", "mean", "avg"]):
            agg_func = 'mean'
        elif any(w in q for w in ["count", "number of", "how many"]):
            agg_func = 'count'
        elif any(w in q for w in ["max", "maximum"]):
            agg_func = 'max'
        elif any(w in q for w in ["min", "minimum"]):
            agg_func = 'min'

        ascending = any(w in q for w in ["lowest", "least", "bottom", "worst", "min"])

        if group_col and (metric_col or agg_func == 'count'):
            if agg_func == 'count':
                res = df.groupby(group_col).size().reset_index(name='Count')
                sort_col = 'Count'
            else:
                temp_df = df.copy()
                temp_df[metric_col] = pd.to_numeric(temp_df[metric_col], errors='coerce')
                res = temp_df.groupby(group_col)[metric_col].agg(agg_func).reset_index()
                sort_col = metric_col

            res = res.sort_values(by=sort_col, ascending=ascending).dropna().head(limit)
            
            top_item = res.iloc[0]
            val_str = format_number(top_item[sort_col])
            adj = "lowest" if ascending else "highest"
            
            answer_text = f"The {group_col} with the {adj} {agg_func} {sort_col.lower()} is **'{top_item[group_col]}'** with **{val_str}**."
            if limit > 1:
                answer_text += f" Here are the top {len(res)} results:"

            # Generate chart
            fig = px.bar(
                res,
                x=group_col,
                y=sort_col,
                title=f"{agg_func.capitalize()} {sort_col} by {group_col}",
                color=sort_col,
                color_continuous_scale='Tealgrn' if not ascending else 'Reds'
            )
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=30, r=20, t=40, b=30))

            # Format data table
            table_data = res.to_dict(orient='records')
            for r in table_data:
                r[sort_col] = format_number(r[sort_col])

            return {
                "question": question,
                "answer": answer_text,
                "data": table_data,
                "chart": fig_to_spec(fig)
            }

    # 6. Direct Aggregation ("What is the average sales?", "Total profit?", "Maximum quantity?")
    metric_col = next((c for c in mentioned_cols if c in num_cols), num_cols[0] if num_cols else None)
    if metric_col:
        series = pd.to_numeric(df[metric_col], errors='coerce').dropna()
        if not series.empty:
            if any(w in q for w in ["average", "mean", "avg"]):
                val = series.mean()
                answer_text = f"The **average {metric_col}** is **{format_number(val)}** (Min: {format_number(series.min())}, Max: {format_number(series.max())})."
                return {
                    "question": question,
                    "answer": answer_text,
                    "data": [{
                        "metric": f"Average {metric_col}",
                        "mean": format_number(val),
                        "median": format_number(series.median()),
                        "std": format_number(series.std()),
                        "count": len(series)
                    }],
                    "chart": None
                }
            elif any(w in q for w in ["total", "sum", "overall"]):
                val = series.sum()
                answer_text = f"The **total {metric_col}** across all records is **{format_number(val)}**."
                return {
                    "question": question,
                    "answer": answer_text,
                    "data": [{"metric": f"Total {metric_col}", "sum": format_number(val), "count": len(series)}],
                    "chart": None
                }
            elif any(w in q for w in ["max", "highest", "maximum"]):
                val = series.max()
                answer_text = f"The **maximum {metric_col}** recorded is **{format_number(val)}**."
                return {
                    "question": question,
                    "answer": answer_text,
                    "data": [{"metric": f"Max {metric_col}", "value": format_number(val)}],
                    "chart": None
                }
            elif any(w in q for w in ["min", "lowest", "minimum"]):
                val = series.min()
                answer_text = f"The **minimum {metric_col}** recorded is **{format_number(val)}**."
                return {
                    "question": question,
                    "answer": answer_text,
                    "data": [{"metric": f"Min {metric_col}", "value": format_number(val)}],
                    "chart": None
                }

    # 7. Correlation question
    if "correlation" in q or "correlate" in q or "relationship" in q:
        if len(num_cols) >= 2:
            c1, c2 = (mentioned_cols[:2] if len(mentioned_cols) >= 2 else (num_cols[0], num_cols[1]))
            r = df[[c1, c2]].apply(pd.to_numeric, errors='coerce').corr().iloc[0, 1]
            answer_text = f"The Pearson correlation between **'{c1}'** and **'{c2}'** is **{r:.3f}**."
            fig = px.scatter(df, x=c1, y=c2, title=f"{c1} vs {c2} (r={r:.2f})")
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=30, r=20, t=40, b=30))
            return {
                "question": question,
                "answer": answer_text,
                "data": [{"col1": c1, "col2": c2, "correlation": round(float(r), 3)}],
                "chart": fig_to_spec(fig)
            }

    # Fallback: helpful response with guided suggestions
    suggestions = []
    if num_cols:
        suggestions.append(f"What is the average {num_cols[0]}?")
        suggestions.append(f"What is the total {num_cols[0]}?")
    if cat_cols and num_cols:
        suggestions.append(f"Which {cat_cols[0]} generated the highest {num_cols[0]}?")
        suggestions.append(f"Top 5 {cat_cols[0]}")
    if date_cols:
        suggestions.append("Which month had the highest sales?")
    suggestions.append("Are there missing values?")

    return {
        "question": question,
        "answer": f"I analyzed your question regarding '{question}', but need a bit more clarity. You can ask about aggregations, rankings, comparisons, or missing values.",
        "data": [{"hint": "Try one of the suggested queries below"}],
        "suggestions": suggestions,
        "chart": None
    }
