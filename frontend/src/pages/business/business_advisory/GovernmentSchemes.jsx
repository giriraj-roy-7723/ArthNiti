import { useNavigate, useParams } from "react-router-dom";
import { ArrowLeft, Landmark, Search, Sparkles } from "lucide-react";

const GovernmentSchemes = () => {
  const { businessId } = useParams();
  const navigate = useNavigate();

  // TODO(API): Add government-scheme recommendation API call.
  // TODO(API): Send/load business profile and eligibility profile.
  // TODO(API): Load recommended schemes from pgvector-backed backend.
  // TODO(API): Add scheme search/filter API later.

  const demoSchemes = [
    {
      name: "Business Development Assistance",
      level: "State",
      match: "High Match",
      description: "Placeholder recommendation based on the business profile.",
    },
    {
      name: "Small Enterprise Support Scheme",
      level: "Central",
      match: "Potential Match",
      description: "Placeholder scheme recommendation.",
    },
    {
      name: "Entrepreneurship Development Support",
      level: "State",
      match: "Potential Match",
      description: "Placeholder entrepreneurship support scheme.",
    },
  ];

  return (
    <div className="min-h-screen bg-gray-950 px-4 py-8 text-white sm:px-6 lg:px-8">
      <div className="mx-auto max-w-7xl">
        <button
          type="button"
          onClick={() => navigate(`/businesses/${businessId}`)}
          className="mb-6 inline-flex items-center gap-2 text-sm font-semibold text-gray-400 transition hover:text-white"
        >
          <ArrowLeft size={16} />
          Back to Workspace
        </button>

        <div className="mb-8 flex flex-col gap-5 lg:flex-row lg:items-end lg:justify-between">
          <div className="flex items-center gap-4">
            <div className="flex h-14 w-14 items-center justify-center rounded-2xl border border-blue-500/20 bg-blue-500/10">
              <Landmark size={27} className="text-blue-400" />
            </div>
            <div>
              <div className="flex items-center gap-2 text-sm font-semibold text-blue-400">
                <Sparkles size={15} />
                AI Recommendations
              </div>
              <h1 className="mt-1 text-3xl font-extrabold">Government Schemes</h1>
              <p className="mt-1 text-sm text-gray-500">Business ID: {businessId}</p>
            </div>
          </div>

          <div className="flex items-center gap-2 rounded-xl border border-gray-800 bg-gray-900/70 px-4 py-3">
            <Search size={17} className="text-gray-500" />
            <span className="text-sm text-gray-500">Scheme search placeholder</span>
          </div>
        </div>

        <div className="mb-6 rounded-2xl border border-blue-500/20 bg-blue-500/5 p-5">
          <p className="text-sm leading-6 text-gray-400">
            Recommended schemes will be generated from the business profile,
            eligibility profile and government-scheme vector search.
          </p>
        </div>

        <div className="grid grid-cols-1 gap-5 lg:grid-cols-3">
          {demoSchemes.map((scheme) => (
            <div
              key={scheme.name}
              className="rounded-2xl border border-gray-800 bg-gray-900/60 p-6 backdrop-blur-xl"
            >
              <div className="flex items-start justify-between gap-3">
                <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-blue-500/10">
                  <Landmark size={21} className="text-blue-400" />
                </div>
                <span className="rounded-full border border-emerald-500/20 bg-emerald-500/10 px-2.5 py-1 text-xs font-semibold text-emerald-400">
                  {scheme.match}
                </span>
              </div>

              <h2 className="mt-5 text-lg font-bold">{scheme.name}</h2>
              <p className="mt-2 text-xs font-semibold text-blue-400">{scheme.level} Scheme</p>
              <p className="mt-3 text-sm leading-6 text-gray-500">{scheme.description}</p>

              <div className="mt-5 rounded-lg border border-dashed border-gray-800 px-3 py-2 text-xs text-gray-600">
                API integration placeholder
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default GovernmentSchemes;
