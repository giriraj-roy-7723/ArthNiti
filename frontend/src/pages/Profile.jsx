import { useEffect, useState } from "react";
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
  Pencil,
  Sparkles,
} from "lucide-react";

import { api } from "../utils/api";
import { useLanguage } from "../context/LanguageContext";

const PROFILE_ENDPOINT = "/auth/me";

const Profile = () => {
  const { language } = useLanguage();

  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const translations = {
    english: {
      profile: "Profile",
      subtitle: "Manage your personal information and profile details.",
      loading: "Loading your profile...",
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

      entrepreneurDescription:
        "Your entrepreneur-specific information will appear here.",
      buyerDescription: "Your buyer-specific information will appear here.",
      governmentDescription: "Your government official information.",

      designation: "Designation",
      agencyName: "Agency Name",
      agencyAddress: "Agency Address",
      agencyCity: "Agency City",
      agencyState: "Agency State",
      agencyCountry: "Agency Country",
      agencyType: "Agency Type",
      agencyPincode: "Agency Pincode",

      notAvailable: "Not available",
      profileUpdated: "Profile information",
      poweredBy: "AI-powered business platform",
    },

    hindi: {
      profile: "प्रोफ़ाइल",
      subtitle: "अपनी व्यक्तिगत जानकारी और प्रोफ़ाइल विवरण प्रबंधित करें।",
      loading: "आपकी प्रोफ़ाइल लोड हो रही है...",
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

      entrepreneurDescription: "आपकी उद्यमी संबंधी जानकारी यहाँ दिखाई देगी।",
      buyerDescription: "आपकी खरीदार संबंधी जानकारी यहाँ दिखाई देगी।",
      governmentDescription: "आपकी सरकारी अधिकारी संबंधी जानकारी।",

      designation: "पद",
      agencyName: "एजेंसी का नाम",
      agencyAddress: "एजेंसी का पता",
      agencyCity: "एजेंसी का शहर",
      agencyState: "एजेंसी का राज्य",
      agencyCountry: "एजेंसी का देश",
      agencyType: "एजेंसी का प्रकार",
      agencyPincode: "एजेंसी पिनकोड",

      notAvailable: "उपलब्ध नहीं",
      profileUpdated: "प्रोफ़ाइल जानकारी",
      poweredBy: "AI-संचालित बिज़नेस प्लेटफ़ॉर्म",
    },

    bengali: {
      profile: "প্রোফাইল",
      subtitle: "আপনার ব্যক্তিগত তথ্য এবং প্রোফাইলের বিবরণ পরিচালনা করুন।",
      loading: "আপনার প্রোফাইল লোড হচ্ছে...",
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

      entrepreneurDescription:
        "আপনার উদ্যোক্তা সম্পর্কিত তথ্য এখানে প্রদর্শিত হবে।",
      buyerDescription: "আপনার ক্রেতা সম্পর্কিত তথ্য এখানে প্রদর্শিত হবে।",
      governmentDescription: "আপনার সরকারি কর্মকর্তা সম্পর্কিত তথ্য।",

      designation: "পদবি",
      agencyName: "এজেন্সির নাম",
      agencyAddress: "এজেন্সির ঠিকানা",
      agencyCity: "এজেন্সির শহর",
      agencyState: "এজেন্সির রাজ্য",
      agencyCountry: "এজেন্সির দেশ",
      agencyType: "এজেন্সির ধরন",
      agencyPincode: "এজেন্সির পিনকোড",

      notAvailable: "উপলব্ধ নয়",
      profileUpdated: "প্রোফাইলের তথ্য",
      poweredBy: "AI-চালিত বিজনেস প্ল্যাটফর্ম",
    },
  };

  const t = translations[language] || translations.english;

  // =========================================================
  // Dummy role-specific functions
  // =========================================================

  /**
   * Entrepreneur-specific data.
   *
   * Later you can replace this with something like:
   *
   * const response = await api.get("/entrepreneurs/me");
   * return response.data;
   */
  const fetchEntrepreneurDetails = async () => {
    return {
      available: false,
      data: null,
    };
  };

  /**
   * Buyer-specific data.
   *
   * Later you can replace this with something like:
   *
   * const response = await api.get("/buyers/me");
   * return response.data;
   */
  const fetchBuyerDetails = async () => {
    return {
      available: false,
      data: null,
    };
  };

  // =========================================================
  // Fetch profile
  // =========================================================

  const fetchProfile = async () => {
    try {
      setLoading(true);
      setError("");

      const response = await api.get(PROFILE_ENDPOINT, {
        params: {
          language: language || "english",
        },
      });

      const profileData = response.data;

      // -------------------------------------------------------
      // Fetch additional role-specific data
      // -------------------------------------------------------

      const role = String(profileData.role || "")
        .toLowerCase()
        .replace(/[\s-]/g, "_");

      if (role === "entrepreneur" || role === "enterpreneur") {
        const entrepreneurDetails = await fetchEntrepreneurDetails();

        profileData.role_specific = entrepreneurDetails.data;
      }

      if (role === "buyer") {
        const buyerDetails = await fetchBuyerDetails();

        profileData.role_specific = buyerDetails.data;
      }

      setProfile(profileData);
    } catch (err) {
      console.error("Failed to fetch profile:", err);

      setError(err.response?.data?.detail || "Unable to load your profile.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProfile();
  }, [language]);

  // =========================================================
  // Helpers
  // =========================================================

  const getRoleKey = () => {
    if (!profile?.role) {
      return "unknown";
    }

    return String(profile.role).toLowerCase().replace(/[\s-]/g, "_");
  };

  const getRoleLabel = () => {
    const role = getRoleKey();

    if (role === "entrepreneur" || role === "enterpreneur") {
      return t.entrepreneur;
    }

    if (role === "buyer") {
      return t.buyer;
    }

    if (role === "government" || role === "government_official") {
      return t.government;
    }

    return profile?.role || t.unknownRole;
  };

  const getRoleIcon = () => {
    const role = getRoleKey();

    if (role === "entrepreneur" || role === "enterpreneur") {
      return BriefcaseBusiness;
    }

    if (role === "buyer") {
      return ShoppingBag;
    }

    if (role === "government" || role === "government_official") {
      return Landmark;
    }

    return User;
  };

  const getInitials = () => {
    const first = profile?.first_name || "";
    const last = profile?.last_name || "";

    const initials = `${first.charAt(0)}${last.charAt(0)}`;

    return initials.toUpperCase() || "U";
  };

  const displayValue = (value) => {
    if (value === null || value === undefined || value === "") {
      return t.notAvailable;
    }

    return value;
  };

  // =========================================================
  // Reusable information item
  // =========================================================

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
          <p className="text-xs font-medium uppercase tracking-wide text-gray-600">
            {label}
          </p>

          <p className="mt-1 break-words text-sm font-semibold text-gray-200">
            {displayValue(value)}
          </p>
        </div>
      </div>
    </div>
  );

  // =========================================================
  // Section wrapper
  // =========================================================

  const ProfileSection = ({ icon: Icon, title, children }) => (
    <section className="overflow-hidden rounded-2xl border border-gray-800 bg-gray-900/60 shadow-[0_15px_40px_rgba(0,0,0,0.18)] backdrop-blur-xl">
      <div className="flex items-center gap-3 border-b border-gray-800 px-6 py-5">
        <div className="flex h-10 w-10 items-center justify-center rounded-xl border border-blue-500/20 bg-blue-500/10">
          <Icon size={19} className="text-blue-400" />
        </div>

        <div>
          <h2 className="text-base font-bold text-white">{title}</h2>
        </div>
      </div>

      <div className="p-6">{children}</div>
    </section>
  );

  // =========================================================
  // Government official section
  // =========================================================

  const GovernmentOfficialSection = () => {
    const info = profile?.role_info || {};

    return (
      <ProfileSection icon={Landmark} title={t.roleInformation}>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
          <InfoItem
            icon={BriefcaseBusiness}
            label={t.designation}
            value={info.designation}
          />

          <InfoItem
            icon={Building2}
            label={t.agencyName}
            value={info.agency_name}
          />

          <InfoItem
            icon={MapPin}
            label={t.agencyAddress}
            value={info.agency_address}
            fullWidth
          />

          <InfoItem
            icon={MapPin}
            label={t.agencyCity}
            value={info.agency_city}
          />

          <InfoItem
            icon={MapPin}
            label={t.agencyState}
            value={info.agency_state}
          />

          <InfoItem
            icon={Globe2}
            label={t.agencyCountry}
            value={info.agency_country}
          />

          <InfoItem
            icon={Building2}
            label={t.agencyType}
            value={info.agency_type}
          />

          <InfoItem
            icon={Hash}
            label={t.agencyPincode}
            value={info.agency_pincode}
          />
        </div>
      </ProfileSection>
    );
  };

  // =========================================================
  // Entrepreneur section
  // =========================================================

  const EntrepreneurSection = () => (
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
  );

  // =========================================================
  // Buyer section
  // =========================================================

  const BuyerSection = () => (
    <ProfileSection icon={ShoppingBag} title={t.roleInformation}>
      <div className="rounded-2xl border border-purple-500/10 bg-purple-500/5 p-6">
        <div className="flex items-start gap-4">
          <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-purple-500/10">
            <ShoppingBag size={22} className="text-purple-400" />
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
  );

  // =========================================================
  // Loading
  // =========================================================

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

  // =========================================================
  // Error
  // =========================================================

  if (error) {
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

              <p className="mt-2 text-sm leading-6 text-gray-400">{error}</p>

              <button
                type="button"
                onClick={fetchProfile}
                className="mt-6 inline-flex items-center gap-2 rounded-xl border border-gray-700 bg-gray-800/80 px-5 py-3 text-sm font-bold text-white transition hover:border-gray-600 hover:bg-gray-700"
              >
                <RefreshCw size={16} />
                {t.tryAgain}
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (!profile) {
    return null;
  }

  const RoleIcon = getRoleIcon();
  const role = getRoleKey();

  return (
    <div className="relative min-h-screen overflow-hidden bg-gray-950 text-white">
      {/* =====================================================
          Background
          ===================================================== */}

      <div className="pointer-events-none absolute inset-0">
        <div className="absolute -right-40 -top-40 h-96 w-96 rounded-full bg-blue-600/10 blur-3xl" />

        <div className="absolute -left-40 top-1/3 h-96 w-96 rounded-full bg-indigo-600/10 blur-3xl" />

        <div className="absolute -bottom-40 right-1/3 h-96 w-96 rounded-full bg-purple-600/5 blur-3xl" />
      </div>

      <div className="relative z-10 mx-auto max-w-6xl px-4 py-8 sm:px-6 lg:px-8">
        {/* =================================================
            Header
            ================================================= */}

        <div className="mb-8">
          <div className="mb-3 flex items-center gap-2 text-sm font-semibold text-blue-400">
            <Sparkles size={16} />
            <span>{t.poweredBy}</span>
          </div>

          <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
            <div>
              <h1 className="text-3xl font-extrabold tracking-tight text-white sm:text-4xl">
                {t.profile}
              </h1>

              <p className="mt-3 max-w-2xl text-sm leading-6 text-gray-400 sm:text-base">
                {t.subtitle}
              </p>
            </div>

            {/* Future edit button */}
            <button
              type="button"
              disabled
              className="inline-flex cursor-not-allowed items-center justify-center gap-2 rounded-xl border border-gray-800 bg-gray-900/70 px-5 py-3 text-sm font-bold text-gray-600"
            >
              <Pencil size={16} />
              Edit Profile
            </button>
          </div>
        </div>

        {/* =================================================
            Profile Hero
            ================================================= */}

        <div className="mb-6 overflow-hidden rounded-3xl border border-gray-800 bg-gray-900/70 shadow-[0_20px_60px_rgba(0,0,0,0.25)] backdrop-blur-xl">
          <div className="relative overflow-hidden p-6 sm:p-8">
            {/* Glow */}
            <div className="pointer-events-none absolute -right-20 -top-20 h-60 w-60 rounded-full bg-blue-600/10 blur-3xl" />

            <div className="relative flex flex-col gap-6 sm:flex-row sm:items-center">
              {/* Profile image */}
              <div className="relative shrink-0">
                {profile.profile_image ? (
                  <img
                    src={profile.profile_image}
                    alt={`${profile.first_name || ""} ${
                      profile.last_name || ""
                    }`}
                    className="h-24 w-24 rounded-2xl border border-gray-700 object-cover shadow-xl sm:h-28 sm:w-28"
                  />
                ) : (
                  <div className="flex h-24 w-24 items-center justify-center rounded-2xl border border-blue-500/20 bg-gradient-to-br from-blue-500/10 to-indigo-500/10 text-2xl font-extrabold text-blue-400 shadow-xl sm:h-28 sm:w-28 sm:text-3xl">
                    {getInitials()}
                  </div>
                )}
              </div>

              {/* Main identity */}
              <div className="min-w-0 flex-1">
                <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
                  <div>
                    <h2 className="break-words text-2xl font-extrabold text-white sm:text-3xl">
                      {[profile.first_name, profile.last_name]
                        .filter(Boolean)
                        .join(" ") || "User"}
                    </h2>

                    <div className="mt-2 flex flex-wrap items-center gap-2">
                      <span className="inline-flex items-center gap-1.5 rounded-full border border-blue-500/20 bg-blue-500/10 px-3 py-1.5 text-xs font-bold text-blue-400">
                        <RoleIcon size={13} />
                        {getRoleLabel()}
                      </span>
                    </div>
                  </div>
                </div>

                <div className="mt-5 grid grid-cols-1 gap-3 text-sm sm:grid-cols-2">
                  <div className="flex min-w-0 items-center gap-2 text-gray-400">
                    <Mail size={15} className="shrink-0 text-gray-600" />

                    <span className="truncate">
                      {displayValue(profile.email)}
                    </span>
                  </div>

                  <div className="flex min-w-0 items-center gap-2 text-gray-400">
                    <Phone size={15} className="shrink-0 text-gray-600" />

                    <span className="truncate">
                      {displayValue(profile.phone)}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* =================================================
            Personal Information
            ================================================= */}

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

              <InfoItem icon={Phone} label={t.phone} value={profile.phone} />
            </div>
          </ProfileSection>

          {/* =================================================
              Address
              ================================================= */}

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

          {/* =================================================
              Role specific
              ================================================= */}

          {(role === "government" || role === "government_official") && (
            <GovernmentOfficialSection />
          )}

          {(role === "entrepreneur" || role === "enterpreneur") && (
            <EntrepreneurSection />
          )}

          {role === "buyer" && <BuyerSection />}

          {/* Future roles */}
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

                      <p className="mt-1 text-xs text-gray-500">
                        {t.profileUpdated}
                      </p>
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

export default Profile;
