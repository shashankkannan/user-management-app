import axios from 'axios';

const API = axios.create({
  baseURL: 'http://localhost:7000',
});

// Add token to headers if exists
API.interceptors.request.use((req) => {
  const token = localStorage.getItem('token');
  if (token) {
    req.headers.Authorization = `Bearer ${token}`;
  }
  return req;
});

export const register = (data) => API.post('/register', data);
export const login = (data) => API.post('/login', data);
export const getUsers = () => API.get('/users');
export const updateUser = (id, data) => API.put(`/users/${id}`, data);
export const deleteUser = (id) => API.delete(`/users/${id}`);
