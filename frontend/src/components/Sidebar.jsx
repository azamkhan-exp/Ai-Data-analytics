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
  Database
} from 'lucide-react';

export default function Sidebar({
  activeTab,
  setActiveTab,
  datasetInfo,
  onOpenCleaner,
  onOpenExport
}) {
  const menuItems = [
    { id: 'upload', label: 'Upload Dataset', icon: FileUp },
    { id: 'overview', label: 'Dataset Overview', icon: Layers, disabled: !datasetInfo },
    { id: 'statistics', label: 'Statistics', icon: Table, disabled: !datasetInfo },
    { id: 'visualizations', label: 'Visualizations', icon: BarChart3, disabled: !datasetInfo },
    { id: 'insights', label: 'AI Insights', icon: BrainCircuit, disabled: !datasetInfo },
    { id: 'ask', label: 'Ask Your Data', icon: HelpCircle, disabled: !datasetInfo },
  ];

  return (
    <aside className="w-64 bg-white border-r border-slate-200 flex flex-col justify-between shrink-0 select-none">
      {/* Brand Header */}
      <div>
        <div className="h-16 flex items-center px-6 border-b border-slate-100 gap-3">
          <div className="w-9 h-9 rounded-xl bg-blue-600 flex items-center justify-center text-white shadow-md shadow-blue-500/20">
            <Sparkles className="w-5 h-5" />
          </div>
          <div>
            <h1 className="text-base font-bold text-slate-900 tracking-tight">InsightPulse</h1>
            <p className="text-[11px] font-medium text-slate-400 uppercase tracking-wider">AI Data Analyst</p>
          </div>
        </div>

        {/* Current Dataset Badge */}
        {datasetInfo && (
          <div className="mx-4 mt-4 p-3 bg-slate-50 border border-slate-200/80 rounded-xl">
            <div className="flex items-center gap-2 text-xs font-semibold text-slate-700 truncate mb-1.5">
              <FileSpreadsheet className="w-3.5 h-3.5 text-blue-600 shrink-0" />
              <span className="truncate">{datasetInfo.filename}</span>
            </div>
            <div className="flex items-center gap-2 text-[11px] text-slate-500 font-mono">
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
                onClick={() => setActiveTab(item.id)}
                className={`w-full flex items-center gap-3 px-3.5 py-2.5 rounded-lg text-sm font-medium transition-all ${
                  isActive
                    ? 'bg-blue-50 text-blue-700 font-semibold shadow-sm'
                    : isDisabled
                    ? 'text-slate-300 cursor-not-allowed'
                    : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
                }`}
              >
                <Icon className={`w-4 h-4 ${isActive ? 'text-blue-600' : isDisabled ? 'text-slate-300' : 'text-slate-400'}`} />
                <span>{item.label}</span>
                {item.id === 'insights' && datasetInfo && (
                  <span className="ml-auto text-[10px] font-bold px-1.5 py-0.5 rounded-full bg-blue-100 text-blue-700">
                    AI
                  </span>
                )}
              </button>
            );
          })}
        </nav>
      </div>

      {/* Footer Actions */}
      {datasetInfo && (
        <div className="p-4 border-t border-slate-100 space-y-2 bg-slate-50/50">
          <button
            onClick={onOpenCleaner}
            className="w-full flex items-center justify-center gap-2 px-3 py-2 text-xs font-medium text-slate-700 bg-white border border-slate-200 rounded-lg hover:bg-slate-50 hover:border-slate-300 transition-colors shadow-sm"
          >
            <SlidersHorizontal className="w-3.5 h-3.5 text-slate-500" />
            <span>Clean Dataset</span>
          </button>
          <button
            onClick={onOpenExport}
            className="w-full flex items-center justify-center gap-2 px-3 py-2 text-xs font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition-colors shadow-sm shadow-blue-600/20"
          >
            <Download className="w-3.5 h-3.5" />
            <span>Export & Download</span>
          </button>
        </div>
      )}
    </aside>
  );
}
