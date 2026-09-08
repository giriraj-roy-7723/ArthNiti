import { createContext, useContext, useState, useEffect } from 'react';
import { getToken, setToken as setAuthToken, removeToken, isAuthenticated } from '../utils/auth';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if user is authenticated on initial load
    if (isAuthenticated()) {
      // Decode token or fetch user info here if needed
      // For now, we'll just set a generic user object to signify they are logged in
      setUser({ loggedIn: true });
    }
    setLoading(false);
  }, []);

  const login = (token, userData) => {
    setAuthToken(token);
    setUser(userData || { loggedIn: true });
  };

  const logout = () => {
    removeToken();
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
