# Category: Frequently Asked Questions (FAQ)

---
CHUNK_ID: faq_general_001
TITLE: General FAQ: What is ArthNiti and Who is it Built For?
CATEGORY: faq
PAGE/MODULE: Global FAQ
AUTHENTICATION: Not Required
KEYWORDS: faq, who is behind arthniti, is it free, what does it do, target audience, micro enterprise

CONTENT:
Q: What is ArthNiti (Finance Assistant)?
A: ArthNiti is an advanced digital consulting platform that democratizes institutional-grade business advisory and financial planning for rural and semi-urban entrepreneurs in India.

Q: Who is it built for?
A: It is built for micro-enterprises, small rural producers, women entrepreneurs, farmers starting value-add businesses, self-help groups (SHGs), and traders seeking data-driven guidance on market feasibility, bank loan sizing, and government subsidies.

Q: In what languages can I use the platform?
A: The platform fully supports English, Hindi (हिंदी), and Bengali (বাংলা), with language-switchable UI elements and native AI translation.

USER QUESTIONS THIS CHUNK SHOULD ANSWER:
- What is ArthNiti and who made it?
- Is this service intended for rural businesses?
- Can I use it in Hindi or Bengali?
- What problem does ArthNiti solve?

NAVIGATION/ACTION:
Visit the Home page (`/`) to learn more about the platform's vision.

RELATED CHUNKS:
- overview_001
- languages_001
---

---
CHUNK_ID: faq_businesses_001
TITLE: FAQ: Creating Multiple Businesses and Category Rules
CATEGORY: faq
PAGE/MODULE: My Businesses (/businesses)
AUTHENTICATION: Required (Role: Entrepreneur)
KEYWORDS: how many businesses, multiple businesses, limits, change category, add second business

CONTENT:
Q: How many businesses can I create on my account?
A: There is no strict artificial limit. An entrepreneur can register and maintain multiple separate business ventures (e.g., an agro-processing unit, a dairy cooperative, and a retail store) under one login account.

Q: Can I change my business category after creating it?
A: No. As per system design, the business category is immutable once created because all underlying geospatial models, competitor tags, and commodity rate feeds are keyed to that specific category. If you want to start in a new category, simply click "+ Create Business" to create a fresh business profile.

Q: Can I manage businesses in different villages or states?
A: Yes. Each business profile maintains its own individual location, coordinates, margin capital, and distinct workspace.

USER QUESTIONS THIS CHUNK SHOULD ANSWER:
- Can I create more than one business on one account?
- Is there a fee or limit on adding businesses?
- Can I change my business category?
- How do I set up a second venture?

NAVIGATION/ACTION:
Go to `/businesses` → Click "+ Create Business" to add additional ventures.

RELATED CHUNKS:
- business_overview_001
- business_create_001
- business_category_rule_001
---

---
CHUNK_ID: faq_analysis_time_001
TITLE: FAQ: Why Does Business Analysis Take 5 to 10 Minutes?
CATEGORY: faq
PAGE/MODULE: Business Analysis (/businesses/:businessId/analysis)
AUTHENTICATION: Required (Role: Entrepreneur)
KEYWORDS: why 5 to 10 minutes, analysis time, slow analysis, long running notice, generation delay

CONTENT:
Q: Why does the Business Feasibility Analysis take 5 to 10 minutes to generate?
A: Unlike generic chatbots that produce generic text immediately, ArthNiti executes a multi-stage empirical research pipeline:
1. Geospatial Querying: It queries spatial OpenStreetMap databases across your selected radius to locate and count real commercial competitors.
2. Demographic Aggregation: It calculates local population densities and household counts.
3. Market Mandi Integration: It queries agricultural price databases for current commodity rates.
4. Logistics & Route Simulation: It models real road network routes, travel times, vehicle suitability, and freight fuel expenditures.
5. Multi-Agent Synthesis: The AI orchestrator compiles these distinct datasets into an executive feasibility report.

