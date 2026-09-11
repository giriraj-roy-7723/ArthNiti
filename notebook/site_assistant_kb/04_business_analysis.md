# Category: Business Analysis & Feasibility

---
CHUNK_ID: business_analysis_001
TITLE: Business Feasibility Analysis Overview
CATEGORY: business_analysis
PAGE/MODULE: Business Analysis (/businesses/:businessId/analysis)
AUTHENTICATION: Required (Role: Entrepreneur)
KEYWORDS: business analysis, feasibility analysis, feasibility report, market viability, business intelligence

CONTENT:
The Business Analysis module provides an AI-driven, hyper-local feasibility study for a business venture. Rather than generic industry estimates, it collects real empirical evidence within a designated geographic radius around the business's location.

The Analysis is Structured into Two Major Parts:
1. The Feasibility Report: An executive AI-generated assessment synthesizing the overall viability of the enterprise, local competitive pressures, customer purchasing power, supply strengths, and strategic recommendations.
2. Evidence & Insights Modules: Six dedicated, deep-dive analytical sections:
   - Population Analysis (Demographics, household counts, customer reach)
   - Competition Analysis (Competitor density, proximity, market saturation)
   - Market Prices (Commodity price statistics, APMC mandi rates)
   - Supply Chain (Sourcing infrastructure, cold storage, supply chain scoring)
   - Transportation (Modeled route logistics, vehicle selection, monthly freight costs)
   - Seasonality (Monthly demand curves, agricultural cycles, weather impact)

USER QUESTIONS THIS CHUNK SHOULD ANSWER:
- What is Business Analysis on ArthNiti?
- What does the feasibility analysis calculate?
- What information does Business Analysis provide?
- How is hyper-local feasibility assessed?

NAVIGATION/ACTION:
Open your Business Workspace (`/businesses/:businessId`) → Click "Business Analysis" or navigate directly to `/businesses/:businessId/analysis`.

RELATED CHUNKS:
- business_analysis_002
- analysis_feasibility_report_001
- business_workspace_001
---

---
CHUNK_ID: business_analysis_002
TITLE: Configuring and Generating Business Analysis (Radius, Background Execution)
CATEGORY: business_analysis
PAGE/MODULE: Business Analysis (/businesses/:businessId/analysis)
AUTHENTICATION: Required (Role: Entrepreneur)
KEYWORDS: generate analysis, analysis radius, run feasibility, background processing, 5-10 minutes, execution time

CONTENT:
How to Configure and Run Business Analysis:
1. In the Business Workspace, click "Business Analysis".
2. If analysis has never been generated, click "Generate Analysis" (or "Configure Business Analysis").
3. Set the Analysis Radius:
   - Use the slider to define the geographic radius around your location (e.g., 5 km, 10 km, 25 km, or 50 km).
   - Default is 10 km. For retail or local services, smaller radii (5–10 km) are ideal; for manufacturing, agro-processing, or wholesale, larger radii (25–50 km) are recommended.
4. Click "Generate Analysis".

Background Execution and Duration:
- Comprehensive multi-source market research (demographic modeling, OpenStreetMap competitor mapping, mandi price feeds, and freight simulation) takes approximately 5 to 10 minutes.
- The task runs asynchronously in the backend. You do NOT need to keep the screen open! You can safely close the modal, navigate to other workspaces, or log out. The report is saved automatically upon completion.

USER QUESTIONS THIS CHUNK SHOULD ANSWER:
- How do I generate a Business Analysis?
- What is the Analysis Radius and how do I choose it?
- How long does Business Analysis take to complete?
- Can I close the website while analysis is running?

NAVIGATION/ACTION:
Go to `/businesses/:businessId/analysis` → Click "Generate Analysis" → Choose Radius → Click Confirm.

RELATED CHUNKS:
- business_analysis_001
- business_analysis_003
- faq_analysis_time_001
---

---
CHUNK_ID: business_analysis_003
TITLE: Handling Stale Business Analysis and Regeneration
CATEGORY: business_analysis
PAGE/MODULE: Business Analysis (/businesses/:businessId/analysis)
AUTHENTICATION: Required (Role: Entrepreneur)
KEYWORDS: regenerate analysis, stale analysis, outdated report, business details changed, update feasibility

CONTENT:
When Business Details Change:
If you edit key parameters of your business—such as changing its physical address, moving to a different village/district, modifying coordinates, or altering your available margin capital—your previously generated Feasibility Report becomes out of date.

