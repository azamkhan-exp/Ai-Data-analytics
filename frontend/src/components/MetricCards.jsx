import React from 'react';
import { Rows, Columns, AlertTriangle, Copy, HardDrive, Hash, Tag, Calendar, CheckSquare } from 'lucide-react';

export default function MetricCards({ summary }) {
  if (!summary) return null;

  const cards = [
    {
      title: 'Total Rows',
      value: summary.total_rows?.toLocaleString(),
      subtext: 'Data records',
      icon: Rows,
      color: 'blue',
      bgColor: 'bg-blue-50',
      textColor: 'text-blue-600',
    },
    {
      title: 'Total Columns',
      value: summary.total_columns,
      subtext: `${summary.numerical_columns_count} num • ${summary.categorical_columns_count} cat`,
      icon: Columns,
      color: 'indigo',
      bgColor: 'bg-indigo-50',
      textColor: 'text-indigo-600',
    },
    {
      title: 'Missing Values',
      value: `${summary.overall_missing_percentage}%`,
      subtext: `${summary.overall_missing_cells?.toLocaleString()} empty cells`,
      icon: AlertTriangle,
      color: summary.overall_missing_percentage > 5 ? 'amber' : 'emerald',
      bgColor: summary.overall_missing_percentage > 5 ? 'bg-amber-50' : 'bg-emerald-50',
      textColor: summary.overall_missing_percentage > 5 ? 'text-amber-600' : 'text-emerald-600',
    },
    {
      title: 'Duplicate Rows',
      value: summary.duplicate_rows?.toLocaleString(),
      subtext: summary.duplicate_rows > 0 ? 'Cleaning advised' : 'Zero duplicates',
      icon: Copy,
      color: summary.duplicate_rows > 0 ? 'rose' : 'emerald',
      bgColor: summary.duplicate_rows > 0 ? 'bg-rose-50' : 'bg-emerald-50',
      textColor: summary.duplicate_rows > 0 ? 'text-rose-600' : 'text-emerald-600',
    },
    {
      title: 'Memory Footprint',
      value: summary.memory_usage,
      subtext: 'In-memory buffer',
      icon: HardDrive,
      color: 'slate',
      bgColor: 'bg-slate-100',
      textColor: 'text-slate-600',
    },
  ];

  return (
    <div>
      {/* 5 KPI Metric Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4 mb-6">
        {cards.map((card, idx) => {
          const Icon = card.icon;
          return (
            <div
              key={idx}
              className="p-4 bg-white border border-slate-200/90 rounded-2xl shadow-xs flex flex-col justify-between hover:border-slate-300 transition-colors"
            >
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">{card.title}</span>
                <div className={`w-7 h-7 rounded-lg ${card.bgColor} ${card.textColor} flex items-center justify-center`}>
                  <Icon className="w-3.5 h-3.5" />
                </div>
              </div>
              <div>
                <div className="text-2xl font-black text-slate-800 tracking-tight">{card.value}</div>
                <div className="text-[11px] text-slate-400 font-medium mt-0.5">{card.subtext}</div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Column Types Breakdown Badge Row */}
      <div className="p-3 bg-white border border-slate-200 rounded-xl mb-6 flex flex-wrap items-center gap-3 text-xs">
        <span className="font-semibold text-slate-600">Column Types:</span>
        <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full bg-blue-50 text-blue-700 font-medium border border-blue-200/60">
          <Hash className="w-3 h-3 text-blue-500" />
          {summary.numerical_columns_count} Numerical
        </span>
        <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full bg-purple-50 text-purple-700 font-medium border border-purple-200/60">
          <Tag className="w-3 h-3 text-purple-500" />
          {summary.categorical_columns_count} Categorical
        </span>
        {summary.datetime_columns_count > 0 && (
          <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full bg-emerald-50 text-emerald-700 font-medium border border-emerald-200/60">
            <Calendar className="w-3 h-3 text-emerald-500" />
            {summary.datetime_columns_count} Date/Time
          </span>
        )}
        {summary.boolean_columns_count > 0 && (
          <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full bg-amber-50 text-amber-700 font-medium border border-amber-200/60">
            <CheckSquare className="w-3 h-3 text-amber-500" />
            {summary.boolean_columns_count} Boolean
          </span>
        )}
      </div>
    </div>
  );
}
