# Category: Government Schemes

---
CHUNK_ID: government_schemes_001
TITLE: Government Schemes Module and Matching Engine Overview
CATEGORY: government_schemes
PAGE/MODULE: Government Schemes (/businesses/:businessId/government-schemes)
AUTHENTICATION: Required (Role: Entrepreneur)
KEYWORDS: government schemes, sarkari yojana, scheme recommendation, subsidies, grants, mudra, pmegp, myscheme

CONTENT:
The Government Schemes module (`/businesses/:businessId/government-schemes`) helps rural and semi-urban entrepreneurs identify, evaluate, and access state and central government support schemes, capital subsidies, subsidized credit lines, and developmental grants (e.g., PMEGP, PM MUDRA Yojana, Stand-Up India, PMFME, state industrial subsidies).

Rather than forcing entrepreneurs to navigate thousands of bureaucratic documents, the platform employs a semantic vector embedding engine (built with pgvector) and an eligibility matching algorithm.

How the Matching Engine Operates:
1. It combines your enterprise profile (business category, location, margin capital, project scale) with your individual demographic eligibility profile.
2. It ranks relevant government schemes using a calculated percentage "Match Score".
3. For each matched scheme, it details specific financial benefits (subsidy percentages, interest subvention, collateral-free credit), eligibility criteria, required documentation, and direct application links.

USER QUESTIONS THIS CHUNK SHOULD ANSWER:
- What are Government Schemes on ArthNiti?
- How does the platform recommend government schemes for my business?
- Can I get subsidies or grants for my business?
- Where do I find schemes like PMEGP or MUDRA?

NAVIGATION/ACTION:
Open Business Workspace (`/businesses/:businessId`) → Click "Government Schemes" or navigate to `/businesses/:businessId/government-schemes`.

RELATED CHUNKS:
- schemes_prerequisites_001
- schemes_eligibility_001
- schemes_recommendations_001
- business_workspace_001
---

---
CHUNK_ID: schemes_prerequisites_001
TITLE: Prerequisite for Government Schemes (Business Analysis Required)
CATEGORY: government_schemes
PAGE/MODULE: Government Schemes (/businesses/:businessId/government-schemes)
AUTHENTICATION: Required (Role: Entrepreneur)
KEYWORDS: complete feasibility first, schemes prerequisite, business analysis required for schemes

CONTENT:
Important System Requirement:
You should complete the Business Analysis (Feasibility Report) before generating Government Scheme recommendations for a business.

Why is Business Analysis Recommended First?
Government schemes have strict sectoral criteria, investment caps, and geographic eligibility conditions. The matching engine relies on the verified parameters established in the Business Feasibility study (exact industry classification, capital scale, rural/urban classification, and feasibility metrics) to avoid recommending schemes for which the business is ineligible.

What to Do:
If your Business Analysis is not yet generated, open the Business Analysis module first, configure the radius, and run the feasibility study. Once generated, proceed to Government Schemes to receive high-precision scheme recommendations.

USER QUESTIONS THIS CHUNK SHOULD ANSWER:
- Why do I need to complete Business Analysis before finding schemes?
- Can I search government schemes without running a feasibility study?
- How does feasibility data improve scheme recommendations?

NAVIGATION/ACTION:
Go to `/businesses/:businessId/analysis` → Generate Feasibility Report → Then navigate to `/businesses/:businessId/government-schemes`.

RELATED CHUNKS:
- business_analysis_001
- government_schemes_001
- schemes_eligibility_001
---

---
CHUNK_ID: schemes_eligibility_001
TITLE: Scheme Eligibility Information Form
CATEGORY: government_schemes
PAGE/MODULE: Government Schemes (/businesses/:businessId/government-schemes)
AUTHENTICATION: Required (Role: Entrepreneur)
KEYWORDS: eligibility form, social category, ownership type, annual income, turnover, farmer status, land ownership

CONTENT:
To maximize recommendation accuracy, the Government Schemes page provides an Eligibility Questionnaire. While business details (location, category) are pulled automatically from your business profile, your personal socio-economic attributes are entered here:

Eligibility Fields:
- Age: Enter the entrepreneur's age (many schemes target youth or specific age brackets, e.g., 18–35).
- Gender: Male, Female, or Other (unlocks women-entrepreneur specific subsidies, such as enhanced PMEGP subsidies or Stand-Up India).
- Ownership Type: Individual, Proprietorship, Partnership, Company, Cooperative, or Other.
- Social Category: General, SC (Scheduled Caste), ST (Scheduled Tribe), OBC (Other Backward Class), or Minority. (Special welfare schemes offer up to 35% capital subsidy for SC/ST/women/rural entrepreneurs).
- Annual Family Income & Annual Business Turnover: Calibrates income thresholds and micro-enterprise ceilings.
- Investment Amount: Target capital requirement.
- Business Registered: Yes / No (whether the unit has Udyam, GST, or shop establishment registration).
- Farmer Status: Yes / No (unlocks agri-allied schemes, NABARD subsidies, and PM Kisan Sampada).
- Land Ownership: Yes / No.