The "Business Details Have Changed" Alert:
When this happens, the platform displays a prominent warning banner at the top of the Business Analysis page:
"Business details have changed. This feasibility report was generated with older business information. Update parameters and regenerate for current insights."

How to Regenerate:
1. Click the "Review & Regenerate" button on the banner (or click "Regenerate Analysis" in the top bar).
2. Review your updated business parameters and select your desired analysis radius.
3. Confirm generation. The backend re-runs the geospatial and demographic simulations and replaces the old report with newly computed data.

USER QUESTIONS THIS CHUNK SHOULD ANSWER:
- Can I regenerate my business analysis?
- Why does it say "Business details have changed" or "Needs regeneration"?
- What happens to my report if I move my business location?
- How do I get fresh market data?

NAVIGATION/ACTION:
Go to `/businesses/:businessId/analysis` → Click the "Review & Regenerate" or "Regenerate Analysis" button.

RELATED CHUNKS:
- business_edit_001
- business_analysis_002
---

---
CHUNK_ID: analysis_population_001
TITLE: Population Analysis Module
CATEGORY: business_analysis
PAGE/MODULE: Population Analysis (/businesses/:businessId/analysis/population)
AUTHENTICATION: Required (Role: Entrepreneur)
KEYWORDS: population analysis, demographics, household count, customer density, market radius, customer base

CONTENT:
The Population Analysis submodule evaluates the demographic scale and density of the potential customer base living within your selected market radius.

What Population Analysis Calculates:
- Total Reachable Population: Estimated count of individuals living within the chosen radius.
- Household Counts: Number of distinct family/household units.
- Population Density: Number of residents per square kilometer, highlighting whether the market is dense urban, peri-urban, or dispersed rural.
- Demographic Segmentation: Age bracket breakdowns, gender ratios, literacy figures, and economic activity indicators (where local census data is available).
- Market Reach Score: A quantitative evaluation of customer accessibility based on settlement patterns.

Why This Matters:
It prevents entrepreneurs from overestimating local customer demand. For instance, a high-volume bakery requires a minimum threshold of reachable households, while specialized machinery repair can operate in lower population densities.

USER QUESTIONS THIS CHUNK SHOULD ANSWER:
- What is Population Analysis?
- How does the platform estimate my customer base?
- What demographic details are included in the report?
- Where do I find the population analysis for my business?

NAVIGATION/ACTION:
Go to `/businesses/:businessId/analysis` → In the Evidence & Insights section, click "Population Analysis" (or go to `/businesses/:businessId/analysis/population`).

RELATED CHUNKS:
- business_analysis_001
- business_analysis_002
- analysis_competition_001
---

---
CHUNK_ID: analysis_competition_001
TITLE: Competition Analysis Module
CATEGORY: business_analysis
PAGE/MODULE: Competition Analysis (/businesses/:businessId/analysis/competitors)
AUTHENTICATION: Required (Role: Entrepreneur)
KEYWORDS: competition analysis, competitors, market saturation, competitor mapping, competitive landscape

CONTENT:
The Competition Analysis submodule identifies, maps, and evaluates commercial rivals and similar businesses operating within your selected market radius.

What Competition Analysis Calculates:
- Total Competitor Count: Total number of active businesses operating in the same or adjacent product/service category within the analysis radius.
- Competitor Density: Ratio of competitors relative to geographic area and population (competitors per 1,000 residents).
- Geographic Competitor Mapping: Interactive map plotting the spatial locations of nearby competing shops, enterprises, or factories.
- Proximity & Clustering: Identifies whether competitors are concentrated in a central market hub (bazaar) or dispersed along transport arteries.
- Market Saturation Index: Assesses whether the local market is underserved (high opportunity), balanced, or oversaturated (high price war risk).

Why This Matters:
Understanding competitor density prevents setting up a business in an oversaturated zone and highlights opportunities for differentiation (e.g., offering doorstep delivery, extended hours, or higher quality).

USER QUESTIONS THIS CHUNK SHOULD ANSWER:
- How does competitor analysis work on ArthNiti?
- How many competitors are located near my business?
- Where can I see a map of my competitors?
- Is my local market oversaturated?

NAVIGATION/ACTION:
Go to `/businesses/:businessId/analysis` → Click "Competition Analysis" (or navigate directly to `/businesses/:businessId/analysis/competitors`).

