# Category: Website Navigation & Directory

---
CHUNK_ID: nav_overview_001
TITLE: Website Navigation and Sidebar Structure
CATEGORY: navigation
PAGE/MODULE: Global Navigation (Sidebar)
AUTHENTICATION: Public & Role-Based
KEYWORDS: navigation, sidebar, menu, site map, where to find, website links, collapse sidebar

CONTENT:
ArthNiti uses a sleek, collapsible left sidebar as the primary navigation anchor across the entire application:

Sidebar Elements for Logged-Out Guests:
- Brand Logo & Title: Clicking "ArthNiti" returns to the Home page (`/`).
- Home (`/`): Platform landing page and overview.
- Business Directory (`/businesses/details`): Public catalogue of active enterprises.
- Login (`/login`): Access an existing account.
- Sign Up (`/signup`): Create a new user account.
- Language Switcher: Toggle between English, Hindi, and Bengali.

Sidebar Elements for Logged-In Users:
- Home (`/`): Returns to the landing page.
- Dashboard (`/dashboard`): Role-tailored action hub.
- My Businesses (`/businesses`): Portfolio of ventures (visible to users with the "Entrepreneur" role).
- Business Directory (`/businesses/details`): Public enterprise discovery.
- User Profile Card (`/profile`): Displays user name, avatar, and username, leading to the full profile page.
- Log Out Button: Secure session termination.
- Language Switcher: Switch language at any point.
- Collapse / Expand Controls: Use the panel button to collapse the sidebar for full-screen workspace views.

USER QUESTIONS THIS CHUNK SHOULD ANSWER:
- How is the website navigation organized?
- Where can I find the menu on the website?
- Why don't I see "My Businesses" in the sidebar?
- How do I collapse the sidebar to get more screen space?

NAVIGATION/ACTION:
Use the persistent left sidebar on any screen, or click the panel toggle button at top-left.

RELATED CHUNKS:
- languages_001
- nav_home_dashboard_001
- nav_directory_001
---

---
CHUNK_ID: nav_home_dashboard_001
TITLE: Home Page vs Role Dashboard
CATEGORY: navigation
PAGE/MODULE: Home (/) & Dashboard (/dashboard)
AUTHENTICATION: Home is Public; Dashboard requires Authentication
KEYWORDS: home page vs dashboard, role dashboard, dashboard routing, landing page, where to go after login

CONTENT:
Understanding the Distinction Between Home and Dashboard:

1. Home Page (`/`):
   - The public landing page of ArthNiti.
   - Designed for discovery, explaining the platform's vision, hyper-local consulting methodology, institutional consulting benefits, and testimonials.
   - Available to anyone, logged in or out.

2. Role Dashboard (`/dashboard`):
   - The personalized command center for logged-in users.
   - Dynamically adapts its UI depending on your registered role:
     - For Entrepreneurs: Displays quick links to "Manage My Businesses", cards to review feasibility studies, financial plans, and government schemes, plus shortcuts to create your next business.
     - For Buyers: Displays the "Buyer Discovery Hub", with tools to search active businesses, compare enterprise profiles, and contact local producers.
     - For Government: Displays an official workspace notice, allowing profile management and directory access while specialized government tools are finalized.

USER QUESTIONS THIS CHUNK SHOULD ANSWER:
- What is the difference between the Home page and the Dashboard?
- Where do I land after I log in?
- What does the Dashboard look like for an entrepreneur versus a buyer?
- How do I get back to my dashboard from the home page?

NAVIGATION/ACTION:
- Home: Click "Home" in the sidebar (`/`).
- Dashboard: Click "Dashboard" in the sidebar (`/dashboard`).

RELATED CHUNKS:
- nav_overview_001
- overview_002
- nav_buyer_experience_001
---

---
CHUNK_ID: nav_directory_001
TITLE: Business Directory (Search, Filter, and Connect)
CATEGORY: navigation
PAGE/MODULE: Business Directory (/businesses/details)
AUTHENTICATION: Public Browsing; Authentication Required to Contact Owners
KEYWORDS: business directory, search businesses, filter businesses, local enterprises, find suppliers, contact owner

CONTENT:
The Business Directory (`/businesses/details`) is a public repository showcasing active micro-enterprises, small producers, and rural businesses registered across ArthNiti.

Key Features & Capabilities:
1. Advanced Multi-Parameter Search:
   - Search by Business Name or Keyword.
   - Filter by Business Category (e.g., Agro Processing, Dairy, Retail, Handicrafts).
   - Filter by Geographic Location: Village, City, District, State, Country, or Postal Pincode.
2. Comprehensive Business Cards:
   - Displays enterprise name, category tag, location, margin capital scale, and operational description.
   - Includes business image galleries showcasing facilities, goods, or storefronts.
