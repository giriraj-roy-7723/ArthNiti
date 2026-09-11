# Category: Troubleshooting

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
