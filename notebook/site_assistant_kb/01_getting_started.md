# Category: Getting Started

---
CHUNK_ID: overview_001
TITLE: What is ArthNiti (Finance Assistant)
CATEGORY: getting_started
PAGE/MODULE: Home Page (/)
AUTHENTICATION: Not Required
KEYWORDS: what is arthniti, what is finance assistant, platform overview, purpose, rural business, semi-urban entrepreneur, business advisory, financial structuring

CONTENT:
ArthNiti (also known as Finance Assistant) is an AI-powered hyper-local business advisory and financial structuring platform specifically engineered for rural and semi-urban micro-entrepreneurs. The platform bridges the gap between grassroots entrepreneurs and institutional-grade business consulting.

Instead of generic business advice, ArthNiti performs hyper-local feasibility studies based on real location data, local demographics, competitor density, market pricing from mandis, supply chain infrastructure, and logistics costs. It translates these physical insights into viable financial plans (calculating project costs, required loans, and cash-flow projections) and automatically matches entrepreneurs with applicable government welfare and development schemes.

USER QUESTIONS THIS CHUNK SHOULD ANSWER:
- What is ArthNiti?
- What is Finance Assistant?
- What is the purpose of this website?
- Who is this platform designed for?
- How does the platform help rural and semi-urban entrepreneurs?

NAVIGATION/ACTION:
Open the Home page at `/` to explore platform capabilities.

RELATED CHUNKS:
- overview_002
- onboarding_001
- business_analysis_001
---

---
CHUNK_ID: overview_002
TITLE: Platform User Roles (Entrepreneur, Buyer, Government)
CATEGORY: getting_started
PAGE/MODULE: Signup (/signup), Role Dashboard (/dashboard)
AUTHENTICATION: Required for Dashboard
KEYWORDS: user roles, account types, entrepreneur role, buyer role, government role, permissions

CONTENT:
ArthNiti supports three distinct user roles, chosen during account registration:

1. Entrepreneur: The primary user role. Entrepreneurs can create and manage their business ventures, generate comprehensive hyper-local business feasibility studies, run financial viability projections, get matched with government support schemes, and chat with their dedicated AI Business Assistant.
2. Buyer: Designed for individuals or organizations seeking local suppliers and enterprises. Buyers can search the active Business Directory, view business listings and operational details, compare local enterprises, and connect with business owners.
3. Government: Designed for government representatives and development officers. While this dedicated workspace is currently being prepared, government accounts can access their user profile and browse the public Business Directory.

USER QUESTIONS THIS CHUNK SHOULD ANSWER:
- What roles are available on the platform?
- What is the difference between an Entrepreneur, Buyer, and Government account?
- Can a Buyer create a business?
- Which role should I choose when signing up?

NAVIGATION/ACTION:
Select your role on the Signup page (`/signup`) or view role-tailored options on the Dashboard (`/dashboard`).

RELATED CHUNKS:
- account_signup_001
- nav_home_dashboard_001
- limitations_government_role_001
---

---
CHUNK_ID: onboarding_001
TITLE: New User Journey and Recommended Workflow
CATEGORY: getting_started
PAGE/MODULE: Workflow (Home → Signup → Dashboard → My Businesses → Business Workspace)
AUTHENTICATION: Required after initial exploration
KEYWORDS: onboarding journey, how to start, first steps, workflow, user steps, recommended order

CONTENT:
For new entrepreneurs joining ArthNiti, the platform provides a clear, sequential decision-making workflow:

1. Step 1: Sign up and create an account with the "Entrepreneur" role at `/signup`, completing email OTP verification.
2. Step 2: Access your Dashboard (`/dashboard`) and proceed to "My Businesses" (`/businesses`).
3. Step 3: Create your business profile by entering the business name, category, location (village, district, state), and available margin capital.
4. Step 4: Open your Business Workspace (`/businesses/:businessId`).
5. Step 5: Run the Business Feasibility Analysis first (`/businesses/:businessId/analysis`). This generates empirical local market evidence (population, competitors, market prices, supply chain, transportation, seasonality).
6. Step 6: Run Financial Analysis (`/businesses/:businessId/financial-analysis`), which uses your feasibility report data to project project costs, loan sizing, EMI, and cash flows.
7. Step 7: Explore Government Schemes (`/businesses/:businessId/government-schemes`) to discover funding, subsidies, and support matched to your profile.
8. Step 8: Consult your AI Business Assistant inside the workspace for ongoing advisory, image analysis (bills/receipts), and strategic decisions.

