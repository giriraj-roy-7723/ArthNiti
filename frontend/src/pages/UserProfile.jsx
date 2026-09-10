import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import {
  User,
  Mail,
  Phone,
  MapPin,
  Building2,
  BriefcaseBusiness,
  ShieldCheck,
  ShoppingBag,
  Loader2,
  AlertCircle,
  RefreshCw,
  Landmark,
  Globe2,
  Hash,
  Sparkles,
  ArrowLeft,
} from "lucide-react";
import { api } from "../utils/api";
import { useLanguage } from "../context/LanguageContext";

const translations = {
  english: {
    back: "Back",
    profile: "User Profile",
    subtitle: "Public details and official information.",
    loading: "Loading profile...",
    unableToLoad: "Unable to load profile",
    tryAgain: "Try Again",
    personalInformation: "Personal Information",
    contactInformation: "Contact Information",
    addressInformation: "Address Information",
    roleInformation: "Role Information",
    firstName: "First Name",
    lastName: "Last Name",
    email: "Email",
    phone: "Phone",
    address: "Address",
    village: "Village",
    district: "District",
    city: "City",
    state: "State",
    country: "Country",
    pincode: "Pincode",
    entrepreneur: "Entrepreneur",
    buyer: "Buyer",
    government: "Government Official",
    unknownRole: "Profile",
    entrepreneurDescription: "Registered entrepreneur on the platform.",
    buyerDescription: "Verified buyer exploring local opportunities.",
    governmentDescription: "Verified government official.",
    designation: "Designation",
    agencyName: "Agency Name",
    agencyAddress: "Agency Address",
    agencyCity: "Agency City",
    agencyState: "Agency State",
    agencyCountry: "Agency Country",
    agencyType: "Agency Type",
    agencyPincode: "Agency Pincode",
    notAvailable: "Not available",
    poweredBy: "AI-powered business platform",
  },
  hindi: {
    back: "पीछे जाएं",
    profile: "उपयोगकर्ता प्रोफ़ाइल",
    subtitle: "सार्वजनिक विवरण और आधिकारिक जानकारी।",
    loading: "प्रोफ़ाइल लोड हो रही है...",
    unableToLoad: "प्रोफ़ाइल लोड नहीं हो सकी",
    tryAgain: "पुनः प्रयास करें",
    personalInformation: "व्यक्तिगत जानकारी",
    contactInformation: "संपर्क जानकारी",
    addressInformation: "पते की जानकारी",
    roleInformation: "भूमिका की जानकारी",
    firstName: "पहला नाम",
    lastName: "अंतिम नाम",
    email: "ईमेल",
    phone: "फ़ोन",
    address: "पता",
    village: "गाँव",
    district: "जिला",
    city: "शहर",
    state: "राज्य",
    country: "देश",
    pincode: "पिनकोड",
    entrepreneur: "उद्यमी",
    buyer: "खरीदार",
    government: "सरकारी अधिकारी",
    unknownRole: "प्रोफ़ाइल",
    entrepreneurDescription: "प्लेटफ़ॉर्म पर पंजीकृत उद्यमी।",
    buyerDescription: "स्थानीय अवसरों की तलाश करने वाला सत्यापित खरीदार।",
    governmentDescription: "सत्यापित सरकारी अधिकारी।",
    designation: "पद",
    agencyName: "एजेंसी का नाम",
    agencyAddress: "एजेंसी का पता",
    agencyCity: "एजेंसी का शहर",
    agencyState: "एजेंसी का राज्य",
    agencyCountry: "एजेंसी का देश",
    agencyType: "एजेंसी का प्रकार",
    agencyPincode: "एजेंसी पिनकोड",
    notAvailable: "उपलब्ध नहीं",
    poweredBy: "AI-संचालित बिज़नेस प्लेटफ़ॉर्म",
  },
  bengali: {
    back: "ফিরে যান",
    profile: "ব্যবহারকারীর প্রোফাইল",
    subtitle: "পাবলিক বিবরণ এবং অফিসিয়াল তথ্য।",
    loading: "প্রোফাইল লোড হচ্ছে...",
    unableToLoad: "প্রোফাইল লোড করা যায়নি",
    tryAgain: "আবার চেষ্টা করুন",
    personalInformation: "ব্যক্তিগত তথ্য",
    contactInformation: "যোগাযোগের তথ্য",
    addressInformation: "ঠিকানার তথ্য",
    roleInformation: "ভূমিকার তথ্য",
    firstName: "নাম",
    lastName: "পদবি",
    email: "ইমেল",
    phone: "ফোন",
    address: "ঠিকানা",
    village: "গ্রাম",
    district: "জেলা",
    city: "শহর",
    state: "রাজ্য",
    country: "দেশ",
    pincode: "পিনকোড",
    entrepreneur: "উদ্যোক্তা",
    buyer: "ক্রেতা",
    government: "সরকারি কর্মকর্তা",
    unknownRole: "প্রোফাইল",
    entrepreneurDescription: "প্ল্যাটফর্মে নিবন্ধিত উদ্যোক্তা।",
    buyerDescription: "যাচাইকৃত ক্রেতা।",
    governmentDescription: "যাচাইকৃত সরকারি কর্মকর্তা।",
    designation: "পদবি",
    agencyName: "এজেন্সির নাম",
    agencyAddress: "এজেন্সির ঠিকানা",
    agencyCity: "এজেন্সির শহর",
    agencyState: "এজেন্সির রাজ্য",
    agencyCountry: "এজেন্সির দেশ",
    agencyType: "এজেন্সির ধরন",
    agencyPincode: "এজেন্সির পিনকোড",
    notAvailable: "উপলব্ধ নয়",
    poweredBy: "AI-চালিত বিজনেস প্ল্যাটফর্ম",
  },
};

