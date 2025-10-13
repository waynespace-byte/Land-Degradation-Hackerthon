import axios from 'axios';

// Base config
const API_BASE = '/api'; // Proxied to backend via package.json

const api = axios.create({
  baseURL: API_BASE,
  headers: { 'Content-Type': 'application/json' }
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// User endpoints
export const authAPI = {
  register: (data) => api.post('/users/register', data),
  login: (data) => api.post('/users/login', data),
};

// Land endpoints
export const landsAPI = {
  create: (data) => api.post('/lands', data),
  getAll: () => api.get('/lands'),
  analyze: (id) => api.post(`/lands/${id}/analyze`),
};

// Sensor endpoints
export const sensorsAPI = {
  ingest: (data) => api.post('/sensors', data),
};

// Alerts endpoints
export const alertsAPI = {
  getAll: () => api.get('/alerts'),
  resolve: (id) => api.post(`/alerts/${id}/resolve`),
};

export default api;