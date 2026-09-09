import React from 'react';
import {
  Rows,
  Columns,
  AlertTriangle,
  Copy,
  HardDrive,
  Hash,
  Tag,
  Calendar,
  CheckSquare,
  ShieldCheck,
  TrendingUp
} from 'lucide-react';

export default function MetricCards({ summary, qualityScore, smartKpis = [] }) {
  if (!summary) return null;

  const defaultCards = [
    {
      title: 'Total Records',
      value: summary.total_rows?.toLocaleString(),
      subtext: `${summary.total_columns} columns total`,
      icon: Rows,
      bgColor: 'bg-blue-50 dark:bg-blue-950/40',
      textColor: 'text-blue-600 dark:text-blue-400',
    },
    {
      title: 'Data Quality Score',
      value: `${qualityScore?.score ?? 100}/100`,
      subtext: qualityScore?.rating || 'Good Quality',
      icon: ShieldCheck,
      bgColor: (qualityScore?.score ?? 100) >= 80 ? 'bg-emerald-50 dark:bg-emerald-950/40' : 'bg-amber-50 dark:bg-amber-950/40',
      textColor: (qualityScore?.score ?? 100) >= 80 ? 'text-emerald-600 dark:text-emerald-400' : 'text-amber-600 dark:text-amber-400',
    },
    {
      title: 'Missing Values',
      value: `${summary.overall_missing_percentage}%`,
      subtext: `${summary.overall_missing_cells?.toLocaleString()} empty cells`,
      icon: AlertTriangle,
      bgColor: summary.overall_missing_percentage > 5 ? 'bg-amber-50 dark:bg-amber-950/40' : 'bg-emerald-50 dark:bg-emerald-950/40',
      textColor: summary.overall_missing_percentage > 5 ? 'text-amber-600 dark:text-amber-400' : 'text-emerald-600 dark:text-emerald-400',
    },
    {
      title: 'Duplicate Rows',
      value: summary.duplicate_rows?.toLocaleString(),
      subtext: summary.duplicate_rows > 0 ? 'Deduplication advised' : 'Zero duplicates',
      icon: Copy,
      bgColor: summary.duplicate_rows > 0 ? 'bg-rose-50 dark:bg-rose-950/40' : 'bg-emerald-50 dark:bg-emerald-950/40',
      textColor: summary.duplicate_rows > 0 ? 'text-rose-600 dark:text-rose-400' : 'text-emerald-600 dark:text-emerald-400',
    },
    {
      title: 'Memory Footprint',
      value: summary.memory_usage,
      subtext: 'In-memory buffer',
      icon: HardDrive,
      bgColor: 'bg-slate-100 dark:bg-slate-800',
      textColor: 'text-slate-600 dark:text-slate-300',
    },
  ];

  return (
    <div className="space-y-4">
      {/* 5 Structural Metric Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-3 sm:gap-4">
        {defaultCards.map((card, idx) => {
          const Icon = card.icon;
          return (
            <div
              key={idx}
              className="p-4 bg-white dark:bg-slate-900 border border-slate-200/90 dark:border-slate-800 rounded-2xl shadow-xs flex flex-col justify-between hover:border-slate-300 dark:hover:border-slate-700 transition-all"
            >
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs font-bold text-slate-500 dark:text-slate-400 truncate">{card.title}</span>
                <div className={`w-8 h-8 rounded-xl ${card.bgColor} ${card.textColor} flex items-center justify-center shrink-0`}>
                  <Icon className="w-4 h-4" />
                </div>
              </div>
              <div>
                <div className="text-xl sm:text-2xl font-extrabold text-slate-900 dark:text-slate-100 tracking-tight">
                  {card.value}
                </div>
                <div className="text-[11px] font-medium text-slate-400 dark:text-slate-500 mt-0.5 truncate">
                  {card.subtext}
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Smart Business KPIs (detected by Python) */}
      {smartKpis.length > 0 && (
        <div>
          <div className="flex items-center gap-1.5 text-xs font-bold text-slate-400 dark:text-slate-500 uppercase tracking-wider mb-2">
            <TrendingUp className="w-3.5 h-3.5 text-blue-600 dark:text-blue-400" />
            <span>Detected Business Metrics & KPIs</span>
          </div>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 sm:gap-4">
            {smartKpis.map((kpi, kIdx) => (
              <div
                key={kIdx}
                className="p-3.5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200/90 dark:border-slate-800 shadow-xs hover:border-blue-300 dark:hover:border-blue-700 transition-all"
              >
                <div className="text-[11px] font-bold text-slate-500 dark:text-slate-400 truncate">{kpi.label}</div>
                <div className="text-lg sm:text-xl font-extrabold text-blue-600 dark:text-blue-400 mt-0.5">
                  {kpi.value}
                </div>
                <div className="text-[10px] text-slate-400 dark:text-slate-500 truncate mt-0.5">{kpi.subtext}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Column Schema Type Breakdown Tags */}
      <div className="flex flex-wrap items-center gap-2 pt-1 text-xs">
        <span className="text-slate-400 dark:text-slate-500 font-bold text-[11px] uppercase tracking-wider mr-1">
          Schema:
        </span>
        <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full bg-blue-50 dark:bg-blue-950/50 text-blue-700 dark:text-blue-300 font-bold border border-blue-200/60 dark:border-blue-800/60">
          <Hash className="w-3 h-3" />
          {summary.numerical_columns_count} Numerical
        </span>
        <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full bg-purple-50 dark:bg-purple-950/50 text-purple-700 dark:text-purple-300 font-bold border border-purple-200/60 dark:border-purple-800/60">
          <Tag className="w-3 h-3" />
          {summary.categorical_columns_count} Categorical
        </span>
        {summary.datetime_columns_count > 0 && (
          <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full bg-emerald-50 dark:bg-emerald-950/50 text-emerald-700 dark:text-emerald-300 font-bold border border-emerald-200/60 dark:border-emerald-800/60">
            <Calendar className="w-3 h-3" />
            {summary.datetime_columns_count} Datetime
          </span>
        )}
        {summary.boolean_columns_count > 0 && (
          <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full bg-amber-50 dark:bg-amber-950/50 text-amber-700 dark:text-amber-300 font-bold border border-amber-200/60 dark:border-amber-800/60">
            <CheckSquare className="w-3 h-3" />
            {summary.boolean_columns_count} Boolean
          </span>
        )}
      </div>
    </div>
  );
}
