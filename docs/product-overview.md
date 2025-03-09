1. Product Overview

Promo-Finder MVP is a lightweight application that automates the collection of promotions from a single financial institution’s website, processes the data, enhances it with an AI agent, and presents the results in a simple web interface.

1.1 Goals
	1.	Automated Scraping: Crawl and extract promotional offers from a specific URL.
	2.	Data Processing & Storage: Convert raw scraped data into a structured format in PostgreSQL.
	3.	AI Enhancement: Use an AI agent (LangGraph + Mistral) to generate or refine textual summaries of each offer.
	4.	Simple Frontend: Display a minimalist list of promotions, ensuring clarity and user-friendliness.
	5.	Cloud Deployment: Deploy to Google Cloud Platform (GCP) for easy presentation.

⸻

2. MVP Scope

The MVP focuses on delivering core functionality with minimal complexity:
	1.	Single Website Scraping
	•	Target: https://banco.santander.cl/beneficios
	•	Handle JavaScript rendering with a headless browser (e.g., Playwright).
	2.	Data Extraction
	•	Required fields: Restaurant Name, Restaurant Logo Image, Valid Date(s), Discount Rate, Address, Expiration Date, Source.
	•	Store in PostgreSQL for persistence.
	3.	AI Agent
	•	Integrate with LangGraph + Mistral.
	•	Generate short or refined text summaries from structured data.
	4.	Minimal React Frontend
	•	Display promotions in a list or card view (using Tailwind CSS).
	•	No advanced filtering or sorting required.
	•	No user authentication or roles.
	5.	Deployment
	•	Use GCP (e.g., Cloud Run) with containerization.
	•	Provide a URL to showcase the MVP.

2.1 Out of Scope
	•	User accounts, authentication, or role-based access.
	•	Observability, advanced security, or rate limiting.
	•	Complex business logic or multi-institution scraping.
	•	Mobile app or push notifications.

⸻

3. Key Requirements

3.1 Functional Requirements
	1.	Scraping
	•	Must reliably fetch promotional content from the target site.
	•	Handle dynamic content with JavaScript rendering.
	•	Provide a simple method (manual trigger) to initiate scraping.
	2.	Data Processing
	•	Parse promotions into specific fields.
	•	Store structured data in PostgreSQL.
	•	Handle missing or partial data gracefully.
	3.	AI Summaries
	•	Call Mistral’s API through LangGraph for basic text generation or summarization.
	•	Store AI-generated text back into the promotions data.
	4.	Frontend Display
	•	Basic React app using Tailwind CSS to display each promotion’s data (including AI-derived text).
	•	Minimal design, focusing on clarity.
	5.	Deployment
	•	Containerize the backend (scraping + AI logic) and the frontend.
	•	Host on GCP with minimal cost and straightforward setup.

3.2 Non-Functional Requirements
	•	Performance: The scraping process should complete in a reasonable time (e.g., under 2 minutes for the single site).
	•	Reliability: Data and code should be version-controlled (GitHub).
	•	Maintainability: Code should be organized (separate folders for backend, frontend).
	•	Security: Basic .env file for credentials; no user data to protect.

⸻

4. Technology Stack
	1.	Backend
	•	Language: Python
	•	Framework: FastAPI (optional but recommended for a quick API layer)
	•	Scraping: Playwright (for JavaScript-heavy site)
	•	Database: PostgreSQL
	•	AI Integration: LangGraph + Mistral API
	2.	Frontend
	•	Framework: React (minimal setup)
	•	Styling: Tailwind CSS
	•	Build Tool: Vite or Create React App (developer’s preference)
	3.	Deployment
	•	Containerization: Docker + Docker Compose for local dev
	•	Hosting: GCP (Cloud Run or equivalent service)

⸻

5. Data Model

5.1 Promotions Table (PostgreSQL)

Column	Type	Description
id	SERIAL (PK)	Unique promotion ID
restaurant_name	VARCHAR	Name of the restaurant or brand
logo_url	VARCHAR	Image URL for the restaurant’s logo
valid_days	VARCHAR	Days of the week or date range (e.g., “Mon-Fri”)
discount_rate	VARCHAR	Promotion discount (e.g., “20%”)
address	VARCHAR	Address or location of the restaurant
expiration_date	DATE / VARCHAR	Promotion validity date if applicable
source	VARCHAR	e.g., “Santander Chile”
ai_summary	TEXT	Generated text from the AI agent
created_at	TIMESTAMP	Timestamp of insertion



⸻

6. AI Agent Usage
	1.	Integration: Use LangGraph to create a pipeline from the structured data to Mistral’s API.
	2.	Function:
	•	Possibly a short summary or “key highlights” for each promotion.
	•	Minimal logic—mainly to show how AI can enrich the data.
	3.	Invocation:
	•	Either automatically after scraping or via a simple endpoint to process new promotions.

⸻

7. Frontend UI
	•	Page Layout:
	•	A single page listing promotions in card format.
	•	Each card includes: restaurant name, discount, valid days, expiration, address, and AI summary.
	•	Design:
	•	Minimal, functional styling with Tailwind CSS.
	•	No user interactivity beyond viewing.

⸻

8. Deployment Strategy
	1.	Docker for backend and frontend to ensure consistency.
	2.	Cloud Run (preferred) to host containers:
	•	Container for backend (Python + FastAPI + Playwright).
	•	Container for frontend (React build served by a lightweight web server).
	3.	Environment Variables:
	•	Database connection, Mistral API keys, etc., stored in a secure location or .env for MVP.

⸻

9. Implementation Timeline (Approx. 30 Hours Total)
	1.	Setup & Environment (2–3 hours)
	2.	Scraper & Data Model (7–8 hours)
	3.	AI Agent Integration (5–6 hours)
	4.	React Frontend (5–6 hours)
	5.	Deployment (4–5 hours)
	6.	Testing & Buffer (2–3 hours)

⸻

10. Success Criteria
	•	A functional end-to-end MVP:
	1.	Scrapes real promotions from the specified site.
	2.	Stores them in PostgreSQL with all required fields.
	3.	Generates short AI summaries.
	4.	Displays the promotions via a lightweight React app.
	5.	Runs on GCP (temporarily or on-demand) for demonstration.

⸻

11. Outstanding Questions / Assumptions
	•	Handling Captchas: If the site implements CAPTCHAs or anti-scraping measures, we assume minimal interference.
	•	Database Costs: Low usage with a single Cloud SQL or ephemeral local DB if needed.
	•	AI Rate Limits: The MVP usage is minimal, assuming free-tier or small usage in Mistral.

⸻

12. Conclusion

The Promo-Finder MVP offers an automated pipeline from scraping real promotions on the Santander Chile site, processing the data with AI for simple textual enhancements, and presenting it in a minimal React interface. This specification ensures a concise, functioning prototype that can be extended for broader use cases in future iterations.