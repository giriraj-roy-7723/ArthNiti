import { useNavigate, useParams } from "react-router-dom";
import { ArrowLeft, Sparkles, WalletCards } from "lucide-react";

const FinancialAnalysis = () => {
  const { businessId } = useParams();
  const navigate = useNavigate();

  // TODO(API): Add financial-analysis API calls here.
  // TODO(API): Send financial inputs.
  // TODO(API): Load generated financial analysis.
  // TODO(API): Load financial-analysis translations later if required.

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

        <div className="mb-8 flex items-center gap-4">
          <div className="flex h-14 w-14 items-center justify-center rounded-2xl border border-blue-500/20 bg-blue-500/10">
            <WalletCards size={27} className="text-blue-400" />
          </div>
          <div>
            <div className="flex items-center gap-2 text-sm font-semibold text-blue-400">
              <Sparkles size={15} />
              AI Financial Planning
            </div>
            <h1 className="mt-1 text-3xl font-extrabold">Financial Analysis</h1>
            <p className="mt-1 text-sm text-gray-500">Business ID: {businessId}</p>
          </div>
        </div>

        <div className="grid grid-cols-1 gap-5 md:grid-cols-2">
          {[
            ["Investment & Capital", "Investment requirements and capital structure placeholder."],
            ["Revenue Projection", "Projected revenue and sales assumptions placeholder."],
            ["Expenses", "Operating and fixed-cost analysis placeholder."],
            ["Profitability", "Profit, margin and break-even analysis placeholder."],
            ["Loan / Repayment", "Loan repayment and financing plan placeholder."],
            ["Financial Report", "AI-generated financial report placeholder."],
          ].map(([title, description]) => (
            <div
              key={title}
              className="min-h-[180px] rounded-2xl border border-gray-800 bg-gray-900/60 p-6 backdrop-blur-xl"
            >
              <h2 className="text-lg font-bold">{title}</h2>
              <p className="mt-3 text-sm leading-6 text-gray-500">{description}</p>
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

export default FinancialAnalysis;
