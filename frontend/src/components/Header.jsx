import React, { useEffect, useState } from 'react';
import { getSamples, loadSample, getHealth } from '../api';
import { Database, FileSpreadsheet, PlusCircle, CheckCircle2, AlertCircle, RefreshCw } from 'lucide-react';

export default function Header({
  activeTab,
  datasetInfo,
  onLoadDataset,
  onResetUpload,
  loading
}) {
  const [samples, setSamples] = useState([]);
  const [health, setHealth] = useState(null);
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  useEffect(() => {
    getSamples().then(data => setSamples(data.samples || [])).catch(() => {});
    getHealth().then(setHealth).catch(() => setHealth({ status: 'offline' }));
  }, []);

  const handleSelectSample = async (sampleName) => {
    setIsMenuOpen(false);
    await onLoadDataset(sampleName);
  };

  const tabTitles = {
    upload: 'Upload & Select Dataset',
    overview: 'Dataset Overview & Structure',
    statistics: 'Statistical Analysis & Metrics',
    visualizations: 'Interactive Data Visualizations',
    insights: 'Automated AI Insights & Findings',
    ask: 'Ask Natural Language Questions',
  };

  return (
    <header className="h-16 bg-white border-b border-slate-200 px-6 flex items-center justify-between shrink-0">
      {/* Title & Section */}
      <div>
        <h2 className="text-base font-semibold text-slate-800 tracking-tight">
          {tabTitles[activeTab] || 'Dashboard'}
        </h2>
      </div>

      {/* Right controls */}
      <div className="flex items-center gap-3">
        {/* Backend health status pill */}
        <div className="hidden sm:flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium bg-emerald-50 text-emerald-700 border border-emerald-200/60">
          <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
          <span>FastAPI Engine</span>
          {health?.has_llm_configured && (
            <span className="ml-1 text-[10px] bg-emerald-200/60 px-1 py-0.2 rounded font-bold">LLM+</span>
          )}
        </div>

        {/* Try Sample Dropdown */}
        {samples.length > 0 && (
          <div className="relative">
            <button
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              disabled={loading}
              className="flex items-center gap-2 px-3 py-1.5 text-xs font-medium text-slate-700 bg-slate-100 hover:bg-slate-200 rounded-lg transition-colors border border-slate-200/80"
            >
              <Database className="w-3.5 h-3.5 text-blue-600" />
              <span>Sample Datasets</span>
            </button>

            {isMenuOpen && (
              <div className="absolute right-0 mt-2 w-64 bg-white border border-slate-200 rounded-xl shadow-xl py-2 z-50">
                <div className="px-3 py-1 text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
                  Quick Load Demo
                </div>
                {samples.map((s) => (
                  <button
                    key={s.name}
                    onClick={() => handleSelectSample(s.name)}
                    className="w-full text-left px-3 py-2 text-xs hover:bg-blue-50 transition-colors flex flex-col gap-0.5"
                  >
                    <div className="flex items-center justify-between font-medium text-slate-800">
                      <span>{s.name}</span>
                      <span className="text-[10px] font-mono text-slate-400">{s.size_kb} KB</span>
                    </div>
                    <span className="text-[11px] text-slate-500 line-clamp-1">{s.description}</span>
                  </button>
                ))}
              </div>
            )}
          </div>
        )}

        {/* New Upload Button */}
        {datasetInfo && (
          <button
            onClick={onResetUpload}
            className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-blue-600 bg-blue-50 hover:bg-blue-100 rounded-lg transition-colors border border-blue-200/60"
          >
            <PlusCircle className="w-3.5 h-3.5" />
            <span>New Dataset</span>
          </button>
        )}
      </div>
    </header>
  );
}
