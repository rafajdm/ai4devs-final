Below is a concise project plan to build the Promo-Finder MVP in 30 hours, incorporating the requirements and clarifications you provided:

⸻

High-Level Requirements & Scope
	1.	Scrape a single website:
	•	Site: https://banco.santander.cl/beneficios
	•	Handle JavaScript-rendered content (e.g., using Playwright).
	2.	Process & Store scraped data in PostgreSQL with the following fields:
	•	Restaurant Name
	•	Restaurant Logo Image (URL or path)
	•	Valid Date (days of week or date range)
	•	Discount Rate
	•	Address
	•	Expiration Date
	•	Source (e.g., “Santander Chile”)
	3.	AI Agent
	•	Use LangGraph with Mistral API (basic NLP).
	•	Likely minimal functionality: e.g., confirm consistency, possibly provide short descriptions or highlight key info.
	4.	Frontend (React + Tailwind)
	•	Very simple: No sorting/filtering.
	•	Just present the promotions in “cards” format.
	5.	Deployment
	•	Cheapest GCP option that can be turned on/off easily – typically Cloud Run with Docker or a small Compute Engine instance.
	•	Single developer, use GitHub for version control.
	6.	No login, observability, or advanced security in this MVP.

⸻

Task Breakdown & Estimated Hours

Below is a step-by-step plan with estimated hours to fit within a 30-hour total budget. Since one developer is doing all tasks, consider this a linear timeline. If any task runs over, you’ll adjust or simplify the approach accordingly.

1. Project Setup & Environment

1.1 Initialize GitHub Repo & Project Structure
	•	Create two main folders: backend/ (Python) and frontend/ (React).
	•	Add a docker-compose.yml or plan for separate Dockerfiles.
	•	Set up a basic .env for local DB credentials, Mistral API keys, etc.
	•	Estimated Time: 1.5 hours

1.2 Local Dev Environment
	•	Install Python, Node.js, create virtual environment, etc.
	•	Confirm Playwright runs locally, confirm PostgreSQL instance is up (can be Dockerized for local dev).
	•	Estimated Time: 1 hour

Total for Step 1: ~2.5 hours

⸻

2. Backend Scraper & Data Model

2.1 PostgreSQL Setup & Basic Schema
	•	Create a simple schema with a promotions table containing the fields (restaurant name, discount, etc.).
	•	Use SQLAlchemy or a lightweight approach (e.g., psycopg2 directly) to interact with PostgreSQL.
	•	Estimated Time: 1 hour

2.2 Playwright Scraper
	•	Implement headless scraping to handle JavaScript.
	•	Navigate to <banco.santander.cl/beneficios>, extract relevant restaurant entries, discount info, etc.
	•	Estimated Time: 3 hours

2.3 Data Extraction & Ingestion
	•	Parse the DOM to locate each restaurant’s details (name, discount, date, etc.).
	•	Store the results in the promotions table.
	•	Handle edge cases (missing data, dynamic content).
	•	Estimated Time: 2 hours

2.4 Scheduled / On-Demand Scrape
	•	For MVP, you can simply provide a manual endpoint (/scrape) that triggers a new scrape.
	•	Keep it minimal—just enough to run the scraper and update the DB.
	•	Estimated Time: 1 hour

Total for Step 2: ~7 hours

⸻

3. AI Agent Integration

3.1 LangGraph + Mistral Setup
	•	Install and configure the LangGraph library.
	•	Set up the credentials for Mistral’s API.
	•	Estimated Time: 1.5 hours

3.2 Implement Basic NLP Processing
	•	Identify what the AI agent should do with the scraped data (e.g., summarize or ensure consistent format).
	•	Possibly produce a short blurb or “key highlights” to display on the frontend.
	•	For MVP, keep logic simple (e.g., pass each promotion’s data to Mistral for a short text summary).
	•	Estimated Time: 2.5 hours

3.3 Integration & Testing
	•	Add a route (e.g., /ai-process) that fetches newly scraped promotions and calls the AI agent to generate any needed text.
	•	Store the AI-generated result in a new column, e.g., summary_text.
	•	Verify the process flow: Scrape → DB → AI → updated DB.
	•	Estimated Time: 2 hours

Total for Step 3: ~6 hours

⸻

4. Basic React Frontend

4.1 Initialize React + Tailwind
	•	Create a new React app (e.g., using Create React App or Vite).
	•	Integrate Tailwind CSS.
	•	Estimated Time: 1.5 hours

4.2 Fetch & Display Promotions
	•	Create an endpoint in the backend to list all promotions (/promotions).
	•	Fetch them from the React app.
	•	Display each promotion in a card layout (title, discount, address, etc.).
	•	Estimated Time: 2 hours

4.3 Add AI Summary Display
	•	If you store a summary_text (or similar) from the AI, show it on the card.
	•	Estimated Time: 1 hour

4.4 Basic Styling & Polish
	•	Make sure the UI is legible, spacing is reasonable, etc.
	•	Estimated Time: 1 hour

Total for Step 4: ~5.5 hours

⸻

5. Deployment to GCP

5.1 Containerization
	•	Create Dockerfile for the backend (Python + requirements).
	•	Create Dockerfile for the frontend (React build).
	•	Potentially combine them or run them as separate services.
	•	Estimated Time: 1.5 hours

5.2 Set Up GCP (Cloud Run or App Engine)
	•	If using Cloud Run:
	•	Build and push the Docker images to Google Container Registry (GCR) or Artifact Registry.
	•	Configure environment variables (DB connection, Mistral keys, etc.).
	•	Provide minimal instructions or scripts for deployment.
	•	Estimated Time: 2.5 hours

Total for Step 5: ~4 hours

⸻

6. Testing & Final Touches

6.1 Basic QA
	•	End-to-end check: Trigger scrape → watch data in DB → AI processing → confirm data appears on frontend.
	•	Fix small bugs or formatting issues.
	•	Estimated Time: 2 hours

6.2 Buffer
	•	Some tasks inevitably spill over; keep a buffer for dealing with unexpected complexities in JS rendering, AI integration, or deployment hiccups.
	•	Estimated Time: ~3 hours

Total for Step 6: ~5 hours

⸻

Overall Time Allocation

Step	Est. Hours
1. Setup & Environment	2.5
2. Scraper & Data Model	7
3. AI Agent Integration	6
4. React Frontend	5.5
5. Deployment (GCP)	4
6. Testing & Buffer	5
Total	~30 hours



⸻

Additional Implementation Notes
	•	Playwright typically handles JavaScript navigation easily, but watch out for dynamic elements. You may need to click or scroll for full content.
	•	Keep AI usage minimal. Since it’s an MVP, even a single text summary per promotion might suffice.
	•	Data consistency: Make sure each promotion has all the required fields; some data might be missing or named differently on the target site.
	•	Secure Secrets: For now (MVP), storing credentials in .env is acceptable, but consider more secure approaches if you expand.
	•	If you find scraping too complex in the allotted time (due to dynamic front-end code from the target site), you might pivot to simpler partial scraping to demonstrate the concept.

⸻