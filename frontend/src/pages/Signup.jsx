import { useEffect, useMemo, useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useLanguage } from "../context/LanguageContext";
import { useAuth } from "../context/AuthContext";
import { api } from "../utils/api";

import {
  Mail,
  Lock,
  User,
  ArrowRight,
  Loader2,
  Phone,
  MapPin,
  Building2,
  Globe2,
  Map,
  Home,
  BriefcaseBusiness,
  ChevronDown,
} from "lucide-react";

import { Country, State, City } from "country-state-city";

// ============================================================
// REUSABLE INPUT FIELD
// ============================================================

const InputField = ({
  name,
  label,
  placeholder,
  type = "text",
  icon: Icon,
  required = true,
  value,
  onChange,
}) => {
  return (
    <div>
      <label
        htmlFor={name}
        className="block text-sm font-medium text-gray-300 mb-2"
      >
        {label}

        {required && <span className="text-red-400 ml-1">*</span>}
      </label>

      <div className="relative">
        {Icon && (
          <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
            <Icon className="h-5 w-5 text-gray-500" />
          </div>
        )}

        <input
          id={name}
          type={type}
          name={name}
          required={required}
          value={value}
          onChange={onChange}
          placeholder={placeholder}
          className={`
            w-full
            ${Icon ? "pl-12" : "pl-4"}
            pr-4
            py-3
            bg-gray-950/70
            border
            border-gray-700
            rounded-xl
            text-white
            placeholder-gray-500
            outline-none
            transition-all
            duration-200
            hover:border-gray-600
            focus:border-blue-500
            focus:ring-2
            focus:ring-blue-500/20
          `}
        />
      </div>
    </div>
  );
};

// ============================================================
// REUSABLE SELECT FIELD
// ============================================================

const SelectField = ({
  name,
  label,
  options,
  value,
  onChange,
  icon: Icon,
  required = true,
  disabled = false,
}) => {
  return (
    <div>
      <label
        htmlFor={name}
        className="block text-sm font-medium text-gray-300 mb-2"
      >
        {label}

        {required && <span className="text-red-400 ml-1">*</span>}
      </label>

      <div className="relative">
        {Icon && (
          <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none z-10">
            <Icon className="h-5 w-5 text-gray-500" />
          </div>
        )}

        <select
          id={name}
          name={name}
          required={required}
          value={value}
          onChange={onChange}
          disabled={disabled}
          className={`
            appearance-none
            w-full
            ${Icon ? "pl-12" : "pl-4"}
            pr-10
            py-3
            bg-gray-950/70
            border
            border-gray-700
            rounded-xl
            text-white
            outline-none
            transition-all
            duration-200
            hover:border-gray-600
            focus:border-blue-500
            focus:ring-2
            focus:ring-blue-500/20
            disabled:opacity-50
            disabled:cursor-not-allowed
          `}
        >
          {options.map((option) => (
            <option
              key={option.value}
              value={option.value}
              className="bg-gray-900 text-white"
            >
              {option.label}
            </option>
          ))}
        </select>

        <ChevronDown className="absolute right-4 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-500 pointer-events-none" />
      </div>
    </div>
  );
};

// ============================================================
// SECTION HEADER
// ============================================================

const SectionHeader = ({ icon: Icon, title, description }) => {
  return (
    <div className="flex items-start gap-3 mb-6">
      <div className="flex-shrink-0 w-10 h-10 rounded-xl bg-blue-500/10 border border-blue-500/20 flex items-center justify-center">
        <Icon className="w-5 h-5 text-blue-400" />
      </div>

      <div>
        <h3 className="text-lg font-semibold text-white">{title}</h3>

        {description && (
          <p className="text-sm text-gray-500 mt-1">{description}</p>
        )}
      </div>
    </div>
  );
};

// ============================================================
// SIGNUP
// ============================================================