3. Owner Connection & Contact Modal:
   - Clicking "View details" opens the full business modal.
   - If logged in, you can view the business owner's verified email address, direct phone number, and WhatsApp link, or click "Visit Profile" to view their public entrepreneur page (`/profile/:userId`).
   - If logged out, contact details are protected with a sign-in prompt to prevent spam.

USER QUESTIONS THIS CHUNK SHOULD ANSWER:
- Where can I find other businesses on the website?
- How do I search for businesses in my district or state?
- Can I filter businesses by category?
- How do I contact a business owner from the directory?

NAVIGATION/ACTION:
Click "Business Directory" in the left sidebar or navigate directly to `/businesses/details`.

RELATED CHUNKS:
- account_public_profile_001
- nav_buyer_experience_001
- onboarding_002
---

---
CHUNK_ID: nav_workspace_routes_001
TITLE: Direct Routes and URLs Inside the Business Workspace
CATEGORY: navigation
PAGE/MODULE: Business Workspace Routes
AUTHENTICATION: Required (Role: Entrepreneur)
KEYWORDS: workspace routes, urls, direct links, page paths, analysis route, financial route, schemes route

CONTENT:
For rapid navigation, here is the complete URL routing scheme inside any business workspace (where `:businessId` represents your specific business identifier, e.g., `42`):

Core Workspace Modules:
- Main Business Workspace: `/businesses/:businessId` (Houses the AI Business Assistant and quick module links)
- Business Feasibility Analysis: `/businesses/:businessId/analysis`
- Financial Analysis & Planning: `/businesses/:businessId/financial-analysis`
- Government Schemes Recommender: `/businesses/:businessId/government-schemes`

Individual Deep-Dive Evidence Submodules (under Business Analysis):
- Population Demographics: `/businesses/:businessId/analysis/population`
- Competitor Mapping & Density: `/businesses/:businessId/analysis/competitors`
- Mandi Commodity Market Prices: `/businesses/:businessId/analysis/market-prices`
- Supply Chain & Infrastructure: `/businesses/:businessId/analysis/supply-chain`
- Transportation & Logistics OPEX: `/businesses/:businessId/analysis/transportation`
- Seasonality & Weather Cycles: `/businesses/:businessId/analysis/seasonality`

All sub-pages feature a top "Back to Workspace" or "Back to Analysis" navigation button for seamless transitions.

USER QUESTIONS THIS CHUNK SHOULD ANSWER:
- What are the direct links to each feature in my business workspace?
- Where do I find the population analysis page URL?
- How do I return to the business workspace from an analysis page?
- What is the URL for the financial analysis module?

NAVIGATION/ACTION:
Navigate via buttons inside `/businesses/:businessId` or click "Back to Workspace" from any sub-page.

RELATED CHUNKS:
- business_workspace_001
- business_analysis_001
- financial_analysis_001
- government_schemes_001
---

---
CHUNK_ID: nav_buyer_experience_001
TITLE: Buyer Navigation and Operational Workflow
CATEGORY: navigation
PAGE/MODULE: Buyer Dashboard (/dashboard) & Directory (/businesses/details)
AUTHENTICATION: Required (Role: Buyer)
KEYWORDS: buyer workflow, buyer navigation, buyer role, find local suppliers, sourcing products

CONTENT:
Users who register with the "Buyer" role enjoy an experience tailored for commercial discovery and local procurement:

The Buyer Workflow:
1. Logging In: Upon signing in, buyers land on the "Buyer Discovery Hub" on the Dashboard (`/dashboard`).
2. Discover Local Suppliers: The primary action button "Browse Business Directory" directs buyers to `/businesses/details`.
3. Filter & Shortlist: Buyers apply multi-faceted filters (e.g., Category: "Agro Processing", State: "Uttar Pradesh", District: "Varanasi") to locate verified regional suppliers.
4. Review Enterprise Credentials: Click "View details" to inspect product descriptions, business scale, location coordinates, and storefront imagery.
5. Initiate Direct Contact: Access authenticated owner phone numbers, emails, and direct WhatsApp links to negotiate bulk purchases, supply contracts, or retail orders.
6. Profile Maintenance: Buyers maintain their personal and company contact details under `/profile` so sellers can recognize and reply to them.

USER QUESTIONS THIS CHUNK SHOULD ANSWER:
- How does a Buyer use the platform?
- Can a Buyer browse and filter local suppliers?
- Where do Buyers see business contact numbers?
- Can a Buyer generate feasibility reports?

NAVIGATION/ACTION:
As a Buyer: Log in → Go to `/dashboard` → Click "Browse Business Directory" (`/businesses/details`).

RELATED CHUNKS:
- overview_002
- nav_directory_001
- account_public_profile_001
---
