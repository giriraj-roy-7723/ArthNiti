# ArthNiti Site Assistant Master Knowledge Base (All 60 Chunks)
# Purpose: RAG Vector Ingestion for Onboarding & Navigation Chatbot
# Format: Each chunk is delimited by standard YAML-like frontmatter and semantic blocks

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

---
CHUNK_ID: account_signup_001
TITLE: How to Create an Account and Complete Signup
CATEGORY: account
PAGE/MODULE: Signup (/signup)
AUTHENTICATION: Not Required
KEYWORDS: signup, create account, register, new user registration, otp verification, email verification

CONTENT:
To create an account on ArthNiti:

1. Open the left sidebar and click "Sign Up" or navigate to `/signup`.
2. Fill out Section 1 (Personal Information): First Name, Last Name, Email Address, Password, and Confirm Password. Passwords can be toggled visible using the eye icon.
3. Complete Email OTP Verification:
   - Click the button to send an OTP to your email address.
   - Enter the 6-digit verification code received in your inbox.
   - Once verified, a green confirmation badge appears.
4. Fill out Section 2 (Account Type): Choose your role—"Entrepreneur" (to start and manage businesses), "Buyer" (to discover suppliers), or "Government" (official role).
5. Fill out Section 3 (Contact Information): Country code (defaults to +91 for India) and mobile phone number.
6. Fill out Section 4 (Address Information): Address line, Village, District, City, State, Country (defaults to India), and Pincode. (Dropdown selections for Country, State, and City dynamically filter available administrative regions).
7. If registering as a Government Official, supply your Designation, Agency Type (e.g., State Channelising Agency - SCA), and Agency Name.
8. Click "Create Account". Once processed, your account is established and you can log in.

USER QUESTIONS THIS CHUNK SHOULD ANSWER:
- How do I sign up on ArthNiti?
- What details are needed to register an account?
- Why do I need email OTP verification during signup?
- What should I do if I am an entrepreneur versus a buyer?

NAVIGATION/ACTION:
Navigate to the left sidebar → Click "Sign Up" (`/signup`).

RELATED CHUNKS:
- overview_002
- account_login_001
- troubleshoot_otp_002
---

---
CHUNK_ID: account_login_001
TITLE: How to Log In and Log Out
CATEGORY: account
PAGE/MODULE: Login (/login), Sidebar
AUTHENTICATION: Not Required to Login; Required to Logout
KEYWORDS: login, sign in, log in, sign out, log out, session, credentials

CONTENT:
Logging In:
1. Open the left sidebar and click "Login" or go to `/login`.
2. Enter your registered Email Address or Username.
3. Enter your Password. You can click the eye icon to verify that your password was typed correctly.
4. Click "Sign In". Upon successful authentication, your security token is stored securely, and you are automatically redirected to your personal Dashboard (`/dashboard`).

Logging Out:
1. In the left sidebar, look at the bottom user profile card.
2. Click the red "Log Out" button with the exit door icon.
3. Your session is terminated securely, your local storage credentials are removed, and you are redirected to the Home page (`/`).

USER QUESTIONS THIS CHUNK SHOULD ANSWER:
- How do I log in to my account?
- Can I log in using either my email or username?
- How do I log out of my account?
- Where does the site take me after logging in?

NAVIGATION/ACTION:
To Log In: Sidebar → "Login" (`/login`).
To Log Out: Sidebar bottom → Red "Log Out" button.

RELATED CHUNKS:
- account_signup_001
- troubleshoot_login_001
- nav_home_dashboard_001
---

---
CHUNK_ID: account_profile_001
TITLE: Viewing Your User Profile
CATEGORY: account
PAGE/MODULE: Profile (/profile)
AUTHENTICATION: Required
KEYWORDS: profile, view profile, account details, user information, contact details, address

CONTENT:
Logged-in users can inspect their full personal and organizational details on the Profile page:

How to Access:
- Click your user card at the bottom of the left sidebar, or navigate directly to `/profile`.

What is Displayed on Your Profile:
- Identity Header: Profile picture, full name, username, role badge (e.g., Entrepreneur, Buyer, Government), user ID, and joined date.
- Personal Information: First name, last name, username, and role.
- Contact Information: Email address and verified mobile phone number.
- Address Information: Street address, village, city, district, state, country, and postal pincode.
- Role-Specific Information:
  - For Entrepreneurs: Overview of businesses created.
  - For Government Officials: Agency name, agency type (e.g., SCA), and official designation.

USER QUESTIONS THIS CHUNK SHOULD ANSWER:
- Where can I view my profile?
- What information is saved in my user profile?
- How do I check my registered phone number and address?

NAVIGATION/ACTION:
Click the user card at the bottom of the left sidebar → Opens `/profile`.

RELATED CHUNKS:
- account_profile_002
- account_public_profile_001
---

