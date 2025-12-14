/**
 * API service for communicating with Django backend
 */
import axios from 'axios';

// Use Vite proxy in development, direct URL in production
const isDevelopment = import.meta.env.DEV;
// Development'da ham to'g'ridan-to'g'ri backend URL ga so'rov yuborish
const API_URL = isDevelopment 
  ? 'http://139.59.137.138/api/v1'  // To'g'ridan-to'g'ri backend URL
  : (import.meta.env.VITE_API_URL || 'http://139.59.137.138/api/v1');
const MEDIA_URL = isDevelopment
  ? 'http://139.59.137.138/media'  // To'g'ridan-to'g'ri backend URL
  : (import.meta.env.VITE_MEDIA_URL || 'http://139.59.137.138/media');

// Create axios instance
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refresh_token');
        if (refreshToken) {
          // Handle CustomResponse format for token refresh
          const response = await axios.post(`${API_URL}/auth/token/refresh/`, {
            refresh: refreshToken,
          });
          const responseData = response.data?.data || response.data;
          const access = responseData?.access || responseData?.access_token;
          localStorage.setItem('access_token', access);
          originalRequest.headers.Authorization = `Bearer ${access}`;
          return api(originalRequest);
        }
      } catch (refreshError) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  register: (data) => api.post('/auth/register/', data),
  login: (data) => api.post('/auth/token/', data),
  refreshToken: (refresh) => api.post('/auth/token/refresh/', { refresh }),
  getProfile: () => api.get('/auth/profile/'),
};

// Movies API
export const moviesAPI = {
  list: (params) => api.get('/movies/', { params }),
  get: (id) => api.get(`/movies/${id}/`),  // Supports both slug and id
  create: (data) => {
    const formData = new FormData();
    Object.keys(data).forEach((key) => {
      if (key === 'poster' && data[key]) {
        formData.append(key, data[key]);
      } else if (key === 'genre_ids' || key === 'actor_ids') {
        // Handle array of IDs
        if (Array.isArray(data[key])) {
          data[key].forEach((id) => formData.append(key, id));
        }
      } else if (key === 'genres' || key === 'categories') {
        // Handle if genres/categories passed as array of objects
        if (Array.isArray(data[key])) {
          data[key].forEach((item) => {
            const id = typeof item === 'object' ? item.id : item;
            formData.append(key === 'genres' ? 'genre_ids' : 'category_ids', id);
          });
        }
      } else if (data[key] !== null && data[key] !== undefined && data[key] !== '') {
        formData.append(key, data[key]);
      }
    });
    return api.post('/movies/create/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
  update: (id, data) => {
    const formData = new FormData();
    Object.keys(data).forEach((key) => {
      if (key === 'poster' && data[key]) {
        formData.append(key, data[key]);
      } else if (key === 'genre_ids' || key === 'actor_ids') {
        // Handle array of IDs
        if (Array.isArray(data[key])) {
          data[key].forEach((id) => formData.append(key, id));
        }
      } else if (key === 'genres' || key === 'categories') {
        // Handle if genres/categories passed as array of objects
        if (Array.isArray(data[key])) {
          data[key].forEach((item) => {
            const id = typeof item === 'object' ? item.id : item;
            formData.append(key === 'genres' ? 'genre_ids' : 'category_ids', id);
          });
        }
      } else if (data[key] !== null && data[key] !== undefined && data[key] !== '') {
        formData.append(key, data[key]);
      }
    });
    return api.patch(`/movies/${id}/update/`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
  delete: (id) => api.delete(`/movies/${id}/delete/`),
  importCSV: (file) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/movies/import_csv/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
};

// Reviews API
export const reviewsAPI = {
  list: (params) => api.get('/movies/reviews/', { params }),
  create: (data) => api.post('/movies/reviews/create/', data),
  update: (id, data) => api.patch(`/movies/reviews/${id}/`, data),
  delete: (id) => api.delete(`/movies/reviews/${id}/`),
};

// Genres API
export const genresAPI = {
  list: () => api.get('/movies/genres/'),
};

// Actors API
export const actorsAPI = {
  list: (params) => api.get('/movies/actors/', { params }),
};

export { API_URL, MEDIA_URL };
export default api;