Q: Do I have to wait on the page while it generates?
A: No! The process runs as an asynchronous background worker. You can safely close the modal, navigate to other pages, work on a different business, or close your browser. When you return to the page, your completed report is stored and displayed.

USER QUESTIONS THIS CHUNK SHOULD ANSWER:
- Why does business analysis take so long?
- Is the website frozen while generating analysis?
- Can I close my browser while the feasibility report is running?
- What happens in the background during the 5–10 minutes?

NAVIGATION/ACTION:
Start analysis on `/businesses/:businessId/analysis` → You can safely click "Close & continue in background".

RELATED CHUNKS:
- business_analysis_002
- troubleshoot_analysis_stuck_001
---

---
CHUNK_ID: faq_financing_001
TITLE: FAQ: Does ArthNiti Directly Lend Money or Approve Schemes?
CATEGORY: faq
PAGE/MODULE: Financial Analysis & Government Schemes
AUTHENTICATION: Required
KEYWORDS: does arthniti give loans, direct lending, loan approval, scheme approval, nbfc, bank sanction

CONTENT:
Q: Does ArthNiti directly lend money or provide cash loans?
A: No. ArthNiti is a business advisory, feasibility intelligence, and financial structuring software platform. It is not a bank, non-banking financial company (NBFC), or money lender.

Q: Does receiving a 95% Match Score mean my government scheme is approved?
A: No. A Match Score indicates that your business profile and demographic credentials satisfy the formal eligibility criteria of the scheme. Actual scheme sanction, subsidy disbursement, and loan approvals are executed exclusively by government departments (e.g., KVIC, DIC) and partner commercial banks upon reviewing your physical application and documents.

Q: How do I use ArthNiti to get a loan?
A: Take your generated Feasibility Report and Financial Plan to your local bank branch or DIC officer. These reports serve as a comprehensive Detailed Project Report (DPR), giving bank loan officers the verifiable evidence and DSCR numbers they need to process your loan application faster.

USER QUESTIONS THIS CHUNK SHOULD ANSWER:
- Does ArthNiti disburse loans directly?
- Does a high match score guarantee my scheme will be approved?
- Can I withdraw subsidy money directly from this website?
- How does ArthNiti help me get a bank loan?

NAVIGATION/ACTION:
Download your report from `/businesses/:businessId/analysis` and take it to your lending bank or DIC office.

RELATED CHUNKS:
- financial_analysis_001
- government_schemes_001
- limitations_platform_001
---

---
CHUNK_ID: faq_data_privacy_001
TITLE: FAQ: Data Privacy, Security, and Business Confidentiality
CATEGORY: faq
PAGE/MODULE: Platform Security & Privacy
AUTHENTICATION: Not Required
KEYWORDS: data privacy, security, confidentiality, is my data safe, who can see my business

CONTENT:
Q: Is my business and financial information kept private?
A: Yes. Your business workspaces, feasibility reports, financial plans, chat sessions, and margin capital are private to your authenticated user account. Other entrepreneurs cannot view or edit your business workspace.

Q: What information is visible in the public Business Directory?
A: The Business Directory showcases basic operational business cards (business name, category, general location, and business description) so that potential buyers, clients, and partners can discover your enterprise. Your detailed internal financial models, bank loan calculations, and AI assistant chat history are NEVER shared publicly.

Q: Are owner phone numbers visible to everyone?
A: Owner phone numbers and emails on the Business Directory are hidden from logged-out guests to prevent web scrapers and telemarketing spam. Only logged-in, authenticated users can view owner contact buttons.

USER QUESTIONS THIS CHUNK SHOULD ANSWER:
- Is my business data private?
- Who can see my financial analysis?
- What details are shown publicly in the Business Directory?
- Can other users read my AI assistant chats?

NAVIGATION/ACTION:
Manage your public listings via `/businesses/details` and your private workspace at `/businesses/:businessId`.

RELATED CHUNKS:
- nav_directory_001
- account_public_profile_001
- business_workspace_001
---