---
CHUNK_ID: account_profile_002
TITLE: Editing Profile Information and Uploading an Avatar
CATEGORY: account
PAGE/MODULE: Profile (/profile)
AUTHENTICATION: Required
KEYWORDS: edit profile, change phone number, update address, upload photo, change avatar, profile picture

CONTENT:
You can update your personal contact info, location, and avatar directly from the Profile page:

Editing Details:
1. Navigate to `/profile`.
2. Click the "Edit Profile" button (pencil icon).
3. The info fields turn into editable input boxes. You can update your phone number, street address, village, city, district, state, or postal pincode.
4. Click "Save Changes". Your profile is updated immediately across the platform.

Uploading a Profile Picture:
1. On the Profile page (`/profile`), locate the profile photo circle at the top of the page.
2. Click the camera or edit badge on your avatar.
3. Select an image file (JPG, PNG, WebP) from your computer or phone.
4. The image is uploaded securely to dedicated cloud storage (Supabase bucket) and linked to your account. Your new avatar will display in the sidebar and on your public business listings.

USER QUESTIONS THIS CHUNK SHOULD ANSWER:
- How do I change my profile information?
- Can I update my phone number or address after signup?
- How do I upload or change my profile picture?

NAVIGATION/ACTION:
Sidebar bottom user card → `/profile` → Click "Edit Profile" or the camera icon on the avatar.

RELATED CHUNKS:
- account_profile_001
- business_location_001
---

---
CHUNK_ID: account_public_profile_001
TITLE: Public Entrepreneur Profiles and Connecting with Owners
CATEGORY: account
PAGE/MODULE: Public Profile (/profile/:userId)
AUTHENTICATION: Viewing profile is Public; Contact details require Authentication
KEYWORDS: public profile, view entrepreneur, contact owner, entrepreneur profile, user profile id

CONTENT:
Every entrepreneur on ArthNiti has a public profile located at `/profile/:userId`. This page enables buyers, partners, and other entrepreneurs to learn about the person behind a business.

Features of the Public Profile Page:
- Entrepreneur Overview: Full name, location (city, district, state), and role badge.
- Verified Contact Actions: If logged in, users can view direct contact channels: email address, telephone call button, and direct WhatsApp messaging link.
- Privacy Guard: If a visitor is not logged in, contact numbers and emails are masked with a prompt: "Sign in to view owner details, visit their profile, and contact them."
- Published Businesses Showcase: Lists all active enterprises registered by this entrepreneur, with direct links to view business details in the Business Directory.

USER QUESTIONS THIS CHUNK SHOULD ANSWER:
- Can other users see my profile?
- What is shown on a public entrepreneur profile (`/profile/:userId`)?
- How can a buyer contact an entrepreneur?
- Why are owner phone numbers hidden when I am logged out?

NAVIGATION/ACTION:
From the Business Directory (`/businesses/details`) → Click "View details" on any business → Click "Visit Profile" to open `/profile/:userId`.

RELATED CHUNKS:
- nav_directory_001
- onboarding_002
---

---
CHUNK_ID: business_overview_001
TITLE: My Businesses Section and Multi-Business Management
CATEGORY: businesses
PAGE/MODULE: My Businesses (/businesses)
AUTHENTICATION: Required (Role: Entrepreneur)
KEYWORDS: my businesses, manage businesses, multiple businesses, business dashboard, enterprise list

CONTENT:
The "My Businesses" page (`/businesses`) is the centralized command center for an entrepreneur. ArthNiti allows an entrepreneur to create, operate, and analyze multiple distinct business ventures under a single account.

Key Features of the "My Businesses" Page:
- Business Portfolio: Displays cards for all businesses registered by the logged-in entrepreneur, showing the business name, category badge, location, margin capital, and creation date.
- Create Business Trigger: Features an intuitive "+ Create Business" button at the top right to launch new venture setups.
- Workspace Launcher: Each business card provides an "Open Workspace" button that directs the entrepreneur into the dedicated, full-featured workspace for that specific business (`/businesses/:businessId`).
- Quick Actions: Allows editing business information or managing status directly from the card.

USER QUESTIONS THIS CHUNK SHOULD ANSWER:
- Where can I see all the businesses I created?
- Can I create and manage more than one business?
- How do I open a business to run analysis?
- Who can access the My Businesses page?

NAVIGATION/ACTION:
Sidebar → Click "My Businesses" (`/businesses`).

RELATED CHUNKS:
- business_create_001
- business_workspace_001
- nav_overview_001
---

---
CHUNK_ID: business_create_001
TITLE: How to Create a New Business
CATEGORY: businesses
PAGE/MODULE: My Businesses (/businesses) → Create Business Modal
AUTHENTICATION: Required (Role: Entrepreneur)
KEYWORDS: create business, add business, new business, start business, register business, business modal

CONTENT:
To create a new business on ArthNiti:

1. Navigate to "My Businesses" (`/businesses`) from the sidebar.
2. Click the "+ Create Business" button. This opens the Create Business Modal.
3. Provide the Required Business Details:
   - Business Name (Required): The name of your enterprise (e.g., "Maa Durga Flour Mill", "Kisan Cold Storage").
   - Category (Required): Select the core industry/sector (e.g., Agro Processing, Dairy, Retail, Manufacturing, Handicrafts, Services). Note: Choose carefully, as category cannot be changed later.
   - Description: A clear summary of what products or services your business offers.
   - Available Margin Capital (Required): The self-financed money you can personally invest upfront in INR (₹).
4. Provide Location Information:
   - Enter Village/Street, City, District, State, Country, and Pincode.
   - You can click "Use Profile Location" to instantly populate these fields with your home address.
   - Pinpoint your location on the interactive Leaflet map to capture exact latitude and longitude coordinates.
5. Click "Create Business". Once created, the business immediately appears in your "My Businesses" list, ready for workspace analysis.

USER QUESTIONS THIS CHUNK SHOULD ANSWER:
- How do I add a new business to my account?
- What information is needed to create a business?
- What is margin capital during business creation?
- Can I copy my home address from my profile?

NAVIGATION/ACTION:
Go to `/businesses` → Click "+ Create Business".

RELATED CHUNKS:
- business_location_001
- business_category_rule_001
- financial_margin_capital_001
---

---
CHUNK_ID: business_location_001
TITLE: Setting Business Location (Interactive Map, Geocoding, Profile Autofill)
CATEGORY: businesses
PAGE/MODULE: Create Business Modal & Edit Business Modal
AUTHENTICATION: Required
KEYWORDS: business location, map picker, coordinates, latitude, longitude, leaflet map, address autofill

CONTENT:
Accurate geographic location is critical on ArthNiti because all hyper-local feasibility analyses (population demographics, competitor mapping, mandi market rates, transportation freight simulations) are computed based on the business's physical coordinates.

ArthNiti provides three flexible ways to set your business location:
1. Interactive Leaflet Map: Click anywhere on the map interface to drop a marker. The system automatically registers the exact latitude and longitude coordinates.
2. Smart Geocoding: As you type your Village, City, District, and State, the built-in geocoding service (OpenStreetMap Nominatim) automatically shifts the map center and adjusts the zoom level to match your locality.
3. Use Profile Location Button: If your business is operating from your residential or registered location, click "Use Profile Location" to instantly populate your address fields and coordinates without manual retyping.

USER QUESTIONS THIS CHUNK SHOULD ANSWER:
- Why does the platform ask for latitude and longitude?
- How do I pick my business location on the map?
- How does the map find my city or village?
- Can I use my saved profile address for my business?

NAVIGATION/ACTION:
Inside the Create Business or Edit Business modal → Use the text fields, click "Use Profile Location", or click directly on the interactive Leaflet map.

RELATED CHUNKS:
- business_create_001
- business_analysis_002
- analysis_transportation_001
---

---
CHUNK_ID: business_category_rule_001
TITLE: Immutability of Business Category
CATEGORY: businesses
PAGE/MODULE: My Businesses (/businesses) & Business Workspace
AUTHENTICATION: Required
KEYWORDS: change category, edit category, immutable category, category locked, change business type

CONTENT:
Important Platform Rule:
Once a business profile is created, its "Category" (such as Agro Processing, Dairy, Retail, Textile, or Manufacturing) CANNOT be changed or edited.

Why is the Category Immutable?
The business category serves as the foundational key for generating:
- The entire hyper-local competitor search parameters.
- Mandi commodity market rate indexing.
- Supply chain processing and cold storage scoring.
- Sector-specific financial benchmarking and debt capacity ratios.
- Targeted government welfare scheme matching.

What to Do if You Want to Pivot or Change Categories:
If you decide to operate in an entirely different sector or category, you should simply create a new business profile in "My Businesses" with your new desired category. You can retain, deactivate, or delete your previous business profile.

USER QUESTIONS THIS CHUNK SHOULD ANSWER:
- Can I change my business category after creating it?
- Why is the business category field locked or disabled during edit?
- What should I do if I selected the wrong category?
- How do I switch my business from retail to manufacturing?

NAVIGATION/ACTION:
If you need a different category: Go to `/businesses` → Click "+ Create Business" and select the new category.

RELATED CHUNKS:
- business_create_001
- business_edit_001
---

---
CHUNK_ID: business_edit_001
TITLE: Editing Existing Business Details
CATEGORY: businesses
PAGE/MODULE: My Businesses (/businesses) → Edit Business Modal
AUTHENTICATION: Required (Role: Entrepreneur)
KEYWORDS: edit business, update business, change business name, update margin capital, change location

CONTENT:
Entrepreneurs can update their business details whenever operational parameters change:

How to Edit:
1. Go to "My Businesses" (`/businesses`).
2. Find the business card you wish to update and click the edit/pencil icon or menu option.
3. The Edit Business Modal opens.

What Fields You Can Update:
- Business Name: Reflect any renaming of your enterprise.
- Description: Refine the explanation of products, services, or business scale.
- Available Margin Capital: Update your own capital contribution if your savings or funds increase or decrease.
- Address & Location: Adjust street, village, city, district, state, pincode, or re-pin the Leaflet map marker.

