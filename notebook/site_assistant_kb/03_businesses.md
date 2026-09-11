# Category: Businesses & Workspace

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
