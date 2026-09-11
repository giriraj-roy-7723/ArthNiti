# Category: Financial Analysis & Planning

---
CHUNK_ID: financial_analysis_001
TITLE: Financial Analysis and Planning Engine Overview
CATEGORY: financial_analysis
PAGE/MODULE: Financial Analysis (/businesses/:businessId/financial-analysis)
AUTHENTICATION: Required (Role: Entrepreneur)
KEYWORDS: financial analysis, financial plan, financial planning, ai financial report, project cost, debt planning

CONTENT:
The Financial Analysis module (`/businesses/:businessId/financial-analysis`) is an AI-powered financial structuring engine. It bridges the gap between field-level market evidence and formal bankable financial structuring.

Instead of guessing revenue and expenditure numbers, the financial engine uses the completed Business Analysis data (population reach, competitor counts, mandi market rates, transportation OPEX, and seasonality) to generate an institutional-grade financial blueprint.

What Financial Analysis Delivers:
- Total Project Cost breakdown (Fixed capital + initial working capital).
- Margin Capital requirement (entrepreneur's own equity) vs Recommended Loan Amount.
- Multi-scenario cash-flow forecasts (Best Case, Expected Case, Worst Case).
- Operating metrics: Monthly Revenue, Direct Costs (raw materials, freight), Fixed Costs (rent, utilities, salaries), Gross Profit, Net Profit, and Break-even Revenue.
- Institutional Debt Sizing: Recommended Loan Amount, Loan Tenure (in months), Interest Rate, Moratorium Period, Monthly EMI, and DSCR (Debt Service Coverage Ratio).
- Comprehensive AI Financial Report summarizing bankability and financial risk mitigations.

USER QUESTIONS THIS CHUNK SHOULD ANSWER:
- What is Financial Analysis on ArthNiti?
- What financial projections does the platform generate?
- How does the system calculate my required project cost and loan?
- How is the financial plan linked to the business analysis?

NAVIGATION/ACTION:
Open Business Workspace (`/businesses/:businessId`) → Click "Financial Analysis" or navigate to `/businesses/:businessId/financial-analysis`.

RELATED CHUNKS:
- financial_prerequisites_001
- financial_scenarios_001
- financial_debt_capacity_001
- business_workspace_001
---

---
CHUNK_ID: financial_prerequisites_001
TITLE: Prerequisite for Financial Analysis (Business Analysis Required)
CATEGORY: financial_analysis
PAGE/MODULE: Financial Analysis (/businesses/:businessId/financial-analysis)
AUTHENTICATION: Required (Role: Entrepreneur)
KEYWORDS: business analysis required, financial prerequisite, complete feasibility first, cannot generate financial plan

CONTENT:
Critical System Rule:
You MUST complete the Business Analysis (Feasibility Study) before generating Financial Analysis for a business.

Why is Business Analysis Required First?
The financial engine does not use generic, ungrounded estimates. It requires the empirical evidence produced by the Business Analysis engine:
- Population and household numbers to model realistic sales volumes.
- Competitor density to calibrate realistic local market share.
- Mandi commodity rates to price direct raw material consumption.
- Modeled freight costs from Transportation Analysis to calculate accurate logistics OPEX.
- Seasonality profiles to model monthly cash flow troughs.

What Happens if You Try to Generate Financials Without Business Analysis:
The Financial Analysis page displays a blocking screen:
"Business Analysis Required: Complete the Business Analysis first. The financial engine uses the business feasibility analysis and its evidence to produce more reliable revenue, cost, working-capital and financing estimates."
A direct button "Complete Business Analysis" is provided to guide you there.

USER QUESTIONS THIS CHUNK SHOULD ANSWER:
- Why can't I generate financial analysis yet?
- What do I need before running financial analysis?
- Why is Business Analysis required before Financial Planning?
- How do I unlock the financial analysis module?

NAVIGATION/ACTION:
If locked: Click "Complete Business Analysis" to navigate to `/businesses/:businessId/analysis` → Generate Feasibility Report → Return to `/businesses/:businessId/financial-analysis`.

RELATED CHUNKS:
- business_analysis_001
- business_analysis_002
- financial_analysis_001
---

---
CHUNK_ID: financial_scenarios_001
TITLE: Financial Scenarios (Best Case, Expected Case, Worst Case)
CATEGORY: financial_analysis
PAGE/MODULE: Financial Analysis (/businesses/:businessId/financial-analysis) → Financial Scenarios
AUTHENTICATION: Required (Role: Entrepreneur)
KEYWORDS: financial scenarios, expected case, best case, worst case, revenue scenarios, stress test, risk confidence

CONTENT:
Because real-world rural enterprise revenue fluctuates, ArthNiti's financial engine models three distinct financial scenarios:

1. Expected Case (Baseline):
   - The most realistic scenario based on average local demand, normal seasonal conditions, and modal competitor behavior.
   - Represents the core operational benchmark for budgeting and bank loan assessments.
2. Best Case (Optimistic):
   - Assumes peak seasonal demand, higher customer adoption, favorable commodity buying prices, and high operational efficiency.
   - Shows the maximum profit potential and accelerated loan repayment capacity.
3. Worst Case (Pessimistic / Stress Test):
   - Models severe stress: adverse weather/monsoon disruption, raw material price inflation, lower customer footfall, or aggressive competitor discounting.
   - Evaluates whether the enterprise maintains positive cash flow and can still service its monthly bank loan EMI during crisis periods without defaulting.

For each scenario, the dashboard displays:
- Projected Monthly Revenue
- Projected Monthly Expenses
- Operating Surplus
- Risk Level & Confidence Score

USER QUESTIONS THIS CHUNK SHOULD ANSWER:
- What are the three financial scenarios?
- What is the difference between Expected, Best, and Worst case?
- How does the platform test if my business can survive bad months?
- What happens if my sales are lower than expected?

NAVIGATION/ACTION:
Go to `/businesses/:businessId/financial-analysis` → In the tab/section navigation, select "Financial Scenarios".

RELATED CHUNKS:
- financial_analysis_001
- financial_profitability_001
- analysis_seasonality_001
---

---
CHUNK_ID: financial_margin_capital_001
TITLE: Margin Capital vs Total Project Cost
CATEGORY: financial_analysis
PAGE/MODULE: Financial Analysis (/businesses/:businessId/financial-analysis) & Business Setup
AUTHENTICATION: Required (Role: Entrepreneur)
KEYWORDS: margin capital, own contribution, project cost, promoter equity, down payment, bank loan gap

CONTENT:
Key Financial Concepts Explained:

1. Total Project Cost:
   - The total financial capital required to establish and launch the business.
   - Includes capital expenditure (CAPEX) for machinery, tools, shed/renovation, equipment, plus the initial working capital required to purchase inventory and fund operations before revenue arrives.

2. Margin Capital (Promoter's Contribution / Equity):
   - The money the entrepreneur brings from their own personal savings, family contributions, or retained funds.
   - Entered during business creation and updatable via the Edit Business modal.
   - Banks and government loan schemes mandate that the entrepreneur provide a minimum percentage (typically 10% to 25%) as margin capital to demonstrate commitment and skin in the game.

3. Required Bank Loan / Debt Financing:
   - Total Project Cost minus Margin Capital = Required Loan Amount.
   - Example: If a mini mustard oil mill requires ₹5,00,000 Total Project Cost, and the entrepreneur provides ₹1,00,000 Margin Capital (20%), the Required Bank Loan is ₹4,00,000 (80%).

USER QUESTIONS THIS CHUNK SHOULD ANSWER:
- What is margin capital?
- What is the difference between margin capital and total project cost?
- How much money do I need to invest from my own pocket?
- How is the required loan amount calculated from my margin capital?

NAVIGATION/ACTION:
Check your margin capital on `/businesses/:businessId` or update it via Edit Business in `/businesses`. View its impact on `/businesses/:businessId/financial-analysis`.

RELATED CHUNKS:
- business_create_001
- financial_analysis_001
- financial_debt_capacity_001
---

---
CHUNK_ID: financial_profitability_001
TITLE: Operating Expenses, Profitability, and Break-Even Analysis
CATEGORY: financial_analysis
PAGE/MODULE: Financial Analysis (/businesses/:businessId/financial-analysis) → Financial Plan
AUTHENTICATION: Required (Role: Entrepreneur)
KEYWORDS: profitability, gross profit, net profit, profit margin, direct costs, fixed costs, break even revenue

CONTENT:
The Financial Plan section provides a granular operational breakdown of ongoing revenues, costs, and profits:

1. Monthly Revenue: Total projected gross cash generated from product sales or services rendered.
2. Operating Cost Breakdown:
   - Direct Costs (Variable OPEX): Expenses that scale directly with production, including raw material purchases (indexed from mandi rates) and transportation/freight costs.
   - Fixed Costs: Invariant monthly overheads, including shop/land rent, machinery depreciation, permanent staff wages, electricity, utility connections, and license renewals.
3. Profitability Metrics:
   - Gross Profit: Revenue minus Direct Costs.
   - Net Profit: Gross Profit minus Fixed Costs minus Monthly Loan EMI. This is the true net income retained by the entrepreneur.
   - Profit Margin (%): Net Profit as a percentage of Total Revenue.
4. Break-Even Revenue:
   - The minimum monthly sales revenue the business must achieve just to cover all fixed costs, direct costs, and loan EMI (zero net profit, zero loss).
   - Any sales generated beyond this break-even threshold represent pure enterprise profit.

USER QUESTIONS THIS CHUNK SHOULD ANSWER:
- How does the platform calculate my monthly net profit?
- What are direct costs and fixed costs?
- What is break-even revenue?
- How much money do I need to sell each month to avoid losing money?

NAVIGATION/ACTION:
Go to `/businesses/:businessId/financial-analysis` → View the "Financial Plan" overview cards and cost breakdown tables.

RELATED CHUNKS:
- financial_analysis_001
- financial_scenarios_001
- analysis_market_prices_001
- analysis_transportation_001
---

---
CHUNK_ID: financial_debt_capacity_001
TITLE: Debt Capacity, Loan Sizing, EMI, Moratorium, and DSCR
CATEGORY: financial_analysis
PAGE/MODULE: Financial Analysis (/businesses/:businessId/financial-analysis) → Debt & Financing
AUTHENTICATION: Required (Role: Entrepreneur)
KEYWORDS: debt capacity, loan amount, emi, interest rate, tenure, moratorium, dscr, debt service coverage ratio

CONTENT:
To help entrepreneurs apply for bank loans (such as MUDRA, PMEGP, or commercial term loans) with confidence, the financial engine calculates institutional debt-servicing metrics:

Key Debt Parameters Calculated:
- Recommended Loan Amount: The prudent borrowing amount that avoids underfunding while ensuring the entrepreneur is not burdened with excessive debt.
- Monthly EMI (Equated Monthly Installment): The estimated monthly principal + interest repayment obligation.
- Indicative Interest Rate (% p.a.): Realistic interest rates based on current micro-finance and priority-sector commercial lending rates in India.
- Recommended Loan Tenure (Months): The repayment lifespan (typically 36 to 84 months) matched to machinery longevity and cash flow.
- Moratorium Period (Grace Period): The initial grace window (e.g., 3 to 6 months) during which the entrepreneur sets up operations before principal repayments begin.
- DSCR (Debt Service Coverage Ratio):
  - DSCR = Net Operating Income / Total Debt Service (EMI).
  - A DSCR above 1.5 indicates a healthy, safe borrower capable of easily paying bank installments even if sales dip. Commercial lenders look for a DSCR between 1.5 and 2.0.

USER QUESTIONS THIS CHUNK SHOULD ANSWER:
- How much loan can my business safely afford to borrow?
- What will my monthly loan EMI be?
- What is DSCR and why do banks check it?
- What is a loan moratorium period?

NAVIGATION/ACTION:
Go to `/businesses/:businessId/financial-analysis` → Locate the "Debt Capacity" and "Loan & EMI" assessment cards.

RELATED CHUNKS:
- financial_analysis_001
- financial_margin_capital_001
- government_schemes_001
---

---
CHUNK_ID: financial_working_capital_001
TITLE: Working Capital Requirements and Input Assumptions
CATEGORY: financial_analysis
PAGE/MODULE: Financial Analysis (/businesses/:businessId/financial-analysis)
AUTHENTICATION: Required (Role: Entrepreneur)
KEYWORDS: working capital, operating buffer, input warnings, financial assumptions, accepted values

CONTENT:
Working Capital Insights:
Working capital is the operational cash required to fund day-to-day cycles—procuring inventory, paying seasonal labor, fuel, packaging, and extending customer credit—before receiving cash payments from sales.
The module models the working capital cycle (typically 30 to 90 days) so the entrepreneur does not run out of operational cash immediately after opening.

Input Validation & Assumptions Transparency:
The Financial Analysis engine provides complete transparency into its mathematical assumptions:
- Values Used & Adjustments: Shows exactly which inputs were accepted from the business profile and feasibility report.
- Input Warnings & Sanity Checks: If a user enters an unrealistic margin capital (e.g., ₹100 for a ₹10,00,000 project), the validation engine flags this: "The supplied value was adjusted to adhere to micro-enterprise lending guidelines."
- Financial Assumptions: Documents assumptions regarding commodity spoilage rates, raw material credit periods, electricity unit rates, and customer collection cycles.

USER QUESTIONS THIS CHUNK SHOULD ANSWER:
- What is working capital and why do I need it?
- Why did the financial engine adjust my margin capital?
- Where can I see the assumptions behind the financial plan?
- How does the system prevent unrealistic financial numbers?

NAVIGATION/ACTION:
Go to `/businesses/:businessId/financial-analysis` → Scroll to "Input Validation & Adjustments" and "Financial Assumptions".

RELATED CHUNKS:
- financial_analysis_001
- financial_profitability_001
- business_create_001
---