Important Note on Stale Analysis:
If you update significant parameters (such as location or margin capital) after running Business Analysis or Financial Analysis, the platform flags the existing reports with a warning: "Business details have changed. Needs regeneration." You can then easily regenerate your analyses with the updated values.

USER QUESTIONS THIS CHUNK SHOULD ANSWER:
- How do I edit my business name or description?
- Can I change my margin capital after creating a business?
- What happens to my feasibility analysis if I change my business address?
- Where is the edit button for a business?

NAVIGATION/ACTION:
Sidebar → "My Businesses" (`/businesses`) → Click the edit icon on the target business card.

RELATED CHUNKS:
- business_create_001
- business_category_rule_001
- business_analysis_003
---

---
CHUNK_ID: business_workspace_001
TITLE: Navigating the Business Workspace
CATEGORY: businesses
PAGE/MODULE: Business Workspace (/businesses/:businessId)
AUTHENTICATION: Required (Role: Entrepreneur)
KEYWORDS: business workspace, workspace, business id, modules, workspace navigation, chat workspace

CONTENT:
The Business Workspace (`/businesses/:businessId`) is the dedicated operational hub for an individual business enterprise. Everything related to that venture is integrated into this single, unified screen.

What the Workspace Contains:
1. Workspace Header: Displays the business name, unique Business ID, and active status.
2. Direct Module Access Buttons (Collapsible):
   - Business Analysis (`/businesses/:businessId/analysis`): Launches feasibility reports, population, competitor, and supply chain insights.
   - Financial Analysis (`/businesses/:businessId/financial-analysis`): Launches cash flow, loan requirements, and financial scenario models.
   - Government Schemes (`/businesses/:businessId/government-schemes`): Launches scheme recommendation engine and eligibility profiler.
3. The AI Business Assistant: The central interactive feature of the workspace, featuring a chat interface where entrepreneurs can converse with their AI advisor, upload photos (bills, products, facilities), and manage persistent chat sessions.

USER QUESTIONS THIS CHUNK SHOULD ANSWER:
- What is the Business Workspace?
- How do I access the Business Workspace?
- What tools are available inside a business workspace?
- Where do I find the AI Business Assistant?

NAVIGATION/ACTION:
Go to `/businesses` → Click "Open Workspace" on any business card → Navigates to `/businesses/:businessId`.

RELATED CHUNKS:
- business_overview_001
- business_analysis_001
- financial_analysis_001
- government_schemes_001
- business_assistant_overview_001
---

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

---
CHUNK_ID: assistant_comparison_001
TITLE: Site Assistant vs Business AI Assistant (Key Differences & Security)
CATEGORY: business_assistant
PAGE/MODULE: Global Architecture & Platform Boundary
AUTHENTICATION: Site Assistant is Public/Global; Business Assistant requires Auth + Business Context
KEYWORDS: site assistant vs business assistant, difference between assistants, which assistant to use, two chatbots

CONTENT:
ArthNiti features two distinctly different AI assistants designed for separate purposes. It is vital to understand their distinct roles:

1. The Site Assistant (Platform Onboarding & Navigation Guide):
   - Purpose: Helps visitors and registered users understand how to use ArthNiti, navigate pages, complete onboarding, learn what each feature does, understand prerequisites, and resolve platform issues.
   - Availability: Available globally across the platform.
   - Data Access: Contains general platform knowledge, workflows, navigation paths, and educational guidance. It does NOT have access to an entrepreneur's private business chat sessions or private ledger records.
   - Limitation: It does NOT perform live deep feasibility calculations or financial simulations directly in chat. It directs users to the proper workspace tools.

2. The Business AI Assistant (Dedicated In-Workspace Advisory Agent):
   - Purpose: Acts as an executive business consultant, financial planner, and strategist for a specific business venture.
   - Availability: Exclusively located inside an entrepreneur's individual Business Workspace (`/businesses/:businessId`).
   - Data Access: Deeply integrated with that specific business's database records, feasibility findings, mandi rates, financial statements, and matched government schemes.
   - Multimodal: Can accept and visually inspect photos of equipment, receipts, supplier invoices, and retail locations.
   - Tool Execution: Can trigger report generations and update business state upon explicit user confirmation.

USER QUESTIONS THIS CHUNK SHOULD ANSWER:
- What is the difference between the Site Assistant and the Business Assistant?
- Why are there two AI chatbots on the website?
- Can the Site Assistant see my business data or financial figures?
- Which assistant should I ask about my specific business questions?

NAVIGATION/ACTION:
- For site questions, navigation, and feature guidance: Ask the Site Assistant.
- For business strategy, financial advice, or document analysis: Go to `/businesses/:businessId` and talk to the Business AI Assistant.

RELATED CHUNKS:
- business_assistant_overview_001
- limitations_site_assistant_001
- business_workspace_001
---

