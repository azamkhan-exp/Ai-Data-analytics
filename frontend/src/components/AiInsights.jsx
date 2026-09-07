import React, { useState } from 'react';
import {
  Sparkles,
  AlertTriangle,
  TrendingUp,
  Activity,
  CheckCircle2,
  HelpCircle,
  Flame,
  Info,
  Layers,
  BrainCircuit
} from 'lucide-react';

export default function AiInsights({ insights }) {
  const [filter, setFilter] = useState('All');

  if (!insights || insights.length === 0) {
    return (
      <div className="p-8 bg-white border border-slate-200 rounded-2xl text-center text-slate-500">
        No insights generated yet.
      </div>
    );
  }

  const categories = ['All', ...new Set(insights.map((i) => i.category))];

  const filteredInsights =
    filter === 'All' ? insights : insights.filter((i) => i.category === filter);

  const getCategoryIcon = (category, type) => {
    switch (category) {
      case 'Data Quality':
        return <CheckCircle2 className="w-4 h-4 text-emerald-600" />;
      case 'Correlations':
        return <Flame className="w-4 h-4 text-orange-500" />;
      case 'Trends':
        return <TrendingUp className="w-4 h-4 text-blue-600" />;
      case 'Anomalies':
        return <AlertTriangle className="w-4 h-4 text-rose-500" />;
      case 'Patterns':
        return <Layers className="w-4 h-4 text-purple-600" />;
      case 'Executive':
        return <Sparkles className="w-4 h-4 text-indigo-600" />;
      default:
        return <Activity className="w-4 h-4 text-slate-600" />;
    }
  };

  const getImportanceBadge = (importance) => {
    switch (importance) {
      case 'high':
        return (
          <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-rose-50 text-rose-700 border border-rose-200/60 uppercase tracking-wider">
            High Priority
          </span>
        );
      case 'medium':
        return (
          <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-amber-50 text-amber-700 border border-amber-200/60 uppercase tracking-wider">
            Key Metric
          </span>
        );
      default:
        return (
          <span className="px-2 py-0.5 rounded-full text-[10px] font-medium bg-slate-100 text-slate-600 uppercase tracking-wider">
            Info
          </span>
        );
    }
  };

  return (
    <div className="space-y-6">
      {/* Banner */}
      <div className="p-5 bg-gradient-to-r from-blue-600 to-indigo-700 rounded-2xl text-white shadow-md flex items-start gap-4">
        <div className="w-10 h-10 rounded-xl bg-white/10 backdrop-blur-xs flex items-center justify-center shrink-0">
          <BrainCircuit className="w-6 h-6 text-white" />
        </div>
        <div>
          <h3 className="text-base font-bold tracking-tight">AI & Statistical Intelligence Engine</h3>
          <p className="text-xs text-blue-100 mt-1 leading-relaxed max-w-2xl">
            Insights are computed dynamically using verifiable statistical algorithms—including Pearson correlation coefficients, interquartile range (IQR) anomaly bounds, timeline delta trends, and category concentrations.
          </p>
        </div>
      </div>

      {/* Filter Tabs */}
      <div className="flex flex-wrap items-center gap-2 border-b border-slate-200 pb-3">
        {categories.map((cat) => (
          <button
            key={cat}
            onClick={() => setFilter(cat)}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
              filter === cat
                ? 'bg-blue-600 text-white shadow-xs'
                : 'bg-white text-slate-600 border border-slate-200 hover:bg-slate-50'
            }`}
          >
            {cat} ({cat === 'All' ? insights.length : insights.filter((i) => i.category === cat).length})
          </button>
        ))}
      </div>

      {/* Insights Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {filteredInsights.map((insight, idx) => (
          <div
            key={insight.id || idx}
            className="p-5 bg-white border border-slate-200/90 rounded-2xl shadow-xs hover:border-blue-300 hover:shadow-md transition-all flex flex-col justify-between"
          >
            <div>
              <div className="flex items-center justify-between gap-2 mb-3">
                <div className="flex items-center gap-2">
                  <div className="p-1.5 rounded-lg bg-slate-50 border border-slate-100">
                    {getCategoryIcon(insight.category, insight.type)}
                  </div>
                  <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">
                    {insight.category}
                  </span>
                </div>
                {getImportanceBadge(insight.importance)}
              </div>

              <h4 className="text-sm font-bold text-slate-900 mb-2 leading-snug">
                {insight.title}
              </h4>

              <p className="text-xs text-slate-600 leading-relaxed">
                {insight.description}
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
