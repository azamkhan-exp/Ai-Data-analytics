import React, { useEffect, useState } from 'react';
import { getSamples, getHealth } from '../api';
import { 
  Database, 
  PlusCircle, 
  CheckCircle2, 
  Sparkles, 
  Sun, 
  Moon, 
  Menu, 
  X 
} from 'lucide-react';

export default function Header({
  activeTab,
  datasetInfo,
  onLoadDataset,
  onResetUpload,
  loading,
  isMobileNavOpen,
  setIsMobileNavOpen,
  isDark,
  setIsDark
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
    upload: 'Upload & Ingest Dataset',
    overview: 'Executive Dashboard & Overview',
    explorer: 'Data Explorer & Dictionary 2.0',
    statistics: 'Descriptive Moments & Statistics',
    visualizations: 'Visual Analytics & Chart Builder',
    anomalies: 'Anomaly Detection Center',
    quality: 'Data Quality & Hygiene Diagnostic',
    insights: 'Automated & AI Insights',
    ask: 'Ask Your Data 2.0',
  };

  return (
    <header className="h-16 bg-white dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800 px-4 md:px-6 flex items-center justify-between shrink-0 z-20 transition-colors duration-200">
      {/* Mobile Toggle & Section Title */}
      <div className="flex items-center gap-3">
        <button
          onClick={() => setIsMobileNavOpen(!isMobileNavOpen)}
          className="md:hidden p-2 rounded-xl text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-100 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors cursor-pointer"
          aria-label="Toggle navigation"
        >
          {isMobileNavOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
        </button>

        <h2 className="text-sm md:text-base font-bold text-slate-800 dark:text-slate-100 tracking-tight truncate max-w-[180px] sm:max-w-xs md:max-w-none">
          {tabTitles[activeTab] || 'Dashboard'}
        </h2>
      </div>

      {/* Right controls */}
      <div className="flex items-center gap-2 sm:gap-3">
        {/* Production Status Badge */}
        <div className="hidden lg:flex items-center gap-2 px-3 py-1 rounded-full text-[11px] font-semibold bg-slate-100/90 dark:bg-slate-800/90 border border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-300">
          <span className="flex items-center gap-1.5 text-slate-700 dark:text-slate-200">
            <span className="w-1.5 h-1.5 rounded-full bg-slate-400 dark:bg-slate-500"></span>
            Database: Not Required
          </span>
          <span className="text-slate-300 dark:text-slate-600">•</span>
          <span className="text-blue-600 dark:text-blue-400 flex items-center gap-1">
            <Sparkles className="w-3 h-3" />
            AI: Optional
          </span>
          <span className="text-slate-300 dark:text-slate-600">•</span>
          <span className="text-emerald-600 dark:text-emerald-400 flex items-center gap-1">
            <CheckCircle2 className="w-3 h-3" />
            Engine: Python (FastAPI + Pandas)
          </span>
        </div>

        {/* Theme Switcher */}
        <button
          onClick={() => setIsDark(!isDark)}
          className="p-2 rounded-xl text-slate-500 dark:text-slate-400 hover:text-slate-800 dark:hover:text-slate-100 bg-slate-100 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 transition-colors cursor-pointer"
          title={isDark ? 'Switch to Light Mode' : 'Switch to Dark Mode'}
          aria-label="Toggle color theme"
        >
          {isDark ? <Sun className="w-4 h-4 text-amber-400" /> : <Moon className="w-4 h-4 text-slate-600" />}
        </button>

        {/* Sample Datasets Dropdown */}
        {samples.length > 0 && (
          <div className="relative">
            <button
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              disabled={loading}
              className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-bold text-slate-700 dark:text-slate-200 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 rounded-xl transition-colors border border-slate-200 dark:border-slate-700 disabled:opacity-50 cursor-pointer"
            >
              <Database className="w-3.5 h-3.5 text-blue-600 dark:text-blue-400 shrink-0" />
              <span className="hidden sm:inline">Samples</span>
            </button>

            {isMenuOpen && (
              <div className="absolute right-0 mt-2 w-72 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-2xl py-2 z-50 animate-in fade-in zoom-in-95 duration-100">
                <div className="px-3.5 py-1.5 text-[10px] font-extrabold text-slate-400 dark:text-slate-500 uppercase tracking-wider">
                  Instant 1-Click Demo
                </div>
                {samples.map((s) => (
                  <button
                    key={s.name}
                    onClick={() => handleSelectSample(s.name)}
                    className="w-full text-left px-3.5 py-2.5 text-xs hover:bg-blue-50 dark:hover:bg-slate-800/60 transition-colors flex flex-col gap-0.5 cursor-pointer"
                  >
                    <div className="flex items-center justify-between font-bold text-slate-800 dark:text-slate-100">
                      <span>{s.name}</span>
                      <span className="text-[10px] font-mono text-slate-400">{s.size_kb} KB</span>
                    </div>
                    <span className="text-[11px] text-slate-500 dark:text-slate-400 line-clamp-1">{s.description}</span>
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
            className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-bold text-blue-600 dark:text-blue-400 bg-blue-50 dark:bg-blue-950/50 hover:bg-blue-100 dark:hover:bg-blue-900/50 rounded-xl transition-colors border border-blue-200/80 dark:border-blue-800/80 cursor-pointer"
          >
            <PlusCircle className="w-3.5 h-3.5 shrink-0" />
            <span className="hidden sm:inline">New Upload</span>
            <span className="sm:hidden">New</span>
          </button>
        )}
      </div>
    </header>
  );
}
