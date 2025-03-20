# 1. Scraping & Data Ingestion

## User Story
“As an **admin**, I want to **initiate a manual scrape** of the target website, so that the system can **collect, parse, and store** the latest promotions in the database.”

## Acceptance Criteria
1. An **API endpoint** (e.g., `POST /scrape`) or **UI button** exists to trigger scraping.
2. The scraper **handles JavaScript** (via Playwright) and fetches relevant promotional data.
3. The system **parses** the promotion fields (name, discount, dates, address, etc.) and **persists** them in PostgreSQL.
4. A **successful response** is returned (e.g., status 200), with a simple message confirming that scraping was initiated.
5. **Error handling** is in place for common issues (e.g., network failures, unexpected HTML structure).

## Estimation
- **Story Points**: 5
- **Hours (approx.)**: 6–8

---

### Additional Notes
- These estimates assume one developer working through all tasks.
- Acceptance Criteria can be refined further if edge cases arise (e.g., handling partial data, network timeouts, etc.).
- The Story Points are illustrative; your team might use a different scale or approach to sizing.