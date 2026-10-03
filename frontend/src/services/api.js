import axios from 'axios';

// ---------------------------------------------------------------------------
// Central Axios instance
// The base URL is read from the Vite environment variable VITE_API_BASE_URL.
// Default (dev): http://127.0.0.1:8000
// Override by creating frontend/.env.local:
//   VITE_API_BASE_URL=http://127.0.0.1:8000
// ---------------------------------------------------------------------------
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000',
  timeout: 8000,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * GET /api/health
 * Returns the backend health status object or throws on failure.
 */
export const fetchHealth = async () => {
  const response = await apiClient.get('/api/health');
  return response.data;
};

export const getAnalyticsStatus = async () => {
  const response = await apiClient.get('/api/analytics/status');
  return response.data;
};

export const getAnalyticsSummary = async () => {
  const response = await apiClient.get('/api/analytics/summary');
  return response.data;
};

export const getCategories = async () => {
  const response = await apiClient.get('/api/analytics/categories');
  return response.data;
};

export const getProducts = async (limit) => {
  const url = limit ? `/api/analytics/products?limit=${limit}` : '/api/analytics/products';
  const response = await apiClient.get(url);
  return response.data;
};

export const getPayments = async () => {
  const response = await apiClient.get('/api/analytics/payments');
  return response.data;
};

export const getCities = async () => {
  const response = await apiClient.get('/api/analytics/cities');
  return response.data;
};

export const getChannels = async () => {
  const response = await apiClient.get('/api/analytics/channels');
  return response.data;
};

export const getDailyRevenue = async () => {
  const response = await apiClient.get('/api/analytics/daily');
  return response.data;
};

export const getMonthlyRevenue = async () => {
  const response = await apiClient.get('/api/analytics/monthly');
  return response.data;
};

export const getTopProducts = async () => {
  const response = await apiClient.get('/api/analytics/top-products');
  return response.data;
};

export default apiClient;