const resolveLanguageKey = (lang) => {
  const normalized = String(lang || "")
    .toLowerCase()
    .trim();
  if (["hi", "hindi"].includes(normalized)) return "hindi";
  if (["bn", "bengali", "bangla"].includes(normalized)) return "bengali";
  return "english";
};

const UserProfile = () => {
  const { userId } = useParams();
  const navigate = useNavigate();
  const { language } = useLanguage();

  const langKey = resolveLanguageKey(language);
  const t = translations[langKey] || translations.english;

  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const getLocalizedValue = (value) => {
    if (value === null || value === undefined || value === "") return "";
    if (typeof value === "string" || typeof value === "number")
      return String(value);

    if (Array.isArray(value)) {
      return value
        .map((item) => getLocalizedValue(item))
        .filter(Boolean)
        .join(", ");
    }

    if (typeof value === "object") {
      const languageKeys = {
        english: ["english", "en"],
        hindi: ["hindi", "hi"],
        bengali: ["bengali", "bn"],
      };

      const keys = languageKeys[langKey] || languageKeys.english;

      for (const key of keys) {
        if (
          value[key] !== undefined &&
          value[key] !== null &&
          value[key] !== ""
        ) {
          return getLocalizedValue(value[key]);
        }
      }

      for (const key of ["en", "english", "hi", "hindi", "bn", "bengali"]) {
        if (
          value[key] !== undefined &&
          value[key] !== null &&
          value[key] !== ""
        ) {
          return getLocalizedValue(value[key]);
        }
      }
      return "";
    }

    return String(value);
  };

  const fetchUserProfile = async () => {
    if (!userId) {
      setError(t.unableToLoad);
      setLoading(false);
      return;
    }

    try {
      setLoading(true);
      setError("");

      const response = await api.get("/auth/profile", {
        params: {
          user_id: userId,
          language: langKey,
        },
      });

      setProfile(response.data || null);
    } catch (err) {
      console.error("Failed to fetch user profile:", err);
      setError(getLocalizedValue(err.response?.data?.detail) || t.unableToLoad);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUserProfile();
  }, [userId, langKey]);

  const getRoleKey = () => {
    if (!profile?.role) return "unknown";
    return getLocalizedValue(profile.role).toLowerCase().replace(/[\s-]/g, "_");
  };

  const getRoleLabel = () => {
    const role = getRoleKey();
    if (role === "entrepreneur" || role === "enterpreneur")
      return t.entrepreneur;
    if (role === "buyer") return t.buyer;
    if (role === "government" || role === "government_official")
      return t.government;
    return getLocalizedValue(profile?.role) || t.unknownRole;
  };

  const getRoleIcon = () => {
    const role = getRoleKey();
    if (role === "entrepreneur" || role === "enterpreneur")
      return BriefcaseBusiness;
    if (role === "buyer") return ShoppingBag;
    if (role === "government" || role === "government_official")
      return Landmark;
    return User;
  };

  const getInitials = () => {
    const first = getLocalizedValue(profile?.first_name);
    const last = getLocalizedValue(profile?.last_name);
    const initials = `${first.charAt(0)}${last.charAt(0)}`;
    return initials.toUpperCase() || "U";
  };

  const displayValue = (value) => {
    const resolvedValue = getLocalizedValue(value);
    return resolvedValue || t.notAvailable;
  };

  const InfoItem = ({ icon: Icon, label, value, fullWidth = false }) => (
    <div
      className={`rounded-xl border border-gray-800 bg-gray-950/40 p-4 ${
        fullWidth ? "sm:col-span-2" : ""
      }`}
    >
      <div className="flex items-start gap-3">
        <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-gray-800/70">
          <Icon size={16} className="text-blue-400" />
        </div>
        <div className="min-w-0 flex-1">
          <p className="text-xs font-medium uppercase tracking-wide text-gray-500">
            {label}
          </p>
          <p className="mt-1 break-words text-sm font-semibold text-gray-200">
            {displayValue(value)}
          </p>
        </div>
      </div>
    </div>
  );

  const ProfileSection = ({ icon: Icon, title, children }) => (
    <section className="overflow-hidden rounded-2xl border border-gray-800 bg-gray-900/60 shadow-[0_15px_40px_rgba(0,0,0,0.18)] backdrop-blur-xl">
      <div className="flex items-center gap-3 border-b border-gray-800 px-6 py-5">
        <div className="flex h-10 w-10 items-center justify-center rounded-xl border border-blue-500/20 bg-blue-500/10">
          <Icon size={19} className="text-blue-400" />
        </div>
        <h2 className="text-base font-bold text-white">{title}</h2>
      </div>
      <div className="p-6">{children}</div>
    </section>
  );

  if (loading) {
    return (
      <div className="relative min-h-screen overflow-hidden bg-gray-950 text-white">
        <div className="pointer-events-none absolute inset-0">
          <div className="absolute -right-40 -top-40 h-96 w-96 rounded-full bg-blue-600/10 blur-3xl" />
          <div className="absolute -left-40 top-1/3 h-96 w-96 rounded-full bg-indigo-600/10 blur-3xl" />
        </div>
        <div className="relative z-10 flex min-h-screen items-center justify-center p-6">
          <div className="flex flex-col items-center gap-4">
            <div className="flex h-16 w-16 items-center justify-center rounded-2xl border border-blue-500/20 bg-blue-500/10">
              <Loader2 size={30} className="animate-spin text-blue-400" />
            </div>
            <p className="text-sm font-medium text-gray-400">{t.loading}</p>
          </div>
        </div>
      </div>
    );
  }

  if (error || !profile) {
    return (
      <div className="relative min-h-screen overflow-hidden bg-gray-950 text-white">
        <div className="pointer-events-none absolute inset-0">
          <div className="absolute -right-40 -top-40 h-96 w-96 rounded-full bg-blue-600/10 blur-3xl" />
          <div className="absolute -left-40 top-1/3 h-96 w-96 rounded-full bg-indigo-600/10 blur-3xl" />
        </div>
        <div className="relative z-10 mx-auto flex min-h-screen max-w-xl items-center justify-center p-6">
          <div className="w-full rounded-3xl border border-red-500/20 bg-red-500/5 p-8 backdrop-blur-xl">
            <div className="flex flex-col items-center text-center">
              <div className="flex h-14 w-14 items-center justify-center rounded-xl bg-red-500/10">
                <AlertCircle size={26} className="text-red-400" />
              </div>
              <h2 className="mt-5 text-xl font-bold text-white">
                {t.unableToLoad}
              </h2>
              <p className="mt-2 text-sm leading-6 text-gray-400">
                {error || t.unableToLoad}
              </p>
              <div className="mt-6 flex gap-3">
                <button
                  type="button"
                  onClick={() => navigate(-1)}
                  className="inline-flex items-center gap-2 rounded-xl border border-gray-700 bg-gray-900/80 px-4 py-2.5 text-sm font-bold text-gray-300 transition hover:bg-gray-800"
                >
                  <ArrowLeft size={16} />
                  {t.back}
                </button>
                <button
                  type="button"
                  onClick={fetchUserProfile}
                  className="inline-flex items-center gap-2 rounded-xl border border-blue-500/30 bg-blue-600 px-5 py-2.5 text-sm font-bold text-white transition hover:bg-blue-500"
                >
                  <RefreshCw size={16} />
                  {t.tryAgain}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  const RoleIcon = getRoleIcon();
  const role = getRoleKey();
  const firstName = getLocalizedValue(profile.first_name);
  const lastName = getLocalizedValue(profile.last_name);
  const email = getLocalizedValue(profile.email);
  const phone = getLocalizedValue(profile.phone || profile.phone_number);
  const profileImage =
    getLocalizedValue(profile.profile_pic) ||
    getLocalizedValue(profile.profile_image);
  const roleInfo = profile.role_info || {};

  return (
    <div className="relative min-h-screen overflow-hidden bg-gray-950 text-white">
      <div className="pointer-events-none absolute inset-0">
        <div className="absolute -right-40 -top-40 h-96 w-96 rounded-full bg-blue-600/10 blur-3xl" />
        <div className="absolute -left-40 top-1/3 h-96 w-96 rounded-full bg-indigo-600/10 blur-3xl" />
        <div className="absolute -bottom-40 right-1/3 h-96 w-96 rounded-full bg-blue-500/5 blur-3xl" />
      </div>

      <div className="relative z-10 mx-auto max-w-6xl px-4 py-8 sm:px-6 lg:px-8">
        <div className="mb-6 flex items-center justify-between">
          <button
            type="button"
            onClick={() => navigate(-1)}
            className="inline-flex items-center gap-2 rounded-xl border border-gray-800 bg-gray-900/60 px-4 py-2 text-sm font-semibold text-gray-300 backdrop-blur-xl transition hover:border-gray-700 hover:bg-gray-800 hover:text-white"
          >
            <ArrowLeft size={16} />
            {t.back}
          </button>
          <div className="flex items-center gap-2 text-xs font-semibold text-blue-400">
            <Sparkles size={14} />
            <span>{t.poweredBy}</span>
          </div>
        </div>

        {/* Profile Card Header */}
        <div className="mb-6 overflow-hidden rounded-3xl border border-gray-800 bg-gray-900/70 shadow-[0_20px_60px_rgba(0,0,0,0.25)] backdrop-blur-xl">
          <div className="relative overflow-hidden p-6 sm:p-8">
            <div className="pointer-events-none absolute -right-20 -top-20 h-60 w-60 rounded-full bg-blue-600/10 blur-3xl" />

            <div className="relative flex flex-col gap-6 sm:flex-row sm:items-center">
              <div className="relative shrink-0">
                {profileImage ? (
                  <img
                    src={profileImage}
                    alt={`${firstName} ${lastName}`}
                    className="h-24 w-24 rounded-2xl border border-gray-700 object-cover shadow-xl sm:h-28 sm:w-28"
                    onError={(e) => {
                      e.currentTarget.style.display = "none";
                    }}
                  />
                ) : (
                  <div className="flex h-24 w-24 items-center justify-center rounded-2xl border border-blue-500/20 bg-gradient-to-br from-blue-500/10 to-indigo-500/10 text-2xl font-extrabold text-blue-400 shadow-xl sm:h-28 sm:w-28 sm:text-3xl">
                    {getInitials()}
                  </div>
                )}
              </div>

              <div className="min-w-0 flex-1">
                <h1 className="break-words text-2xl font-extrabold text-white sm:text-3xl">
                  {[firstName, lastName].filter(Boolean).join(" ") || "User"}
                </h1>
                <div className="mt-2 flex flex-wrap items-center gap-2">
                  <span className="inline-flex items-center gap-1.5 rounded-full border border-blue-500/20 bg-blue-500/10 px-3 py-1.5 text-xs font-bold text-blue-400">
                    <RoleIcon size={13} />
                    {getRoleLabel()}
                  </span>
                </div>

                <div className="mt-5 grid grid-cols-1 gap-3 text-sm sm:grid-cols-2">
                  <div className="flex min-w-0 items-center gap-2 text-gray-400">
                    <Mail size={15} className="shrink-0 text-gray-500" />
                    <span className="truncate">{displayValue(email)}</span>
                  </div>
                  <div className="flex min-w-0 items-center gap-2 text-gray-400">
                    <Phone size={15} className="shrink-0 text-gray-500" />
                    <span className="truncate">{displayValue(phone)}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Info Grid Sections */}
        <div className="space-y-6">
          <ProfileSection icon={User} title={t.personalInformation}>
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
              <InfoItem
                icon={User}
                label={t.firstName}
                value={profile.first_name}
              />
              <InfoItem
                icon={User}
                label={t.lastName}
                value={profile.last_name}
              />
              <InfoItem icon={Mail} label={t.email} value={profile.email} />
              <InfoItem
                icon={Phone}
                label={t.phone}
                value={profile.phone || profile.phone_number}
              />
            </div>
          </ProfileSection>

          <ProfileSection icon={MapPin} title={t.addressInformation}>
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
              <InfoItem
                icon={MapPin}
                label={t.address}
                value={profile.address}
                fullWidth
              />
              <InfoItem
                icon={MapPin}
                label={t.village}
                value={profile.village}
              />
              <InfoItem
                icon={MapPin}
                label={t.district}
                value={profile.district}
              />
              <InfoItem icon={MapPin} label={t.city} value={profile.city} />
              <InfoItem icon={MapPin} label={t.state} value={profile.state} />
              <InfoItem
                icon={Globe2}
                label={t.country}
                value={profile.country}
              />
              <InfoItem icon={Hash} label={t.pincode} value={profile.pincode} />
            </div>
          </ProfileSection>

          {/* Role-Specific Sections */}
          {(role === "government" || role === "government_official") && (
            <ProfileSection icon={Landmark} title={t.roleInformation}>
              <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
                <InfoItem
                  icon={BriefcaseBusiness}
                  label={t.designation}
                  value={roleInfo.designation}
                />
                <InfoItem
                  icon={Building2}
                  label={t.agencyName}
                  value={roleInfo.agency_name}
                />
                <InfoItem
                  icon={MapPin}
                  label={t.agencyAddress}
                  value={roleInfo.agency_address}
                  fullWidth
                />
                <InfoItem
                  icon={MapPin}
                  label={t.agencyCity}
                  value={roleInfo.agency_city}
                />
                <InfoItem
                  icon={MapPin}
                  label={t.agencyState}
                  value={roleInfo.agency_state}
                />
                <InfoItem
                  icon={Globe2}
                  label={t.agencyCountry}
                  value={roleInfo.agency_country}
                />
                <InfoItem
                  icon={Building2}
                  label={t.agencyType}
                  value={roleInfo.agency_type}
                />
                <InfoItem
                  icon={Hash}
                  label={t.agencyPincode}
                  value={roleInfo.agency_pincode}
                />
              </div>
            </ProfileSection>
          )}

          {(role === "entrepreneur" || role === "enterpreneur") && (
            <ProfileSection icon={BriefcaseBusiness} title={t.roleInformation}>
              <div className="rounded-2xl border border-blue-500/10 bg-blue-500/5 p-6">
                <div className="flex items-start gap-4">
                  <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-blue-500/10">
                    <BriefcaseBusiness size={22} className="text-blue-400" />
                  </div>
                  <div>
                    <h3 className="font-bold text-white">{t.entrepreneur}</h3>
                    <p className="mt-2 text-sm leading-6 text-gray-400">
                      {t.entrepreneurDescription}
                    </p>
                  </div>
                </div>
              </div>
            </ProfileSection>
          )}

          {role === "buyer" && (
            <ProfileSection icon={ShoppingBag} title={t.roleInformation}>
              <div className="rounded-2xl border border-blue-500/10 bg-blue-500/5 p-6">
                <div className="flex items-start gap-4">
                  <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-blue-500/10">
                    <ShoppingBag size={22} className="text-blue-400" />
                  </div>
                  <div>
                    <h3 className="font-bold text-white">{t.buyer}</h3>
                    <p className="mt-2 text-sm leading-6 text-gray-400">
                      {t.buyerDescription}
                    </p>
                  </div>
                </div>
              </div>
            </ProfileSection>
          )}

          {role !== "government" &&
            role !== "government_official" &&
            role !== "entrepreneur" &&
            role !== "enterpreneur" &&
            role !== "buyer" && (
              <ProfileSection icon={ShieldCheck} title={t.roleInformation}>
                <div className="rounded-xl border border-gray-800 bg-gray-950/40 p-5">
                  <div className="flex items-center gap-3">
                    <RoleIcon size={20} className="text-blue-400" />
                    <div>
                      <p className="text-sm font-bold text-white">
                        {getRoleLabel()}
                      </p>
                      <p className="mt-1 text-xs text-gray-500">{t.subtitle}</p>
                    </div>
                  </div>
                </div>
              </ProfileSection>
            )}
        </div>
      </div>
    </div>
  );
};

export default UserProfile;
