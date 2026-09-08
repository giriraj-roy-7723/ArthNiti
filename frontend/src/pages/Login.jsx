import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useLanguage } from '../context/LanguageContext';
import { useAuth } from '../context/AuthContext';
import { api } from '../utils/api';
import { Mail, Lock, ArrowRight, Loader2 } from 'lucide-react';

const Login = () => {
  const [formData, setFormData] = useState({ email: '', password: '' });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  const { language } = useLanguage();
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const res = await api.post(`/auth/login?language=${encodeURIComponent(language)}`, formData);
      if (res.data.access_token) {
        login(res.data.access_token, res.data.user);
        navigate('/');
      }
    } catch (err) {
      if (!err.response) {
        setError('Unable to reach the backend. Start the API on port 8000 and try again.');
      } else if (Array.isArray(err.response.data?.detail)) {
        setError(err.response.data.detail.map((item) => item.msg).join(', '));
      } else {
        setError(err.response.data?.detail || 'Invalid email or password');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-6 perspective-[1000px]">
      <div className="w-full max-w-md relative group">
        {/* 3D Glow Effect */}
        <div className="absolute -inset-1 bg-gradient-to-r from-blue-600 to-purple-600 rounded-3xl blur-md opacity-30 group-hover:opacity-60 transition duration-500"></div>
        
        {/* 3D Card Container */}
        <div className="relative transform transition-all duration-500 hover:rotate-y-6 hover:-rotate-x-6 hover:scale-105 preserve-3d bg-gray-900 border border-gray-700/50 p-8 rounded-3xl shadow-[0_20px_50px_rgba(0,0,0,0.5)] backdrop-blur-xl">
          {/* Top light reflection */}
          <div className="absolute inset-0 bg-gradient-to-br from-white/10 to-transparent rounded-3xl pointer-events-none border-t border-l border-white/10"></div>
          
          <div className="mb-8 text-center transform translate-z-10">
            <h2 className="text-3xl font-extrabold text-transparent bg-clip-text bg-gradient-to-br from-white via-blue-100 to-gray-400 drop-shadow-sm mb-2">
              Welcome Back
            </h2>
            <p className="text-gray-400 text-sm">Sign in to continue to Finance Assistant</p>
          </div>

          {error && (
            <div className="mb-6 p-4 bg-red-500/10 border border-red-500/20 rounded-xl text-red-500 text-sm text-center transform translate-z-6 shadow-[inset_0_2px_10px_rgba(0,0,0,0.2)]">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-5 transform translate-z-6">
            <div className="relative group/input">
              <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                <Mail className="h-5 w-5 text-gray-500 group-focus-within/input:text-blue-500 transition-colors" />
              </div>
              <input
                type="email"
                name="email"
                required
                value={formData.email}
                onChange={handleChange}
                className="w-full pl-12 pr-4 py-3 bg-gray-950/80 border border-gray-800 rounded-xl text-white placeholder-gray-500 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all shadow-[inset_0_2px_4px_rgba(0,0,0,0.4)]"
                placeholder="Email Address"
              />
            </div>

            <div className="relative group/input">
              <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                <Lock className="h-5 w-5 text-gray-500 group-focus-within/input:text-blue-500 transition-colors" />
              </div>
              <input
                type="password"
                name="password"
                required
                value={formData.password}
                onChange={handleChange}
                className="w-full pl-12 pr-4 py-3 bg-gray-950/80 border border-gray-800 rounded-xl text-white placeholder-gray-500 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all shadow-[inset_0_2px_4px_rgba(0,0,0,0.4)]"
                placeholder="Password"
              />
            </div>

            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <input
                  id="remember-me"
                  name="remember-me"
                  type="checkbox"
                  className="h-4 w-4 rounded border-gray-700 bg-gray-950 text-blue-600 focus:ring-blue-600 shadow-inner"
                />
                <label htmlFor="remember-me" className="ml-2 block text-sm text-gray-400">
                  Remember me
                </label>
              </div>

              <div className="text-sm">
                <a href="#" className="font-medium text-blue-400 hover:text-blue-300 transition-colors">
                  Forgot your password?
                </a>
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full flex items-center justify-center space-x-2 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white py-3 rounded-xl font-medium transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed shadow-[0_10px_20px_rgba(37,99,235,0.3)] hover:shadow-[0_15px_30px_rgba(37,99,235,0.4)] hover:-translate-y-1 transform active:translate-y-0 active:shadow-inner"
            >
              {loading ? (
                <Loader2 className="h-5 w-5 animate-spin" />
              ) : (
                <>
                  <span>Sign In</span>
                  <ArrowRight className="h-5 w-5" />
                </>
              )}
            </button>
          </form>

          <div className="mt-8 text-center text-sm text-gray-400 transform translate-z-6">
            Don't have an account?{' '}
            <Link to="/signup" className="text-blue-400 hover:text-blue-300 font-bold transition-colors">
              Sign Up
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
