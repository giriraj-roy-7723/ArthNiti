# Category: Account & Profile

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
