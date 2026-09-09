import React, { useState } from 'react';
import PlotlyChart from './PlotlyChart';
import { createCustomChart } from '../api';
import { BarChart3, TrendingUp, Grid, Sparkles, Filter, Sliders, Play, AlertCircle } from 'lucide-react';

export default function Visualizations({ visualizations, datasetId, columnTypes, columns }) {
  const [activeCategory, setActiveCategory] = useState('all'); // 'all' | 'distributions' | 'categories' | 'correlations' | 'trends' | 'custom'

  // Custom Chart Builder State
  const [chartType, setChartType] = useState('bar');
  const [xCol, setXCol] = useState(columns?.[0] || '');
  const [yCol, setYCol] = useState(columns?.[1] || '');
  const [colorCol, setColorCol] = useState('');
  const [aggFunc, setAggFunc] = useState('sum');
  const [customChartSpec, setCustomChartSpec] = useState(null);
  const [customLoading, setCustomLoading] = useState(false);
  const [customError, setCustomError] = useState(null);

  const handleGenerateCustomChart = async () => {
    if (!xCol) return;
    setCustomLoading(true);
    setCustomError(null);
    try {
      const res = await createCustomChart(datasetId, {
        chart_type: chartType,
        x_col: xCol,
        y_col: yCol || undefined,
        color_col: colorCol || undefined,
        agg_func: aggFunc || undefined,
      });
      setCustomChartSpec(res.spec);
    } catch (err) {
      setCustomError(err.response?.data?.detail || 'Failed to generate custom chart.');
    } finally {
      setCustomLoading(false);
    }
  };

  const histograms = visualizations?.histograms || [];
  const barCharts = visualizations?.bar_charts || [];
  const correlationHeatmap = visualizations?.correlation_heatmap;
  const timeSeries = visualizations?.time_series;
  const scatterPlots = visualizations?.scatter_plots || [];

  return (
    <div className="space-y-6">
      {/* Category selector pills */}
      <div className="flex flex-wrap items-center gap-2 border-b border-slate-200 dark:border-slate-800 pb-3">
        <button
          onClick={() => setActiveCategory('all')}
          className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
            activeCategory === 'all'
              ? 'bg-blue-600 text-white shadow-xs'
              : 'bg-white dark:bg-slate-900 text-slate-600 dark:text-slate-300 border border-slate-200 dark:border-slate-800 hover:bg-slate-50 dark:hover:bg-slate-800'
          }`}
        >
          All Auto Charts
        </button>
        {histograms.length > 0 && (
          <button
            onClick={() => setActiveCategory('distributions')}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
              activeCategory === 'distributions'
                ? 'bg-blue-600 text-white shadow-xs'
                : 'bg-white dark:bg-slate-900 text-slate-600 dark:text-slate-300 border border-slate-200 dark:border-slate-800 hover:bg-slate-50 dark:hover:bg-slate-800'
            }`}
          >
            Distributions ({histograms.length})
          </button>
        )}
        {barCharts.length > 0 && (
          <button
            onClick={() => setActiveCategory('categories')}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
              activeCategory === 'categories'
                ? 'bg-blue-600 text-white shadow-xs'
                : 'bg-white dark:bg-slate-900 text-slate-600 dark:text-slate-300 border border-slate-200 dark:border-slate-800 hover:bg-slate-50 dark:hover:bg-slate-800'
            }`}
          >
            Categorical ({barCharts.length})
          </button>
        )}
        {correlationHeatmap && (
          <button
            onClick={() => setActiveCategory('correlations')}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
              activeCategory === 'correlations'
                ? 'bg-blue-600 text-white shadow-xs'
                : 'bg-white dark:bg-slate-900 text-slate-600 dark:text-slate-300 border border-slate-200 dark:border-slate-800 hover:bg-slate-50 dark:hover:bg-slate-800'
            }`}
          >
            Correlation Heatmap
          </button>
        )}
        {timeSeries && (
          <button
            onClick={() => setActiveCategory('trends')}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
              activeCategory === 'trends'
                ? 'bg-blue-600 text-white shadow-xs'
                : 'bg-white dark:bg-slate-900 text-slate-600 dark:text-slate-300 border border-slate-200 dark:border-slate-800 hover:bg-slate-50 dark:hover:bg-slate-800'
            }`}
          >
            Time Series Trend
          </button>
        )}
        <button
          onClick={() => setActiveCategory('custom')}
          className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
            activeCategory === 'custom'
              ? 'bg-indigo-600 text-white shadow-xs'
              : 'bg-indigo-50 dark:bg-indigo-950/60 text-indigo-700 dark:text-indigo-300 border border-indigo-200 dark:border-indigo-800 hover:bg-indigo-100 dark:hover:bg-indigo-900/60'
          }`}
        >
          <Sliders className="w-3.5 h-3.5" />
          <span>Custom Chart Builder</span>
        </button>
      </div>

      {/* 1. Custom Chart Builder Tab */}
      {activeCategory === 'custom' && (
        <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-xs p-6 transition-colors duration-200">
          <div className="mb-6">
            <h3 className="text-base font-bold text-slate-800 dark:text-slate-100 tracking-tight">Interactive Chart Builder</h3>
            <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
              Configure axes, chart types, groupings, and aggregation functions to build custom Plotly visualizations.
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-5 gap-4 mb-6">
            {/* Chart Type */}
            <div>
              <label className="block text-xs font-semibold text-slate-600 dark:text-slate-300 mb-1.5">Chart Type</label>
              <select
                value={chartType}
                onChange={(e) => setChartType(e.target.value)}
                className="w-full px-3 py-2 text-xs border border-slate-200 dark:border-slate-700 rounded-lg bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="bar">Bar Chart</option>
                <option value="line">Line Chart</option>
                <option value="scatter">Scatter Plot</option>
                <option value="box">Box Plot</option>
                <option value="pie">Pie Chart</option>
                <option value="histogram">Histogram</option>
              </select>
            </div>

            {/* X-Axis */}
            <div>
              <label className="block text-xs font-semibold text-slate-600 dark:text-slate-300 mb-1.5">X-Axis Column</label>
              <select
                value={xCol}
                onChange={(e) => setXCol(e.target.value)}
                className="w-full px-3 py-2 text-xs border border-slate-200 dark:border-slate-700 rounded-lg bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                {(columns || []).map((c) => (
                  <option key={c} value={c}>{c}</option>
                ))}
              </select>
            </div>

            {/* Y-Axis */}
            <div>
              <label className="block text-xs font-semibold text-slate-600 dark:text-slate-300 mb-1.5">Y-Axis (Numerical)</label>
              <select
                value={yCol}
                onChange={(e) => setYCol(e.target.value)}
                className="w-full px-3 py-2 text-xs border border-slate-200 dark:border-slate-700 rounded-lg bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">None (Count)</option>
                {(columns || []).map((c) => (
                  <option key={c} value={c}>{c}</option>
                ))}
              </select>
            </div>

            {/* Color Grouping */}
            <div>
              <label className="block text-xs font-semibold text-slate-600 dark:text-slate-300 mb-1.5">Group / Color</label>
              <select
                value={colorCol}
                onChange={(e) => setColorCol(e.target.value)}
                className="w-full px-3 py-2 text-xs border border-slate-200 dark:border-slate-700 rounded-lg bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">None</option>
                {(columns || []).map((c) => (
                  <option key={c} value={c}>{c}</option>
                ))}
              </select>
            </div>

            {/* Aggregation */}
            <div>
              <label className="block text-xs font-semibold text-slate-600 dark:text-slate-300 mb-1.5">Aggregation</label>
              <select
                value={aggFunc}
                onChange={(e) => setAggFunc(e.target.value)}
                className="w-full px-3 py-2 text-xs border border-slate-200 dark:border-slate-700 rounded-lg bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="sum">Sum</option>
                <option value="mean">Mean (Average)</option>
                <option value="count">Count</option>
                <option value="median">Median</option>
                <option value="max">Max</option>
                <option value="min">Min</option>
              </select>
            </div>
          </div>

          <div className="flex items-center justify-between border-t border-slate-100 dark:border-slate-800 pt-4">
            <button
              onClick={handleGenerateCustomChart}
              disabled={customLoading || !xCol}
              className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-xs font-semibold transition-colors shadow-sm disabled:opacity-50 cursor-pointer"
            >
              <Play className="w-3.5 h-3.5 fill-current" />
              <span>{customLoading ? 'Rendering Chart...' : 'Generate Custom Visualization'}</span>
            </button>
          </div>

          {customError && (
            <div className="mt-4 p-3 bg-red-50 dark:bg-rose-950/40 border border-red-200 dark:border-rose-800 text-red-700 dark:text-rose-400 text-xs rounded-lg flex items-center gap-2">
              <AlertCircle className="w-4 h-4 text-red-500 shrink-0" />
              <span>{customError}</span>
            </div>
          )}

          {customChartSpec && (
            <div className="mt-6 border border-slate-200 dark:border-slate-800 rounded-xl p-4 bg-white dark:bg-slate-900">
              <PlotlyChart spec={customChartSpec} style={{ height: '420px' }} />
            </div>
          )}
        </div>
      )}

      {/* Auto Visualizations Grid */}
      {activeCategory !== 'custom' && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Time series if available */}
          {(activeCategory === 'all' || activeCategory === 'trends') && timeSeries && (
            <div className="lg:col-span-2 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-5 shadow-xs">
              <div className="flex items-center gap-2 mb-2 font-semibold text-slate-800 dark:text-slate-100 text-sm">
                <TrendingUp className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
                <span>{timeSeries.title}</span>
              </div>
              <PlotlyChart spec={timeSeries.spec} style={{ height: '360px' }} />
            </div>
          )}

          {/* Correlation Heatmap */}
          {(activeCategory === 'all' || activeCategory === 'correlations') && correlationHeatmap && (
            <div className="lg:col-span-2 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-5 shadow-xs">
              <div className="flex items-center gap-2 mb-2 font-semibold text-slate-800 dark:text-slate-100 text-sm">
                <Grid className="w-4 h-4 text-blue-600 dark:text-blue-400" />
                <span>{correlationHeatmap.title}</span>
              </div>
              <PlotlyChart spec={correlationHeatmap.spec} style={{ height: '380px' }} />
            </div>
          )}

          {/* Histograms */}
          {(activeCategory === 'all' || activeCategory === 'distributions') &&
            histograms.map((h, i) => (
              <div key={i} className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-5 shadow-xs">
                <div className="font-semibold text-slate-800 dark:text-slate-100 text-sm mb-2">{h.title}</div>
                <PlotlyChart spec={h.spec} style={{ height: '320px' }} />
              </div>
            ))}

          {/* Bar charts */}
          {(activeCategory === 'all' || activeCategory === 'categories') &&
            barCharts.map((b, i) => (
              <div key={i} className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-5 shadow-xs">
                <div className="font-semibold text-slate-800 dark:text-slate-100 text-sm mb-2">{b.title}</div>
                <PlotlyChart spec={b.spec} style={{ height: '320px' }} />
              </div>
            ))}

          {/* Scatter plots */}
          {(activeCategory === 'all' || activeCategory === 'correlations') &&
            scatterPlots.map((s, i) => (
              <div key={i} className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-5 shadow-xs">
                <div className="font-semibold text-slate-800 dark:text-slate-100 text-sm mb-2">{s.title}</div>
                <PlotlyChart spec={s.spec} style={{ height: '320px' }} />
              </div>
            ))}
        </div>
      )}
    </div>
  );
}
