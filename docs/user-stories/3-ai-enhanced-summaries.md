# 3. AI-Enhanced Summaries

## User Story
“As a **user**, I want the system to **generate short AI summaries** of each promotion, so that I can **quickly understand** the main highlights without reading every detail.”

## Acceptance Criteria
1. A **POST /ai-process** endpoint triggers AI-based processing of promotions in the database.
2. **LangGraph + Mistral** integration is set up to create concise text summaries of each promotion’s key info (discount, valid days, etc.).
3. Successfully processed promotions have an `ai_summary` field saved to PostgreSQL.
4. If a promotion is **already** processed, the endpoint either **skips** it or **reprocesses** it (depending on MVP design).
5. The frontend **displays** the `ai_summary` text on each promotion card once available.

## Estimation
- **Story Points**: 5
- **Hours (approx.)**: 6–8

---

### Additional Notes
- These estimates assume one developer working through all tasks.
- Acceptance Criteria can be refined further if edge cases arise (e.g., handling partial data, network timeouts, etc.).
- The Story Points are illustrative; your team might use a different scale or approach to sizing.