import React, { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import Header from './components/Header';
import FileUpload from './components/FileUpload';
import MetricCards from './components/MetricCards';
import DataPreview from './components/DataPreview';
import Statistics from './components/Statistics';
import Visualizations from './components/Visualizations';
import AiInsights from './components/AiInsights';
import ChatInterface from './components/ChatInterface';
import AnomaliesView from './components/AnomaliesView';
import DataQualityView from './components/DataQualityView';
import DataCleanerModal from './components/DataCleanerModal';
import ExportModal from './components/ExportModal';

import { getAnalysis, getVisualizations, getInsights, loadSample } from './api';

export default function App() {
  const [activeTab, setActiveTab] = useState('upload');
  const [datasetInfo, setDatasetInfo] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [visualizations, setVisualizations] = useState(null);
  const [insights, setInsights] = useState([]);
  const [loading, setLoading] = useState(false);

  // Mobile navigation drawer state
  const [isMobileNavOpen, setIsMobileNavOpen] = useState(false);

  // Dark mode state
  const [isDark, setIsDark] = useState(() => {
    if (typeof window !== 'undefined') {
      const saved = localStorage.getItem('insightpulse_theme');
      if (saved) return saved === 'dark';
      return window.matchMedia('(prefers-color-scheme: dark)').matches;
    }
    return false;
  });

  useEffect(() => {
    if (isDark) {
      document.documentElement.classList.add('dark');
      localStorage.setItem('insightpulse_theme', 'dark');
    } else {
      document.documentElement.classList.remove('dark');
      localStorage.setItem('insightpulse_theme', 'light');
    }
  }, [isDark]);

  // Modals
  const [isCleanerOpen, setIsCleanerOpen] = useState(false);
  const [isExportOpen, setIsExportOpen] = useState(false);

  const fetchDatasetDetails = async (datasetId, baseInfo) => {
    setLoading(true);
    try {
      const [analysisRes, visualsRes, insightsRes] = await Promise.all([
        getAnalysis(datasetId),
        getVisualizations(datasetId),
        getInsights(datasetId),
      ]);

      setDatasetInfo(baseInfo);
      setAnalysis(analysisRes.analysis);
      setVisualizations(visualsRes.visualizations);
      setInsights(insightsRes.insights || []);
      setActiveTab('overview');
    } catch (err) {
      console.error('Error fetching dataset details:', err);
      alert('Failed to load dataset analysis details.');
    } finally {
      setLoading(false);
    }
  };

  const handleDatasetLoaded = (uploadData) => {
    fetchDatasetDetails(uploadData.dataset_id, uploadData);
  };

  const handleLoadSample = async (sampleName) => {
    setLoading(true);
    try {
      const data = await loadSample(sampleName);
      await fetchDatasetDetails(data.dataset_id, data);
    } catch (err) {
      console.error(err);
      alert('Failed to load sample dataset.');
    } finally {
      setLoading(false);
    }
  };

  const handleDatasetCleaned = async (updatedAnalysis) => {
    setAnalysis(updatedAnalysis);
    if (datasetInfo?.dataset_id) {
      const [visualsRes, insightsRes] = await Promise.all([
        getVisualizations(datasetInfo.dataset_id),
        getInsights(datasetInfo.dataset_id),
      ]);
      setVisualizations(visualsRes.visualizations);
      setInsights(insightsRes.insights || []);
    }
  };

  const handleResetUpload = () => {
    setActiveTab('upload');
  };

  return (
    <div className="flex h-screen w-screen overflow-hidden bg-slate-50 dark:bg-slate-950 text-slate-900 dark:text-slate-100 font-sans transition-colors duration-200">
      {/* Sidebar Navigation */}
      <Sidebar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        datasetInfo={datasetInfo}
        onOpenCleaner={() => setIsCleanerOpen(true)}
        onOpenExport={() => setIsExportOpen(true)}
        isMobileNavOpen={isMobileNavOpen}
        setIsMobileNavOpen={setIsMobileNavOpen}
      />

      {/* Main Container */}
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
        <Header
          activeTab={activeTab}
          datasetInfo={datasetInfo}
          onLoadDataset={handleLoadSample}
          onResetUpload={handleResetUpload}
          loading={loading}
          isMobileNavOpen={isMobileNavOpen}
          setIsMobileNavOpen={setIsMobileNavOpen}
          isDark={isDark}
          setIsDark={setIsDark}
        />

        {/* Scrollable Main Area */}
        <main className="flex-1 overflow-y-auto p-4 sm:p-6 md:p-8">
          {/* 1. Upload Tab */}
          {activeTab === 'upload' && (
            <FileUpload
              onDatasetLoaded={handleDatasetLoaded}
              onSelectSample={handleLoadSample}
              loading={loading}
              setLoading={setLoading}
            />
          )}

          {/* 2. Overview Tab */}
          {activeTab === 'overview' && analysis && (
            <div className="space-y-6">
              <MetricCards
                summary={analysis.summary}
                qualityScore={analysis.quality_score}
                smartKpis={analysis.smart_kpis}
              />
              <DataPreview
                previewRows={analysis.preview_rows}
                columnDetails={analysis.column_details}
                totalRows={analysis.summary.total_rows}
              />
            </div>
          )}

          {/* 3. Explorer Tab (Dedicated Full Preview & Schema) */}
          {activeTab === 'explorer' && analysis && (
            <div className="space-y-6">
              <DataPreview
                previewRows={analysis.preview_rows}
                columnDetails={analysis.column_details}
                totalRows={analysis.summary.total_rows}
              />
            </div>
          )}

          {/* 4. Visualizations Tab */}
          {activeTab === 'visualizations' && visualizations && datasetInfo && (
            <Visualizations
              visualizations={visualizations}
              datasetId={datasetInfo.dataset_id}
              columnTypes={analysis?.column_types}
              columns={datasetInfo.columns}
            />
          )}

          {/* 5. Statistics Tab */}
          {activeTab === 'statistics' && analysis && (
            <Statistics
              numericalStats={analysis.numerical_stats}
              categoricalStats={analysis.categorical_stats}
              strongCorrelations={analysis.strong_correlations}
            />
          )}

          {/* 6. Anomalies Tab */}
          {activeTab === 'anomalies' && analysis && (
            <AnomaliesView
              anomalySummary={analysis.anomaly_summary}
              numericalStats={analysis.numerical_stats}
            />
          )}

          {/* 7. Data Quality Tab */}
          {activeTab === 'quality' && analysis && (
            <DataQualityView
              qualityScore={analysis.quality_score}
              onOpenCleaner={() => setIsCleanerOpen(true)}
            />
          )}

          {/* 8. AI Insights Tab */}
          {activeTab === 'insights' && (
            <AiInsights insights={insights} />
          )}

          {/* 9. Ask Your Data Tab */}
          {activeTab === 'ask' && datasetInfo && (
            <ChatInterface datasetId={datasetInfo.dataset_id} />
          )}
        </main>
      </div>

      {/* Modals */}
      {datasetInfo && (
        <>
          <DataCleanerModal
            isOpen={isCleanerOpen}
            onClose={() => setIsCleanerOpen(false)}
            datasetId={datasetInfo.dataset_id}
            onDatasetCleaned={handleDatasetCleaned}
          />
          <ExportModal
            isOpen={isExportOpen}
            onClose={() => setIsExportOpen(false)}
            datasetId={datasetInfo.dataset_id}
            filename={datasetInfo.filename}
          />
        </>
      )}
    </div>
  );
}
