import { useState } from "react";
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
  User,
  ChevronRight,
  PanelLeftClose,
  PanelLeftOpen,
  FileText,
} from "lucide-react";

const Sidebar = () => {
  const { language, toggleLanguage } = useLanguage();
  const { user, logout } = useAuth();
  const location = useLocation();
  const [isOpen, setIsOpen] = useState(true);

  const isActive = (path) => location.pathname === path;

  const translations = {
    english: {
      brand: "ArthNiti",
      home: "Home",
      login: "Login",
      signup: "Sign Up",
      dashboard: "Dashboard",
      myBusinesses: "My Businesses",
      businessDetails: "Business Directory",
      language: "Language",
      profile: "Profile",
      english: "English",
      hindi: "Hindi (हिंदी)",
      bengali: "Bengali (বাংলা)",
      logout: "Log Out",
      logoAlt: "ArthNiti Logo",
      openNavigation: "Open Navigation",
      collapseNavigation: "Collapse Navigation",
    },
    hindi: {
      brand: "अर्थनीति",
      home: "होम",
      login: "लॉग इन",
      signup: "साइन अप",
      dashboard: "डैशबोर्ड",
      myBusinesses: "मेरे व्यवसाय",
      businessDetails: "व्यवसाय निर्देशिका",
      language: "भाषा",
      profile: "प्रोफ़ाइल",
      english: "अंग्रेज़ी",
      hindi: "हिंदी (हिंदी)",
      bengali: "बंगाली (বাংলা)",
      logout: "लॉग आउट",
      logoAlt: "अर्थनीति लोगो",
      openNavigation: "नेविगेशन खोलें",
      collapseNavigation: "नेविगेशन संक्षिप्त करें",
    },
    bengali: {
      brand: "অর্থনীতি",
      home: "হোম",
      login: "লগইন",
      signup: "সাইন আপ",
      dashboard: "ড্যাশবোর্ড",
      myBusinesses: "আমার ব্যবসা",
      businessDetails: "ব্যবসা ডিরেক্টরি",
      language: "ভাষা",
      profile: "প্রোফাইল",
      english: "ইংরেজি",
      hindi: "হিন্দি (हिंदी)",
      bengali: "বাংলা (বাংলা)",
      logout: "লগ আউট",
      logoAlt: "অর্থনীতি লোগো",
      openNavigation: "নেভিগেশন খুলুন",
      collapseNavigation: "নেভিগেশন বন্ধ করুন",
    },
  };

  const t = translations[language] || translations.english;

  const getLinkClasses = (path) => {
    return `flex items-center space-x-3 px-4 py-3 rounded-xl transition-all duration-300 transform preserve-3d ${
      isActive(path)
        ? "bg-gradient-to-r from-blue-600 to-indigo-600 text-white shadow-[0_10px_20px_rgba(37,99,235,0.3)] translate-z-10 scale-105"
        : "text-gray-400 hover:bg-gray-800/80 hover:text-white hover:translate-x-2 hover:shadow-lg"
    }`;
  };

  const getUserName = () => {
    if (!user) return "";
    const firstName = user.first_name || "";
    const lastName = user.last_name || "";
    const fullName = `${firstName} ${lastName}`.trim();
    return fullName || user.name || "User";
  };

  const getUsername = () => {
    if (!user) return "";
    return user.username || user.email || "";
  };

  return (
    <>
      {!isOpen && (
        <button
          type="button"
          onClick={() => setIsOpen(true)}
          className="fixed top-5 left-5 z-50 flex h-10 w-10 items-center justify-center rounded-xl border border-gray-800 bg-gray-900/90 text-gray-400 shadow-xl backdrop-blur-md transition-all hover:border-blue-500/40 hover:bg-gray-800 hover:text-white"
          title={t.openNavigation}
        >
          <PanelLeftOpen size={20} />
        </button>
      )}

      <aside
        className={`h-screen bg-gray-950/90 backdrop-blur-md border-r border-gray-800 flex flex-col justify-between flex-shrink-0 sticky top-0 shadow-[20px_0_50px_rgba(0,0,0,0.5)] z-40 transition-all duration-300 ease-in-out ${
          isOpen
            ? "w-64 opacity-100"
            : "w-0 opacity-0 pointer-events-none border-none p-0 overflow-hidden"
        }`}
      >
        <div className="w-64 h-full flex flex-col justify-between">
          <div className="absolute inset-y-0 right-0 w-px bg-gradient-to-b from-white/10 via-white/5 to-transparent pointer-events-none" />

          <div className="p-6 relative z-10 overflow-y-auto">
            <div className="flex items-center justify-between mb-8">
              <Link
                to="/"
                className="flex items-center space-x-3 transform preserve-3d hover:rotate-y-12 transition-transform duration-500"
              >
                <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500/20 to-indigo-600/20 p-2 flex items-center justify-center shadow-[0_10px_20px_rgba(37,99,235,0.25)] translate-z-10 border border-blue-500/30">
                  <img
                    src="/icon.svg"
                    alt={t.logoAlt}
                    className="w-full h-full object-contain drop-shadow-md"
                  />
                </div>

                <h1 className="text-xl font-extrabold bg-clip-text text-transparent bg-gradient-to-r from-white via-blue-100 to-gray-400 drop-shadow-sm translate-z-6">
                  {t.brand}
                </h1>
              </Link>

              <button
                type="button"
                onClick={() => setIsOpen(false)}
                className="flex h-8 w-8 items-center justify-center rounded-lg border border-gray-800 bg-gray-900/60 text-gray-400 transition hover:border-gray-700 hover:bg-gray-800 hover:text-white"
                title={t.collapseNavigation}
              >
                <PanelLeftClose size={16} />
              </button>
            </div>

            <nav className="space-y-3 perspective-[1000px]">
              <Link to="/" className={getLinkClasses("/")}>
                <Home
                  size={20}
                  className={isActive("/") ? "drop-shadow-md" : ""}
                />
                <span className="font-semibold">{t.home}</span>
              </Link>

              {!user ? (
                <>
                  <Link to="/login" className={getLinkClasses("/login")}>
                    <LogIn
                      size={20}
                      className={isActive("/login") ? "drop-shadow-md" : ""}
                    />
                    <span className="font-semibold">{t.login}</span>
                  </Link>

                  <Link to="/signup" className={getLinkClasses("/signup")}>
                    <UserPlus
                      size={20}
                      className={isActive("/signup") ? "drop-shadow-md" : ""}
                    />
                    <span className="font-semibold">{t.signup}</span>
                  </Link>
                </>
              ) : (
                <>
                  <Link
                    to="/dashboard"
                    className={getLinkClasses("/dashboard")}
                  >
                    <Settings
                      size={20}
                      className={isActive("/dashboard") ? "drop-shadow-md" : ""}
                    />
                    <span className="font-semibold">{t.dashboard}</span>
                  </Link>

                  {["enterpreneur", "entrepreneur"].includes(
                    String(user.role || "").toLowerCase(),
                  ) && (
                    <Link
                      to="/businesses"
                      className={getLinkClasses("/businesses")}
                    >
                      <Building2
                        size={20}
                        className={
                          isActive("/businesses") ? "drop-shadow-md" : ""
                        }
                      />
                      <span className="font-semibold">{t.myBusinesses}</span>
                    </Link>
                  )}
                </>
              )}

              {/* Public Business Details - available to logged-in and logged-out users */}
              <Link
                to="/businesses/details"
                className={getLinkClasses("/businesses/details")}
              >
                <FileText
                  size={20}
                  className={
                    isActive("/businesses/details") ? "drop-shadow-md" : ""
                  }
                />
                <span className="font-semibold">{t.businessDetails}</span>
              </Link>
            </nav>
          </div>

          <div className="p-6 space-y-4 relative z-10 perspective-[1000px]">
            <div className="bg-gray-900/80 rounded-2xl p-4 border border-gray-800 shadow-[inset_0_2px_10px_rgba(0,0,0,0.5),0_10px_20px_rgba(0,0,0,0.2)] transform preserve-3d hover:rotate-x-6 transition-transform duration-500">
              <div className="flex items-center space-x-2 text-gray-400 mb-4 text-sm font-semibold translate-z-6">
                <Globe size={16} />
                <span>{t.language}</span>
              </div>

              <div className="flex flex-col space-y-2 translate-z-6">
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

            {user && (
              <Link
                to="/profile"
                className={`group flex items-center gap-3 w-full p-3 rounded-2xl border transition-all duration-300 transform ${
                  isActive("/profile")
                    ? "bg-gradient-to-r from-blue-600/20 to-indigo-600/20 border-blue-500/40 shadow-[0_8px_20px_rgba(37,99,235,0.15)]"
                    : "bg-gray-900/80 border-gray-800 hover:bg-gray-800/80 hover:border-gray-700 hover:-translate-y-1 hover:shadow-lg"
                }`}
              >
                <div className="w-11 h-11 rounded-xl bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center flex-shrink-0 overflow-hidden shadow-[0_5px_15px_rgba(37,99,235,0.25)]">
                  {user.profile_image || user.profile_pic ? (
                    <img
                      src={user.profile_image || user.profile_pic}
                      alt={getUserName()}
                      className="w-full h-full object-cover"
                    />
                  ) : (
                    <User size={22} className="text-white" />
                  )}
                </div>

                <div className="flex-1 min-w-0">
                  <p className="text-white font-bold text-sm truncate">
                    {getUserName()}
                  </p>
                  <p className="text-gray-500 text-xs truncate mt-0.5">
                    {getUsername()}
                  </p>
                </div>

                <ChevronRight
                  size={18}
                  className={`flex-shrink-0 transition-all duration-300 ${
                    isActive("/profile")
                      ? "text-blue-400"
                      : "text-gray-600 group-hover:text-gray-300 group-hover:translate-x-1"
                  }`}
                />
              </Link>
            )}

            {user && (
              <button
                onClick={logout}
                className="flex items-center justify-center w-full space-x-2 px-4 py-3 rounded-xl bg-red-500/10 text-red-500 hover:bg-gradient-to-r hover:from-red-500 hover:to-red-600 hover:text-white transition-all duration-300 font-bold border border-red-500/20 hover:border-transparent hover:shadow-[0_10px_20px_rgba(239,68,68,0.3)] hover:-translate-y-1 transform"
              >
                <LogOut size={20} />
                <span>{t.logout}</span>
              </button>
            )}
          </div>
        </div>
      </aside>
    </>
  );
};

export default Sidebar;
