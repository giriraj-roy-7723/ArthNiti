import { useEffect, useState, useRef } from "react";
import { useNavigate, useParams } from "react-router-dom";
import {
  ArrowLeft,
  BarChart3,
  Sparkles,
  Users,
  ShoppingCart,
  Boxes,
  Truck,
  CloudSun,
  FileText,
  MapPin,
  TrendingUp,
  AlertCircle,
  Loader2,
  RefreshCw,
  LocateFixed,
  Play,
  Clock,
  CheckCircle2,
} from "lucide-react";

import { api, aiApi } from "../../../utils/api";
import { useLanguage } from "../../../context/LanguageContext";

const translations = {
  english: {
    loading: "Loading business analysis...",
    backWorkspace: "Back to Workspace",
    aiAnalysis: "AI Analysis",
    businessAnalysis: "Business Analysis",
    regenerate: "Regenerate Analysis",
    regenerating: "Regenerating...",
    operationFailed: "Analysis operation failed",
    report: "Feasibility Report",
    generatedAssessment: "AI-Generated Business Assessment",
    evidenceInsights: "Evidence & Insights",
    exploreData: "Explore Analysis Data",
    selectSection: "Select a section to view detailed evidence",
    viewDetails: "View details →",
    dataAvailable: "Analysis data available",
    noData: "No data available",
    population: "Population Analysis",
    populationDescription:
      "Understand the population, household base, density and market reach around your business.",
    competition: "Competition Analysis",
    competitionDescription:
      "Explore nearby competitors, competitor density and the local competitive landscape.",
    marketPrices: "Market Prices",
    marketPricesDescription:
      "Review commodity pricing statistics, market data and available price intelligence.",
    supplyChain: "Supply Chain",
    supplyChainDescription:
      "Inspect sourcing, processing, cold-chain infrastructure and supply-chain scores.",
    transportation: "Transportation",
    transportationDescription:
      "Review modeled routes, travel distances, vehicles and estimated logistics costs.",
    seasonality: "Seasonality",
    seasonalityDescription:
      "Analyze monthly demand, production, pricing, rainfall and seasonal business risks.",
    populationStat: "Population",
    radius: "Market Radius",
    competitors: "Competitors",
    supplyScore: "Supply Chain Score",
    logisticsCost: "Modeled Logistics Cost",
    monthlyFreight: "Estimated monthly freight OPEX:",
    generationFailed: "Generation failed",
    generateBusinessAnalysis: "Generate Business Analysis",
    aiBusinessIntelligence: "AI Business Intelligence",
    generationDescription:
      "Review business details and define your market radius to initiate AI intelligence analysis.",
    businessInformation: "Business Details",
    analysisParameters: "Analysis Parameters",
    analysisRadius: "Analysis Radius",
    radiusDescription:
      "Geographic radius used for population and competitor analysis.",
    cancel: "Cancel",
    generate: "Generate Analysis",
    generating: "Generating Analysis...",
    noReport: "No feasibility report is available.",
    businessId: "Business ID",
    noAnalysisError: "Failed to load business analysis.",
    tryAgain: "Try Again",
    longRunningNoticeTitle: "Analysis is being processed in the background",
    longRunningNoticeText:
      "Comprehensive market analysis (population, competitors, supply-chain & logistics) typically takes 5 to 10 minutes. You don't need to stay on this page — feel free to continue other work in your workspace. We'll have everything ready when you return.",
    continueWorkspace: "Continue with other tasks",
  },
  hindi: {
    loading: "व्यवसाय विश्लेषण लोड हो रहा है...",
    backWorkspace: "वर्कस्पेस पर वापस जाएँ",
    aiAnalysis: "AI विश्लेषण",
    businessAnalysis: "व्यवसाय विश्लेषण",
    regenerate: "विश्लेषण दोबारा बनाएँ",
    regenerating: "दोबारा बनाया जा रहा है...",
    operationFailed: "विश्लेषण प्रक्रिया विफल रही",
    report: "व्यवहार्यता रिपोर्ट",
    generatedAssessment: "AI द्वारा तैयार व्यवसाय मूल्यांकन",
    evidenceInsights: "साक्ष्य और जानकारी",
    exploreData: "विश्लेषण डेटा देखें",
    selectSection: "विस्तृत जानकारी देखने के लिए एक अनुभाग चुनें",
    viewDetails: "विवरण देखें →",
    dataAvailable: "विश्लेषण डेटा उपलब्ध है",
    noData: "डेटा उपलब्ध नहीं है",
    population: "जनसंख्या विश्लेषण",
    populationDescription:
      "अपने व्यवसाय के आसपास की जनसंख्या, परिवारों, घनत्व और बाजार पहुँच को समझें।",
    competition: "प्रतिस्पर्धा विश्लेषण",
    competitionDescription:
      "आसपास के प्रतिस्पर्धियों, प्रतिस्पर्धी घनत्व और स्थानीय बाजार की स्थिति देखें।",
    marketPrices: "बाजार मूल्य",
    marketPricesDescription:
      "वस्तुओं के मूल्य आँकड़े, बाजार डेटा और उपलब्ध मूल्य जानकारी देखें।",
    supplyChain: "आपूर्ति श्रृंखला",
    supplyChainDescription:
      "स्रोत, प्रसंस्करण, कोल्ड-चेन और आपूर्ति श्रृंखला स्कोर का निरीक्षण करें।",
    transportation: "परिवहन",
    transportationDescription:
      "मार्ग, दूरी, वाहन और अनुमानित लॉजिस्टिक्स लागत देखें।",
    seasonality: "मौसमी विश्लेषण",
    seasonalityDescription:
      "मासिक मांग, उत्पादन, मूल्य, वर्षा और मौसमी व्यावसायिक जोखिमों का विश्लेषण करें।",
    populationStat: "जनसंख्या",
    radius: "बाजार त्रिज्या",
    competitors: "प्रतिस्पर्धी",
    supplyScore: "आपूर्ति श्रृंखला स्कोर",
    logisticsCost: "अनुमानित लॉजिस्टिक्स लागत",
    monthlyFreight: "अनुमानित मासिक फ्रेट OPEX:",
    generationFailed: "विश्लेषण निर्माण विफल रहा",
    generateBusinessAnalysis: "व्यवसाय विश्लेषण बनाएँ",
    aiBusinessIntelligence: "AI बिज़नेस इंटेलिजेंस",
    generationDescription:
      "व्यवसाय विवरण की समीक्षा करें और विश्लेषण शुरू करने के लिए त्रिज्या चुनें।",
    businessInformation: "व्यवसाय विवरण",
    analysisParameters: "विश्लेषण पैरामीटर",
    analysisRadius: "विश्लेषण त्रिज्या",
    radiusDescription:
      "जनसंख्या और प्रतिस्पर्धा विश्लेषण के लिए उपयोग की जाने वाली भौगोलिक सीमा।",
    cancel: "रद्द करें",
    generate: "विश्लेषण बनाएँ",
    generating: "विश्लेषण बनाया जा रहा है...",
    noReport: "कोई व्यवहार्यता रिपोर्ट उपलब्ध नहीं है।",
    businessId: "व्यवसाय ID",
    noAnalysisError: "व्यवसाय विश्लेषण लोड नहीं हो सका।",
    tryAgain: "फिर से प्रयास करें",
    longRunningNoticeTitle: "विश्लेषण बैकग्राउंड में तैयार हो रहा है",
    longRunningNoticeText:
      "जनसंख्या, प्रतिस्पर्धा और लॉजिस्टिक्स डेटा का विस्तृत विश्लेषण तैयार करने में 5 से 10 मिनट लग सकते हैं। आपको इस पेज पर रुके रहने की आवश्यकता नहीं है — आप अपने अन्य कार्य जारी रख सकते हैं।",
    continueWorkspace: "अन्य काम जारी रखें",
  },
  bengali: {
    loading: "ব্যবসায়িক বিশ্লেষণ লোড হচ্ছে...",
    backWorkspace: "ওয়ার্কস্পেসে ফিরে যান",
    aiAnalysis: "AI বিশ্লেষণ",
    businessAnalysis: "ব্যবসায়িক বিশ্লেষণ",
    regenerate: "বিশ্লেষণ পুনরায় তৈরি করুন",
    regenerating: "পুনরায় তৈরি হচ্ছে...",
    operationFailed: "বিশ্লেষণ প্রক্রিয়া ব্যর্থ হয়েছে",
    report: "ব্যবসায়িক সম্ভাব্যতা রিপোর্ট",
    generatedAssessment: "AI-তৈরি ব্যবসায়িক মূল্যায়ন",
    evidenceInsights: "প্রমাণ ও অন্তর্দৃষ্টি",
    exploreData: "বিশ্লেষণের তথ্য দেখুন",
    selectSection: "বিস্তারিত তথ্য দেখতে একটি বিভাগ নির্বাচন করুন",
    viewDetails: "বিস্তারিত দেখুন →",
    dataAvailable: "বিশ্লেষণের তথ্য উপলব্ধ",
    noData: "কোনো তথ্য উপলব্ধ নেই",
    population: "জনসংখ্যা বিশ্লেষণ",
    populationDescription:
      "আপনার ব্যবসার আশেপাশের জনসংখ্যা, পরিবার, ঘনত্ব এবং বাজারের পরিধি বুঝুন।",
    competition: "প্রতিযোগিতা বিশ্লেষণ",
    competitionDescription:
      "কাছাকাছি প্রতিযোগী, প্রতিযোগিতার ঘনত্ব এবং স্থানীয় বাজারের পরিস্থিতি দেখুন।",
    marketPrices: "বাজার মূল্য",
    marketPricesDescription:
      "পণ্যের মূল্য পরিসংখ্যান, বাজার তথ্য এবং উপলব্ধ মূল্য সংক্রান্ত তথ্য দেখুন।",
    supplyChain: "সরবরাহ ব্যবস্থা",
    supplyChainDescription:
      "উৎস, প্রক্রিয়াকরণ, কোল্ড-চেইন এবং সরবরাহ ব্যবস্থার স্কোর দেখুন।",
    transportation: "পরিবহন",
    transportationDescription:
      "রুট, দূরত্ব, যানবাহন এবং আনুমানিক লজিস্টিক খরচ দেখুন।",
    seasonality: "মৌসুমি বিশ্লেষণ",
    seasonalityDescription:
      "মাসিক চাহিদা, উৎপাদন, মূল্য, বৃষ্টিপাত এবং মৌসুমি ব্যবসায়িক ঝুঁকি বিশ্লেষণ করুন।",
    populationStat: "জনসংখ্যা",
    radius: "বাজারের পরিধি",
    competitors: "প্রতিযোগী",
    supplyScore: "সরবরাহ ব্যবস্থার স্কোর",
    logisticsCost: "আনুমানিক লজিস্টিক খরচ",
    monthlyFreight: "আনুমানিক মাসিক ফ্রেট OPEX:",
    generationFailed: "বিশ্লেষণ তৈরি ব্যর্থ হয়েছে",
    generateBusinessAnalysis: "ব্যবসায়িক বিশ্লেষণ তৈরি করুন",
    aiBusinessIntelligence: "AI বিজনেস ইন্টেলিজেন্স",
    generationDescription:
      "ব্যবসায়ের বিবরণ পর্যালোচনা করুন এবং বিশ্লেষণের পরিধি নির্ধারণ করুন।",
    businessInformation: "ব্যবসায়ের তথ্য",
    analysisParameters: "বিশ্লেষণের প্যারামিটার",
    analysisRadius: "বিশ্লেষণের পরিধি",
    radiusDescription:
      "জনসংখ্যা এবং প্রতিযোগিতা বিশ্লেষণের জন্য ব্যবহৃত ভৌগোলিক পরিধি।",
    cancel: "বাতিল",
    generate: "বিশ্লেষণ তৈরি করুন",
    generating: "বিশ্লেষণ তৈরি হচ্ছে...",
    noReport: "কোনো ব্যবসায়িক সম্ভাব্যতা রিপোর্ট উপলব্ধ নেই।",
    businessId: "ব্যবসার ID",
    noAnalysisError: "ব্যবসায়িক বিশ্লেষণ লোড করা যায়নি।",
    tryAgain: "আবার চেষ্টা করুন",
    longRunningNoticeTitle: "বিশ্লেষণ ব্যাকগ্রাউন্ডে তৈরি হচ্ছে",
    longRunningNoticeText:
      "জনসংখ্যা, প্রতিযোগী এবং লজিস্টিকসের সম্পূর্ণ তথ্য বিশ্লেষণ করতে প্রায় ৫ থেকে ১০ মিনিট সময় লাগতে পারে। আপনাকে এই পৃষ্ঠায় অপেক্ষা করতে হবে না — আপনি নিরাপদে অন্য কাজ চালিয়ে যেতে পারেন।",
    continueWorkspace: "অন্যান্য কাজ চালিয়ে যান",
  },
};

