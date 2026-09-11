import React, { createContext, useState, useEffect } from 'react';
import axios from 'axios';

axios.defaults.baseURL = import.meta.env.VITE_API_BASE_URL || '';

// Globally configure Axios to attach the JWT token to every request
axios.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, (error) => {
  return Promise.reject(error);
});

axios.interceptors.response.use((response) => {
  return response;
}, (error) => {
  if (error.response && error.response.status === 401) {
    localStorage.removeItem('token');
    delete axios.defaults.headers.common['Authorization'];
    window.location.href = '/login';
  }
  return Promise.reject(error);
});

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const token = localStorage.getItem('token');
        if (token) {
          const res = await axios.get('/api/auth/me', {
            headers: { Authorization: `Bearer ${token}` }
          });
          setUser(res.data);
        }
      } catch (err) {
        localStorage.removeItem('token');
      } finally {
        setLoading(false);
      }
    };
    fetchUser();
  }, []);

  const login = async (username, password) => {
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);
    const res = await axios.post('/api/auth/login', formData);
    localStorage.setItem('token', res.data.access_token);
    const userRes = await axios.get('/api/auth/me', {
      headers: { Authorization: `Bearer ${res.data.access_token}` }
    });
    setUser(userRes.data);
  };

  const googleLogin = async (token) => {
    const res = await axios.post('/api/auth/google', { token });
    localStorage.setItem('token', res.data.access_token);
    const userRes = await axios.get('/api/auth/me', {
      headers: { Authorization: `Bearer ${res.data.access_token}` }
    });
    setUser(userRes.data);
  };

  const register = async (username, email, password) => {
    await axios.post('/api/auth/register', { username, email, password });
  };

  const logout = () => {
    localStorage.removeItem('token');
    delete axios.defaults.headers.common['Authorization'];
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, googleLogin, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
};
