import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  Building2,
  Plus,
  Loader2,
  AlertCircle,
  Sparkles,
  RefreshCw,
} from "lucide-react";

import { api } from "../../utils/api";
import { useLanguage } from "../../context/LanguageContext";
import BusinessCard from "./BusinessCard";
import CreateBusinessModal from "./CreateBusinessModal";

const translations = {
  english: {
    title: "My Businesses",
    subtitle: "Manage your businesses and access their AI-powered insights.",
    addBusiness: "Add Business",
    loading: "Loading your businesses...",
    unableToLoad: "Unable to load businesses",
    tryAgain: "Try Again",
    noBusinesses: "No businesses yet",
    emptyDescription:
      "Create your first business to start exploring business analysis, financial insights, government schemes, and your AI business assistant.",
    createFirst: "Create Your First Business",
    openWorkspace: "Open Workspace",
    unnamedBusiness: "Unnamed Business",
    approved: "Approved",
    rejected: "Rejected",
    pending: "Pending",
    underReview: "Under Review",
    businessCount: "business",
    businessesCount: "businesses",
    locationUnavailable: "Location unavailable",
    errorDefault: "Unable to load your businesses. Please try again.",
    poweredBy: "AI-powered business workspace",

    // Modal translations
    createBusiness: "Create Business",
    createBusinessDescription:
      "Tell us about your business and where it is located.",
    businessLocationQuestion:
      "Is your business location the same as your profile address?",
    yesUseProfile: "Yes, use my profile address",
    noDifferentLocation: "No, use a different location",
    profileLocationLoading: "Fetching your profile address...",
    profileLocationLoaded: "Profile address loaded",
    profileLocationFailed:
      "Unable to fetch your profile address. Please enter the location manually.",
    businessInformation: "Business Information",
    locationInformation: "Business Location",
    businessName: "Business Name",
    businessNamePlaceholder: "Enter your business name",
    category: "Category",
    categoryPlaceholder: "e.g. Grocery, Restaurant, Manufacturing",
    description: "Description",
    descriptionPlaceholder: "Briefly describe your business",
    marginCapital: "Capital / Investment",
    marginCapitalPlaceholder: "Enter amount",
    village: "Village",
    villagePlaceholder: "Enter village",
    district: "District",
    districtPlaceholder: "Enter district",
    city: "City",
    cityPlaceholder: "Enter city",
    state: "State",
    statePlaceholder: "Enter state",
    country: "Country",
    countryPlaceholder: "Enter country",
    pincode: "Pincode",
    pincodePlaceholder: "Enter pincode",
    latitude: "Latitude",
    latitudePlaceholder: "Optional",
    longitude: "Longitude",
    longitudePlaceholder: "Optional",
    cancel: "Cancel",
    create: "Create Business",
    creating: "Creating Business...",
    requiredBusinessName: "Business name is required.",
    requiredCategory: "Business category is required.",
    createFailed: "Unable to create business. Please try again.",
  },
  hindi: {
    title: "मेरे व्यवसाय",
    subtitle:
      "अपने व्यवसायों को प्रबंधित करें और AI द्वारा संचालित जानकारी प्राप्त करें।",
    addBusiness: "व्यवसाय जोड़ें",
    loading: "आपके व्यवसाय लोड हो रहे हैं...",
    unableToLoad: "व्यवसाय लोड नहीं हो सके",
    tryAgain: "पुनः प्रयास करें",
    noBusinesses: "अभी कोई व्यवसाय नहीं है",
    emptyDescription:
      "अपना पहला व्यवसाय बनाएं और व्यवसाय विश्लेषण, वित्तीय जानकारी, सरकारी योजनाओं और अपने AI बिज़नेस असिस्टेंट का उपयोग शुरू करें।",
    createFirst: "अपना पहला व्यवसाय बनाएं",
    openWorkspace: "वर्कस्पेस खोलें",
    unnamedBusiness: "बिना नाम का व्यवसाय",
    approved: "स्वीकृत",
    rejected: "अस्वीकृत",
    pending: "लंबित",
    underReview: "समीक्षा में",
    businessCount: "व्यवसाय",
    businessesCount: "व्यवसाय",
    locationUnavailable: "स्थान उपलब्ध नहीं है",
    errorDefault: "आपके व्यवसाय लोड नहीं हो सके। कृपया फिर से प्रयास करें।",
    poweredBy: "AI-संचालित बिज़नेस वर्कस्पेस",

    createBusiness: "व्यवसाय बनाएं",
    createBusinessDescription:
      "अपने व्यवसाय और उसके स्थान के बारे में जानकारी दें।",
    businessLocationQuestion:
      "क्या आपके व्यवसाय का स्थान आपके प्रोफ़ाइल पते के समान है?",
    yesUseProfile: "हाँ, मेरा प्रोफ़ाइल पता उपयोग करें",
    noDifferentLocation: "नहीं, अलग स्थान उपयोग करें",
    profileLocationLoading: "आपका प्रोफ़ाइल पता प्राप्त किया जा रहा है...",
    profileLocationLoaded: "प्रोफ़ाइल पता लोड हो गया",
    profileLocationFailed:
      "प्रोफ़ाइल पता प्राप्त नहीं हो सका। कृपया स्थान मैन्युअली भरें।",
    businessInformation: "व्यवसाय की जानकारी",
    locationInformation: "व्यवसाय का स्थान",
    businessName: "व्यवसाय का नाम",
    businessNamePlaceholder: "व्यवसाय का नाम दर्ज करें",
    category: "श्रेणी",
    categoryPlaceholder: "जैसे किराना, रेस्तरां, निर्माण",
    description: "विवरण",
    descriptionPlaceholder: "अपने व्यवसाय का संक्षिप्त विवरण दें",
    marginCapital: "पूंजी / निवेश",
    marginCapitalPlaceholder: "राशि दर्ज करें",
    village: "गाँव",
    villagePlaceholder: "गाँव दर्ज करें",
    district: "जिला",
    districtPlaceholder: "जिला दर्ज करें",
    city: "शहर",
    cityPlaceholder: "शहर दर्ज करें",
    state: "राज्य",
    statePlaceholder: "राज्य दर्ज करें",
    country: "देश",
    countryPlaceholder: "देश दर्ज करें",
    pincode: "पिनकोड",
    pincodePlaceholder: "पिनकोड दर्ज करें",
    latitude: "अक्षांश",
    latitudePlaceholder: "वैकल्पिक",
    longitude: "देशांतर",
    longitudePlaceholder: "वैकल्पिक",
    cancel: "रद्द करें",
    create: "व्यवसाय बनाएं",
    creating: "व्यवसाय बनाया जा रहा है...",
    requiredBusinessName: "व्यवसाय का नाम आवश्यक है।",
    requiredCategory: "व्यवसाय की श्रेणी आवश्यक है।",
    createFailed: "व्यवसाय बनाने में असमर्थ। कृपया फिर से प्रयास करें।",
  },
  bengali: {
    title: "আমার ব্যবসা",
    subtitle:
      "আপনার ব্যবসাগুলি পরিচালনা করুন এবং AI-চালিত তথ্য ও বিশ্লেষণ পান।",
    addBusiness: "ব্যবসা যোগ করুন",
    loading: "আপনার ব্যবসাগুলি লোড হচ্ছে...",
    unableToLoad: "ব্যবসাগুলি লোড করা যায়নি",
    tryAgain: "আবার চেষ্টা করুন",
    noBusinesses: "এখনও কোনো ব্যবসা নেই",
    emptyDescription:
      "আপনার প্রথম ব্যবসা তৈরি করুন এবং ব্যবসায়িক বিশ্লেষণ, আর্থিক তথ্য, সরকারি প্রকল্প এবং AI বিজনেস অ্যাসিস্ট্যান্ট ব্যবহার শুরু করুন।",
    createFirst: "প্রথম ব্যবসা তৈরি করুন",
    openWorkspace: "ওয়ার্কস্পেস খুলুন",
    unnamedBusiness: "নামহীন ব্যবসা",
    approved: "অনুমোদিত",
    rejected: "প্রত্যাখ্যাত",
    pending: "অপেক্ষমাণ",
    underReview: "পর্যালোচনাধীন",
    businessCount: "ব্যবসা",
    businessesCount: "ব্যবসা",
    locationUnavailable: "অবস্থান উপলব্ধ নয়",
    errorDefault:
      "আপনার ব্যবসাগুলি লোড করা যায়নি। অনুগ্রহ করে আবার চেষ্টা করুন।",
    poweredBy: "AI-চালিত বিজনেস ওয়ার্কস্পেস",

    createBusiness: "ব্যবসা তৈরি করুন",
    createBusinessDescription:
      "আপনার ব্যবসা এবং তার অবস্থান সম্পর্কে তথ্য দিন।",
    businessLocationQuestion:
      "আপনার ব্যবসার অবস্থান কি আপনার প্রোফাইলের ঠিকানার মতো?",
    yesUseProfile: "হ্যাঁ, আমার প্রোফাইলের ঠিকানা ব্যবহার করুন",
    noDifferentLocation: "না, অন্য অবস্থান ব্যবহার করুন",
    profileLocationLoading: "আপনার প্রোফাইলের ঠিকানা আনা হচ্ছে...",
    profileLocationLoaded: "প্রোফাইলের ঠিকানা লোড হয়েছে",
    profileLocationFailed:
      "প্রোফাইলের ঠিকানা আনা যায়নি। অনুগ্রহ করে অবস্থান ম্যানুয়ালি পূরণ করুন।",
    businessInformation: "ব্যবসার তথ্য",
    locationInformation: "ব্যবসার অবস্থান",
    businessName: "ব্যবসার নাম",
    businessNamePlaceholder: "ব্যবসার নাম লিখুন",
    category: "ক্যাটাগরি",
    categoryPlaceholder: "যেমন: মুদি দোকান, রেস্তোরাঁ, উৎপাদন",
    description: "বিবরণ",
    descriptionPlaceholder: "আপনার ব্যবসার সংক্ষিপ্ত বিবরণ দিন",
    marginCapital: "মূলধন / বিনিয়োগ",
    marginCapitalPlaceholder: "পরিমাণ লিখুন",
    village: "গ্রাম",
    villagePlaceholder: "গ্রাম লিখুন",
    district: "জেলা",
    districtPlaceholder: "জেলা লিখুন",
    city: "শহর",
    cityPlaceholder: "শহর লিখুন",
    state: "রাজ্য",
    statePlaceholder: "রাজ্য লিখুন",
    country: "দেশ",
    countryPlaceholder: "দেশ লিখুন",
    pincode: "পিনকোড",
    pincodePlaceholder: "পিনকোড লিখুন",
    latitude: "অক্ষাংশ",
    latitudePlaceholder: "ঐচ্ছিক",
    longitude: "দ্রাঘিমাংশ",
    longitudePlaceholder: "ঐচ্ছিক",
    cancel: "বাতিল",
    create: "ব্যবসা তৈরি করুন",
    creating: "ব্যবসা তৈরি হচ্ছে...",
    requiredBusinessName: "ব্যবসার নাম আবশ্যক।",
    requiredCategory: "ব্যবসার ক্যাটাগরি আবশ্যক।",
    createFailed: "ব্যবসা তৈরি করা যায়নি। অনুগ্রহ করে আবার চেষ্টা করুন।",
  },
};

