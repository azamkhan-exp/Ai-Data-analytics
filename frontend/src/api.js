import axios from 'axios';

const api = axios.create({
  baseURL: '/api',
  timeout: 30000,
});

export const getHealth = async () => {
  const res = await api.get('/health');
  return res.data;
};

export const uploadDataset = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  const res = await api.post('/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return res.data;
};

export const getSamples = async () => {
  const res = await api.get('/samples');
  return res.data;
};

export const loadSample = async (name) => {
  const res = await api.post(`/samples/load?name=${encodeURIComponent(name)}`);
  return res.data;
};

export const getAnalysis = async (datasetId) => {
  const res = await api.get(`/analysis/${datasetId}`);
  return res.data;
};

export const getVisualizations = async (datasetId) => {
  const res = await api.get(`/visualizations/${datasetId}`);
  return res.data;
};

export const createCustomChart = async (datasetId, params) => {
  const res = await api.post(`/visualizations/${datasetId}/custom`, params);
  return res.data;
};

export const getInsights = async (datasetId) => {
  const res = await api.get(`/insights/${datasetId}`);
  return res.data;
};

export const askQuestion = async (datasetId, question) => {
  const res = await api.post(`/query/${datasetId}`, { question });
  return res.data;
};

export const cleanDataset = async (datasetId, options) => {
  const res = await api.post(`/clean/${datasetId}`, options);
  return res.data;
};

export const getExportUrl = (datasetId, format = 'csv') => {
  return `/api/export/${datasetId}?format=${format}`;
};

export default api;
