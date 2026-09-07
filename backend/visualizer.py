import json
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Any, Optional

def fig_to_spec(fig) -> Dict[str, Any]:
    """Safely converts Plotly figure to standard Python JSON dict."""
    return json.loads(fig.to_json())

# Standard dark/light neutral styling template for Plotly figures
CHART_LAYOUT_DEFAULTS = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Inter, sans-serif', color='#334155', size=12),
    margin=dict(l=40, r=20, t=50, b=40),
    xaxis=dict(gridcolor='#f1f5f9', zerolinecolor='#e2e8f0'),
    yaxis=dict(gridcolor='#f1f5f9', zerolinecolor='#e2e8f0'),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

def generate_automatic_visualizations(df: pd.DataFrame, col_types: Dict[str, str], strong_corrs: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Generates a full suite of automatic, interactive Plotly visualizations as JSON dicts.
    """
    charts = {}

    numerical_cols = [c for c, t in col_types.items() if t == 'numerical']
    categorical_cols = [c for c, t in col_types.items() if t in ['categorical', 'text']]
    datetime_cols = [c for c, t in col_types.items() if t == 'datetime']

    # 1. Histograms for top numerical columns (up to 4)
    histograms = []
    for col in numerical_cols[:4]:
        series = pd.to_numeric(df[col], errors='coerce').dropna()
        if series.empty:
            continue
        fig = px.histogram(
            df,
            x=col,
            marginal="box",
            title=f"Distribution of {col}",
            color_discrete_sequence=['#3b82f6'],
            opacity=0.85
        )
        fig.update_layout(**CHART_LAYOUT_DEFAULTS)
        histograms.append({
            "column": col,
            "title": f"Distribution: {col}",
            "spec": fig_to_spec(fig)
        })
    charts["histograms"] = histograms

    # 2. Bar charts for categorical columns (up to 4)
    bar_charts = []
    for col in categorical_cols[:4]:
        val_counts = df[col].dropna().value_counts().head(10).reset_index()
        val_counts.columns = [col, 'Count']
        if val_counts.empty:
            continue
        fig = px.bar(
            val_counts,
            x=col,
            y='Count',
            title=f"Top Categories: {col}",
            color='Count',
            color_continuous_scale='Blues'
        )
        fig.update_layout(**CHART_LAYOUT_DEFAULTS)
        fig.update_layout(coloraxis_showscale=False)
        bar_charts.append({
            "column": col,
            "title": f"Frequency: {col}",
            "spec": fig_to_spec(fig)
        })
    charts["bar_charts"] = bar_charts

    # 3. Correlation Heatmap
    if len(numerical_cols) >= 2:
        num_df = df[numerical_cols].apply(pd.to_numeric, errors='coerce')
        corr = num_df.corr().round(2)
        fig = go.Figure(data=go.Heatmap(
            z=corr.values,
            x=corr.columns.tolist(),
            y=corr.index.tolist(),
            colorscale='RdBu',
            zmin=-1,
            zmax=1,
            text=np.around(corr.values, 2),
            texttemplate="%{text}",
            textfont={"size": 11},
            hoverongaps=False
        ))
        fig.update_layout(
            title="Correlation Matrix Heatmap",
            **CHART_LAYOUT_DEFAULTS
        )
        charts["correlation_heatmap"] = {
            "title": "Numerical Correlation Heatmap",
            "spec": fig_to_spec(fig)
        }

    # 4. Time Series Chart if datetime column exists
    if datetime_cols and numerical_cols:
        date_col = datetime_cols[0]
        # Sort and parse
        temp_df = df.copy()
        temp_df[date_col] = pd.to_datetime(temp_df[date_col], errors='coerce')
        temp_df = temp_df.dropna(subset=[date_col]).sort_values(by=date_col)
        
        if not temp_df.empty:
            metric_col = numerical_cols[0]
            # Aggregate by date if multiple rows per date
            time_agg = temp_df.groupby(temp_df[date_col].dt.date)[metric_col].sum().reset_index()
            time_agg.columns = ['Date', metric_col]
            
            fig = px.line(
                time_agg,
                x='Date',
                y=metric_col,
                markers=True,
                title=f"{metric_col} Over Time ({date_col})",
                color_discrete_sequence=['#10b981']
            )
            fig.update_layout(**CHART_LAYOUT_DEFAULTS)
            charts["time_series"] = {
                "title": f"Time Series: {metric_col} vs {date_col}",
                "spec": fig_to_spec(fig)
            }

    # 5. Scatter plot for strongly correlated or top 2 numerical columns
    scatter_charts = []
    if strong_corrs:
        for sc in strong_corrs[:2]:
            c1, c2 = sc["col1"], sc["col2"]
            color_col = categorical_cols[0] if categorical_cols else None
            fig = px.scatter(
                df,
                x=c1,
                y=c2,
                color=color_col,
                trendline="ols" if len(df) < 5000 else None,
                title=f"{c1} vs {c2} (Correlation: {sc['correlation']:.2f})"
            )
            fig.update_layout(**CHART_LAYOUT_DEFAULTS)
            scatter_charts.append({
                "title": f"Scatter: {c1} vs {c2}",
                "spec": fig_to_spec(fig)
            })
    elif len(numerical_cols) >= 2:
        c1, c2 = numerical_cols[0], numerical_cols[1]
        fig = px.scatter(
            df,
            x=c1,
            y=c2,
            title=f"{c1} vs {c2}"
        )
        fig.update_layout(**CHART_LAYOUT_DEFAULTS)
        scatter_charts.append({
            "title": f"Scatter: {c1} vs {c2}",
            "spec": fig_to_spec(fig)
        })
    charts["scatter_plots"] = scatter_charts

    return charts


def generate_custom_chart(
    df: pd.DataFrame,
    chart_type: str,
    x_col: str,
    y_col: Optional[str] = None,
    color_col: Optional[str] = None,
    agg_func: Optional[str] = None
) -> Dict[str, Any]:
    """
    Generates a user-customized Plotly chart safely.
    """
    # Validate columns exist
    if x_col not in df.columns:
        raise ValueError(f"Column '{x_col}' does not exist in dataset.")
    if y_col and y_col not in df.columns:
        raise ValueError(f"Column '{y_col}' does not exist in dataset.")
    if color_col and color_col not in df.columns:
        color_col = None

    plot_df = df.copy()

    # Aggregation if requested
    if agg_func and y_col and agg_func in ['sum', 'mean', 'count', 'median', 'min', 'max']:
        if agg_func == 'count':
            plot_df = plot_df.groupby([x_col] + ([color_col] if color_col else [])).size().reset_index(name=y_col)
        else:
            plot_df[y_col] = pd.to_numeric(plot_df[y_col], errors='coerce')
            group_cols = [x_col]
            if color_col:
                group_cols.append(color_col)
            plot_df = plot_df.groupby(group_cols)[y_col].agg(agg_func).reset_index()

    title = f"{chart_type.title()}: {x_col}" + (f" vs {y_col}" if y_col else "")
    if agg_func:
        title += f" ({agg_func.upper()})"

    if chart_type == 'bar':
        fig = px.bar(plot_df, x=x_col, y=y_col, color=color_col, title=title)
    elif chart_type == 'line':
        fig = px.line(plot_df, x=x_col, y=y_col, color=color_col, markers=True, title=title)
    elif chart_type == 'scatter':
        fig = px.scatter(plot_df, x=x_col, y=y_col, color=color_col, title=title)
    elif chart_type == 'box':
        fig = px.box(plot_df, x=x_col, y=y_col, color=color_col, title=title)
    elif chart_type == 'pie':
        fig = px.pie(plot_df, names=x_col, values=y_col, title=title)
    elif chart_type == 'histogram':
        fig = px.histogram(plot_df, x=x_col, y=y_col, color=color_col, marginal="box", title=title)
    else:
        fig = px.bar(plot_df, x=x_col, y=y_col, color=color_col, title=title)

    fig.update_layout(**CHART_LAYOUT_DEFAULTS)
    return fig_to_spec(fig)
