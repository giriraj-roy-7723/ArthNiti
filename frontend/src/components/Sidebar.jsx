import { Link, useLocation } from "react-router-dom";
import { useLanguage } from "../context/LanguageContext";
import { useAuth } from "../context/AuthContext";
import {
  Home,
  LogIn,
  UserPlus,
  LogOut,
  Settings,
  Globe,
  Building2,
} from "lucide-react";

const Sidebar = () => {
  const { language, toggleLanguage } = useLanguage();
  const { user, logout } = useAuth();
  const location = useLocation();

  const isActive = (path) => location.pathname === path;

  const translations = {
    english: {
      finance: "Finance",
      home: "Home",
      login: "Login",
      signup: "Sign Up",
      dashboard: "Dashboard",
      myBusinesses: "My Businesses",
      language: "Language",
      english: "English",
      hindi: "Hindi (हिंदी)",
      bengali: "Bengali (বাংলা)",
      logout: "Log Out",
    },

    hindi: {
      finance: "वित्त",
      home: "होम",
      login: "लॉग इन",
      signup: "साइन अप",
      dashboard: "डैशबोर्ड",
      myBusinesses: "मेरे व्यवसाय",
      language: "भाषा",
      english: "अंग्रेज़ी",
      hindi: "हिंदी (हिंदी)",
      bengali: "बंगाली (বাংলা)",
      logout: "लॉग आउट",
    },

    bengali: {
      finance: "অর্থ",
      home: "হোম",
      login: "লগইন",
      signup: "সাইন আপ",
      dashboard: "ড্যাশবোর্ড",
      myBusinesses: "আমার ব্যবসা",
      language: "ভাষা",
      english: "ইংরেজি",
      hindi: "হিন্দি (हिंदी)",
      bengali: "বাংলা (বাংলা)",
      logout: "লগ আউট",
    },
  };

  // Fallback to English if an unexpected language value is received
  const t = translations[language] || translations.english;

  const getLinkClasses = (path) => {
    return `flex items-center space-x-3 px-4 py-3 rounded-xl transition-all duration-300 transform preserve-3d ${
      isActive(path)
        ? "bg-gradient-to-r from-blue-600 to-indigo-600 text-white shadow-[0_10px_20px_rgba(37,99,235,0.3)] translate-z-10 scale-105"
        : "text-gray-400 hover:bg-gray-800/80 hover:text-white hover:translate-x-2 hover:shadow-lg"
    }`;
  };

  return (
    <aside className="w-64 h-screen bg-gray-950/90 backdrop-blur-md border-r border-gray-800 flex flex-col justify-between flex-shrink-0 sticky top-0 shadow-[20px_0_50px_rgba(0,0,0,0.5)] z-50">

      {/* 3D Inner Edge Reflection */}
      <div className="absolute inset-y-0 right-0 w-px bg-gradient-to-b from-white/10 via-white/5 to-transparent pointer-events-none" />

      <div className="p-6 relative z-10">

        {/* Logo */}
        <div className="flex items-center space-x-3 mb-10 transform preserve-3d hover:rotate-y-12 transition-transform duration-500">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center shadow-[0_10px_20px_rgba(37,99,235,0.4)] translate-z-10 border-t border-l border-white/20">
            <span className="text-white font-bold text-xl drop-shadow-md">
              F
            </span>
          </div>

          <h1 className="text-xl font-extrabold bg-clip-text text-transparent bg-gradient-to-r from-white via-blue-100 to-gray-400 drop-shadow-sm translate-z-6">
            {t.finance}
          </h1>
        </div>

        {/* Navigation */}
        <nav className="space-y-3 perspective-[1000px]">

          {/* Home */}
          <Link
            to="/"
            className={getLinkClasses("/")}
          >
            <Home
              size={20}
              className={isActive("/") ? "drop-shadow-md" : ""}
            />

            <span className="font-semibold">
              {t.home}
            </span>
          </Link>

          {!user ? (
            <>
              {/* Login */}
              <Link
                to="/login"
                className={getLinkClasses("/login")}
              >
                <LogIn
                  size={20}
                  className={isActive("/login") ? "drop-shadow-md" : ""}
                />

                <span className="font-semibold">
                  {t.login}
                </span>
              </Link>

              {/* Sign Up */}
              <Link
                to="/signup"
                className={getLinkClasses("/signup")}
              >
                <UserPlus
                  size={20}
                  className={isActive("/signup") ? "drop-shadow-md" : ""}
                />

                <span className="font-semibold">
                  {t.signup}
                </span>
              </Link>
            </>
          ) : (
            <>
              {/* Dashboard */}
              <Link
                to="/dashboard"
                className={getLinkClasses("/dashboard")}
              >
                <Settings
                  size={20}
                  className={
                    isActive("/dashboard")
                      ? "drop-shadow-md"
                      : ""
                  }
                />

                <span className="font-semibold">
                  {t.dashboard}
                </span>
              </Link>

              {/* My Businesses */}
              {user.role === "enterpreneur" && (
                <Link
                  to="/businesses"
                  className={getLinkClasses("/businesses")}
                >
                  <Building2
                    size={20}
                    className={
                      isActive("/businesses")
                        ? "drop-shadow-md"
                        : ""
                    }
                  />

                  <span className="font-semibold">
                    {t.myBusinesses}
                  </span>
                </Link>
              )}
            </>
          )}
        </nav>
      </div>

      {/* Bottom Section */}
      <div className="p-6 space-y-6 relative z-10 perspective-[1000px]">

        {/* Language Selector */}
        <div className="bg-gray-900/80 rounded-2xl p-4 border border-gray-800 shadow-[inset_0_2px_10px_rgba(0,0,0,0.5),0_10px_20px_rgba(0,0,0,0.2)] transform preserve-3d hover:rotate-x-6 transition-transform duration-500">

          <div className="flex items-center space-x-2 text-gray-400 mb-4 text-sm font-semibold translate-z-6">
            <Globe size={16} />
            <span>{t.language}</span>
          </div>

          <div className="flex flex-col space-y-2 translate-z-6">

            {/* English */}
            <button
              onClick={() => toggleLanguage("english")}
              className={`text-left px-4 py-2.5 rounded-xl text-sm font-bold transition-all duration-300 ${
                language === "english"
                  ? "bg-gradient-to-r from-blue-600 to-indigo-600 text-white shadow-[0_5px_15px_rgba(37,99,235,0.3)] scale-105"
                  : "text-gray-400 hover:bg-gray-800 hover:text-white hover:translate-x-1"
              }`}
            >
              {t.english}
            </button>

            {/* Hindi */}
            <button
              onClick={() => toggleLanguage("hindi")}
              className={`text-left px-4 py-2.5 rounded-xl text-sm font-bold transition-all duration-300 ${
                language === "hindi"
                  ? "bg-gradient-to-r from-blue-600 to-indigo-600 text-white shadow-[0_5px_15px_rgba(37,99,235,0.3)] scale-105"
                  : "text-gray-400 hover:bg-gray-800 hover:text-white hover:translate-x-1"
              }`}
            >
              {t.hindi}
            </button>

            {/* Bengali */}
            <button
              onClick={() => toggleLanguage("bengali")}
              className={`text-left px-4 py-2.5 rounded-xl text-sm font-bold transition-all duration-300 ${
                language === "bengali"
                  ? "bg-gradient-to-r from-blue-600 to-indigo-600 text-white shadow-[0_5px_15px_rgba(37,99,235,0.3)] scale-105"
                  : "text-gray-400 hover:bg-gray-800 hover:text-white hover:translate-x-1"
              }`}
            >
              {t.bengali}
            </button>

          </div>
        </div>

        {/* Logout */}
        {user && (
          <button
            onClick={logout}
            className="flex items-center justify-center w-full space-x-2 px-4 py-3 rounded-xl bg-red-500/10 text-red-500 hover:bg-gradient-to-r hover:from-red-500 hover:to-red-600 hover:text-white transition-all duration-300 font-bold border border-red-500/20 hover:border-transparent hover:shadow-[0_10px_20px_rgba(239,68,68,0.3)] hover:-translate-y-1 transform"
          >
            <LogOut size={20} />

            <span>
              {t.logout}
            </span>
          </button>
        )}

      </div>
    </aside>
  );
};

export default Sidebar;