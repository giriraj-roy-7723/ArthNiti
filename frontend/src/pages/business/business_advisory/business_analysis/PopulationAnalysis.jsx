import { useEffect, useState } from "react";
import { Users, MapPin, Home, Gauge } from "lucide-react";

import { aiApi } from "../../../../utils/api";
import { useLanguage } from "../../../../context/LanguageContext";
import BusinessEvidenceLayout, {
  SectionCard,
  Metric,
  InfoRow,
} from "../components/BusinessEvidenceLayout";
import { useParams } from "react-router-dom";

const PopulationAnalysis = () => {
  const { businessId } = useParams();
  const { language } = useLanguage();

  const translations = {
    english: {
      title: "Population Analysis",
      subtitle: "Hyper-local population and market reach intelligence",
      population: "Population",
      density: "Density",
      households: "Households",
      averageHousehold: "Average Household",
      people: "people",
      marketReach: "Market Reach",
      analysisRadius: "Analysis Radius",
      geographicArea: "Geographic Area",
      populationDensity: "Population Density",
      estimatedHouseholds: "Estimated Households",
      location: "Location",
      country: "Country",
      latitude: "Latitude",
      longitude: "Longitude",
      dataSources: "Data Sources",
      populationSource: "Population Source",
      populationYear: "Population Year",
      householdSource: "Household Source",
      estimationMethod: "Estimation Method",
      failedToLoad: "Failed to load population analysis.",
    },
    hindi: {
      title: "जनसंख्या विश्लेषण",
      subtitle: "स्थानीय जनसंख्या और बाज़ार पहुंच संबंधी जानकारी",
      population: "जनसंख्या",
      density: "घनत्व",
      households: "परिवार",
      averageHousehold: "औसत परिवार",
      people: "लोग",
      marketReach: "बाज़ार पहुंच",
      analysisRadius: "विश्लेषण की त्रिज्या",
      geographicArea: "भौगोलिक क्षेत्र",
      populationDensity: "जनसंख्या घनत्व",
      estimatedHouseholds: "अनुमानित परिवार",
      location: "स्थान",
      country: "देश",
      latitude: "अक्षांश",
      longitude: "देशांतर",
      dataSources: "डेटा स्रोत",
      populationSource: "जनसंख्या स्रोत",
      populationYear: "जनसंख्या वर्ष",
      householdSource: "परिवार स्रोत",
      estimationMethod: "अनुमान विधि",
      failedToLoad: "जनसंख्या विश्लेषण लोड करने में विफल।",
    },
    bengali: {
      title: "জনসংখ্যা বিশ্লেষণ",
      subtitle: "স্থানীয় জনসংখ্যা এবং বাজারে পৌঁছানোর তথ্য",
      population: "জনসংখ্যা",
      density: "ঘনত্ব",
      households: "পরিবার",
      averageHousehold: "গড় পরিবার",
      people: "জন",
      marketReach: "বাজারে পৌঁছানো",
      analysisRadius: "বিশ্লেষণের ব্যাসার্ধ",
      geographicArea: "ভৌগোলিক এলাকা",
      populationDensity: "জনসংখ্যার ঘনত্ব",
      estimatedHouseholds: "আনুমানিক পরিবার",
      location: "অবস্থান",
      country: "দেশ",
      latitude: "অক্ষাংশ",
      longitude: "দ্রাঘিমাংশ",
      dataSources: "ডেটার উৎস",
      populationSource: "জনসংখ্যার উৎস",
      populationYear: "জনসংখ্যার বছর",
      householdSource: "পরিবারের উৎস",
      estimationMethod: "অনুমান পদ্ধতি",
      failedToLoad: "জনসংখ্যা বিশ্লেষণ লোড করতে ব্যর্থ হয়েছে।",
    },
  };

  const t =
    translations[
      language === "hi" ? "hindi" : language === "bn" ? "bengali" : language
    ] || translations.english;

  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const load = async () => {
      try {
        setLoading(true);

        const response = await aiApi.get(
          `api/v1/businesses/${businessId}/report/evidence?language=${language}&payload_type=population`,
        );

        setData(response.data || response);
      } catch (err) {
        setError(err?.response?.data?.detail || err?.message || t.failedToLoad);
      } finally {
        setLoading(false);
      }
    };

    load();
  }, [businessId, language]);

  const population = data?.payload?.data;

  return (
    <BusinessEvidenceLayout
      title={t.title}
      subtitle={t.subtitle}
      icon={Users}
      iconClassName="text-blue-400"
      loading={loading}
      error={error}
    >
      {population && (
        <>
          <div className="grid grid-cols-2 gap-4 lg:grid-cols-4">
            <Metric
              label={t.population}
              value={population.population?.toLocaleString("en-IN")}
            />

            <Metric
              label={t.density}
              value={population.population_density?.toLocaleString("en-IN")}
              suffix=" / km²"
            />

            <Metric
              label={t.households}
              value={population.estimated_households?.toLocaleString("en-IN")}
            />

            <Metric
              label={t.averageHousehold}
              value={population.average_household_size}
              suffix={` ${t.people}`}
            />
          </div>

          <div className="mt-5 grid grid-cols-1 gap-5 lg:grid-cols-2">
            <SectionCard title={t.marketReach} icon={Gauge}>
              <InfoRow
                label={t.analysisRadius}
                value={`${population.radius_km} km`}
              />

              <InfoRow
                label={t.geographicArea}
                value={`${population.area_km2?.toFixed(2)} km²`}
              />

              <InfoRow
                label={t.populationDensity}
                value={`${population.population_density?.toLocaleString(
                  "en-IN",
                )} ${t.people}/km²`}
              />

              <InfoRow
                label={t.estimatedHouseholds}
                value={population.estimated_households?.toLocaleString("en-IN")}
              />
            </SectionCard>

            <SectionCard title={t.location} icon={MapPin}>
              <InfoRow label={t.country} value={population.country} />

              <InfoRow label={t.location} value={population.location} />

              <InfoRow label={t.latitude} value={population.latitude} />

              <InfoRow label={t.longitude} value={population.longitude} />
            </SectionCard>
          </div>

          <div className="mt-5">
            <SectionCard title={t.dataSources} icon={Home}>
              <InfoRow
                label={t.populationSource}
                value={population.population_data_source}
              />

              <InfoRow label={t.populationYear} value={population.data_year} />

              <InfoRow
                label={t.householdSource}
                value={population.household_data_source}
              />

              <InfoRow
                label={t.estimationMethod}
                value={population.household_estimation_method}
              />
            </SectionCard>
          </div>
        </>
      )}
    </BusinessEvidenceLayout>
  );
};

export default PopulationAnalysis;
