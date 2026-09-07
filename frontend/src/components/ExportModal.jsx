import React from 'react';
import { getExportUrl } from '../api';
import { X, Download, FileSpreadsheet, FileJson, Check } from 'lucide-react';

export default function ExportModal({ isOpen, onClose, datasetId, filename }) {
  if (!isOpen) return null;

  const baseName = filename ? filename.replace(/\.[^/.]+$/, '') : 'dataset';

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 backdrop-blur-xs p-4">
      <div className="bg-white rounded-2xl shadow-2xl border border-slate-200 w-full max-w-md overflow-hidden animate-in fade-in zoom-in-95 duration-150">
        {/* Header */}
        <div className="p-5 border-b border-slate-100 flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-lg bg-blue-50 text-blue-600 flex items-center justify-center">
              <Download className="w-4 h-4" />
            </div>
            <div>
              <h3 className="text-sm font-bold text-slate-900">Export & Download</h3>
              <p className="text-xs text-slate-500">Download data files and analytical reports</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="text-slate-400 hover:text-slate-600 p-1 rounded-lg hover:bg-slate-100 transition-colors"
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
            className="flex items-start gap-4 p-4 rounded-xl border border-slate-200 hover:border-blue-400 hover:bg-blue-50/40 transition-all group"
          >
            <div className="w-10 h-10 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center shrink-0 group-hover:scale-105 transition-transform">
              <FileSpreadsheet className="w-5 h-5" />
            </div>
            <div className="flex-1">
              <div className="text-xs font-bold text-slate-900 flex items-center justify-between">
                <span>Cleaned Dataset (CSV)</span>
                <span className="text-[10px] text-emerald-600 font-mono font-semibold">.CSV</span>
              </div>
              <p className="text-[11px] text-slate-500 mt-0.5">
                Processed, deduplicated and imputed dataset ready for machine learning or reporting.
              </p>
            </div>
          </a>

          {/* Export Option 2: Analytical Report JSON */}
          <a
            href={getExportUrl(datasetId, 'json')}
            download={`report_${baseName}.json`}
            className="flex items-start gap-4 p-4 rounded-xl border border-slate-200 hover:border-blue-400 hover:bg-blue-50/40 transition-all group"
          >
            <div className="w-10 h-10 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center shrink-0 group-hover:scale-105 transition-transform">
              <FileJson className="w-5 h-5" />
            </div>
            <div className="flex-1">
              <div className="text-xs font-bold text-slate-900 flex items-center justify-between">
                <span>Executive Analysis Report (JSON)</span>
                <span className="text-[10px] text-blue-600 font-mono font-semibold">.JSON</span>
              </div>
              <p className="text-[11px] text-slate-500 mt-0.5">
                Full statistical profile, column distributions, correlations, and AI generated insights.
              </p>
            </div>
          </a>
        </div>

        {/* Footer */}
        <div className="p-4 bg-slate-50 border-t border-slate-100 flex items-center justify-end">
          <button
            onClick={onClose}
            className="px-4 py-2 bg-slate-200 hover:bg-slate-300 text-slate-700 rounded-lg text-xs font-medium transition-colors"
          >
            Done
          </button>
        </div>
      </div>
    </div>
  );
}
