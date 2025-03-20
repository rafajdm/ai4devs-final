# Promo-Finder MVP - High-Level Architecture

This document provides a concise overview of the Promo-Finder MVP architecture, focusing on the main components, data flow, and the technologies involved.

---

## 1. Overview

The MVP consists of a **single backend service** that scrapes promotional data from a target website, processes it with an AI agent, and exposes it via a **REST API**. A **React frontend** then fetches and displays the processed promotions.

---

## 2. Components & Technologies

1. **Backend (Python)**  
   - **FastAPI** for creating REST endpoints.  
   - **Playwright** for JavaScript-based web scraping.  
   - **LangGraph** + **Mistral** API for basic AI text processing.  
   - **PostgreSQL** for data storage.

2. **Frontend (React)**  
   - **React** application with **Tailwind CSS** for styling.  
   - Fetches data from the FastAPI endpoints and displays promotions in a simple card layout.

3. **Deployment (GCP)**  
   - Containerized (via **Docker**) for both backend and frontend.  
   - Hosted on **Google Cloud Run** (or similar GCP service) with environment variables for credentials.

---

## 3. Data Flow

1. **Scraping**  
   - A manual or scheduled trigger calls a FastAPI endpoint (`/scrape`), which invokes Playwright to navigate the target site and extract promotions.

2. **Database Ingestion**  
   - Extracted data (e.g., restaurant name, discount, valid dates) is saved to **PostgreSQL** in a `promotions` table.

3. **AI Processing**  
   - A second endpoint (or background task) calls **LangGraph** with **Mistral** to generate or refine text summaries.  
   - The AI-generated output is updated in the `promotions` table (e.g., a `summary_text` field).

4. **Frontend Display**  
   - The React app calls FastAPI’s `/promotions` endpoint to retrieve the processed data.  
   - Renders each promotion as a **card** showing restaurant info, discounts, valid dates, and the AI summary.

---

## 4. Layered Structure

- **API Layer** (FastAPI):  
  - Defines routes for scraping, retrieving promotions, and AI processing triggers.

- **Scraping Subsystem** (Playwright):  
  - Retrieves and parses dynamic web content to create a list of promotions.

- **AI Subsystem** (LangGraph + Mistral):  
  - Generates concise or enriched text for each promotion.

- **Data Layer** (PostgreSQL):  
  - Stores promotion records and AI summaries.

- **Presentation Layer** (React + Tailwind):  
  - Minimal single-page interface for viewing promotions in card format.

---

## 5. Future Extensions

- **User Accounts & Security**: Adding authentication and authorization.  
- **Observability**: Metrics, logging, and monitoring beyond minimal error logs.  
- **Additional Scrapers**: Expanding to multiple financial institutions or other data sources.  
- **Advanced AI**: More complex NLP tasks, personalization, or recommendation features.

---

## 6. Summary

This architecture is designed for a **rapid MVP**: a monolithic backend built on Python + FastAPI, a single React frontend, and a straightforward PostgreSQL database for persistence. It’s containerized for easy deployment to Google Cloud Platform, providing a clear path to showcase core scraping and AI capabilities with minimal overhead.