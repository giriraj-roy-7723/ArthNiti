# Category: AI Assistants (Site Assistant vs Business Assistant)

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