const Signup = () => {
  const [formData, setFormData] = useState({
    first_name: "",
    last_name: "",
    email: "",
    password: "",
    role: "enterpreneur",

    phone_number: "",
    country_code: "+91",

    address: "",
    village: "",
    district: "",
    city: "",
    state: "",
    country: "India",
    pincode: "",

    designation: "",
    agency_type: "sca",
    agency_name: "",
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const { language } = useLanguage();
  const { login } = useAuth();
  const navigate = useNavigate();

  const countries = useMemo(() => {
    return Country.getAllCountries();
  }, []);

  const selectedCountry = useMemo(() => {
    return countries.find((country) => country.name === formData.country);
  }, [countries, formData.country]);

  const states = useMemo(() => {
    if (!selectedCountry?.isoCode) {
      return [];
    }

    return State.getStatesOfCountry(selectedCountry.isoCode);
  }, [selectedCountry]);

  const selectedState = useMemo(() => {
    return states.find((state) => state.name === formData.state);
  }, [states, formData.state]);

  const cities = useMemo(() => {
    if (!selectedCountry?.isoCode || !selectedState?.isoCode) {
      return [];
    }

    return City.getCitiesOfState(
      selectedCountry.isoCode,
      selectedState.isoCode,
    );
  }, [selectedCountry, selectedState]);

  // ============================================================
  // CHANGE HANDLER
  // ============================================================

  const handleChange = (e) => {
    const { name, value } = e.target;

    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  // ============================================================
  // COUNTRY CHANGE
  // ============================================================

  const handleCountryChange = (e) => {
    const countryName = e.target.value;

    const country = countries.find((item) => item.name === countryName);

    setFormData((prev) => ({
      ...prev,
      country: countryName,
      state: "",
      city: "",
      country_code: country ? `+${country.phonecode}` : prev.country_code,
    }));
  };

  // ============================================================
  // STATE CHANGE
  // ============================================================

  const handleStateChange = (e) => {
    setFormData((prev) => ({
      ...prev,
      state: e.target.value,
      city: "",
    }));
  };

  // ============================================================
  // SUBMIT
  // ============================================================

  const handleSubmit = async (e) => {
    e.preventDefault();

    setLoading(true);
    setError("");

    try {
      const payload = {
        ...formData,
        phone_number: `${formData.country_code}${formData.phone_number}`,
      };

      delete payload.country_code;

      const res = await api.post(
        `/auth/signup?language=${encodeURIComponent(language)}`,
        payload,
      );

      if (res.data.access_token) {
        login(res.data.access_token, res.data.user);
        navigate(res.data.user?.role === 'enterpreneur' ? '/dashboard/business-analysis' : '/');
      }
    } catch (err) {
      if (!err.response) {
        setError(
          "Unable to reach the backend. Start the API on port 8000 and try again.",
        );
      } else if (Array.isArray(err.response.data?.detail)) {
        setError(err.response.data.detail.map((item) => item.msg).join(", "));
      } else {
        setError(
          err.response.data?.detail || "Something went wrong during signup",
        );
      }
    } finally {
      setLoading(false);
    }
  };

  // ============================================================
  // RENDER
  // ============================================================

  return (
    <div className="min-h-screen bg-gray-950 py-10 px-4 sm:px-6">
      <div className="max-w-5xl mx-auto">
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-gradient-to-br from-blue-600 to-indigo-600 shadow-lg shadow-blue-500/20 mb-4">
            <User className="w-7 h-7 text-white" />
          </div>

          <h1 className="text-3xl sm:text-4xl font-bold text-white">
            Create Account
          </h1>

          <p className="text-gray-400 mt-2">Join us and start your journey</p>
        </div>

        <div className="relative">
          <div className="absolute -inset-1 bg-gradient-to-r from-blue-600/20 via-indigo-600/10 to-purple-600/20 rounded-3xl blur-xl" />

          <div className="relative bg-gray-900/95 border border-gray-800 rounded-3xl shadow-2xl overflow-hidden">
            <div className="h-1 bg-gradient-to-r from-blue-600 via-indigo-500 to-purple-600" />

            <div className="p-6 sm:p-8 lg:p-10">
              {error && (
                <div className="mb-8 p-4 rounded-xl bg-red-500/10 border border-red-500/20 text-red-400 text-sm">
                  {error}
                </div>
              )}

              <form onSubmit={handleSubmit}>
                {/* ====================================================== */}
                {/* PERSONAL INFORMATION                                    */}
                {/* ====================================================== */}

                <section className="pb-8 border-b border-gray-800">
                  <SectionHeader
                    icon={User}
                    title="Personal Information"
                    description="Enter your basic account details"
                  />

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
                    <InputField
                      name="first_name"
                      label="First Name"
                      placeholder="Enter your first name"
                      icon={User}
                      value={formData.first_name}
                      onChange={handleChange}
                    />

                    <InputField
                      name="last_name"
                      label="Last Name"
                      placeholder="Enter your last name"
                      icon={User}
                      value={formData.last_name}
                      onChange={handleChange}
                    />

                    <InputField
                      name="email"
                      label="Email Address"
                      placeholder="you@example.com"
                      type="email"
                      icon={Mail}
                      value={formData.email}
                      onChange={handleChange}
                    />

                    <InputField
                      name="password"
                      label="Password"
                      placeholder="Create a strong password"
                      type="password"
                      icon={Lock}
                      value={formData.password}
                      onChange={handleChange}
                    />
                  </div>
                </section>

                {/* ====================================================== */}
                {/* ACCOUNT TYPE                                            */}
                {/* ====================================================== */}

                <section className="py-8 border-b border-gray-800">
                  <SectionHeader
                    icon={BriefcaseBusiness}
                    title="Account Type"
                    description="Select how you will use the platform"
                  />

                  <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                    {[
                      {
                        value: "enterpreneur",
                        title: "Entrepreneur",
                        description: "Start and manage businesses",
                      },
                      {
                        value: "buyer",
                        title: "Buyer",
                        description: "Explore and purchase opportunities",
                      },
                      {
                        value: "government",
                        title: "Government",
                        description: "Manage government activities",
                      },
                    ].map((role) => (
                      <label
                        key={role.value}
                        className={`
                          relative
                          cursor-pointer
                          rounded-2xl
                          border
                          p-5
                          transition-all
                          duration-200
                          ${
                            formData.role === role.value
                              ? "border-blue-500 bg-blue-500/10 ring-2 ring-blue-500/20"
                              : "border-gray-700 bg-gray-950/50 hover:border-gray-600"
                          }
                        `}
                      >
                        <input
                          type="radio"
                          name="role"
                          value={role.value}
                          checked={formData.role === role.value}
                          onChange={handleChange}
                          className="sr-only"
                        />

                        <div className="flex items-start justify-between gap-3">
                          <div>
                            <p className="font-semibold text-white">
                              {role.title}
                            </p>

                            <p className="text-xs text-gray-500 mt-1 leading-relaxed">
                              {role.description}
                            </p>
                          </div>

                          <div
                            className={`
                              w-5 h-5 rounded-full border flex items-center justify-center
                              ${
                                formData.role === role.value
                                  ? "border-blue-500"
                                  : "border-gray-600"
                              }
                            `}
                          >
                            {formData.role === role.value && (
                              <div className="w-2.5 h-2.5 rounded-full bg-blue-500" />
                            )}
                          </div>
                        </div>
                      </label>
                    ))}
                  </div>
                </section>

                {/* ====================================================== */}
                {/* CONTACT INFORMATION                                     */}
                {/* ====================================================== */}

                <section className="py-8 border-b border-gray-800">
                  <SectionHeader
                    icon={Phone}
                    title="Contact Information"
                    description="Provide a phone number where you can be reached"
                  />

                  <div className="grid grid-cols-1 md:grid-cols-4 gap-5">
                    <div className="md:col-span-1">
                      <label
                        htmlFor="country_code"
                        className="block text-sm font-medium text-gray-300 mb-2"
                      >
                        Country Code
                        <span className="text-red-400 ml-1">*</span>
                      </label>

                      <div className="relative">
                        <select
                          id="country_code"
                          name="country_code"
                          value={formData.country_code}
                          onChange={handleChange}
                          className="
                            appearance-none
                            w-full
                            px-4
                            pr-9
                            py-3
                            bg-gray-950/70
                            border
                            border-gray-700
                            rounded-xl
                            text-white
                            outline-none
                            focus:border-blue-500
                            focus:ring-2
                            focus:ring-blue-500/20
                          "
                        >
                          {countries.map((country) => (
                            <option
                              key={`${country.isoCode}-${country.phonecode}`}
                              value={`+${country.phonecode}`}
                              className="bg-gray-900"
                            >
                              {country.flag} +{country.phonecode}
                            </option>
                          ))}
                        </select>

                        <ChevronDown className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-500 pointer-events-none" />
                      </div>
                    </div>

                    <div className="md:col-span-3">
                      <InputField
                        name="phone_number"
                        label="Phone Number"
                        placeholder="Enter your phone number"
                        type="tel"
                        icon={Phone}
                        value={formData.phone_number}
                        onChange={handleChange}
                      />
                    </div>
                  </div>
                </section>

                {/* ====================================================== */}
                {/* GOVERNMENT INFORMATION                                  */}
                {/* ====================================================== */}

                {formData.role === "government" && (
                  <section className="py-8 border-b border-gray-800">
                    <SectionHeader
                      icon={Building2}
                      title="Government Information"
                      description="Provide your official organization details"
                    />

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
                      <InputField
                        name="designation"
                        label="Designation"
                        placeholder="e.g. District Officer"
                        icon={BriefcaseBusiness}
                        value={formData.designation}
                        onChange={handleChange}
                      />

                      <InputField
                        name="agency_name"
                        label="Agency Name"
                        placeholder="Enter agency / department name"
                        icon={Building2}
                        value={formData.agency_name}
                        onChange={handleChange}
                      />

                      <SelectField
                        name="agency_type"
                        label="Agency Type"
                        value={formData.agency_type}
                        onChange={handleChange}
                        icon={Building2}
                        options={[
                          {
                            value: "sca",
                            label: "SCA",
                          },
                          {
                            value: "ca",
                            label: "CA",
                          },
                        ]}
                      />
                    </div>
                  </section>
                )}

                {/* ====================================================== */}
                {/* LOCATION                                                */}
                {/* ====================================================== */}

                <section className="py-8">
                  <SectionHeader
                    icon={MapPin}
                    title="Location & Address"
                    description="Tell us where you are located"
                  />

                  <div className="space-y-5">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
                      <SelectField
                        name="country"
                        label="Country"
                        value={formData.country}
                        onChange={handleCountryChange}
                        icon={Globe2}
                        options={[
                          {
                            value: "",
                            label: "Select country",
                          },
                          ...countries.map((country) => ({
                            value: country.name,
                            label: `${country.flag} ${country.name}`,
                          })),
                        ]}
                      />

                      <div>
                        <label
                          htmlFor="state"
                          className="block text-sm font-medium text-gray-300 mb-2"
                        >
                          State / Province
                          <span className="text-red-400 ml-1">*</span>
                        </label>

                        <div className="relative">
                          <Map className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-500 pointer-events-none z-10" />

                          <input
                            id="state"
                            name="state"
                            list="state-options"
                            required
                            value={formData.state}
                            onChange={handleStateChange}
                            placeholder={
                              states.length
                                ? "Select or type state"
                                : "Enter state / province"
                            }
                            className="
                              w-full
                              pl-12
                              pr-4
                              py-3
                              bg-gray-950/70
                              border
                              border-gray-700
                              rounded-xl
                              text-white
                              placeholder-gray-500
                              outline-none
                              focus:border-blue-500
                              focus:ring-2
                              focus:ring-blue-500/20
                            "
                          />

                          <datalist id="state-options">
                            {states.map((state) => (
                              <option
                                key={`${state.isoCode}-${state.name}`}
                                value={state.name}
                              />
                            ))}
                          </datalist>
                        </div>
                      </div>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
                      <InputField
                        name="district"
                        label="District"
                        placeholder="Enter district"
                        icon={MapPin}
                        value={formData.district}
                        onChange={handleChange}
                      />

                      <div>
                        <label
                          htmlFor="city"
                          className="block text-sm font-medium text-gray-300 mb-2"
                        >
                          City
                          <span className="text-red-400 ml-1">*</span>
                        </label>

                        <div className="relative">
                          <Building2 className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-500 pointer-events-none z-10" />

                          <input
                            id="city"
                            name="city"
                            list="city-options"
                            required
                            value={formData.city}
                            onChange={handleChange}
                            placeholder={
                              cities.length
                                ? "Select or type city"
                                : "Enter city"
                            }
                            className="
                              w-full
                              pl-12
                              pr-4
                              py-3
                              bg-gray-950/70
                              border
                              border-gray-700
                              rounded-xl
                              text-white
                              placeholder-gray-500
                              outline-none
                              focus:border-blue-500
                              focus:ring-2
                              focus:ring-blue-500/20
                            "
                          />

                          <datalist id="city-options">
                            {cities.map((city, index) => (
                              <option
                                key={`${city.name}-${index}`}
                                value={city.name}
                              />
                            ))}
                          </datalist>
                        </div>
                      </div>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
                      <InputField
                        name="village"
                        label="Village / Locality"
                        placeholder="Enter village or locality"
                        icon={Home}
                        value={formData.village}
                        onChange={handleChange}
                      />

                      <InputField
                        name="pincode"
                        label="Postal / ZIP Code"
                        placeholder="Enter postal / ZIP code"
                        type="text"
                        icon={MapPin}
                        value={formData.pincode}
                        onChange={handleChange}
                      />
                    </div>

                    <div>
                      <label
                        htmlFor="address"
                        className="block text-sm font-medium text-gray-300 mb-2"
                      >
                        Full Address
                        <span className="text-red-400 ml-1">*</span>
                      </label>

                      <div className="relative">
                        <MapPin className="absolute left-4 top-4 w-5 h-5 text-gray-500 pointer-events-none" />

                        <textarea
                          id="address"
                          name="address"
                          required
                          rows={3}
                          value={formData.address}
                          onChange={handleChange}
                          placeholder="House number, street, area, landmark..."
                          className="
                            w-full
                            pl-12
                            pr-4
                            py-3
                            bg-gray-950/70
                            border
                            border-gray-700
                            rounded-xl
                            text-white
                            placeholder-gray-500
                            outline-none
                            resize-none
                            focus:border-blue-500
                            focus:ring-2
                            focus:ring-blue-500/20
                          "
                        />
                      </div>
                    </div>
                  </div>
                </section>

                {/* ====================================================== */}
                {/* SUBMIT                                                  */}
                {/* ====================================================== */}

                <div className="pt-2">
                  <button
                    type="submit"
                    disabled={loading}
                    className="
                      w-full
                      flex
                      items-center
                      justify-center
                      gap-2
                      bg-gradient-to-r
                      from-blue-600
                      to-indigo-600
                      hover:from-blue-500
                      hover:to-indigo-500
                      disabled:opacity-50
                      disabled:cursor-not-allowed
                      text-white
                      py-3.5
                      rounded-xl
                      font-semibold
                      transition-all
                      duration-300
                      shadow-lg
                      shadow-blue-600/20
                      hover:shadow-blue-600/30
                      hover:-translate-y-0.5
                    "
                  >
                    {loading ? (
                      <>
                        <Loader2 className="h-5 w-5 animate-spin" />
                        <span>Creating Account...</span>
                      </>
                    ) : (
                      <>
                        <span>Create Account</span>
                        <ArrowRight className="h-5 w-5" />
                      </>
                    )}
                  </button>

                  <p className="text-center text-sm text-gray-500 mt-5">
                    By creating an account, you agree to our terms and
                    conditions.
                  </p>

                  <div className="text-center text-sm text-gray-400 mt-4">
                    Already have an account?{" "}
                    <Link
                      to="/login"
                      className="text-blue-400 hover:text-blue-300 font-semibold transition-colors"
                    >
                      Sign In
                    </Link>
                  </div>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Signup;
