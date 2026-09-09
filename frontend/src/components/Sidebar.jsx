import React from 'react';
import {
  BarChart3,
  BrainCircuit,
  FileSpreadsheet,
  FileUp,
  HelpCircle,
  Layers,
  Sparkles,
  Table,
  SlidersHorizontal,
  Download,
  X,
  AlertOctagon,
  ShieldCheck,
  Search
} from 'lucide-react';

export default function Sidebar({
  activeTab,
  setActiveTab,
  datasetInfo,
  onOpenCleaner,
  onOpenExport,
  isMobileNavOpen,
  setIsMobileNavOpen
}) {
  const menuItems = [
    { id: 'upload', label: 'Upload Dataset', icon: FileUp },
    { id: 'overview', label: 'Overview', icon: Layers, disabled: !datasetInfo },
    { id: 'explorer', label: 'Data Explorer', icon: Search, disabled: !datasetInfo },
    { id: 'visualizations', label: 'Visual Analytics', icon: BarChart3, disabled: !datasetInfo },
    { id: 'statistics', label: 'Statistics', icon: Table, disabled: !datasetInfo },
    { id: 'anomalies', label: 'Anomalies', icon: AlertOctagon, disabled: !datasetInfo },
    { id: 'quality', label: 'Data Quality', icon: ShieldCheck, disabled: !datasetInfo },
    { id: 'insights', label: 'AI Insights', icon: BrainCircuit, disabled: !datasetInfo },
    { id: 'ask', label: 'Ask Your Data', icon: HelpCircle, disabled: !datasetInfo },
  ];

  const handleSelectTab = (id) => {
    setActiveTab(id);
    if (setIsMobileNavOpen) setIsMobileNavOpen(false);
  };

  const content = (
    <div className="h-full flex flex-col justify-between select-none bg-white dark:bg-slate-900 transition-colors duration-200">
      {/* Brand & Navigation */}
      <div>
        {/* Brand Header */}
        <div className="h-16 flex items-center justify-between px-6 border-b border-slate-100 dark:border-slate-800">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-blue-600 flex items-center justify-center text-white shadow-md shadow-blue-500/20">
              <Sparkles className="w-5 h-5" />
            </div>
            <div>
              <h1 className="text-base font-extrabold text-slate-900 dark:text-slate-100 tracking-tight">InsightPulse</h1>
              <p className="text-[10px] font-bold text-slate-400 dark:text-slate-500 uppercase tracking-wider">AI Data Analyst</p>
            </div>
          </div>
          {isMobileNavOpen && (
            <button
              onClick={() => setIsMobileNavOpen(false)}
              className="md:hidden p-1 rounded-lg text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 cursor-pointer"
            >
              <X className="w-5 h-5" />
            </button>
          )}
        </div>

        {/* Current Dataset Info Badge */}
        {datasetInfo && (
          <div className="mx-4 mt-4 p-3 bg-slate-50 dark:bg-slate-800/60 border border-slate-200/80 dark:border-slate-700/80 rounded-2xl">
            <div className="flex items-center gap-2 text-xs font-bold text-slate-800 dark:text-slate-200 truncate mb-1">
              <FileSpreadsheet className="w-3.5 h-3.5 text-blue-600 dark:text-blue-400 shrink-0" />
              <span className="truncate">{datasetInfo.filename}</span>
            </div>
            <div className="flex items-center gap-2 text-[11px] text-slate-500 dark:text-slate-400 font-mono">
              <span>{datasetInfo.total_rows?.toLocaleString()} rows</span>
              <span>•</span>
              <span>{datasetInfo.total_columns} cols</span>
            </div>
          </div>
        )}

        {/* Navigation Menu */}
        <nav className="p-3 space-y-1 mt-2">
          {menuItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            const isDisabled = item.disabled;

            return (
              <button
                key={item.id}
                disabled={isDisabled}
                onClick={() => handleSelectTab(item.id)}
                className={`w-full flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-xs font-bold transition-all cursor-pointer ${
                  isActive
                    ? 'bg-blue-50 dark:bg-blue-950/60 text-blue-700 dark:text-blue-400 shadow-xs'
                    : isDisabled
                    ? 'text-slate-300 dark:text-slate-700 cursor-not-allowed opacity-60'
                    : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-100 hover:bg-slate-50 dark:hover:bg-slate-800/60'
                }`}
              >
                <Icon className={`w-4 h-4 shrink-0 ${isActive ? 'text-blue-600 dark:text-blue-400' : isDisabled ? 'text-slate-300 dark:text-slate-700' : 'text-slate-400 dark:text-slate-500'}`} />
                <span>{item.label}</span>
                {item.id === 'insights' && datasetInfo && (
                  <span className="ml-auto text-[9px] font-extrabold px-1.5 py-0.5 rounded-full bg-blue-100 dark:bg-blue-900/50 text-blue-700 dark:text-blue-300">
                    AI
                  </span>
                )}
              </button>
            );
          })}
        </nav>
      </div>

      {/* Footer Quick Actions */}
      {datasetInfo && (
        <div className="p-4 border-t border-slate-100 dark:border-slate-800 space-y-2 bg-slate-50/50 dark:bg-slate-900/50">
          <button
            onClick={() => {
              onOpenCleaner();
              if (setIsMobileNavOpen) setIsMobileNavOpen(false);
            }}
            className="w-full flex items-center justify-center gap-2 px-3 py-2 text-xs font-bold text-slate-700 dark:text-slate-200 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl hover:bg-slate-50 dark:hover:bg-slate-700 transition-colors shadow-xs cursor-pointer"
          >
            <SlidersHorizontal className="w-3.5 h-3.5 text-slate-500 dark:text-slate-400" />
            <span>Clean Dataset</span>
          </button>
          <button
            onClick={() => {
              onOpenExport();
              if (setIsMobileNavOpen) setIsMobileNavOpen(false);
            }}
            className="w-full flex items-center justify-center gap-2 px-3 py-2 text-xs font-bold text-white bg-blue-600 hover:bg-blue-700 dark:bg-blue-600 dark:hover:bg-blue-500 rounded-xl transition-colors shadow-xs shadow-blue-600/20 cursor-pointer"
          >
            <Download className="w-3.5 h-3.5" />
            <span>Export & Download</span>
          </button>
        </div>
      )}
    </div>
  );

  return (
    <>
      {/* Desktop Sidebar */}
      <aside className="hidden md:flex w-64 bg-white dark:bg-slate-900 border-r border-slate-200 dark:border-slate-800 flex-col shrink-0 transition-colors duration-200">
        {content}
      </aside>

      {/* Mobile Drawer Overlay */}
      {isMobileNavOpen && (
        <div className="md:hidden fixed inset-0 z-50 flex">
          <div
            className="fixed inset-0 bg-slate-900/50 backdrop-blur-xs"
            onClick={() => setIsMobileNavOpen(false)}
          />
          <div className="relative w-72 max-w-[80vw] bg-white dark:bg-slate-900 shadow-2xl h-full z-10">
            {content}
          </div>
        </div>
      )}
    </>
  );
}
