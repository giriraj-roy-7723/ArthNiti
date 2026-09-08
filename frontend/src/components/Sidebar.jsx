import { Link, useLocation } from 'react-router-dom';
import { useLanguage } from '../context/LanguageContext';
import { useAuth } from '../context/AuthContext';
import { Home, LogIn, UserPlus, LogOut, Settings, Globe } from 'lucide-react';

const Sidebar = () => {
  const { language, toggleLanguage } = useLanguage();
  const { user, logout } = useAuth();
  const location = useLocation();

  const isActive = (path) => location.pathname === path;

  const getLinkClasses = (path) => {
    return `flex items-center space-x-3 px-4 py-3 rounded-xl transition-all duration-300 transform preserve-3d ${
      isActive(path) 
        ? 'bg-gradient-to-r from-blue-600 to-indigo-600 text-white shadow-[0_10px_20px_rgba(37,99,235,0.3)] translate-z-10 scale-105' 
        : 'text-gray-400 hover:bg-gray-800/80 hover:text-white hover:translate-x-2 hover:shadow-lg'
    }`;
  };

  return (
    <aside className="w-64 h-screen bg-gray-950/90 backdrop-blur-md border-r border-gray-800 flex flex-col justify-between flex-shrink-0 sticky top-0 shadow-[20px_0_50px_rgba(0,0,0,0.5)] z-50">
      {/* 3D Inner Edge Reflection */}
      <div className="absolute inset-y-0 right-0 w-px bg-gradient-to-b from-white/10 via-white/5 to-transparent pointer-events-none"></div>
      
      <div className="p-6 relative z-10">
        <div className="flex items-center space-x-3 mb-10 transform preserve-3d hover:rotate-y-12 transition-transform duration-500">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center shadow-[0_10px_20px_rgba(37,99,235,0.4)] translate-z-10 border-t border-l border-white/20">
            <span className="text-white font-bold text-xl drop-shadow-md">F</span>
          </div>
          <h1 className="text-xl font-extrabold bg-clip-text text-transparent bg-gradient-to-r from-white via-blue-100 to-gray-400 drop-shadow-sm translate-z-6">
            Finance
          </h1>
        </div>

        <nav className="space-y-3 perspective-[1000px]">
          <Link to="/" className={getLinkClasses('/')}>
            <Home size={20} className={isActive('/') ? 'drop-shadow-md' : ''} />
            <span className="font-semibold">Home</span>
          </Link>
          
          {!user ? (
            <>
              <Link to="/login" className={getLinkClasses('/login')}>
                <LogIn size={20} className={isActive('/login') ? 'drop-shadow-md' : ''} />
                <span className="font-semibold">Login</span>
              </Link>
              <Link to="/signup" className={getLinkClasses('/signup')}>
                <UserPlus size={20} className={isActive('/signup') ? 'drop-shadow-md' : ''} />
                <span className="font-semibold">Sign Up</span>
              </Link>
            </>
          ) : (
            <>
               <Link to="/dashboard" className={getLinkClasses('/dashboard')}>
                <Settings size={20} className={isActive('/dashboard') ? 'drop-shadow-md' : ''} />
                <span className="font-semibold">Dashboard</span>
              </Link>
            </>
          )}
        </nav>
      </div>

      <div className="p-6 space-y-6 relative z-10 perspective-[1000px]">
        <div className="bg-gray-900/80 rounded-2xl p-4 border border-gray-800 shadow-[inset_0_2px_10px_rgba(0,0,0,0.5),0_10px_20px_rgba(0,0,0,0.2)] transform preserve-3d hover:rotate-x-6 transition-transform duration-500">
          <div className="flex items-center space-x-2 text-gray-400 mb-4 text-sm font-semibold translate-z-6">
            <Globe size={16} />
            <span>Language</span>
          </div>
          <div className="flex flex-col space-y-2 translate-z-6">
            <button
              onClick={() => toggleLanguage('english')}
              className={`text-left px-4 py-2.5 rounded-xl text-sm font-bold transition-all duration-300 ${
                language === 'english' 
                  ? 'bg-gradient-to-r from-blue-600 to-indigo-600 text-white shadow-[0_5px_15px_rgba(37,99,235,0.3)] scale-105' 
                  : 'text-gray-400 hover:bg-gray-800 hover:text-white hover:translate-x-1'
              }`}
            >
              English
            </button>
            <button
              onClick={() => toggleLanguage('hindi')}
              className={`text-left px-4 py-2.5 rounded-xl text-sm font-bold transition-all duration-300 ${
                language === 'hindi' 
                  ? 'bg-gradient-to-r from-blue-600 to-indigo-600 text-white shadow-[0_5px_15px_rgba(37,99,235,0.3)] scale-105' 
                  : 'text-gray-400 hover:bg-gray-800 hover:text-white hover:translate-x-1'
              }`}
            >
              Hindi (हिंदी)
            </button>
            <button
              onClick={() => toggleLanguage('bengali')}
              className={`text-left px-4 py-2.5 rounded-xl text-sm font-bold transition-all duration-300 ${
                language === 'bengali' 
                  ? 'bg-gradient-to-r from-blue-600 to-indigo-600 text-white shadow-[0_5px_15px_rgba(37,99,235,0.3)] scale-105' 
                  : 'text-gray-400 hover:bg-gray-800 hover:text-white hover:translate-x-1'
              }`}
            >
              Bengali (বাংলা)
            </button>
          </div>
        </div>

        {user && (
          <button
            onClick={logout}
            className="flex items-center justify-center w-full space-x-2 px-4 py-3 rounded-xl bg-red-500/10 text-red-500 hover:bg-gradient-to-r hover:from-red-500 hover:to-red-600 hover:text-white transition-all duration-300 font-bold border border-red-500/20 hover:border-transparent hover:shadow-[0_10px_20px_rgba(239,68,68,0.3)] hover:-translate-y-1 transform"
          >
            <LogOut size={20} />
            <span>Log Out</span>
          </button>
        )}
      </div>
    </aside>
  );
};

export default Sidebar;
