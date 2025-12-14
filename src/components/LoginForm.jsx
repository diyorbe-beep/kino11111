/**
 * Login form component - Oddiy va admin login uchun
 */
import { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import './Form.css';

const LoginForm = () => {
  const [formData, setFormData] = useState({ username: '', password: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login, adminLogin, isAdmin } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  
  // Agar /admin/login dan kelsa, admin login rejimi
  const isAdminLogin = location.pathname === '/admin/login';

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      // Admin login uchun alohida funksiya ishlatamiz
      const result = isAdminLogin 
        ? await adminLogin(formData.username, formData.password)
        : await login(formData.username, formData.password);
      
      setLoading(false);

      if (result.success) {
        // Admin login rejimida admin panelga yuborish
        if (isAdminLogin) {
          navigate('/admin');
        } else {
          // Oddiy login - home sahifasiga
          navigate('/');
        }
      } else {
        setError(result.error || 'Login failed');
      }
    } catch (err) {
      setLoading(false);
      setError('Login failed. Please check your credentials.');
    }
  };

  return (
    <div className="form-container">
      <div className="form-card">
        <h2>{isAdminLogin ? 'Admin Login' : 'Login'}</h2>
        {isAdminLogin && (
          <p className="form-subtitle">Enter your admin credentials to access the admin panel</p>
        )}
        
        {error && (
          <div className="form-error">
            {typeof error === 'object' ? JSON.stringify(error) : error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="form">
          <div className="form-group">
            <label htmlFor="username">{isAdminLogin ? 'Admin Username' : 'Username'}</label>
            <input
              type="text"
              id="username"
              name="username"
              value={formData.username}
              onChange={handleChange}
              required
              autoFocus
              placeholder={isAdminLogin ? 'Enter admin username' : 'Enter username'}
            />
          </div>
          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              required
              placeholder={isAdminLogin ? 'Enter admin password' : 'Enter password'}
            />
          </div>
          <button type="submit" disabled={loading} className="form-button">
            {loading ? 'Logging in...' : (isAdminLogin ? 'Login as Admin' : 'Login')}
          </button>
          
          <div className="form-footer">
            {isAdminLogin ? (
              <>
                <p>
                  <a href="/login">Regular User Login</a>
                </p>
                <p>
                  <a href="/">Back to Home</a>
                </p>
              </>
            ) : (
              <p className="form-link">
                Don't have an account? <a href="/register">Register here</a>
              </p>
            )}
          </div>
        </form>
      </div>
    </div>
  );
};

export default LoginForm;