Note on Flexibility:
All eligibility fields in the backend are optional. However, providing complete details ensures the algorithm filters out ineligible schemes and highlights top-tier subsidies.

USER QUESTIONS THIS CHUNK SHOULD ANSWER:
- What information is needed to find matching government schemes?
- Why does the platform ask for my gender, age, and social category?
- Do I need to be a registered business to get government schemes?
- Are all eligibility questions mandatory?

NAVIGATION/ACTION:
Go to `/businesses/:businessId/government-schemes` → Fill in the "Eligibility Information" section → Click "Find Matching Schemes".

RELATED CHUNKS:
- government_schemes_001
- schemes_recommendations_001
---

---
CHUNK_ID: schemes_recommendations_001
TITLE: Interpreting Scheme Recommendations and Match Scores
CATEGORY: government_schemes
PAGE/MODULE: Government Schemes (/businesses/:businessId/government-schemes) → Recommended Schemes
AUTHENTICATION: Required (Role: Entrepreneur)
KEYWORDS: match score, recommended schemes, subsidy percentage, loan assistance, eligibility criteria

CONTENT:
After submitting your eligibility information, the platform generates a ranked list of matched schemes:

Understanding Each Scheme Card:
1. Scheme Title & Nodal Ministry: Full official name of the scheme (e.g., "Prime Minister's Employment Generation Programme - PMEGP", "Pradhan Mantri Mudra Yojana - Shishu/Kishore/Tarun", "PM Formalisation of Micro Food Processing Enterprises - PMFME").
2. Match Percentage: A quantitative indicator (e.g., 95% Match, 88% Match) showing how closely your business profile and demographic credentials meet the scheme's formal guidelines.
3. Scheme Benefits Summary: Highlights concrete financial support:
   - Margin money subsidy (e.g., 15% to 35% of project cost).
   - Collateral-free credit guarantees (e.g., under CGTMSE).
   - Concession on interest rates (interest subventions of 2%–3%).
   - Capital grants for machinery or solar integration.
4. Detailed Eligibility Criteria: Lists exact conditions (e.g., minimum educational qualification, rural area location, proprietary stake).
5. Comprehensive Description: High-level overview of the scheme objectives and implementing agencies (KVIC, DIC, SIDBI, NABARD, Nationalized Banks).

USER QUESTIONS THIS CHUNK SHOULD ANSWER:
- What does the scheme Match percentage mean?
- How do I know which scheme offers the biggest subsidy?
- What benefits are provided under the recommended schemes?
- Where can I read the full criteria for each scheme?

NAVIGATION/ACTION:
Go to `/businesses/:businessId/government-schemes` → Scroll to "Recommended Schemes" to review matched cards.

RELATED CHUNKS:
- government_schemes_001
- schemes_eligibility_001
- schemes_application_001
---

---
CHUNK_ID: schemes_application_001
TITLE: How to Apply for Schemes and MyScheme Redirect Fallback
CATEGORY: government_schemes
PAGE/MODULE: Government Schemes (/businesses/:businessId/government-schemes)
AUTHENTICATION: Required (Role: Entrepreneur)
KEYWORDS: apply for scheme, official portal, myscheme, official link, application link, how to apply

CONTENT:
How to Apply for Recommended Schemes:
ArthNiti assists you in identifying and qualifying for government schemes, but the actual legal application must be filed with the respective government authority or designated banking portal.

Application Links & Actions:
- "View Scheme" Button: Every recommended scheme card includes a direct action button. Clicking this button opens the official central/state government application portal (e.g., kviconline.gov.in for PMEGP, udyamimitra.in for MUDRA, or ministry-specific portals) in a new browser tab.
- Smart MyScheme Fallback: If an individual direct departmental portal link is temporarily deprecated, changed by a ministry, or unavailable, ArthNiti automatically activates a fallback mechanism that redirects you to the relevant search listing on India's official National Government Scheme Portal (MyScheme - `myscheme.gov.in`).
- Notice Banner: The UI informs you if a fallback was used: "The direct scheme page was not available. You will be redirected to MyScheme."

Recommended Next Steps for Entrepreneurs:
1. Print or download your Business Feasibility Report and Financial Plan from ArthNiti.
2. Visit the official scheme portal via the "View Scheme" button.
3. Submit the ArthNiti project report as your detailed project report (DPR) to your local District Industries Centre (DIC) or lending bank branch during application.

USER QUESTIONS THIS CHUNK SHOULD ANSWER:
- How do I apply for a government scheme found on ArthNiti?
- Can I submit my application directly on this website?
- Where does the "View Scheme" button take me?
- What is the MyScheme fallback?

NAVIGATION/ACTION:
On `/businesses/:businessId/government-schemes` → Click "View Scheme" on any scheme card.

RELATED CHUNKS:
- government_schemes_001
- schemes_recommendations_001
- limitations_platform_001
---
