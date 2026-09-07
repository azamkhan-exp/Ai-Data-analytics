import React, { useState } from 'react';
import Sidebar from './components/Sidebar';
import Header from './components/Header';
import FileUpload from './components/FileUpload';
import MetricCards from './components/MetricCards';
import DataPreview from './components/DataPreview';
import Statistics from './components/Statistics';
import Visualizations from './components/Visualizations';
import AiInsights from './components/AiInsights';
import ChatInterface from './components/ChatInterface';
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
    <div className="flex h-screen w-screen overflow-hidden bg-slate-50 font-sans">
      {/* Sidebar Navigation */}
      <Sidebar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        datasetInfo={datasetInfo}
        onOpenCleaner={() => setIsCleanerOpen(true)}
        onOpenExport={() => setIsExportOpen(true)}
      />

      {/* Main Container */}
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
        <Header
          activeTab={activeTab}
          datasetInfo={datasetInfo}
          onLoadDataset={handleLoadSample}
          onResetUpload={handleResetUpload}
          loading={loading}
        />

        {/* Scrollable Main Area */}
        <main className="flex-1 overflow-y-auto p-6 md:p-8">
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
              <MetricCards summary={analysis.summary} />
              <DataPreview
                previewRows={analysis.preview_rows}
                columnDetails={analysis.column_details}
                totalRows={analysis.summary.total_rows}
              />
            </div>
          )}

          {/* 3. Statistics Tab */}
          {activeTab === 'statistics' && analysis && (
            <Statistics
              numericalStats={analysis.numerical_stats}
              categoricalStats={analysis.categorical_stats}
              strongCorrelations={analysis.strong_correlations}
            />
          )}

          {/* 4. Visualizations Tab */}
          {activeTab === 'visualizations' && visualizations && datasetInfo && (
            <Visualizations
              visualizations={visualizations}
              datasetId={datasetInfo.dataset_id}
              columnTypes={analysis.column_types}
              columns={datasetInfo.columns}
            />
          )}

          {/* 5. AI Insights Tab */}
          {activeTab === 'insights' && (
            <AiInsights insights={insights} />
          )}

          {/* 6. Ask Your Data Tab */}
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
