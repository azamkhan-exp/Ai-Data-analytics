import React, { useState } from 'react';
import { Search, Hash, Tag, Calendar, CheckSquare, AlignLeft, AlertCircle, CheckCircle2 } from 'lucide-react';

export default function DataPreview({ previewRows, columnDetails, totalRows }) {
  const [searchTerm, setSearchTerm] = useState('');
  const [activeView, setActiveView] = useState('table'); // 'table' | 'dictionary'

  if (!previewRows || previewRows.length === 0) {
    return (
      <div className="p-8 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl text-center text-slate-500 dark:text-slate-400">
        No preview rows available.
      </div>
    );
  }

  const columns = Object.keys(previewRows[0] || {});

  // Search filter
  const filteredRows = previewRows.filter((row) => {
    if (!searchTerm) return true;
    return Object.values(row).some((val) =>
      String(val).toLowerCase().includes(searchTerm.toLowerCase())
    );
  });

  const getTypeBadge = (type) => {
    switch (type) {
      case 'numerical':
        return (
          <span className="inline-flex items-center gap-0.5 px-1.5 py-0.5 rounded text-[10px] font-semibold bg-blue-100 dark:bg-blue-950/60 text-blue-800 dark:text-blue-300">
            <Hash className="w-2.5 h-2.5" /> num
          </span>
        );
      case 'categorical':
        return (
          <span className="inline-flex items-center gap-0.5 px-1.5 py-0.5 rounded text-[10px] font-semibold bg-purple-100 dark:bg-purple-950/60 text-purple-800 dark:text-purple-300">
            <Tag className="w-2.5 h-2.5" /> cat
          </span>
        );
      case 'datetime':
        return (
          <span className="inline-flex items-center gap-0.5 px-1.5 py-0.5 rounded text-[10px] font-semibold bg-emerald-100 dark:bg-emerald-950/60 text-emerald-800 dark:text-emerald-300">
            <Calendar className="w-2.5 h-2.5" /> date
          </span>
        );
      case 'boolean':
        return (
          <span className="inline-flex items-center gap-0.5 px-1.5 py-0.5 rounded text-[10px] font-semibold bg-amber-100 dark:bg-amber-950/60 text-amber-800 dark:text-amber-300">
            <CheckSquare className="w-2.5 h-2.5" /> bool
          </span>
        );
      default:
        return (
          <span className="inline-flex items-center gap-0.5 px-1.5 py-0.5 rounded text-[10px] font-semibold bg-slate-100 dark:bg-slate-800 text-slate-800 dark:text-slate-300">
            <AlignLeft className="w-2.5 h-2.5" /> text
          </span>
        );
    }
  };

  const colMap = (columnDetails || []).reduce((acc, c) => {
    acc[c.name] = c;
    return acc;
  }, {});

  return (
    <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-xs overflow-hidden transition-colors duration-200">
      {/* Header with Search and Toggle */}
      <div className="p-4 border-b border-slate-200 dark:border-slate-800 flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center gap-2">
          <button
            onClick={() => setActiveView('table')}
            className={`px-3 py-1.5 text-xs font-semibold rounded-lg transition-colors cursor-pointer ${
              activeView === 'table'
                ? 'bg-blue-600 text-white shadow-xs'
                : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-700'
            }`}
          >
            Data Table Preview (First 20 Rows)
          </button>
          <button
            onClick={() => setActiveView('dictionary')}
            className={`px-3 py-1.5 text-xs font-semibold rounded-lg transition-colors cursor-pointer ${
              activeView === 'dictionary'
                ? 'bg-blue-600 text-white shadow-xs'
                : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-700'
            }`}
          >
            Column Schema & Quality ({columns.length} Columns)
          </button>
        </div>

        {activeView === 'table' && (
          <div className="relative w-full sm:w-64">
            <Search className="w-3.5 h-3.5 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              placeholder="Search in preview..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-8 pr-3 py-1.5 text-xs rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500"
            />
          </div>
        )}
      </div>

      {/* Table View */}
      {activeView === 'table' ? (
        <div className="overflow-x-auto max-h-[520px]">
          <table className="w-full text-left border-collapse text-xs">
            <thead className="sticky top-0 bg-slate-50 dark:bg-slate-800/90 backdrop-blur-xs border-b border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-200 z-10">
              <tr>
                <th className="py-2.5 px-3 font-semibold text-slate-400 w-12 text-center">#</th>
                {columns.map((col) => {
                  const meta = colMap[col];
                  const hasMissing = meta?.missing_count > 0;
                  return (
                    <th key={col} className="py-2.5 px-3 font-semibold whitespace-nowrap">
                      <div className="flex items-center gap-1.5 mb-1">
                        <span>{col}</span>
                        {meta && getTypeBadge(meta.inferred_type)}
                      </div>
                      {hasMissing ? (
                        <div className="text-[10px] font-normal text-amber-600 dark:text-amber-400 flex items-center gap-1">
                          <AlertCircle className="w-2.5 h-2.5" />
                          <span>{meta.missing_percentage}% missing</span>
                        </div>
                      ) : (
                        <div className="text-[10px] font-normal text-emerald-600 dark:text-emerald-400 flex items-center gap-1">
                          <CheckCircle2 className="w-2.5 h-2.5" />
                          <span>100% complete</span>
                        </div>
                      )}
                    </th>
                  );
                })}
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 dark:divide-slate-800 text-slate-800 dark:text-slate-200">
              {filteredRows.map((row, idx) => (
                <tr key={idx} className="hover:bg-blue-50/40 dark:hover:bg-slate-800/50 transition-colors">
                  <td className="py-2 px-3 text-center text-slate-400 dark:text-slate-500 font-mono text-[11px] select-none">
                    {idx + 1}
                  </td>
                  {columns.map((col) => {
                    const val = row[col];
                    const isNull = val === null || val === undefined;
                    return (
                      <td key={col} className="py-2 px-3 whitespace-nowrap font-mono">
                        {isNull ? (
                          <span className="px-1.5 py-0.5 rounded text-[10px] bg-amber-50 dark:bg-amber-950/40 text-amber-600 dark:text-amber-400 font-sans italic">
                            null
                          </span>
                        ) : (
                          <span>{String(val)}</span>
                        )}
                      </td>
                    );
                  })}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        /* Dictionary / Column Details View */
        <div className="p-4 overflow-x-auto">
          <table className="w-full text-left border-collapse text-xs">
            <thead className="bg-slate-50 dark:bg-slate-800/90 border-b border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-300">
              <tr>
                <th className="py-2.5 px-3 font-semibold">Column Name</th>
                <th className="py-2.5 px-3 font-semibold">Detected Type</th>
                <th className="py-2.5 px-3 font-semibold">Raw Dtype</th>
                <th className="py-2.5 px-3 font-semibold">Unique Values</th>
                <th className="py-2.5 px-3 font-semibold">Missing Count</th>
                <th className="py-2.5 px-3 font-semibold">Completeness</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
              {(columnDetails || []).map((c) => {
                const completePct = 100 - c.missing_percentage;
                return (
                  <tr key={c.name} className="hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors">
                    <td className="py-2 px-3 font-semibold text-slate-800 dark:text-slate-200 font-mono">{c.name}</td>
                    <td className="py-2 px-3">{getTypeBadge(c.inferred_type)}</td>
                    <td className="py-2 px-3 font-mono text-slate-500 dark:text-slate-400">{c.raw_dtype}</td>
                    <td className="py-2 px-3 font-mono text-slate-700 dark:text-slate-300">{c.unique_count.toLocaleString()}</td>
                    <td className="py-2 px-3 font-mono">
                      {c.missing_count > 0 ? (
                        <span className="text-amber-600 dark:text-amber-400 font-semibold">{c.missing_count.toLocaleString()} ({c.missing_percentage}%)</span>
                      ) : (
                        <span className="text-emerald-600 dark:text-emerald-400 font-semibold">0 (0%)</span>
                      )}
                    </td>
                    <td className="py-2 px-3">
                      <div className="w-32 flex items-center gap-2">
                        <div className="w-full bg-slate-100 dark:bg-slate-800 rounded-full h-2 overflow-hidden">
                          <div
                            className={`h-2 rounded-full ${completePct === 100 ? 'bg-emerald-500' : 'bg-amber-500'}`}
                            style={{ width: `${completePct}%` }}
                          ></div>
                        </div>
                        <span className="text-[10px] font-mono text-slate-500 dark:text-slate-400">{completePct}%</span>
                      </div>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
