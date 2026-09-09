import re
import pandas as pd
from typing import Dict, List, Any

PATTERNS = [
    {"keys": ["revenue", "sales", "turnover", "income"], "label": "Total Revenue", "fmt": "currency", "agg": "sum"},
    {"keys": ["profit", "net_profit", "margin_amount"], "label": "Total Profit", "fmt": "currency", "agg": "sum"},
    {"keys": ["order_id", "order_number", "transaction_id"], "label": "Total Orders", "fmt": "count", "agg": "unique"},
    {"keys": ["customer_id", "customer", "client", "account"], "label": "Unique Customers", "fmt": "unique", "agg": "unique"},
    {"keys": ["quantity", "units", "volume"], "label": "Units Sold", "fmt": "number", "agg": "sum"},
    {"keys": ["discount", "discount_rate", "rebate"], "label": "Avg Discount", "fmt": "percentage", "agg": "mean"},
    {"keys": ["charges", "monthly_charges", "mrr"], "label": "Avg Monthly Charge", "fmt": "currency", "agg": "mean"},
    {"keys": ["tenure", "tenure_months"], "label": "Avg Customer Tenure", "fmt": "months", "agg": "mean"}
]

def format_kpi_value(val: float, fmt: str) -> str:
    """Formats numeric values into standard human-readable KPI representations."""
    if pd.isna(val):
        return "N/A"
    if fmt == "currency":
        return f"${val:,.2f}"
    if fmt == "percentage":
        pct = val * 100 if val <= 1.0 else val
        return f"{pct:.1f}%"
    if fmt == "months":
        return f"{val:.1f} mos"
    if fmt in ["count", "unique"]:
        return f"{int(val):,}"
    if abs(val) >= 1000:
        return f"{val:,.1f}"
    return f"{val:.2f}"

def detect_smart_kpis(df: pd.DataFrame, numerical_stats: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Heuristically discovers primary business KPIs based on column semantics and statistics.
    """
    kpis = []
    matched_cols = set()
    num_stats_map = {s["column"]: s for s in numerical_stats}

    for p in PATTERNS:
        for col in df.columns:
            if col in matched_cols:
                continue

            col_clean = re.sub(r'[^a-zA-Z0-9]', '_', col.lower())
            if any(k in col_clean for k in p["keys"]):
                matched_cols.add(col)

                if p["agg"] == "unique":
                    val = float(df[col].dropna().nunique())
                    kpis.append({
                        "column": col,
                        "label": p["label"],
                        "value": format_kpi_value(val, p["fmt"]),
                        "subtext": f"Distinct entities count",
                        "type": p["fmt"]
                    })
                elif col in num_stats_map:
                    stat = num_stats_map[col]
                    raw_val = stat["mean"] if p["agg"] == "mean" else stat["sum"]
                    subtext = f"Mean average per record" if p["agg"] == "mean" else f"Aggregated sum ({stat['count']:,} rows)"
                    kpis.append({
                        "column": col,
                        "label": p["label"],
                        "value": format_kpi_value(raw_val, p["fmt"]),
                        "subtext": subtext,
                        "type": p["fmt"]
                    })
                break

    # Fallback: if fewer than 2 KPIs discovered, surface top numerical averages
    if len(kpis) < 2:
        for stat in numerical_stats[:3]:
            col_name = stat["column"]
            if col_name not in matched_cols:
                kpis.append({
                    "column": col_name,
                    "label": f"Avg {col_name.replace('_', ' ').title()}",
                    "value": f"{stat['mean']:,.2f}",
                    "subtext": f"Min: {stat['min']:,} • Max: {stat['max']:,}",
                    "type": "number"
                })

    return kpis[:4]
