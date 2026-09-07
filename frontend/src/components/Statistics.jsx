import React, { useState } from 'react';
import { Hash, Tag, Activity, ArrowUpDown, Flame, AlertCircle } from 'lucide-react';

export default function Statistics({ numericalStats, categoricalStats, strongCorrelations }) {
  const [subTab, setSubTab] = useState('numerical'); // 'numerical' | 'categorical' | 'correlations'

  return (
    <div className="space-y-6">
      {/* Sub-navigation tabs */}
      <div className="flex items-center gap-2 border-b border-slate-200 pb-3">
        <button
          onClick={() => setSubTab('numerical')}
          className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-all ${
            subTab === 'numerical'
              ? 'bg-blue-600 text-white shadow-xs'
              : 'bg-white text-slate-600 border border-slate-200 hover:bg-slate-50'
          }`}
        >
          <Hash className="w-3.5 h-3.5" />
          <span>Numerical Statistics ({numericalStats?.length || 0})</span>
        </button>
        <button
          onClick={() => setSubTab('categorical')}
          className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-all ${
            subTab === 'categorical'
              ? 'bg-blue-600 text-white shadow-xs'
              : 'bg-white text-slate-600 border border-slate-200 hover:bg-slate-50'
          }`}
        >
          <Tag className="w-3.5 h-3.5" />
          <span>Categorical Summary ({categoricalStats?.length || 0})</span>
        </button>
        {strongCorrelations?.length > 0 && (
          <button
            onClick={() => setSubTab('correlations')}
            className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-all ${
              subTab === 'correlations'
                ? 'bg-blue-600 text-white shadow-xs'
                : 'bg-white text-slate-600 border border-slate-200 hover:bg-slate-50'
            }`}
          >
            <Flame className="w-3.5 h-3.5 text-amber-500" />
            <span>Strong Correlations ({strongCorrelations.length})</span>
          </button>
        )}
      </div>

      {/* Numerical Stats Table */}
      {subTab === 'numerical' && (
        <div className="bg-white border border-slate-200 rounded-2xl shadow-xs overflow-hidden">
          <div className="p-4 border-b border-slate-100 flex items-center justify-between">
            <h3 className="text-xs font-bold text-slate-700 uppercase tracking-wider">
              Descriptive Statistics for Numerical Features
            </h3>
            <span className="text-[11px] text-slate-400">Values rounded to 2 decimals</span>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse text-xs">
              <thead className="bg-slate-50 border-b border-slate-200 text-slate-600">
                <tr>
                  <th className="py-2.5 px-3 font-semibold">Column</th>
                  <th className="py-2.5 px-3 font-semibold">Count</th>
                  <th className="py-2.5 px-3 font-semibold">Mean</th>
                  <th className="py-2.5 px-3 font-semibold">Median</th>
                  <th className="py-2.5 px-3 font-semibold">Min</th>
                  <th className="py-2.5 px-3 font-semibold">Max</th>
                  <th className="py-2.5 px-3 font-semibold">Std Dev</th>
                  <th className="py-2.5 px-3 font-semibold">IQR</th>
                  <th className="py-2.5 px-3 font-semibold">Skewness</th>
                  <th className="py-2.5 px-3 font-semibold">Outliers</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 font-mono">
                {(numericalStats || []).map((stat) => (
                  <tr key={stat.column} className="hover:bg-slate-50/80 transition-colors">
                    <td className="py-2 px-3 font-semibold text-slate-800 font-sans">{stat.column}</td>
                    <td className="py-2 px-3 text-slate-600">{stat.count?.toLocaleString()}</td>
                    <td className="py-2 px-3 font-semibold text-blue-600">{stat.mean?.toLocaleString()}</td>
                    <td className="py-2 px-3 text-slate-700">{stat.median?.toLocaleString()}</td>
                    <td className="py-2 px-3 text-slate-500">{stat.min?.toLocaleString()}</td>
                    <td className="py-2 px-3 text-slate-900 font-semibold">{stat.max?.toLocaleString()}</td>
                    <td className="py-2 px-3 text-slate-500">{stat.std?.toLocaleString()}</td>
                    <td className="py-2 px-3 text-slate-500">{stat.iqr?.toLocaleString()}</td>
                    <td className="py-2 px-3">
                      <span className={`px-1.5 py-0.5 rounded text-[10px] font-sans ${
                        Math.abs(stat.skewness) > 1 ? 'bg-amber-50 text-amber-700 font-semibold' : 'text-slate-600'
                      }`}>
                        {stat.skewness}
                      </span>
                    </td>
                    <td className="py-2 px-3">
                      {stat.outliers_count > 0 ? (
                        <span className="px-2 py-0.5 rounded-full text-[10px] font-semibold bg-rose-50 text-rose-700 font-sans">
                          {stat.outliers_count} points
                        </span>
                      ) : (
                        <span className="text-slate-400 text-[10px] font-sans">0</span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Categorical Stats Table */}
      {subTab === 'categorical' && (
        <div className="bg-white border border-slate-200 rounded-2xl shadow-xs overflow-hidden">
          <div className="p-4 border-b border-slate-100 flex items-center justify-between">
            <h3 className="text-xs font-bold text-slate-700 uppercase tracking-wider">
              Categorical Features & Frequency Distributions
            </h3>
            <span className="text-[11px] text-slate-400">Showing top values and category shares</span>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse text-xs">
              <thead className="bg-slate-50 border-b border-slate-200 text-slate-600">
                <tr>
                  <th className="py-2.5 px-3 font-semibold">Column</th>
                  <th className="py-2.5 px-3 font-semibold">Unique Items</th>
                  <th className="py-2.5 px-3 font-semibold">Most Frequent (Mode)</th>
                  <th className="py-2.5 px-3 font-semibold">Frequency</th>
                  <th className="py-2.5 px-3 font-semibold">Concentration</th>
                  <th className="py-2.5 px-3 font-semibold">Top 5 Categories Breakdown</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {(categoricalStats || []).map((cat) => (
                  <tr key={cat.column} className="hover:bg-slate-50/80 transition-colors">
                    <td className="py-3 px-3 font-semibold text-slate-800">{cat.column}</td>
                    <td className="py-3 px-3 font-mono font-medium">{cat.unique_count}</td>
                    <td className="py-3 px-3 font-medium text-slate-700">
                      <span className="px-2 py-0.5 rounded bg-slate-100 text-slate-800 font-mono text-[11px]">
                        {cat.top_value}
                      </span>
                    </td>
                    <td className="py-3 px-3 font-mono">{cat.top_frequency?.toLocaleString()}</td>
                    <td className="py-3 px-3">
                      <div className="flex items-center gap-2">
                        <div className="w-16 bg-slate-100 rounded-full h-1.5 overflow-hidden">
                          <div className="bg-blue-600 h-1.5 rounded-full" style={{ width: `${cat.top_percentage}%` }}></div>
                        </div>
                        <span className="text-[10px] font-mono text-slate-600">{cat.top_percentage}%</span>
                      </div>
                    </td>
                    <td className="py-3 px-3">
                      <div className="flex flex-wrap gap-1 max-w-md">
                        {cat.top_breakdown?.map((b, bIdx) => (
                          <span
                            key={bIdx}
                            className="inline-flex items-center gap-1 px-1.5 py-0.5 rounded text-[10px] bg-slate-50 border border-slate-200 text-slate-600"
                          >
                            <span className="font-medium truncate max-w-[90px]">{b.value}</span>
                            <span className="text-slate-400 font-mono">({b.percentage}%)</span>
                          </span>
                        ))}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Correlations Table */}
      {subTab === 'correlations' && (
        <div className="bg-white border border-slate-200 rounded-2xl shadow-xs overflow-hidden">
          <div className="p-4 border-b border-slate-100 flex items-center justify-between">
            <h3 className="text-xs font-bold text-slate-700 uppercase tracking-wider">
              Strong Linear Dependencies (|r| ≥ 0.4)
            </h3>
            <span className="text-[11px] text-slate-400">Pearson Correlation Coefficients</span>
          </div>
          <div className="divide-y divide-slate-100">
            {(strongCorrelations || []).map((sc, idx) => (
              <div key={idx} className="p-4 flex items-center justify-between hover:bg-slate-50 transition-colors">
                <div className="flex items-center gap-4">
                  <div className={`w-8 h-8 rounded-lg flex items-center justify-center font-mono font-bold text-xs ${
                    sc.correlation > 0 ? 'bg-blue-50 text-blue-700 border border-blue-200' : 'bg-rose-50 text-rose-700 border border-rose-200'
                  }`}>
                    {sc.correlation.toFixed(2)}
                  </div>
                  <div>
                    <div className="text-sm font-bold text-slate-800">
                      {sc.col1} <span className="text-slate-400 font-normal">and</span> {sc.col2}
                    </div>
                    <div className="text-xs text-slate-500">
                      {sc.relationship} relationship
                    </div>
                  </div>
                </div>
                <span className={`px-2.5 py-1 rounded-full text-xs font-semibold ${
                  Math.abs(sc.correlation) >= 0.7
                    ? 'bg-emerald-100 text-emerald-800'
                    : 'bg-blue-100 text-blue-800'
                }`}>
                  {sc.relationship}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
