import { createContext, useContext, useState, useEffect } from 'react';
import { getToken, setToken as setAuthToken, removeToken, isAuthenticated } from '../utils/auth';

const AuthContext = createContext();

const decodeTokenPayload = (token) => {
  try {
    const payload = token.split('.')[1];
    return JSON.parse(atob(payload.replace(/-/g, '+').replace(/_/g, '/')));
  } catch {
    return null;
  }
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if user is authenticated on initial load
    if (isAuthenticated()) {
      const storedUser = localStorage.getItem('user');
      const tokenPayload = decodeTokenPayload(getToken());
      setUser(storedUser ? JSON.parse(storedUser) : { ...tokenPayload, loggedIn: true });
    }
    setLoading(false);
  }, []);

  const login = (token, userData) => {
    setAuthToken(token);
    const nextUser = userData || { ...decodeTokenPayload(token), loggedIn: true };
    localStorage.setItem('user', JSON.stringify(nextUser));
    setUser(nextUser);
  };

  const logout = () => {
    removeToken();
    localStorage.removeItem('user');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, loading }}>
      {!loading && children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
