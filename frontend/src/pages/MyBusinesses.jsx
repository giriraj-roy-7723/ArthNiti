import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  ArrowRight,
  Building2,
  MapPin,
  Plus,
  Loader2,
  AlertCircle,
  Sparkles,
  RefreshCw,
} from "lucide-react";

import { api } from "../utils/api";
import { useLanguage } from "../context/LanguageContext";

const MyBusinesses = () => {
  const navigate = useNavigate();
  const { language } = useLanguage();

  const [businesses, setBusinesses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

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
      errorDefault: "आपके व्यवसाय लोड नहीं हो सके। कृपया पुनः प्रयास करें।",
      poweredBy: "AI-संचालित बिज़नेस वर्कस्पेस",
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
    },
  };

  const t = translations[language] || translations.english;

  useEffect(() => {
    const fetchBusinesses = async () => {
      try {
        setLoading(true);
        setError("");

        // Get business IDs belonging to the authenticated user
        const idsResponse = await api.get("/businesses/my");

        const businessIds = idsResponse.data || [];

        if (businessIds.length === 0) {
          setBusinesses([]);
          return;
        }

        /*
         * Fetch every business using the currently selected language.
         *
         * Example:
         * language = "english" -> backend receives english
         * language = "hindi"   -> backend receives hindi
         * language = "bengali" -> backend receives bengali
         */
        const businessResponses = await Promise.all(
          businessIds.map((businessId) =>
            api.get(`/businesses/${businessId}`, {
              params: {
                language: language || "english",
              },
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

    fetchBusinesses();
  }, [language]);

  const handleOpenBusiness = (businessId) => {
    navigate(`/businesses/${businessId}`);
  };

  const handleCreateBusiness = () => {
    navigate("/businesses/create");
  };

  const getStatusLabel = (status) => {
    if (!status) return "";

    const normalizedStatus = status.toLowerCase();

    if (normalizedStatus === "approved") {
      return t.approved;
    }

    if (normalizedStatus === "rejected") {
      return t.rejected;
    }

    if (normalizedStatus === "pending") {
      return t.pending;
    }

    if (
      normalizedStatus === "under_review" ||
      normalizedStatus === "under-review"
    ) {
      return t.underReview;
    }

    return status
      .replace(/_/g, " ")
      .replace(/\b\w/g, (char) => char.toUpperCase());
  };

  const getStatusClasses = (status) => {
    switch (status?.toLowerCase()) {
      case "approved":
        return "bg-emerald-500/10 text-emerald-400 border-emerald-500/20";

      case "rejected":
        return "bg-red-500/10 text-red-400 border-red-500/20";

      case "pending":
      case "under_review":
      case "under-review":
      default:
        return "bg-amber-500/10 text-amber-400 border-amber-500/20";
    }
  };

  return (
    <div className="min-h-screen bg-gray-950 text-white relative overflow-hidden">
      {/* Background effects */}
      <div className="pointer-events-none absolute inset-0">
        <div className="absolute -top-40 -right-40 h-96 w-96 rounded-full bg-blue-600/10 blur-3xl" />
        <div className="absolute top-1/3 -left-40 h-96 w-96 rounded-full bg-indigo-600/10 blur-3xl" />
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
            onClick={handleCreateBusiness}
            className="group inline-flex items-center justify-center gap-2 rounded-xl border border-blue-400/20 bg-gradient-to-r from-blue-600 to-indigo-600 px-5 py-3 text-sm font-bold text-white shadow-[0_10px_30px_rgba(37,99,235,0.25)] transition-all duration-300 hover:-translate-y-1 hover:from-blue-500 hover:to-indigo-500 hover:shadow-[0_15px_35px_rgba(37,99,235,0.35)]"
          >
            <Plus
              size={18}
              className="transition-transform duration-300 group-hover:rotate-90"
            />
            {t.addBusiness}
          </button>
        </div>

        {/* Loading */}
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

        {/* Error */}
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
                  onClick={() => window.location.reload()}
                  className="mt-5 inline-flex items-center gap-2 rounded-xl border border-gray-700 bg-gray-800/80 px-4 py-2.5 text-sm font-semibold text-white transition hover:border-gray-600 hover:bg-gray-700"
                >
                  <RefreshCw size={16} />
                  {t.tryAgain}
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Empty state */}
        {!loading && !error && businesses.length === 0 && (
          <div className="relative flex min-h-[460px] items-center justify-center overflow-hidden rounded-3xl border border-gray-800 bg-gray-900/50 p-8 backdrop-blur-xl">
            {/* Decorative glow */}
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
                onClick={handleCreateBusiness}
                className="mt-7 inline-flex items-center gap-2 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 px-6 py-3 text-sm font-bold text-white shadow-[0_10px_25px_rgba(37,99,235,0.25)] transition-all duration-300 hover:-translate-y-1 hover:from-blue-500 hover:to-indigo-500"
              >
                <Plus size={18} />
                {t.createFirst}
              </button>
            </div>
          </div>
        )}

        {/* Business cards */}
        {!loading && !error && businesses.length > 0 && (
          <>
            {/* Count */}
            <div className="mb-5 flex items-center gap-2 text-sm text-gray-500">
              <Building2 size={16} />
              <span>
                {businesses.length}{" "}
                {businesses.length === 1 ? t.businessCount : t.businessesCount}
              </span>
            </div>

            <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 xl:grid-cols-3">
              {businesses.map((business) => (
                <button
                  key={business.id}
                  type="button"
                  onClick={() => handleOpenBusiness(business.id)}
                  className="group text-left"
                >
                  <div className="relative h-full overflow-hidden rounded-2xl border border-gray-800 bg-gray-900/70 p-6 shadow-[0_15px_40px_rgba(0,0,0,0.25)] backdrop-blur-xl transition-all duration-300 hover:-translate-y-2 hover:border-blue-500/30 hover:bg-gray-900 hover:shadow-[0_20px_50px_rgba(37,99,235,0.12)]">
                    {/* Top glow */}
                    <div className="pointer-events-none absolute -right-10 -top-10 h-32 w-32 rounded-full bg-blue-600/10 blur-3xl transition-opacity duration-300 group-hover:opacity-100" />

                    {/* Header */}
                    <div className="relative flex items-start justify-between">
                      <div className="flex h-13 w-13 items-center justify-center rounded-xl border border-blue-500/20 bg-gradient-to-br from-blue-500/10 to-indigo-500/10 transition-all duration-300 group-hover:border-blue-500/40 group-hover:from-blue-500/20 group-hover:to-indigo-500/20">
                        <Building2 size={25} className="text-blue-400" />
                      </div>

                      {business.status && (
                        <span
                          className={`rounded-full border px-3 py-1 text-xs font-semibold ${getStatusClasses(
                            business.status,
                          )}`}
                        >
                          {getStatusLabel(business.status)}
                        </span>
                      )}
                    </div>

                    {/* Business information */}
                    <div className="relative mt-6">
                      <h2 className="line-clamp-1 text-xl font-bold text-white">
                        {business.business_name || t.unnamedBusiness}
                      </h2>

                      {business.category && (
                        <p className="mt-1.5 line-clamp-1 text-sm font-medium text-blue-400">
                          {business.category}
                        </p>
                      )}

                      <div className="mt-5 flex min-h-[24px] items-center gap-2 text-sm text-gray-500">
                        <MapPin size={16} className="shrink-0 text-gray-600" />

                        <span className="line-clamp-1">
                          {business.city || business.state
                            ? [business.city, business.state]
                                .filter(Boolean)
                                .join(", ")
                            : t.locationUnavailable}
                        </span>
                      </div>
                    </div>

                    {/* Footer */}
                    <div className="relative mt-6 flex items-center justify-between border-t border-gray-800 pt-5">
                      <span className="text-sm font-bold text-gray-300 transition-colors group-hover:text-white">
                        {t.openWorkspace}
                      </span>

                      <div className="flex h-8 w-8 items-center justify-center rounded-lg border border-gray-800 bg-gray-800/50 transition-all duration-300 group-hover:border-blue-500/30 group-hover:bg-blue-500/10">
                        <ArrowRight
                          size={17}
                          className="text-gray-500 transition-all duration-300 group-hover:translate-x-0.5 group-hover:text-blue-400"
                        />
                      </div>
                    </div>
                  </div>
                </button>
              ))}
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default MyBusinesses;
