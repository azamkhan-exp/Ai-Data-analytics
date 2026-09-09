import React, { useState } from 'react';
import { cleanDataset } from '../api';
import { X, SlidersHorizontal, Check, AlertTriangle, Sparkles, CheckCircle2 } from 'lucide-react';

export default function DataCleanerModal({ isOpen, onClose, datasetId, onDatasetCleaned }) {
  const [dropDuplicates, setDropDuplicates] = useState(true);
  const [fillNumerical, setFillNumerical] = useState('mean');
  const [fillCategorical, setFillCategorical] = useState('mode');
  const [dropNaRows, setDropNaRows] = useState(false);
  const [dropHighMissing, setDropHighMissing] = useState(false);
  const [loading, setLoading] = useState(false);
  const [log, setLog] = useState(null);

  if (!isOpen) return null;

  const handleApplyClean = async () => {
    setLoading(true);
    setLog(null);
    try {
      const res = await cleanDataset(datasetId, {
        drop_duplicates: dropDuplicates,
        fill_missing_numerical: fillNumerical,
        fill_missing_categorical: fillCategorical,
        drop_na_rows: dropNaRows,
        drop_high_missing_cols_threshold: dropHighMissing ? 0.5 : null,
      });
      setLog(res.changes_log || ['Dataset cleaned successfully with no records altered.']);
      onDatasetCleaned(res.analysis);
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to clean dataset.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/60 backdrop-blur-xs p-4">
      <div className="bg-white dark:bg-slate-900 rounded-3xl shadow-2xl border border-slate-200 dark:border-slate-800 w-full max-w-lg overflow-hidden animate-in fade-in zoom-in-95 duration-150 transition-colors duration-200">
        {/* Modal Header */}
        <div className="p-5 border-b border-slate-100 dark:border-slate-800 flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-xl bg-blue-50 dark:bg-blue-950/60 text-blue-600 dark:text-blue-400 flex items-center justify-center">
              <SlidersHorizontal className="w-4 h-4" />
            </div>
            <div>
              <h3 className="text-sm font-bold text-slate-900 dark:text-slate-100">Clean & Preprocess Dataset</h3>
              <p className="text-xs text-slate-500 dark:text-slate-400">In-memory deduplication and missing value imputation</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 p-1.5 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors cursor-pointer"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Form Body */}
        <div className="p-5 space-y-4">
          {/* Drop Duplicates Toggle */}
          <label className="flex items-start gap-3 p-3.5 rounded-2xl border border-slate-200 dark:border-slate-800 hover:bg-slate-50 dark:hover:bg-slate-800/60 cursor-pointer transition-colors">
            <input
              type="checkbox"
              checked={dropDuplicates}
              onChange={(e) => setDropDuplicates(e.target.checked)}
              className="mt-0.5 rounded text-blue-600 focus:ring-blue-500"
            />
            <div>
              <div className="text-xs font-bold text-slate-800 dark:text-slate-200">Deduplicate Rows</div>
              <div className="text-[11px] text-slate-500 dark:text-slate-400">Remove redundant identical rows from in-memory session</div>
            </div>
          </label>

          {/* Fill Numerical Missing */}
          <div className="p-3.5 rounded-2xl border border-slate-200 dark:border-slate-800">
            <label className="block text-xs font-bold text-slate-800 dark:text-slate-200 mb-1.5">
              Impute Missing Numerical Values
            </label>
            <select
              value={fillNumerical}
              onChange={(e) => setFillNumerical(e.target.value)}
              className="w-full text-xs p-2.5 border border-slate-200 dark:border-slate-700 rounded-xl bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="none">Do not impute (leave nulls)</option>
              <option value="mean">Replace with Mean (Average)</option>
              <option value="median">Replace with Median</option>
              <option value="zero">Replace with Zero (0)</option>
            </select>
          </div>

          {/* Fill Categorical Missing */}
          <div className="p-3.5 rounded-2xl border border-slate-200 dark:border-slate-800">
            <label className="block text-xs font-bold text-slate-800 dark:text-slate-200 mb-1.5">
              Impute Missing Categorical Values
            </label>
            <select
              value={fillCategorical}
              onChange={(e) => setFillCategorical(e.target.value)}
              className="w-full text-xs p-2.5 border border-slate-200 dark:border-slate-700 rounded-xl bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="none">Do not impute (leave nulls)</option>
              <option value="mode">Replace with Most Frequent Value (Mode)</option>
              <option value="unknown">Replace with "Unknown"</option>
            </select>
          </div>

          {/* Drop NA rows */}
          <label className="flex items-start gap-3 p-3.5 rounded-2xl border border-slate-200 dark:border-slate-800 hover:bg-slate-50 dark:hover:bg-slate-800/60 cursor-pointer transition-colors">
            <input
              type="checkbox"
              checked={dropNaRows}
              onChange={(e) => setDropNaRows(e.target.checked)}
              className="mt-0.5 rounded text-blue-600 focus:ring-blue-500"
            />
            <div>
              <div className="text-xs font-bold text-slate-800 dark:text-slate-200">Drop Rows with Missing Values</div>
              <div className="text-[11px] text-slate-500 dark:text-slate-400">Discards any row containing empty cells</div>
            </div>
          </label>

          {/* Changes Log Notification */}
          {log && (
            <div className="p-3.5 bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-800 rounded-2xl text-xs text-emerald-800 dark:text-emerald-300 space-y-1">
              <div className="font-bold flex items-center gap-1.5">
                <CheckCircle2 className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
                <span>Transformations Applied:</span>
              </div>
              {log.map((item, idx) => (
                <div key={idx} className="text-[11px] pl-4">• {item}</div>
              ))}
            </div>
          )}
        </div>

        {/* Modal Footer */}
        <div className="p-4 bg-slate-50 dark:bg-slate-800/60 border-t border-slate-100 dark:border-slate-800 flex items-center justify-end gap-2">
          <button
            onClick={onClose}
            className="px-4 py-2 text-xs font-semibold text-slate-600 dark:text-slate-300 hover:text-slate-800 dark:hover:text-slate-100 transition-colors cursor-pointer"
          >
            Close
          </button>
          <button
            onClick={handleApplyClean}
            disabled={loading}
            className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-xl text-xs font-bold transition-colors shadow-xs disabled:opacity-50 flex items-center gap-1.5 cursor-pointer"
          >
            <Sparkles className="w-3.5 h-3.5" />
            <span>{loading ? 'Cleaning...' : 'Apply In-Memory Preprocessing'}</span>
          </button>
        </div>
      </div>
    </div>
  );
}