---
CHUNK_ID: business_assistant_overview_001
TITLE: The AI Business Assistant in the Workspace
CATEGORY: business_assistant
PAGE/MODULE: Business Workspace (/businesses/:businessId)
AUTHENTICATION: Required (Role: Entrepreneur)
KEYWORDS: business assistant, ai advisor, workspace chat, enterprise consultant, business chat

CONTENT:
The AI Business Assistant is an expert advisory agent embedded directly within each Business Workspace (`/businesses/:businessId`). It serves as an on-demand business consultant for rural and semi-urban entrepreneurs.

Core Capabilities:
- Hyper-Local Context Grounding: The assistant knows your business name, category, village/city, margin capital, and exact coordinates without you needing to repeat them.
- Synthesis of Analysis: When you ask questions about market feasibility, competitor saturation, or break-even timelines, it references your completed Feasibility and Financial reports.
- Strategy & Planning: Helps entrepreneurs design marketing tactics, negotiate with raw material suppliers, select optimal loan programs, and prepare for bank interviews.
- Multilingual Natural Dialogue: Operates seamlessly in English, Hindi, and Bengali, translating concepts into culturally relevant business terms.

USER QUESTIONS THIS CHUNK SHOULD ANSWER:
- What is the AI Business Assistant?
- Where do I access the Business AI Assistant?
- What can I ask the Business Assistant?
- Does the assistant know my business location and numbers?

NAVIGATION/ACTION:
Go to `/businesses` → Click "Open Workspace" on your business (`/businesses/:businessId`) → The AI Business Assistant chat occupies the primary center panel.

RELATED CHUNKS:
- assistant_comparison_001
- business_assistant_features_001
- business_assistant_actions_001
---

---
CHUNK_ID: business_assistant_features_001
TITLE: Multimodal Capabilities (Analyzing Images, Invoices, Receipts)
CATEGORY: business_assistant
PAGE/MODULE: Business Workspace (/businesses/:businessId) → AI Chat
AUTHENTICATION: Required (Role: Entrepreneur)
KEYWORDS: upload image, analyze bill, receipt analysis, photo upload, equipment photo, multimodal vision

CONTENT:
The Business AI Assistant is equipped with a multimodal vision reasoning engine that allows entrepreneurs to upload and discuss real-world visual evidence:

Supported Use Cases:
1. Supplier Invoices & Mandi Receipts: Upload a photo of a bill from an equipment vendor or agricultural mandi. The assistant reads product names, item quantities, unit rates, and taxes, evaluating whether you are getting a fair market deal.
2. Equipment & Machinery Specifications: Upload photos of machine nameplates, tractor attachments, or processing machinery to evaluate suitability and capacity.
3. Retail Shop Fronts & Commercial Sites: Upload photos of prospective shop locations or plots. The assistant assesses visibility, signage potential, customer footfall access, and space utilization.
4. Business Documents & Certificates: Upload trade licenses, MSME certificates, or scheme sanction letters to understand next administrative steps.

How to Upload:
- In the chat input box at the bottom of the workspace, click the paperclip / image attachment icon.
- Select your image file (JPEG, PNG, WebP). A thumbnail preview appears.
- Add your question (or use the default "Please analyze this image") and click Send.
- The image is securely uploaded to cloud storage (Supabase bucket) and processed by the vision reasoning node.

USER QUESTIONS THIS CHUNK SHOULD ANSWER:
- Can I upload images or photos to the AI assistant?
- How do I send a bill or invoice to the assistant?
- Can the assistant read handwritten receipts or mandi slips?
- How does the assistant help me with equipment photos?

NAVIGATION/ACTION:
Inside `/businesses/:businessId` → In the message input bar, click the attachment icon → Choose an image file → Click Send.

RELATED CHUNKS:
- business_assistant_overview_001
- business_assistant_sessions_001
---

---
CHUNK_ID: business_assistant_sessions_001
TITLE: Chat Sessions, Conversation History, and Background Summaries
CATEGORY: business_assistant
PAGE/MODULE: Business Workspace (/businesses/:businessId) → Chat Sessions Sidebar
AUTHENTICATION: Required (Role: Entrepreneur)
KEYWORDS: chat sessions, conversation history, new chat, previous conversations, session summary

CONTENT:
Entrepreneurs often discuss multiple distinct business topics over days or weeks (e.g., machinery purchasing on Monday, government scheme eligibility on Thursday, pricing on Friday). The Business Assistant manages this cleanly through dedicated Chat Sessions:

Chat Session Management:
- Session List Panel: A collapsible left drawer in the workspace lists all your previous chat sessions with descriptive titles and message counts.
- "Start New Chat" Button: Click "+ New Chat" at any time to start a fresh conversational thread without losing earlier dialogues.
- Seamless Resumption: Click on any prior session to reload the complete conversation history, including sent text, attached images, and assistant responses.
- Automatic Background Summaries: When a conversation concludes or pauses, an asynchronous background service generates an executive summary of key decisions, keeping the AI's long-term memory sharp without bloating response latency.