RELATED CHUNKS:
- business_analysis_001
- analysis_population_001
- analysis_market_prices_001
---

---
CHUNK_ID: analysis_market_prices_001
TITLE: Market Prices and Mandi Intelligence Module
CATEGORY: business_analysis
PAGE/MODULE: Market Prices (/businesses/:businessId/analysis/market-prices)
AUTHENTICATION: Required (Role: Entrepreneur)
KEYWORDS: market prices, mandi rates, apmc prices, commodity pricing, price intelligence, wholesale rates

CONTENT:
The Market Prices submodule delivers commodity and product price intelligence sourced from regional APMC mandis, government agricultural price portals, and local market trade networks.

What Market Price Analysis Provides:
- Benchmark Commodity Pricing: Recent modal, minimum, and maximum trading prices for commodities relevant to your business category (e.g., wheat, paddy, mustard, milk, spices, timber).
- Mandi Price Comparison: Price differences across nearby district mandis, identifying where raw materials can be purchased at lowest cost or where finished goods can be sold for the highest margin.
- Price Volatility Indicators: Historical price fluctuations to show whether the commodity experiences sudden price spikes or seasonal crashes.
- Profit Margin Implication: How prevailing market rates influence direct material costs and retail markups.

USER QUESTIONS THIS CHUNK SHOULD ANSWER:
- What are market prices in the business analysis?
- Where does ArthNiti get commodity and mandi prices?
- How do I check wholesale market rates for my raw materials?
- How do current market prices affect my profitability?

NAVIGATION/ACTION:
Go to `/businesses/:businessId/analysis` → Click "Market Prices" (or navigate to `/businesses/:businessId/analysis/market-prices`).

RELATED CHUNKS:
- business_analysis_001
- analysis_supply_chain_001
- financial_profitability_001
---

---
CHUNK_ID: analysis_supply_chain_001
TITLE: Supply Chain Analysis Module
CATEGORY: business_analysis
PAGE/MODULE: Supply Chain (/businesses/:businessId/analysis/supply-chain)
AUTHENTICATION: Required (Role: Entrepreneur)
KEYWORDS: supply chain analysis, raw material sourcing, cold chain, processing units, storage infrastructure, supply score

CONTENT:
The Supply Chain submodule evaluates how easily and reliably your business can procure its necessary raw inputs and distribute goods to markets.

Key Dimensions Evaluated:
- Sourcing Proximity: Distance to primary producers, agricultural clusters, or wholesale distributors.
- Critical Infrastructure Availability: Proximity to cold storages, government warehouses, food processing units, grading centers, and packaging suppliers.
- Supply Chain Score: A composite metric (0 to 100) summarizing supply robustness, reliability of supplier lead times, and vulnerability to shortages.
- Inbound Logistics Risk: Potential bottlenecks in procuring raw inventory during peak or off-seasons.

Why This Matters:
For micro-enterprises like food processing, dairy, or handloom, supply chain failure is often the primary reason for operational closure. This module ensures you know where your raw materials come from before spending capital.

USER QUESTIONS THIS CHUNK SHOULD ANSWER:
- What is Supply Chain Analysis?
- What does the Supply Chain Score mean?
- How does the platform evaluate raw material sourcing and cold storage?
- Where do I inspect supply chain risks for my business?

NAVIGATION/ACTION:
Go to `/businesses/:businessId/analysis` → Click "Supply Chain" (or navigate to `/businesses/:businessId/analysis/supply-chain`).

RELATED CHUNKS:
- business_analysis_001
- analysis_market_prices_001
- analysis_transportation_001
---

---
CHUNK_ID: analysis_transportation_001
TITLE: Transportation and Logistics Analysis Module
CATEGORY: business_analysis
PAGE/MODULE: Transportation (/businesses/:businessId/analysis/transportation)
AUTHENTICATION: Required (Role: Entrepreneur)
KEYWORDS: transportation analysis, logistics costs, freight simulation, delivery distance, vehicle selection, opex

CONTENT:
The Transportation Analysis submodule provides modeled simulations of the transportation and freight expenses required to keep your business running.