const MyBusinesses = () => {
  const navigate = useNavigate();
  const { language } = useLanguage();

  const [businesses, setBusinesses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [showCreateModal, setShowCreateModal] = useState(false);

  const t = translations[language] || translations.english;

  const fetchBusinesses = async () => {
    try {
      setLoading(true);
      setError("");

      const idsResponse = await api.get("/businesses/my");
      const businessIds = idsResponse.data || [];

      if (businessIds.length === 0) {
        setBusinesses([]);
        return;
      }

      const businessResponses = await Promise.all(
        businessIds.map((businessId) =>
          api.get(`/businesses/${businessId}`, {
            params: { language: language || "english" },
          }),
        ),
      );

      setBusinesses(businessResponses.map((response) => response.data));
    } catch (err) {
      console.error("Failed to fetch businesses:", err);
      setError(err.response?.data?.detail || t.errorDefault);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchBusinesses();
  }, [language]);

  const handleOpenBusiness = (businessId) => {
    navigate(`/businesses/${businessId}`);
  };

  return (
    <div className="relative min-h-screen overflow-hidden bg-gray-950 text-white">
      {/* Background effects */}
      <div className="pointer-events-none absolute inset-0">
        <div className="absolute -right-40 -top-40 h-96 w-96 rounded-full bg-blue-600/10 blur-3xl" />
        <div className="absolute -left-40 top-1/3 h-96 w-96 rounded-full bg-indigo-600/10 blur-3xl" />
        <div className="absolute -bottom-40 right-1/3 h-96 w-96 rounded-full bg-purple-600/5 blur-3xl" />
      </div>

      <div className="relative z-10 mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-10 flex flex-col gap-6 lg:flex-row lg:items-end lg:justify-between">
          <div>
            <div className="mb-3 flex items-center gap-2 text-sm font-semibold text-blue-400">
              <Sparkles size={16} />
              <span>{t.poweredBy}</span>
            </div>

            <h1 className="text-3xl font-extrabold tracking-tight text-white sm:text-4xl">
              {t.title}
            </h1>

            <p className="mt-3 max-w-2xl text-sm leading-6 text-gray-400 sm:text-base">
              {t.subtitle}
            </p>
          </div>

          <button
            type="button"
            onClick={() => setShowCreateModal(true)}
            className="group inline-flex items-center justify-center gap-2 rounded-xl border border-blue-400/20 bg-gradient-to-r from-blue-600 to-indigo-600 px-5 py-3 text-sm font-bold text-white shadow-[0_10px_30px_rgba(37,99,235,0.25)] transition-all duration-300 hover:-translate-y-1 hover:from-blue-500 hover:to-indigo-500 hover:shadow-[0_15px_35px_rgba(37,99,235,0.35)]"
          >
            <Plus
              size={18}
              className="transition-transform duration-300 group-hover:rotate-90"
            />
            {t.addBusiness}
          </button>
        </div>

        {/* Loading State */}
        {loading && (
          <div className="flex min-h-[420px] items-center justify-center rounded-3xl border border-gray-800 bg-gray-900/50 backdrop-blur-xl">
            <div className="flex flex-col items-center gap-4">
              <div className="flex h-16 w-16 items-center justify-center rounded-2xl border border-blue-500/20 bg-blue-500/10">
                <Loader2 size={30} className="animate-spin text-blue-400" />
              </div>
              <p className="text-sm font-medium text-gray-400">{t.loading}</p>
            </div>
          </div>
        )}

        {/* Error State */}
        {!loading && error && (
          <div className="rounded-3xl border border-red-500/20 bg-red-500/5 p-8 backdrop-blur-xl">
            <div className="flex flex-col items-start gap-5 sm:flex-row">
              <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-red-500/10">
                <AlertCircle size={24} className="text-red-400" />
              </div>

              <div className="flex-1">
                <h2 className="text-lg font-bold text-white">
                  {t.unableToLoad}
                </h2>
                <p className="mt-2 text-sm leading-6 text-gray-400">{error}</p>
                <button
                  type="button"
                  onClick={fetchBusinesses}
                  className="mt-5 inline-flex items-center gap-2 rounded-xl border border-gray-700 bg-gray-800/80 px-4 py-2.5 text-sm font-semibold text-white transition hover:border-gray-600 hover:bg-gray-700"
                >
                  <RefreshCw size={16} />
                  {t.tryAgain}
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Empty State */}
        {!loading && !error && businesses.length === 0 && (
          <div className="relative flex min-h-[460px] items-center justify-center overflow-hidden rounded-3xl border border-gray-800 bg-gray-900/50 p-8 backdrop-blur-xl">
            <div className="pointer-events-none absolute left-1/2 top-1/2 h-72 w-72 -translate-x-1/2 -translate-y-1/2 rounded-full bg-blue-600/10 blur-3xl" />

            <div className="relative z-10 max-w-lg text-center">
              <div className="mx-auto flex h-20 w-20 items-center justify-center rounded-2xl border border-blue-500/20 bg-gradient-to-br from-blue-500/10 to-indigo-500/10 shadow-[0_10px_40px_rgba(37,99,235,0.1)]">
                <Building2 size={34} className="text-blue-400" />
              </div>

              <h2 className="mt-6 text-2xl font-bold text-white">
                {t.noBusinesses}
              </h2>

              <p className="mt-3 text-sm leading-7 text-gray-400">
                {t.emptyDescription}
              </p>

              <button
                type="button"
                onClick={() => setShowCreateModal(true)}
                className="mt-7 inline-flex items-center gap-2 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 px-6 py-3 text-sm font-bold text-white shadow-[0_10px_25px_rgba(37,99,235,0.25)] transition-all duration-300 hover:-translate-y-1 hover:from-blue-500 hover:to-indigo-500"
              >
                <Plus size={18} />
                {t.createFirst}
              </button>
            </div>
          </div>
        )}

        {/* Business Cards Grid */}
        {!loading && !error && businesses.length > 0 && (
          <>
            <div className="mb-5 flex items-center gap-2 text-sm text-gray-500">
              <Building2 size={16} />
              <span>
                {businesses.length}{" "}
                {businesses.length === 1 ? t.businessCount : t.businessesCount}
              </span>
            </div>

            <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 xl:grid-cols-3">
              {businesses.map((business) => (
                <BusinessCard
                  key={business.id}
                  business={business}
                  t={t}
                  onOpen={handleOpenBusiness}
                />
              ))}
            </div>
          </>
        )}
      </div>

      {/* Create Business Modal */}
      <CreateBusinessModal
        isOpen={showCreateModal}
        onClose={() => setShowCreateModal(false)}
        onSuccess={fetchBusinesses}
        language={language}
        t={t}
      />
    </div>
  );
};

export default MyBusinesses;