USER QUESTIONS THIS CHUNK SHOULD ANSWER:
- How do I start a new chat with the AI assistant?
- Where can I see my previous conversations?
- Are my chat messages saved if I leave the page?
- Can I switch between different discussion topics?

NAVIGATION/ACTION:
Inside `/businesses/:businessId` → Click "Chat Sessions" panel on the left → Click "+ New Chat" or click on an existing session title.

RELATED CHUNKS:
- business_assistant_overview_001
- business_assistant_actions_001
---

---
CHUNK_ID: business_assistant_actions_001
TITLE: Assistant Action Tools and Explicit Confirmation Protocol
CATEGORY: business_assistant
PAGE/MODULE: Business Workspace (/businesses/:businessId) → AI Engine
AUTHENTICATION: Required (Role: Entrepreneur)
KEYWORDS: assistant tools, update business details, confirmation protocol, safe actions, database security

CONTENT:
Strict Database Mutation & Safety Protocol:
The Business AI Assistant possesses integrated tools that can interact with the backend database—such as updating your business details (e.g., updating margin capital, business description, or address) or changing business operational status.

To prevent accidental changes, the assistant operates under a Strict Confirmation Protocol:
1. No Speculative Execution: The assistant will NEVER update a database record, change a business status, or overwrite parameters silently or as a side-effect of a casual question.
2. Explicit Verification Step: If you ask the assistant to modify your business (e.g., "Change my margin capital to 2 lakhs" or "Mark my business status as active"):
   - The assistant will clearly summarize the current value and the proposed new value.
   - It will explicitly ask for your affirmative consent: "Would you like me to go ahead and update your margin capital to ₹2,00,000?"
3. Awaiting Explicit Confirmation: It waits for your clear affirmative answer ("Yes", "Confirm", "Go ahead") before executing the tool.

Analytical Generation Tools:
The assistant can also trigger heavy background generation tools (Feasibility Report, Financial Plan, Schemes Profiler). It will only trigger one heavy generation tool at a time and will verify that all required inputs are present.

USER QUESTIONS THIS CHUNK SHOULD ANSWER:
- Can the AI assistant update my business details for me?
- Why does the assistant ask for confirmation before changing my data?
- Can the assistant accidentally delete or modify my business without asking?
- Can the assistant trigger a feasibility analysis for me?

NAVIGATION/ACTION:
Chat with the assistant in `/businesses/:businessId` and reply "Confirm" or "Yes" whenever it requests explicit verification for an action.

RELATED CHUNKS:
- business_assistant_overview_001
- business_edit_001
- business_category_rule_001
---

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

---
CHUNK_ID: troubleshoot_login_001
TITLE: Troubleshooting: Login Problems and Session Expiry
CATEGORY: troubleshooting
PAGE/MODULE: Login (/login)
AUTHENTICATION: Not Required
KEYWORDS: login error, cannot login, invalid credentials, session expired, wrong password, auth error

CONTENT:
Common Login Issues and Solutions:

1. "Invalid credentials" or Incorrect Password:
   - Double-check that your Email or Username is typed without accidental spaces.
   - Click the "Eye" icon in the password field to verify that caps lock is off and your password is typed correctly.
   - Ensure you are using the email address you registered with during signup.

2. "Unable to reach backend" Network Error:
   - Ensure your internet connection is active.
   - If running locally, verify that the backend API services (on port 8000) are running.

3. "Session Expired" While Navigating:
   - For security, user authentication tokens expire after an extended period of inactivity.
   - Simply click "Log In" in the sidebar and re-enter your credentials to restore an active session. Your previously created businesses and saved reports will remain intact.

USER QUESTIONS THIS CHUNK SHOULD ANSWER:
- What should I do if I cannot log into my account?
- Why does it say "Invalid credentials"?
- What does it mean if my session expired?
- Why am I seeing a network error on the login screen?

NAVIGATION/ACTION:
Go to `/login` → Check credentials using the eye icon → Click "Sign In".

RELATED CHUNKS:
- account_login_001
- account_signup_001
---

---
CHUNK_ID: troubleshoot_otp_002
TITLE: Troubleshooting: Email OTP Verification Not Received During Signup
CATEGORY: troubleshooting
PAGE/MODULE: Signup (/signup)
AUTHENTICATION: Not Required
KEYWORDS: otp not received, verification code missing, email otp problem, cannot verify email, resend otp

CONTENT:
During account registration, a 6-digit OTP (One-Time Password) is dispatched to verify that you own the entered email address.

What to Do if You Do Not Receive the OTP:
1. Check Your Spam or Junk Folder: Automated OTP verification emails can occasionally be routed into your email provider's Spam, Promotions, or Updates folder. Search for emails from "ArthNiti" or "Finance Assistant".
2. Verify Your Email Address: Look closely at the Email field on the signup form to ensure there are no typos (e.g., `.con` instead of `.com`, or missing letters).
3. Wait for the Cooldown Timer: Wait 60 seconds before requesting a new code.
4. Click "Resend OTP": Once the timer elapses, click "Resend Code" to trigger a fresh verification dispatch.
5. Enter Code Promptly: OTP codes remain valid for 10 minutes. Once entered, the field will display a green checkmark indicating successful verification.

