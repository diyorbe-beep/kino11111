/**
 * Authentication context for managing user state
 */
import { createContext, useContext, useState, useEffect } from 'react';
import { authAPI } from '../services/api';

const AuthContext = createContext(null);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if user is logged in on mount
    const token = localStorage.getItem('access_token');
    if (token) {
      loadUser();
    } else {
      setLoading(false);
    }
  }, []);

  const loadUser = async () => {
    try {
      const response = await authAPI.getProfile();
      // Handle CustomResponse format: { id, message, data }
      const userData = response.data?.data || response.data;
      setUser(userData);
    } catch (error) {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  const login = async (username, password, skipPassword = false) => {
    try {
      if (skipPassword) {
        // For OAuth login, user is already authenticated
        await loadUser();
        return { success: true };
      }
      
      const response = await authAPI.login({ username, password });
      // Handle CustomResponse format: { id, message, data: { access, refresh, user } }
      const responseData = response.data?.data || response.data;
      const access = responseData?.access || responseData?.access_token;
      const refresh = responseData?.refresh || responseData?.refresh_token;
      
      if (!access || !refresh) {
        return {
          success: false,
          error: response.data?.message || 'Invalid response from server'
        };
      }
      
      localStorage.setItem('access_token', access);
      localStorage.setItem('refresh_token', refresh);
      await loadUser();
      return { success: true };
    } catch (error) {
      // Handle CustomResponse error format
      const errorMessage = error.response?.data?.message || 
                          error.response?.data?.detail ||
                          (error.response?.data?.errors ? JSON.stringify(error.response.data.errors) : null) ||
                          'Login failed';
      return {
        success: false,
        error: errorMessage,
      };
    }
  };

  // Admin login uchun alohida funksiya - 404 xatosi bo'lsa, /auth/login/ endpoint'ini sinab ko'radi
  const adminLogin = async (username, password) => {
    try {
      // Avval /auth/token/ endpoint'ini sinab ko'ramiz
      let response;
      try {
        response = await authAPI.login({ username, password });
      } catch (error) {
        // Agar 404 bo'lsa, /auth/login/ endpoint'ini sinab ko'ramiz
        if (error.response?.status === 404) {
          try {
            response = await authAPI.adminLogin({ username, password });
          } catch (loginError) {
            throw error; // Asl xatoni qaytaramiz
          }
        } else {
          throw error;
        }
      }
      
      // Handle CustomResponse format: { id, message, data: { access, refresh, user } }
      const responseData = response.data?.data || response.data;
      const access = responseData?.access || responseData?.access_token;
      const refresh = responseData?.refresh || responseData?.refresh_token;
      
      if (!access || !refresh) {
        return {
          success: false,
          error: response.data?.message || 'Invalid response from server'
        };
      }
      
      localStorage.setItem('access_token', access);
      localStorage.setItem('refresh_token', refresh);
      await loadUser();
      
      // Admin ekanligini tekshiramiz - user ma'lumotlarini yuklagandan keyin
      // loadUser() chaqirilgandan keyin user state yangilanadi
      const userData = responseData?.user || responseData;
      const isUserAdmin = userData?.is_staff || userData?.is_superuser || false;
      
      if (!isUserAdmin) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        setUser(null);
        return {
          success: false,
          error: 'This account does not have admin privileges.'
        };
      }
      
      return { success: true };
    } catch (error) {
      // Handle CustomResponse error format
      const errorMessage = error.response?.data?.message || 
                          error.response?.data?.detail ||
                          (error.response?.data?.errors ? JSON.stringify(error.response.data.errors) : null) ||
                          'Admin login failed';
      return {
        success: false,
        error: errorMessage,
      };
    }
  };

  const register = async (userData) => {
    try {
      const response = await authAPI.register(userData);
      const { access, refresh } = response.data;
      localStorage.setItem('access_token', access);
      localStorage.setItem('refresh_token', refresh);
      await loadUser();
      return { success: true };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data || 'Registration failed',
      };
    }
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    setUser(null);
  };

  const isAdmin = () => {
    return user?.is_staff || false;
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        login,
        adminLogin,
        register,
        logout,
        isAdmin,
        loadUser,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};