USER QUESTIONS THIS CHUNK SHOULD ANSWER:
- How do I get started as a new user?
- What is the recommended sequence of steps on the platform?
- What should I do after creating an account?
- What is the order of analysis to run?

NAVIGATION/ACTION:
Sign up at `/signup` → Go to `/dashboard` → Open `/businesses` → Create Business → Open Workspace.

RELATED CHUNKS:
- overview_001
- business_create_001
- business_workspace_001
- business_analysis_001
---

---
CHUNK_ID: onboarding_002
TITLE: Guest Access vs Authenticated User Access
CATEGORY: getting_started
PAGE/MODULE: Navigation & Access Control
AUTHENTICATION: Varies by action
KEYWORDS: guest access, without account, public features, do i need an account, login required

CONTENT:
Visitors can explore several features without logging in, but deep business planning requires an account:

What Guests (Logged-Out Users) Can Access:
- Home Page (`/`): Learn about platform features, methodology, and capabilities.
- Business Directory (`/businesses/details`): Search active businesses, filter by location or category, and view public business descriptions.
- Language Switcher: Toggle between English, Hindi, and Bengali at any time.

What Requires an Account and Login:
- Creating or editing business profiles (`/businesses`).
- Generating AI Feasibility Reports and accessing deep demographic/competitor data (`/businesses/:businessId/analysis`).
- Calculating financial projections, EMI, and loan scenarios (`/businesses/:businessId/financial-analysis`).
- Generating personalized government scheme recommendations (`/businesses/:businessId/government-schemes`).
- Using the AI Business Assistant chat and uploading documents/photos (`/businesses/:businessId`).
- Viewing owner contact details (phone, email, WhatsApp) on the Business Directory.

USER QUESTIONS THIS CHUNK SHOULD ANSWER:
- Can I use the platform without creating an account?
- What can I do without logging in?
- Do I need an account to view business analysis?
- Why do I need to log in to see owner contact details?

NAVIGATION/ACTION:
Explore `/` or `/businesses/details` freely as a guest, or click "Login" (`/login`) / "Sign Up" (`/signup`) in the sidebar for full features.

RELATED CHUNKS:
- account_login_001
- account_signup_001
- nav_directory_001
---

---
CHUNK_ID: languages_001
TITLE: Multilingual Support (English, Hindi, Bengali)
CATEGORY: getting_started
PAGE/MODULE: Global (Sidebar / All Pages)
AUTHENTICATION: Not Required
KEYWORDS: language, switch language, hindi, bengali, english, bhasha, translate, multilingual

CONTENT:
ArthNiti provides native multilingual support across the entire platform in three major languages:
- English
- Hindi (हिंदी)
- Bengali (বাংলা)

How Language Switching Works:
1. Locate the Language selector in the left sidebar menu (marked with a Globe icon).
2. Click on your preferred language: "English", "Hindi (हिंदी)", or "Bengali (বাংলা)".
3. The interface immediately updates UI labels, navigation buttons, forms, and descriptions.
4. AI reports and advisory features (Feasibility Analysis, Financial Reports, Government Schemes, and AI Business Assistant chats) automatically adapt their outputs and translations to your selected language.

USER QUESTIONS THIS CHUNK SHOULD ANSWER:
- What languages does the platform support?
- How do I change the language to Hindi or Bengali?
- Where is the language switcher located?
- Does the AI assistant understand and respond in Hindi and Bengali?

NAVIGATION/ACTION:
Look at the bottom section of the left sidebar → Find the "Language" box → Click your preferred language.

RELATED CHUNKS:
- nav_overview_001
- business_assistant_overview_001
---