What Transportation Analysis Models:
- Simulated Sourcing & Delivery Routes: Modeled road paths connecting your business location to district trade centers, nearest railway freight stations, and highway nodes.
- Vehicle Selection & Road Suitability: Recommendations on optimal vehicle types based on rural road quality (e.g., 3-wheeler mini-trucks, 1-ton pickup vans, heavy commercial trucks, or tractor-trailers).
- Travel Distance and Transit Times: Average travel duration accounting for local road topography.
- Estimated Monthly Freight OPEX: A modeled monthly transportation expenditure (fuel, vehicle hiring/lease, driver costs, tolls) that is directly fed into the Financial Analysis module as part of direct operating expenses.

USER QUESTIONS THIS CHUNK SHOULD ANSWER:
- What is Transportation Analysis?
- How does ArthNiti calculate modeled logistics costs?
- What vehicles are recommended for my business transport?
- Where can I see estimated monthly freight expenses?

NAVIGATION/ACTION:
Go to `/businesses/:businessId/analysis` → Click "Transportation" (or navigate to `/businesses/:businessId/analysis/transportation`).

RELATED CHUNKS:
- business_analysis_001
- business_location_001
- financial_profitability_001
---

---
CHUNK_ID: analysis_seasonality_001
TITLE: Seasonality Analysis Module
CATEGORY: business_analysis
PAGE/MODULE: Seasonality (/businesses/:businessId/analysis/seasonality)
AUTHENTICATION: Required (Role: Entrepreneur)
KEYWORDS: seasonality analysis, monthly demand, rainfall, weather risk, seasonal cycles, festival demand

CONTENT:
Rural and semi-urban businesses frequently experience drastic seasonal volatility driven by monsoons, agricultural harvest schedules, wedding seasons, and festival cycles. The Seasonality Analysis submodule models these month-by-month swings.

What Seasonality Analysis Delivers:
- 12-Month Demand Curve: Visual forecast of sales peaks and troughs across all 12 calendar months (January to December).
- Production & Supply Fluctuations: Highlights months where raw materials become scarce or expensive (e.g., monsoon transport disruption or post-harvest gluts).
- Climate and Rainfall Patterns: Historical local precipitation profiles indicating weather risks (flood seasons, extreme summer heat).
- Working Capital Buffer Recommendations: Strategic advice on setting aside reserve cash during boom months to survive lean off-season periods.

USER QUESTIONS THIS CHUNK SHOULD ANSWER:
- What is Seasonality Analysis?
- How do weather, monsoons, and harvest cycles affect my business?
- Which months will have the highest sales and lowest sales?
- How do I prepare for off-season lean periods?

NAVIGATION/ACTION:
Go to `/businesses/:businessId/analysis` → Click "Seasonality" (or navigate to `/businesses/:businessId/analysis/seasonality`).

RELATED CHUNKS:
- business_analysis_001
- financial_working_capital_001
- financial_scenarios_001
---

---
CHUNK_ID: analysis_feasibility_report_001
TITLE: Understanding the AI Feasibility Report
CATEGORY: business_analysis
PAGE/MODULE: Business Analysis (/businesses/:businessId/analysis)
AUTHENTICATION: Required (Role: Entrepreneur)
KEYWORDS: feasibility report, ai report, executive summary, business assessment, swot, strategic recommendations

CONTENT:
The Feasibility Report sits at the top of the Business Analysis page. It represents an executive synthesis generated by ArthNiti's analytical AI engine by pulling together all empirical findings from population, competitors, prices, supply chain, freight, and seasonality.

What the Report Contains:
1. Executive Feasibility Summary: A clear, high-level assessment of whether the business concept is viable in this exact location.
2. Market Viability Score: Overall index of consumer demand vs competitor saturation.
3. Key Strengths & Growth Catalysts: Inherent advantages of the business (e.g., close proximity to raw inputs, low competitor density).
4. Critical Risks & Vulnerabilities: Major operational threats identified (e.g., high logistics costs, heavy off-season dependency, price volatility).
5. Concrete Strategic Directives: Specific actionable recommendations on pricing strategy, required product diversification, and marketing approaches.
6. Handover to Financial Planning: Confirmation that data is verified and ready to be used by the Financial Analysis engine.

USER QUESTIONS THIS CHUNK SHOULD ANSWER:
- What does the Feasibility Report say?
- How do I interpret the AI Feasibility Assessment?
- Does the report tell me if my business will succeed?
- What are the strategic recommendations based on?

NAVIGATION/ACTION:
Go to `/businesses/:businessId/analysis` → The Feasibility Report card is prominently displayed at the top.

RELATED CHUNKS:
- business_analysis_001
- financial_prerequisites_001
- limitations_platform_001
---