USER QUESTIONS THIS CHUNK SHOULD ANSWER:
- Why haven't I received my signup OTP?
- Where do I find the email verification code?
- How do I resend the verification OTP?
- How long is the signup OTP valid?

NAVIGATION/ACTION:
On the `/signup` screen → Check email spam folder or click "Resend OTP" after 60 seconds.

RELATED CHUNKS:
- account_signup_001
---

---
CHUNK_ID: troubleshoot_analysis_stuck_001
TITLE: Troubleshooting: Business Analysis Taking Long or Modal Closed
CATEGORY: troubleshooting
PAGE/MODULE: Business Analysis (/businesses/:businessId/analysis)
AUTHENTICATION: Required (Role: Entrepreneur)
KEYWORDS: analysis taking too long, analysis stuck, modal closed, generation slow, report missing

CONTENT:
Common Concerns During Business Analysis Generation:

1. "I accidentally closed the analysis modal or left the page while it was generating":
   - Do not worry! Business Analysis does not run in your browser window; it runs as a detached background worker on the server.
   - Closing the modal, navigating to another page, or closing your browser does NOT cancel the calculation.
   - Simply return to `/businesses/:businessId/analysis` after 5 to 10 minutes. The completed report and evidence cards will be waiting for you.

2. "It has been more than 10 minutes and the report still says generating":
   - Refresh the page using your browser's reload button or click the "Try Again" / "Refresh" icon on the analysis screen.
   - Sometimes the page view needs a fresh fetch to pull the newly saved database records.
   - If an error banner appears ("Analysis operation failed"), click "Try Again" to re-trigger the generation. Ensure the business has valid coordinates and address details.

USER QUESTIONS THIS CHUNK SHOULD ANSWER:
- What happens if I close the tab while business analysis is running?
- Did I lose my analysis by leaving the page?
- Why is the feasibility report taking more than 10 minutes?
- How do I refresh the analysis page?

NAVIGATION/ACTION:
Go to `/businesses/:businessId/analysis` → Refresh the browser page or click the refresh button.

RELATED CHUNKS:
- business_analysis_002
- faq_analysis_time_001
---

---
CHUNK_ID: troubleshoot_location_picker_001
TITLE: Troubleshooting: Location Coordinates and Map Pin Issues
CATEGORY: troubleshooting
PAGE/MODULE: Create Business Modal & Edit Business Modal
AUTHENTICATION: Required
KEYWORDS: map not loading, coordinates missing, pin location error, geocoding failed, latitude longitude empty

CONTENT:
How to Resolve Location and Map Issues:

1. Map Marker Not Dropping:
   - Ensure you click firmly within the boundaries of the Leaflet map container.
   - Once clicked, a blue pin marker will appear, and the Latitude and Longitude fields will automatically populate with decimal numbers (e.g., Lat: 25.3176, Lng: 82.9739).

2. Map Shows Ocean or Incorrect Country:
   - By default, the map initializes to the center of India.
   - As you type your Village, City, District, and State into the form fields, the smart geocoding service automatically pans the map to your area. Allow 1–2 seconds for the automatic geocoding to complete.
   - Use the "+" and "−" zoom buttons on the top-left of the map to zoom in closer to your village, road, or landmark.

3. "Location details missing" Error When Creating Business:
   - Make sure that City, District, State, and Country are filled in.
   - Ensure a location marker has been clicked on the map so that latitude and longitude coordinates are captured.
   - If you already entered your home address during signup, simply click the "Use Profile Location" button to auto-populate all address and coordinate fields instantly.

USER QUESTIONS THIS CHUNK SHOULD ANSWER:
- Why won't the location map load?
- How do I set latitude and longitude if I don't know the exact numbers?
- Why did business creation say location details are missing?
- How can I quickly fill my business location?

NAVIGATION/ACTION:
Inside the Create Business Modal on `/businesses` → Click "Use Profile Location" or click directly on the Leaflet map.

RELATED CHUNKS:
- business_create_001
- business_location_001
---

---
CHUNK_ID: limitations_platform_001
TITLE: Platform Scope and Advisory Disclaimers
CATEGORY: limitations
PAGE/MODULE: Global Platform
AUTHENTICATION: Not Required
KEYWORDS: disclaimer, legal limitations, not loan approval, no guarantee, financial advice disclaimer, official schemes

CONTENT:
Important Operational Boundaries and Disclaimers for ArthNiti:

1. Decision-Support & Simulation Nature:
   - ArthNiti is an AI-powered hyper-local advisory and simulation platform. It generates feasibility assessments, demographic estimates, and financial projections based on available public databases, spatial data, and mathematical models.
   - Analysis results DO NOT guarantee that a business venture will be profitable, nor do they guarantee immunity from commercial risks or market downturns.

