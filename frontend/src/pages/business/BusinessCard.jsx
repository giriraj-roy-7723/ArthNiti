import { ArrowRight, Building2, MapPin } from "lucide-react";

const BusinessCard = ({ business, t, onOpen }) => {
  const getStatusLabel = (status) => {
    if (!status) return "";
    const normalizedStatus = status.toLowerCase();

    if (normalizedStatus === "approved") return t.approved;
    if (normalizedStatus === "rejected") return t.rejected;
    if (normalizedStatus === "pending") return t.pending;
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
    <button
      type="button"
      onClick={() => onOpen(business.id)}
      className="group text-left"
    >
      <div className="relative h-full overflow-hidden rounded-2xl border border-gray-800 bg-gray-900/70 p-6 shadow-[0_15px_40px_rgba(0,0,0,0.25)] backdrop-blur-xl transition-all duration-300 hover:-translate-y-2 hover:border-blue-500/30 hover:bg-gray-900 hover:shadow-[0_20px_50px_rgba(37,99,235,0.12)]">
        <div className="pointer-events-none absolute -right-10 -top-10 h-32 w-32 rounded-full bg-blue-600/10 blur-3xl transition-opacity duration-300 group-hover:opacity-100" />

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
                ? [business.city, business.state].filter(Boolean).join(", ")
                : t.locationUnavailable}
            </span>
          </div>
        </div>

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
  );
};

export default BusinessCard;
