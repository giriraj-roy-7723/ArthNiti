import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { LanguageProvider } from "./context/LanguageContext";
import { AuthProvider } from "./context/AuthContext";
import MainLayout from "./layouts/MainLayout";
import Home from "./pages/Home";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
// import FinanceAnalyser from "./pages/FinanceAnalyser";
// import GovernmentSchemes from "./pages/GovernmentSchemes";
// import Chatbot from "./pages/Chatbot";
import MyBusinesses from "./pages/business/MyBusinesses";
import Profile from "./pages/Profile";
import BusinessWorkspace from "./pages/business/business_advisory/BusinessWorkspace";
import BusinessAnalysis from "./pages/business/business_advisory/BusinessAnalysis";
import FinancialAnalysis from "./pages/business/business_advisory/FinancialAnalysis";
import GovernmentSchemes from "./pages/business/business_advisory/GovernmentSchemes";
import PopulationAnalysis from './pages/business/business_advisory/business_analysis/PopulationAnalysis';
import CompetitionAnalysis from './pages/business/business_advisory/business_analysis/CompetitionAnalysis';
import SeasonalityAnalysis from './pages/business/business_advisory/business_analysis/SeasonalityAnalysis';
import MarketPrices from './pages/business/business_advisory/business_analysis/MarketPrices';
import SupplyChainAnalysis from "./pages/business/business_advisory/business_analysis/SupplyChainAnalysis";
import TransportationAnalysis from "./pages/business/business_advisory/business_analysis/TransportationAnalysis";
import Dashboard from "./pages/Dashboard";


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
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/profile" element={<Profile />} />
              <Route path="/businesses" element={<MyBusinesses />} />
              <Route
                path="/businesses/:businessId"
                element={<BusinessWorkspace />}
              />

              <Route
                path="/businesses/:businessId/analysis"
                element={<BusinessAnalysis />}
              />
              <Route
                path="/businesses/:businessId/analysis/population"
                element={<PopulationAnalysis />}
              />
              <Route
                path="/businesses/:businessId/analysis/competitors"
                element={<CompetitionAnalysis />}
              />
              <Route
                path="/businesses/:businessId/analysis/seasonality"
                element={<SeasonalityAnalysis />}
              />
              <Route
                path="/businesses/:businessId/analysis/supply-chain"
                element={<SupplyChainAnalysis />}
              />
              <Route
                path="/businesses/:businessId/analysis/transportation"
                element={<TransportationAnalysis />}
              />
              <Route
                path="/businesses/:businessId/analysis/market-prices"
                element={<MarketPrices />}
              />

              <Route
                path="/businesses/:businessId/financial-analysis"
                element={<FinancialAnalysis />}
              />

              <Route
                path="/businesses/:businessId/government-schemes"
                element={<GovernmentSchemes />}
              />
            </Routes>
          </MainLayout>
        </LanguageProvider>
      </AuthProvider>
    </Router>
  );
}
