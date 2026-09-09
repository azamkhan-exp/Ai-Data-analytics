import React from 'react';
import { AlertOctagon, ShieldAlert, CheckCircle2, TrendingDown, Activity, Cpu } from 'lucide-react';

export default function AnomaliesView({ anomalySummary = {}, numericalStats = [] }) {
  const { 
    total_anomalies = 0, 
    affected_columns = [], 
    affected_rows_count = 0, 
    anomaly_percentage = 0.0,
    ml_anomalies_detected = 0
  } = anomalySummary;

  return (
    <div className="space-y-6">
      {/* Top Banner KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="p-5 rounded-3xl bg-white dark:bg-slate-900 border border-slate-200/90 dark:border-slate-800 shadow-xs">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-bold text-slate-500 dark:text-slate-400">Total Detected Anomalies</span>
            <div className="w-8 h-8 rounded-xl bg-amber-50 dark:bg-amber-950/40 text-amber-600 dark:text-amber-400 flex items-center justify-center">
              <AlertOctagon className="w-4 h-4" />
            </div>
          </div>
          <div className="text-2xl font-extrabold text-slate-900 dark:text-slate-100">
            {total_anomalies.toLocaleString()}
          </div>
          <div className="text-[11px] text-slate-400 dark:text-slate-500 mt-0.5">
            Tukey 1.5× IQR + Gaussian Z-Score
          </div>
        </div>

        <div className="p-5 rounded-3xl bg-white dark:bg-slate-900 border border-slate-200/90 dark:border-slate-800 shadow-xs">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-bold text-slate-500 dark:text-slate-400">Affected Records</span>
            <div className="w-8 h-8 rounded-xl bg-rose-50 dark:bg-rose-950/40 text-rose-600 dark:text-rose-400 flex items-center justify-center">
              <TrendingDown className="w-4 h-4" />
            </div>
          </div>
          <div className="text-2xl font-extrabold text-slate-900 dark:text-slate-100">
            {affected_rows_count.toLocaleString()} rows
          </div>
          <div className="text-[11px] text-slate-400 dark:text-slate-500 mt-0.5">
            {anomaly_percentage}% of total dataset records
          </div>
        </div>

        <div className="p-5 rounded-3xl bg-white dark:bg-slate-900 border border-slate-200/90 dark:border-slate-800 shadow-xs">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-bold text-slate-500 dark:text-slate-400">Affected Numerical Features</span>
            <div className="w-8 h-8 rounded-xl bg-blue-50 dark:bg-blue-950/40 text-blue-600 dark:text-blue-400 flex items-center justify-center">
              <Activity className="w-4 h-4" />
            </div>
          </div>
          <div className="text-2xl font-extrabold text-slate-900 dark:text-slate-100">
            {affected_columns.length} columns
          </div>
          <div className="text-[11px] text-slate-400 dark:text-slate-500 mt-0.5">
            Exhibiting tail outliers
          </div>
        </div>

        <div className="p-5 rounded-3xl bg-white dark:bg-slate-900 border border-slate-200/90 dark:border-slate-800 shadow-xs">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-bold text-slate-500 dark:text-slate-400">Isolation Forest (ML)</span>
            <div className="w-8 h-8 rounded-xl bg-purple-50 dark:bg-purple-950/40 text-purple-600 dark:text-purple-400 flex items-center justify-center">
              <Cpu className="w-4 h-4" />
            </div>
          </div>
          <div className="text-2xl font-extrabold text-slate-900 dark:text-slate-100">
            {ml_anomalies_detected.toLocaleString()}
          </div>
          <div className="text-[11px] text-slate-400 dark:text-slate-500 mt-0.5">
            scikit-learn ensemble outliers
          </div>
        </div>
      </div>

      {/* Anomaly Diagnosis Cards */}
      <div className="bg-white dark:bg-slate-900 border border-slate-200/90 dark:border-slate-800 rounded-3xl shadow-xs p-6 space-y-4">
        <div className="flex items-center gap-2">
          <ShieldAlert className="w-4 h-4 text-amber-500" />
          <h3 className="text-sm font-bold text-slate-900 dark:text-slate-100">
            Feature Anomaly Diagnosis & Boundaries
          </h3>
        </div>

        {affected_columns.length === 0 ? (
          <div className="p-8 text-center text-emerald-600 dark:text-emerald-400 flex flex-col items-center gap-2">
            <CheckCircle2 className="w-8 h-8" />
            <span className="font-bold text-sm">Zero anomalous data points detected across all numerical columns!</span>
            <span className="text-xs text-slate-400">All data points fall cleanly within standard variance boundaries.</span>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-1">
            {affected_columns.map(ac => (
              <div
                key={ac.column}
                className="p-4 rounded-2xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200/80 dark:border-slate-700/80 space-y-3"
              >
                <div className="flex items-center justify-between">
                  <span className="font-bold text-slate-900 dark:text-slate-100 text-sm font-mono">{ac.column}</span>
                  <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-amber-100 dark:bg-amber-950 text-amber-800 dark:text-amber-300 border border-amber-200 dark:border-amber-800">
                    {ac.iqr_count} IQR • {ac.zscore_count} Z-Score
                  </span>
                </div>

                <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
                  {ac.explanation}
                </p>

                <div className="flex items-center justify-between pt-2 border-t border-slate-200 dark:border-slate-700 text-xs text-slate-500 dark:text-slate-400 font-mono">
                  <span>IQR Lower: {ac.lower_bound}</span>
                  <span>IQR Upper: {ac.upper_bound}</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
