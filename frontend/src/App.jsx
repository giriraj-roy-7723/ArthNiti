import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { LanguageProvider } from './context/LanguageContext';
import { AuthProvider } from './context/AuthContext';
import MainLayout from './layouts/MainLayout';
import Home from './pages/Home';
import Login from './pages/Login';
import Signup from './pages/Signup';
import BusinessAnalysis from './pages/BusinessAnalysis';
import FinanceAnalyser from './pages/FinanceAnalyser';
import GovernmentSchemes from './pages/GovernmentSchemes';
import Chatbot from './pages/Chatbot';
import MyBusinesses from "./pages/MyBusinesses";

export default function App() {
  return (
    <Router>
      <AuthProvider>
        <LanguageProvider>
          <MainLayout>
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/login" element={<Login />} />
              <Route path="/signup" element={<Signup />} />
              <Route path="/dashboard" element={<BusinessAnalysis />} />
              <Route
                path="/dashboard/business-analysis"
                element={<BusinessAnalysis />}
              />
              <Route
                path="/dashboard/finance-analyser"
                element={<FinanceAnalyser />}
              />
              <Route
                path="/dashboard/government-schemes"
                element={<GovernmentSchemes />}
              />
              <Route path="/dashboard/chatbot" element={<Chatbot />} />
              <Route path="/businesses" element={<MyBusinesses />} />
            </Routes>
          </MainLayout>
        </LanguageProvider>
      </AuthProvider>
    </Router>
  );
}
