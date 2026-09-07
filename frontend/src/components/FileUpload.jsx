import React, { useState, useRef } from 'react';
import { UploadCloud, FileSpreadsheet, Sparkles, Database, Check, AlertCircle, ArrowRight } from 'lucide-react';
import { uploadDataset } from '../api';

export default function FileUpload({ onDatasetLoaded, onSelectSample, loading, setLoading }) {
  const [dragActive, setDragActive] = useState(false);
  const [error, setError] = useState(null);
  const inputRef = useRef(null);

  const handleFiles = async (file) => {
    if (!file) return;

    const validExtensions = ['.csv', '.xlsx', '.xls'];
    const hasValidExt = validExtensions.some(ext => file.name.toLowerCase().endsWith(ext));

    if (!hasValidExt) {
      setError('Please upload a valid CSV (.csv) or Excel (.xlsx, .xls) file.');
      return;
    }

    if (file.size > 50 * 1024 * 1024) {
      setError('File size exceeds the 50MB limit.');
      return;
    }

    setError(null);
    setLoading(true);

    try {
      const data = await uploadDataset(file);
      onDatasetLoaded(data);
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || 'Failed to parse and analyze file. Please check formatting.');
    } finally {
      setLoading(false);
    }
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFiles(e.dataTransfer.files[0]);
    }
  };

  const handleChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFiles(e.target.files[0]);
    }
  };

  return (
    <div className="max-w-4xl mx-auto py-10 px-4">
      {/* Hero title */}
      <div className="text-center mb-8">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-50 border border-blue-200/60 text-blue-700 text-xs font-semibold mb-3 shadow-xs">
          <Sparkles className="w-3.5 h-3.5" />
          Autonomous AI Data Analyst
        </div>
        <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight sm:text-4xl">
          Analyze Any Dataset in Seconds
        </h1>
        <p className="mt-2 text-base text-slate-500 max-w-xl mx-auto">
          Upload your raw CSV or Excel sheet. We'll automatically detect data types, clean anomalies, compute distributions, and uncover actionable insights.
        </p>
      </div>

      {/* Upload Dropzone */}
      <div
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        onClick={() => inputRef.current?.click()}
        className={`relative border-2 border-dashed rounded-2xl p-10 text-center cursor-pointer transition-all bg-white ${
          dragActive
            ? 'border-blue-500 bg-blue-50/50 scale-[1.01]'
            : 'border-slate-300 hover:border-slate-400 hover:bg-slate-50/50'
        } ${loading ? 'opacity-60 pointer-events-none' : ''}`}
      >
        <input
          ref={inputRef}
          type="file"
          accept=".csv,.xlsx,.xls"
          onChange={handleChange}
          className="hidden"
        />

        <div className="w-16 h-16 rounded-2xl bg-blue-50 text-blue-600 mx-auto flex items-center justify-center mb-4 shadow-sm">
          <UploadCloud className="w-8 h-8 animate-bounce-slow" />
        </div>

        <h3 className="text-lg font-semibold text-slate-800 mb-1">
          {loading ? 'Analyzing Dataset...' : 'Click to browse or drag and drop'}
        </h3>
        <p className="text-sm text-slate-500 mb-4">
          Structured CSV or Excel worksheets up to 50MB
        </p>

        <div className="flex items-center justify-center gap-3 text-xs text-slate-400 font-medium">
          <span className="flex items-center gap-1">
            <Check className="w-3.5 h-3.5 text-emerald-500" /> Automatic Type Inference
          </span>
          <span>•</span>
          <span className="flex items-center gap-1">
            <Check className="w-3.5 h-3.5 text-emerald-500" /> Plotly Visualizations
          </span>
          <span>•</span>
          <span className="flex items-center gap-1">
            <Check className="w-3.5 h-3.5 text-emerald-500" /> Instant Q&A
          </span>
        </div>

        {loading && (
          <div className="absolute inset-0 bg-white/80 backdrop-blur-xs rounded-2xl flex flex-col items-center justify-center">
            <div className="w-10 h-10 border-3 border-blue-600 border-t-transparent rounded-full animate-spin mb-3"></div>
            <p className="text-sm font-semibold text-slate-700">Profiling rows, distributions & correlations...</p>
          </div>
        )}
      </div>

      {/* Error Banner */}
      {error && (
        <div className="mt-4 p-4 rounded-xl bg-red-50 border border-red-200 text-red-700 flex items-center gap-3 text-sm">
          <AlertCircle className="w-5 h-5 text-red-500 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* One-Click Sample Datasets */}
      <div className="mt-10">
        <div className="flex items-center gap-2 mb-4">
          <Database className="w-4 h-4 text-blue-600" />
          <h2 className="text-sm font-bold text-slate-800 uppercase tracking-wider">
            Or test immediately with bundled datasets
          </h2>
        </div>

        <div className="grid sm:grid-cols-2 gap-4">
          {/* Sample 1: Sales */}
          <div
            onClick={() => onSelectSample('sales_performance.csv')}
            className="p-5 bg-white border border-slate-200 rounded-xl hover:border-blue-300 hover:shadow-md transition-all cursor-pointer group"
          >
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center gap-2">
                <FileSpreadsheet className="w-5 h-5 text-emerald-600" />
                <span className="font-semibold text-slate-800 text-sm">sales_performance.csv</span>
              </div>
              <span className="text-[11px] font-mono font-medium px-2 py-0.5 rounded-full bg-slate-100 text-slate-600">
                50 rows • 10 cols
              </span>
            </div>
            <p className="text-xs text-slate-500 mb-3">
              Multi-region retail performance tracking revenue, products, discounts, and net profits over 2024.
            </p>
            <div className="flex items-center text-xs font-semibold text-blue-600 group-hover:translate-x-1 transition-transform">
              <span>Load sample dataset</span>
              <ArrowRight className="w-3.5 h-3.5 ml-1" />
            </div>
          </div>

          {/* Sample 2: Churn */}
          <div
            onClick={() => onSelectSample('customer_churn.xlsx')}
            className="p-5 bg-white border border-slate-200 rounded-xl hover:border-blue-300 hover:shadow-md transition-all cursor-pointer group"
          >
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center gap-2">
                <FileSpreadsheet className="w-5 h-5 text-blue-600" />
                <span className="font-semibold text-slate-800 text-sm">customer_churn.xlsx</span>
              </div>
              <span className="text-[11px] font-mono font-medium px-2 py-0.5 rounded-full bg-slate-100 text-slate-600">
                40 rows • 9 cols
              </span>
            </div>
            <p className="text-xs text-slate-500 mb-3">
              Subscription customer metrics analyzing tenure, contract type, monthly charges, and churn probability.
            </p>
            <div className="flex items-center text-xs font-semibold text-blue-600 group-hover:translate-x-1 transition-transform">
              <span>Load sample dataset</span>
              <ArrowRight className="w-3.5 h-3.5 ml-1" />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
