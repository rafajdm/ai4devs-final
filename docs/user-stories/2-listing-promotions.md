# 2. Listing Promotions (Frontend)

## User Story
“As a **user**, I want to **view a list** of all current promotions on a simple webpage, so that I can **quickly see** the available deals.”

## Acceptance Criteria
1. A **React** frontend fetches a list of promotions from `GET /promotions`.
2. Promotions display in a **Tailwind CSS**-styled **card layout**, showing key fields (restaurant name, discount, valid dates, etc.).
3. No login or authentication is required; the page is **publicly accessible**.
4. The data displayed reflects the **most recent scrape**, including updates (if any) from the AI step.
5. The frontend handles **basic loading/error states** (e.g., “No promotions available” if the response is empty).

## Estimation
- **Story Points**: 3
- **Hours (approx.)**: 4–5

---

### Additional Notes
- These estimates assume one developer working through all tasks.
- Acceptance Criteria can be refined further if edge cases arise (e.g., handling partial data, network timeouts, etc.).
- The Story Points are illustrative; your team might use a different scale or approach to sizing.