const normalizeLanguage = (value) => {
  const normalized = String(value || "").toLowerCase();
  if (normalized === "hi" || normalized === "hindi") return "hindi";
  if (normalized === "bn" || normalized === "bengali") return "bengali";
  return "english";
};

const BusinessAnalysis = () => {
  const { businessId } = useParams();
  const navigate = useNavigate();
  const { language } = useLanguage();

  const currentLanguage = normalizeLanguage(language);
  const t = translations[currentLanguage];

  const [report, setReport] = useState(null);
  const [businessData, setBusinessData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [showGenerationModal, setShowGenerationModal] = useState(false);
  const [generating, setGenerating] = useState(false);
  const [regenerating, setRegenerating] = useState(false);
  const [radiusKm, setRadiusKm] = useState("10");

  const pollIntervalRef = useRef(null);

  const getApiLanguage = () => currentLanguage;

  const fetchBusinessProfile = async () => {
    const res = await api.get(`/businesses/${businessId}`);
    return res?.data?.business || res?.data || res;
  };

  const loadReport = async (silent = false) => {
    try {
      if (!silent) setLoading(true);
      setError("");

      const response = await aiApi.get(
        `api/v1/businesses/${businessId}/report?language=${getApiLanguage()}`,
      );
      setReport(response.data || response);
      setShowGenerationModal(false);
      setGenerating(false);
      setRegenerating(false);

      if (pollIntervalRef.current) {
        clearInterval(pollIntervalRef.current);
        pollIntervalRef.current = null;
      }
    } catch (err) {
      if (err?.response?.status === 404) {
        setReport(null);
        setError("");
        try {
          const business = await fetchBusinessProfile();
          setBusinessData(business);
          setShowGenerationModal(true);
        } catch (fetchErr) {
          setError(
            fetchErr?.response?.data?.detail ||
              fetchErr.message ||
              t.noAnalysisError,
          );
        }
      } else {
        if (!silent) {
          setError(
            err?.response?.data?.detail || err?.message || t.noAnalysisError,
          );
        }
      }
    } finally {
      if (!silent) setLoading(false);
    }
  };

  useEffect(() => {
    if (businessId) {
      loadReport();
    }
    return () => {
      if (pollIntervalRef.current) {
        clearInterval(pollIntervalRef.current);
      }
    };
  }, [businessId, language]);

  const startBackgroundPolling = () => {
    if (pollIntervalRef.current) clearInterval(pollIntervalRef.current);
    pollIntervalRef.current = setInterval(() => {
      loadReport(true);
    }, 15000); // Check every 15s in background
  };

  const handleGenerate = async (event) => {
    event?.preventDefault();
    if (generating || !businessData) return;

    try {
      setGenerating(true);
      setError("");

      const requestBody = {
        business_id: businessId,
        business_name: businessData.business_name,
        business_type: businessData.category,
        business_description: businessData.description || null,
        country: businessData.country || "India",
        state: businessData.state,
        district: businessData.district,
        city: businessData.city || null,
        village: businessData.village || null,
        pincode: businessData.pincode || null,
        margin_capital: Number(businessData.margin_capital || 0),
        radius_km: Number(radiusKm),
        language: getApiLanguage(),
      };

      startBackgroundPolling();

      const response = await aiApi.post("api/v1/report/generate", requestBody);
      setReport(response.data || response);
      setShowGenerationModal(false);
      setGenerating(false);
      if (pollIntervalRef.current) clearInterval(pollIntervalRef.current);
    } catch (err) {
      setError(
        err?.response?.data?.detail || err?.message || t.generationFailed,
      );
      setGenerating(false);
      if (pollIntervalRef.current) clearInterval(pollIntervalRef.current);
    }
  };

  const handleRegenerate = async () => {
    if (regenerating) return;

    try {
      setRegenerating(true);
      setError("");

      const business = await fetchBusinessProfile();
      const existingRadius =
        report?.raw_evidence?.population?.data?.radius_km ||
        report?.raw_evidence?.population?.radius_km ||
        radiusKm ||
        10;

      const requestBody = {
        business_id: businessId,
        business_name: business.business_name,
        business_type: business.category,
        business_description: business.description || null,
        country: business.country || "India",
        state: business.state,
        district: business.district,
        city: business.city || null,
        village: business.village || null,
        pincode: business.pincode || null,
        margin_capital: Number(business.margin_capital || 0),
        radius_km: Number(existingRadius),
        language: getApiLanguage(),
      };

      startBackgroundPolling();

      const response = await aiApi.post(
        "api/v1/report/generate?force=true",
        requestBody,
      );
      setReport(response.data || response);
      setRegenerating(false);
      if (pollIntervalRef.current) clearInterval(pollIntervalRef.current);
    } catch (err) {
      setError(
        err?.response?.data?.detail ||
          err?.message ||
          "Failed to regenerate business analysis.",
      );
      setRegenerating(false);
      if (pollIntervalRef.current) clearInterval(pollIntervalRef.current);
    }
  };

  const evidenceCards = [
    {
      title: t.population,
      description: t.populationDescription,
      icon: Users,
      path: "population",
      color: "blue",
      key: "population",
    },
    {
      title: t.competition,
      description: t.competitionDescription,
      icon: ShoppingCart,
      path: "competitors",
      color: "violet",
      key: "competitors",
    },
    {
      title: t.marketPrices,
      description: t.marketPricesDescription,
      icon: TrendingUp,
      path: "market-prices",
      color: "emerald",
      key: "market_price",
    },
    {
      title: t.supplyChain,
      description: t.supplyChainDescription,
      icon: Boxes,
      path: "supply-chain",
      color: "amber",
      key: "supply_chain",
    },
    {
      title: t.transportation,
      description: t.transportationDescription,
      icon: Truck,
      path: "transportation",
      color: "cyan",
      key: "transportation",
    },
    {
      title: t.seasonality,
      description: t.seasonalityDescription,
      icon: CloudSun,
      path: "seasonality",
      color: "rose",
      key: "seasonality",
    },
  ];

  const getColorClasses = (color) => {
    const colors = {
      blue: {
        icon: "border-blue-500/20 bg-blue-500/10 text-blue-400",
        hover: "hover:border-blue-500/40",
      },
      violet: {
        icon: "border-violet-500/20 bg-violet-500/10 text-violet-400",
        hover: "hover:border-violet-500/40",
      },
      emerald: {
        icon: "border-emerald-500/20 bg-emerald-500/10 text-emerald-400",
        hover: "hover:border-emerald-500/40",
      },
      amber: {
        icon: "border-amber-500/20 bg-amber-500/10 text-amber-400",
        hover: "hover:border-amber-500/40",
      },
      cyan: {
        icon: "border-cyan-500/20 bg-cyan-500/10 text-cyan-400",
        hover: "hover:border-cyan-500/40",
      },
      rose: {
        icon: "border-rose-500/20 bg-rose-500/10 text-rose-400",
        hover: "hover:border-rose-500/40",
      },
    };
    return colors[color] || colors.blue;
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-950 px-4 py-8 text-white sm:px-6 lg:px-8">
        <div className="mx-auto flex min-h-[70vh] max-w-7xl items-center justify-center">
          <div className="flex flex-col items-center">
            <Loader2 className="mb-4 h-8 w-8 animate-spin text-blue-400" />
            <p className="text-sm text-gray-400">{t.loading}</p>
          </div>
        </div>
      </div>
    );
  }

  if (!report && showGenerationModal) {
    return (
      <GenerationPage
        business={businessData}
        radiusKm={radiusKm}
        onRadiusChange={(e) => setRadiusKm(e.target.value)}
        onSubmit={handleGenerate}
        onClose={() => navigate(`/businesses/${businessId}`)}
        loading={generating}
        error={error}
        t={t}
      />
    );
  }

  if (error && !report) {
    return (
      <div className="min-h-screen bg-gray-950 px-4 py-8 text-white sm:px-6 lg:px-8">
        <div className="mx-auto max-w-7xl">
          <button
            type="button"
            onClick={() => navigate(`/businesses/${businessId}`)}
            className="mb-8 inline-flex items-center gap-2 text-sm font-semibold text-gray-400 transition hover:text-white"
          >
            <ArrowLeft size={16} />
            {t.backWorkspace}
          </button>
          <div className="rounded-2xl border border-red-500/20 bg-red-500/5 p-8 text-center">
            <AlertCircle className="mx-auto mb-4 h-10 w-10 text-red-400" />
            <h2 className="text-xl font-bold">{t.operationFailed}</h2>
            <p className="mx-auto mt-2 max-w-lg text-sm leading-6 text-gray-400">
              {error}
            </p>
            <button
              type="button"
              onClick={() => loadReport(false)}
              className="mt-6 inline-flex items-center gap-2 rounded-xl bg-blue-600 px-5 py-3 text-sm font-bold transition hover:bg-blue-500"
            >
              <RefreshCw size={16} />
              {t.tryAgain}
            </button>
          </div>
        </div>
      </div>
    );
  }

  const population = report?.raw_evidence?.population?.data;
  const competitors = report?.raw_evidence?.competitors?.data;
  const supplyChain = report?.raw_evidence?.supply_chain?.data;
  const transportation = report?.raw_evidence?.transportation?.data;

  return (
    <div className="min-h-screen bg-gray-950 px-4 py-8 text-white sm:px-6 lg:px-8">
      <div className="mx-auto max-w-7xl">
        <button
          type="button"
          onClick={() => navigate(`/businesses/${businessId}`)}
          className="mb-6 inline-flex items-center gap-2 text-sm font-semibold text-gray-400 transition hover:text-white"
        >
          <ArrowLeft size={16} />
          {t.backWorkspace}
        </button>

        {/* Long Running Regeneration Banner */}
        {regenerating && (
          <div className="mb-6 rounded-2xl border border-blue-500/30 bg-blue-500/10 p-5 shadow-lg backdrop-blur-md">
            <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
              <div className="flex items-start gap-3">
                <Loader2 className="mt-1 h-5 w-5 shrink-0 animate-spin text-blue-400" />
                <div>
                  <h3 className="text-sm font-bold text-blue-300">
                    {t.longRunningNoticeTitle}
                  </h3>
                  <p className="mt-1 max-w-2xl text-xs leading-5 text-gray-300">
                    {t.longRunningNoticeText}
                  </p>
                </div>
              </div>
              <button
                type="button"
                onClick={() => navigate(`/businesses/${businessId}`)}
                className="whitespace-nowrap rounded-xl bg-blue-600 px-4 py-2 text-xs font-bold text-white transition hover:bg-blue-500"
              >
                {t.continueWorkspace}
              </button>
            </div>
          </div>
        )}

        <div className="mb-8 flex flex-col justify-between gap-5 lg:flex-row lg:items-center">
          <div className="flex items-center gap-4">
            <div className="flex h-14 w-14 shrink-0 items-center justify-center rounded-2xl border border-blue-500/20 bg-blue-500/10">
              <BarChart3 size={27} className="text-blue-400" />
            </div>
            <div>
              <div className="flex items-center gap-2 text-sm font-semibold text-blue-400">
                <Sparkles size={15} />
                {t.aiAnalysis}
              </div>
              <h1 className="mt-1 text-3xl font-extrabold">
                {t.businessAnalysis}
              </h1>
              <p className="mt-1 flex items-center gap-1 text-sm text-gray-500">
                <MapPin size={13} />
                {population?.location || `${t.businessId}: ${businessId}`}
              </p>
            </div>
          </div>

          <button
            type="button"
            onClick={handleRegenerate}
            disabled={regenerating}
            className="inline-flex items-center justify-center gap-2 rounded-xl border border-gray-800 bg-gray-900 px-4 py-3 text-sm font-bold text-gray-300 transition hover:border-gray-700 hover:bg-gray-800 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {regenerating ? (
              <Loader2 size={16} className="animate-spin" />
            ) : (
              <RefreshCw size={16} />
            )}
            {regenerating ? t.regenerating : t.regenerate}
          </button>
        </div>

        {error && (
          <div className="mb-6 flex items-start gap-3 rounded-xl border border-red-500/20 bg-red-500/5 p-4">
            <AlertCircle className="mt-0.5 h-5 w-5 shrink-0 text-red-400" />
            <div>
              <p className="font-semibold text-red-300">{t.operationFailed}</p>
              <p className="mt-1 text-sm text-gray-500">{error}</p>
            </div>
          </div>
        )}

        <div className="mb-8 rounded-2xl border border-gray-800 bg-gray-900/60 p-6 backdrop-blur-xl">
          <div className="mb-5 flex items-center justify-between">
            <div>
              <div className="flex items-center gap-2 text-sm font-semibold text-blue-400">
                <FileText size={15} />
                {t.report}
              </div>
              <h2 className="mt-1 text-xl font-bold">
                {t.generatedAssessment}
              </h2>
            </div>
            <div className="hidden rounded-lg border border-gray-800 bg-gray-950 px-3 py-2 text-xs text-gray-500 sm:block">
              Version {report?.version}
            </div>
          </div>
          <div className="max-h-[600px] overflow-y-auto rounded-xl border border-gray-800 bg-gray-950/70 p-5">
            <MarkdownReport
              markdown={report?.report_markdown || ""}
              noReport={t.noReport}
            />
          </div>
        </div>

        <div className="mb-5">
          <div className="flex items-end justify-between">
            <div>
              <p className="text-sm font-semibold text-blue-400">
                {t.evidenceInsights}
              </p>
              <h2 className="mt-1 text-2xl font-extrabold">{t.exploreData}</h2>
            </div>
            <span className="hidden text-xs text-gray-600 sm:block">
              {t.selectSection}
            </span>
          </div>
        </div>

        <div className="grid grid-cols-1 gap-5 md:grid-cols-2 xl:grid-cols-3">
          {evidenceCards.map((card) => {
            const Icon = card.icon;
            const colors = getColorClasses(card.color);
            const available = Boolean(report?.raw_evidence?.[card.key]?.data);

            return (
              <button
                key={card.title}
                type="button"
                disabled={!available}
                onClick={() =>
                  navigate(`/businesses/${businessId}/analysis/${card.path}`)
                }
                className={`group min-h-[210px] rounded-2xl border border-gray-800 bg-gray-900/60 p-6 text-left backdrop-blur-xl transition ${colors.hover} hover:-translate-y-0.5 hover:bg-gray-900 disabled:cursor-not-allowed disabled:opacity-50`}
              >
                <div className="flex items-start justify-between">
                  <div
                    className={`flex h-11 w-11 items-center justify-center rounded-xl border ${colors.icon}`}
                  >
                    <Icon size={21} />
                  </div>
                  <span className="text-xs font-semibold text-gray-600 transition group-hover:text-gray-400">
                    {t.viewDetails}
                  </span>
                </div>
                <h3 className="mt-5 text-lg font-bold">{card.title}</h3>
                <p className="mt-2 text-sm leading-6 text-gray-500">
                  {card.description}
                </p>
                <div className="mt-5 rounded-lg border border-gray-800 bg-gray-950/60 px-3 py-2 text-xs text-gray-600">
                  {available ? t.dataAvailable : t.noData}
                </div>
              </button>
            );
          })}
        </div>

        <div className="mt-8 grid grid-cols-2 gap-4 lg:grid-cols-4">
          <StatCard
            label={t.populationStat}
            value={
              population?.population
                ? population.population.toLocaleString("en-IN")
                : "—"
            }
          />
          <StatCard
            label={t.radius}
            value={population?.radius_km ? `${population.radius_km} km` : "—"}
          />
          <StatCard
            label={t.competitors}
            value={
              competitors?.competitor_summary?.total_unique_competitors ?? "—"
            }
          />
          <StatCard
            label={t.supplyScore}
            value={
              supplyChain?.overall_supply_chain_score != null
                ? `${supplyChain.overall_supply_chain_score}/100`
                : "—"
            }
          />
        </div>

        {transportation?.summary?.total_monthly_freight_opex_inr != null && (
          <div className="mt-5 rounded-2xl border border-amber-500/20 bg-amber-500/5 p-5">
            <div className="flex items-start gap-3">
              <Truck className="mt-0.5 h-5 w-5 shrink-0 text-amber-400" />
              <div>
                <h3 className="font-bold text-amber-300">{t.logisticsCost}</h3>
                <p className="mt-1 text-sm leading-6 text-gray-400">
                  {t.monthlyFreight}
                  <span className="ml-1 font-bold text-gray-200">
                    ₹
                    {transportation.summary.total_monthly_freight_opex_inr.toLocaleString(
                      "en-IN",
                      { maximumFractionDigits: 2 },
                    )}
                  </span>
                </p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

const GenerationPage = ({
  business,
  radiusKm,
  onRadiusChange,
  onSubmit,
  onClose,
  loading,
  error,
  t,
}) => {
  const navigate = useNavigate();
  const { businessId } = useParams();

  const locationText = [
    business?.village,
    business?.city,
    business?.district,
    business?.state,
    business?.country,
    business?.pincode,
  ]
    .filter(Boolean)
    .join(", ");

  return (
    <div className="min-h-screen bg-gray-950 px-4 py-8 text-white sm:px-6 lg:px-8">
      <div className="mx-auto max-w-2xl">
        <button
          type="button"
          onClick={onClose}
          className="mb-8 inline-flex items-center gap-2 text-sm font-semibold text-gray-400 transition hover:text-white"
        >
          <ArrowLeft size={16} />
          {t.backWorkspace}
        </button>

        <div className="rounded-3xl border border-gray-800 bg-gray-900/60 p-6 shadow-2xl backdrop-blur-xl sm:p-8">
          <div className="mb-6 flex items-start gap-4">
            <div className="flex h-14 w-14 shrink-0 items-center justify-center rounded-2xl border border-blue-500/20 bg-blue-500/10">
              <Sparkles className="text-blue-400" size={26} />
            </div>
            <div>
              <p className="text-sm font-semibold text-blue-400">
                {t.aiBusinessIntelligence}
              </p>
              <h1 className="mt-1 text-2xl font-extrabold sm:text-3xl">
                {t.generateBusinessAnalysis}
              </h1>
              <p className="mt-2 text-sm leading-6 text-gray-500">
                {t.generationDescription}
              </p>
            </div>
          </div>

          {/* Active Generation State Notice */}
          {loading && (
            <div className="mb-6 rounded-2xl border border-blue-500/30 bg-blue-500/10 p-5">
              <div className="flex items-start gap-3">
                <Clock className="mt-0.5 h-5 w-5 shrink-0 text-blue-400" />
                <div>
                  <h3 className="text-sm font-bold text-blue-300">
                    {t.longRunningNoticeTitle}
                  </h3>
                  <p className="mt-1 text-xs leading-5 text-gray-300">
                    {t.longRunningNoticeText}
                  </p>
                  <button
                    type="button"
                    onClick={() => navigate(`/businesses/${businessId}`)}
                    className="mt-4 inline-flex items-center gap-1.5 rounded-xl bg-blue-600 px-4 py-2 text-xs font-bold text-white transition hover:bg-blue-500"
                  >
                    <ArrowLeft size={14} />
                    {t.continueWorkspace}
                  </button>
                </div>
              </div>
            </div>
          )}

          {error && (
            <div className="mb-6 flex items-start gap-3 rounded-xl border border-red-500/20 bg-red-500/5 p-4">
              <AlertCircle className="mt-0.5 h-5 w-5 shrink-0 text-red-400" />
              <div>
                <p className="font-semibold text-red-300">
                  {t.generationFailed}
                </p>
                <p className="mt-1 text-sm text-gray-500">{error}</p>
              </div>
            </div>
          )}

          {/* Business Details Overview */}
          <div className="mb-6 rounded-2xl border border-gray-800 bg-gray-950/50 p-5">
            <h2 className="mb-4 text-xs font-bold uppercase tracking-wider text-blue-400">
              {t.businessInformation}
            </h2>
            <div className="space-y-3 text-sm">
              <div className="flex justify-between border-b border-gray-800/80 pb-2">
                <span className="text-gray-500">Business Name</span>
                <span className="font-semibold text-gray-200">
                  {business?.business_name || "—"}
                </span>
              </div>
              <div className="flex justify-between border-b border-gray-800/80 pb-2">
                <span className="text-gray-500">Category</span>
                <span className="font-semibold text-gray-200">
                  {business?.category || "—"}
                </span>
              </div>
              <div className="flex justify-between border-b border-gray-800/80 pb-2">
                <span className="text-gray-500">Location</span>
                <span className="max-w-[65%] text-right font-semibold text-gray-200">
                  {locationText || "—"}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-500">Available Capital</span>
                <span className="font-semibold text-gray-200">
                  ₹
                  {Number(business?.margin_capital || 0).toLocaleString(
                    "en-IN",
                  )}
                </span>
              </div>
            </div>
          </div>

          {/* Parameter Configuration */}
          <form onSubmit={onSubmit}>
            <div className="mb-6 rounded-2xl border border-gray-800 bg-gray-950/40 p-5">
              <label className="mb-2 block text-sm font-semibold text-gray-300">
                {t.analysisRadius}
              </label>
              <div className="relative">
                <LocateFixed
                  size={16}
                  className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-600"
                />
                <input
                  type="number"
                  name="radius_km"
                  value={radiusKm}
                  onChange={onRadiusChange}
                  min="0.5"
                  step="0.5"
                  disabled={loading}
                  required
                  className="w-full rounded-xl border border-gray-800 bg-gray-950 py-3 pl-10 pr-12 text-sm text-white outline-none transition focus:border-blue-500/50 focus:ring-1 focus:ring-blue-500/20 disabled:opacity-50"
                />
                <span className="absolute right-4 top-1/2 -translate-y-1/2 text-xs font-semibold text-gray-600">
                  km
                </span>
              </div>
              <p className="mt-2 text-xs text-gray-500">
                {t.radiusDescription}
              </p>
            </div>

            <div className="flex flex-col-reverse gap-3 sm:flex-row sm:justify-end">
              <button
                type="button"
                onClick={onClose}
                disabled={loading}
                className="rounded-xl border border-gray-800 bg-gray-950 px-5 py-3 text-sm font-bold text-gray-400 transition hover:border-gray-700 hover:bg-gray-900 hover:text-white disabled:opacity-50"
              >
                {t.cancel}
              </button>

              <button
                type="submit"
                disabled={loading}
                className="inline-flex items-center justify-center gap-2 rounded-xl bg-blue-600 px-6 py-3 text-sm font-bold text-white shadow-lg shadow-blue-900/20 transition hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-50"
              >
                {loading ? (
                  <>
                    <Loader2 size={17} className="animate-spin" />
                    {t.generating}
                  </>
                ) : (
                  <>
                    <Play size={17} />
                    {t.generate}
                  </>
                )}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

const StatCard = ({ label, value }) => (
  <div className="rounded-xl border border-gray-800 bg-gray-900/50 p-4">
    <p className="text-xs font-semibold uppercase tracking-wider text-gray-600">
      {label}
    </p>
    <p className="mt-2 text-xl font-extrabold text-gray-200">{value}</p>
  </div>
);

const MarkdownReport = ({ markdown, noReport }) => {
  if (!markdown) return <p className="text-sm text-gray-500">{noReport}</p>;

  const lines = markdown.split("\n");
  return (
    <div className="space-y-2 text-sm leading-7 text-gray-400">
      {lines.map((line, index) => {
        const trimmed = line.trim();
        if (!trimmed) return <div key={index} className="h-2" />;
        if (trimmed === "---")
          return <hr key={index} className="my-5 border-gray-800" />;
        if (trimmed.startsWith("### ")) {
          return (
            <h4 key={index} className="mt-5 text-base font-bold text-gray-200">
              {formatInlineMarkdown(trimmed.slice(4))}
            </h4>
          );
        }
        if (trimmed.startsWith("## ")) {
          return (
            <h3 key={index} className="mt-7 text-xl font-extrabold text-white">
              {formatInlineMarkdown(trimmed.slice(3))}
            </h3>
          );
        }
        if (trimmed.startsWith("# ")) {
          return (
            <h2 key={index} className="mb-5 text-2xl font-extrabold text-white">
              {formatInlineMarkdown(trimmed.slice(2))}
            </h2>
          );
        }
        if (trimmed.startsWith("- ")) {
          return (
            <div key={index} className="flex gap-3 pl-2">
              <span className="mt-3 h-1.5 w-1.5 shrink-0 rounded-full bg-blue-400" />
              <p>{formatInlineMarkdown(trimmed.slice(2))}</p>
            </div>
          );
        }
        return <p key={index}>{formatInlineMarkdown(trimmed)}</p>;
      })}
    </div>
  );
};

const formatInlineMarkdown = (text) => {
  const parts = text.split(/(\*\*.*?\*\*)/g);
  return parts.map((part, index) => {
    if (part.startsWith("**") && part.endsWith("**")) {
      return (
        <strong key={index} className="font-bold text-gray-200">
          {part.slice(2, -2)}
        </strong>
      );
    }
    return <span key={index}>{part}</span>;
  });
};

export default BusinessAnalysis;
