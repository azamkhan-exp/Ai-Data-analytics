import React from 'react';
import { getExportUrl } from '../api';
import { X, Download, FileSpreadsheet, FileJson } from 'lucide-react';

export default function ExportModal({ isOpen, onClose, datasetId, filename }) {
  if (!isOpen) return null;

  const baseName = filename ? filename.replace(/\.[^/.]+$/, '') : 'dataset';

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/60 backdrop-blur-xs p-4">
      <div className="bg-white dark:bg-slate-900 rounded-3xl shadow-2xl border border-slate-200 dark:border-slate-800 w-full max-w-md overflow-hidden animate-in fade-in zoom-in-95 duration-150 transition-colors duration-200">
        {/* Header */}
        <div className="p-5 border-b border-slate-100 dark:border-slate-800 flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-xl bg-blue-50 dark:bg-blue-950/60 text-blue-600 dark:text-blue-400 flex items-center justify-center">
              <Download className="w-4 h-4" />
            </div>
            <div>
              <h3 className="text-sm font-bold text-slate-900 dark:text-slate-100">Export & Download</h3>
              <p className="text-xs text-slate-500 dark:text-slate-400">Export cleansed data or the full analytical report</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 p-1.5 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors cursor-pointer"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Content options */}
        <div className="p-5 space-y-3">
          {/* Export Option 1: Cleaned CSV */}
          <a
            href={getExportUrl(datasetId, 'csv')}
            download={`cleaned_${baseName}.csv`}
            className="flex items-start gap-4 p-4 rounded-2xl border border-slate-200 dark:border-slate-800 hover:border-blue-400 dark:hover:border-blue-600 hover:bg-blue-50/40 dark:hover:bg-slate-800/60 transition-all group"
          >
            <div className="w-10 h-10 rounded-xl bg-emerald-50 dark:bg-emerald-950/60 text-emerald-600 dark:text-emerald-400 flex items-center justify-center shrink-0 group-hover:scale-105 transition-transform">
              <FileSpreadsheet className="w-5 h-5" />
            </div>
            <div className="flex-1">
              <div className="text-xs font-bold text-slate-900 dark:text-slate-100 flex items-center justify-between">
                <span>Cleaned Dataset (CSV)</span>
                <span className="text-[10px] text-emerald-600 dark:text-emerald-400 font-mono font-bold">.CSV</span>
              </div>
              <p className="text-[11px] text-slate-500 dark:text-slate-400 mt-0.5">
                Processed, deduplicated and imputed dataset ready for downstream analysis or machine learning.
              </p>
            </div>
          </a>

          {/* Export Option 2: Analytical Report JSON */}
          <a
            href={getExportUrl(datasetId, 'json')}
            download={`report_${baseName}.json`}
            className="flex items-start gap-4 p-4 rounded-2xl border border-slate-200 dark:border-slate-800 hover:border-blue-400 dark:hover:border-blue-600 hover:bg-blue-50/40 dark:hover:bg-slate-800/60 transition-all group"
          >
            <div className="w-10 h-10 rounded-xl bg-blue-50 dark:bg-blue-950/60 text-blue-600 dark:text-blue-400 flex items-center justify-center shrink-0 group-hover:scale-105 transition-transform">
              <FileJson className="w-5 h-5" />
            </div>
            <div className="flex-1">
              <div className="text-xs font-bold text-slate-900 dark:text-slate-100 flex items-center justify-between">
                <span>Executive Analysis Report (JSON)</span>
                <span className="text-[10px] text-blue-600 dark:text-blue-400 font-mono font-bold">.JSON</span>
              </div>
              <p className="text-[11px] text-slate-500 dark:text-slate-400 mt-0.5">
                Full statistical profile, moments, column distributions, correlations, and AI insights.
              </p>
            </div>
          </a>
        </div>

        {/* Footer */}
        <div className="p-4 bg-slate-50 dark:bg-slate-800/60 border-t border-slate-100 dark:border-slate-800 flex items-center justify-end">
          <button
            onClick={onClose}
            className="px-4 py-2 bg-slate-200 dark:bg-slate-700 hover:bg-slate-300 dark:hover:bg-slate-600 text-slate-700 dark:text-slate-200 rounded-xl text-xs font-bold transition-colors cursor-pointer"
          >
            Done
          </button>
        </div>
      </div>
    </div>
  );
}