2. No Direct Loan Approval or Money Lending:
   - ArthNiti is NOT a financial institution, bank, NBFC, or direct lender.
   - Recommended loan amounts, EMI numbers, and interest rates are calculated for financial planning and bank proposal preparation. Final loan sanctions depend entirely on the lending criteria of commercial banks and financial institutions.

3. No Guaranteed Government Scheme Approvals:
   - High scheme Match Scores indicate eligibility alignment based on submitted parameters.
   - ArthNiti CANNOT grant, sanction, or disburse government subsidies. Official applications must be submitted directly through official government portals (e.g., KVIC, DIC, MyScheme) or designated bank branches.

4. Legal and Tax Consultation:
   - Platform reports do not replace formal chartered accounting, taxation, or legal compliance advice. Users should consult qualified professionals for formal statutory filings.

USER QUESTIONS THIS CHUNK SHOULD ANSWER:
- Does this website guarantee that my business will be profitable?
- Can ArthNiti sanction my bank loan?
- Is the platform output considered official legal or tax advice?
- What are the platform's official disclaimers?

NAVIGATION/ACTION:
Use generated reports as advisory planning tools to present to lenders, partners, and government agencies.

RELATED CHUNKS:
- faq_financing_001
- financial_analysis_001
- government_schemes_001
---

---
CHUNK_ID: limitations_site_assistant_001
TITLE: Site Assistant Operational Boundaries and Guardrails
CATEGORY: limitations
PAGE/MODULE: Site Assistant / Global
AUTHENTICATION: Not Required
KEYWORDS: site assistant limits, what assistant cannot do, assistant rules, guardrails, site assistant boundaries

CONTENT:
Operational Directives for the Site Assistant:

The Site Assistant is an onboarding, navigation, and educational guide for the ArthNiti platform. To protect user security and data accuracy, the Site Assistant operates under strict boundaries:

1. No Speculative Feasibility Calculations:
   - The Site Assistant must NOT pretend to compute complex hyper-local feasibility studies, competitor counts, or mandi prices directly in chat.
   - When a user asks: "How profitable is a bakery in Varanasi?", the Site Assistant should direct the user to create a business profile and run the Business Analysis module.
2. No Access to Private Business Data:
   - The Site Assistant does NOT have access to a user's private business workspace, private chat logs with the Business AI Assistant, or specific financial ledgers.
3. No False Claims of Approvals:
   - The Site Assistant will never claim that a loan has been approved, that a government grant is guaranteed, or that a user's business cannot fail.
4. Redirection to Specialized Tools:
   - For business-specific strategic guidance, document review (invoices/bills), or interactive planning, the Site Assistant directs users to open their Business Workspace (`/businesses/:businessId`) and engage the Business AI Assistant.

USER QUESTIONS THIS CHUNK SHOULD ANSWER:
- What can the Site Assistant NOT do?
- Can the Site Assistant calculate my profits in chat?
- Why does the Site Assistant tell me to go to the Business Workspace?
- Can the Site Assistant approve my loan?

NAVIGATION/ACTION:
Ask the Site Assistant questions about how to use the website, where features are located, and how onboarding works.

RELATED CHUNKS:
- assistant_comparison_001
- business_assistant_overview_001
- limitations_platform_001
---

---
CHUNK_ID: limitations_government_role_001
TITLE: Status of Government Official Experience and Workspace
CATEGORY: limitations
PAGE/MODULE: Role Dashboard (/dashboard) & Signup (/signup)
AUTHENTICATION: Required (Role: Government)
KEYWORDS: government role status, government dashboard, under preparation, government official features

CONTENT:
Status of the Government Official Role:

Current Platform Availability:
Users who register with the "Government" role (such as State Channelising Agency officers, District Industries Centre representatives, or development administrators) currently see an informational notice on their Dashboard (`/dashboard`):
"Government workspace is on hold for now. The government-official experience is being prepared. Your profile and the public business directory remain available while this workspace is on hold."

What Government Accounts Can Access Today:
1. Public Business Directory (`/businesses/details`): Search, filter, and inspect registered micro-enterprises and local producers across districts and states.
2. User Profile (`/profile`): Maintain official designation, agency name, agency type (e.g., SCA), and contact details.

Upcoming Capabilities:
Dedicated administrative tools for tracking district enterprise trends, monitoring scheme adoption rates, and communicating directly with regional entrepreneurs are under active development and will be unlocked in a future platform release.

USER QUESTIONS THIS CHUNK SHOULD ANSWER:
- Why is the government dashboard on hold?
- What features can a Government account access right now?
- When will the government official tools be ready?
- Can a government official view local businesses?

NAVIGATION/ACTION:
As a Government user: Log in → Access the Business Directory (`/businesses/details`) and Profile (`/profile`).

RELATED CHUNKS:
- overview_002
- nav_home_dashboard_001
- nav_directory_001
---
