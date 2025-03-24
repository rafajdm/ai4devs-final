# Testing & Security Recommendations

This document provides an **overview of recommended tests** for both the **backend** and **frontend** of your MVP, along with **security enhancements** you can quickly apply.

---

## 1. Backend Testing

Your backend includes **scraping logic**, **database interactions**, and **AI processing**. Here’s a suggested breakdown of tests:

### 1.1 Unit Tests for Scraping

- **Goal**: Validate the logic that extracts promotions from the target site.
- **Tasks**:
  - **Task 1.1.1**: Mock the scraped HTML and verify that fields (restaurant name, discount, etc.) are parsed correctly.
  - **Task 1.1.2**: Test handling of missing/invalid fields (e.g., gracefully skip promotions with incomplete data).
  - **Task 1.1.3**: Check response when encountering unexpected site structure or timeouts.

### 1.2 Database Interaction Tests

- **Goal**: Ensure data is stored and retrieved correctly in PostgreSQL.
- **Tasks**:
  - **Task 1.2.1**: Use a test DB or an in-memory solution (if possible) to confirm inserts/updates for new promotions.
  - **Task 1.2.2**: Validate `DELETE` or update logic if it exists (e.g., removing outdated promotions).
  - **Task 1.2.3**: Confirm that queries return the correct set of promotions when requested (no duplicates, correct fields).

### 1.3 AI Processing Tests

- **Goal**: Verify AI calls to Mistral (or your chosen API) and ensure the `ai_summary` is updated properly.
- **Tasks**:
  - **Task 1.3.1**: Mock AI responses to confirm your logic updates the DB with the `ai_summary`.
  - **Task 1.3.2**: Test fallback behaviors if the AI call fails or returns an error.
  - **Task 1.3.3**: Check that only unprocessed (or outdated) promotions get updated as intended.

### 1.4 Integration / API Tests

- **Goal**: Confirm your **FastAPI** endpoints return expected data and handle edge cases.
- **Tasks**:
  - **Task 1.4.1**: Test `/scrape` endpoint triggers the scraping pipeline successfully.
  - **Task 1.4.2**: Test `/ai-process` endpoint calls AI logic and updates DB.
  - **Task 1.4.3**: Verify `/promotions` returns correct JSON with relevant fields.

---

## 2. Frontend Testing

Your frontend is a **React** + **Tailwind CSS** setup that fetches data from the backend. Focus on **component tests**, **UI sanity checks**, and **integration** with the backend URLs.

### 2.1 Component & UI Tests

- **Goal**: Ensure key components (e.g., promotion cards) render and handle props correctly.
- **Tasks**:
  - **Task 2.1.1**: Snapshot tests for **PromotionCard** (or similar components) using [Jest + React Testing Library] or [Vitest if using Vite].
  - **Task 2.1.2**: Check that a list of promotions is displayed in a grid or list layout.
  - **Task 2.1.3**: Test “empty state” rendering (no promotions).

### 2.2 Integration / E2E Testing

- **Goal**: Confirm the **frontend** properly fetches from the **backend** and displays real data.
- **Tasks**:
  - **Task 2.2.1**: Use [Cypress](https://www.cypress.io/) or [Playwright] for end-to-end tests:
    - Visit the site → Expect to see promotions from the backend.
    - Confirm that any AI summary fields appear on the promotion cards.
  - **Task 2.2.2**: Test for error states if the backend is unavailable or returns an error code.

### 2.3 Basic Security / Performance Checks

- **Goal**: Confirm no obvious security misconfigurations in the UI.
- **Tasks**:
  - **Task 2.3.1**: Verify **HTTPS** usage in all API calls (no mixed content issues).
  - **Task 2.3.2**: Confirm React is not exposing any secrets in the compiled bundle.
  - **Task 2.3.3**: Optionally run a basic [Lighthouse](https://developers.google.com/web/tools/lighthouse/) audit to catch performance or accessibility issues.

---

## 3. Quick Security Enhancements for an MVP

Since this is an MVP, you may not implement advanced security measures yet. However, you **can** apply some quick wins:

1. **Use HTTPS** Everywhere

   - Ensure your **frontend** only references the **backend** via `https://` URLs.
   - Eliminate mixed content warnings.

2. **No Hard-Coded Secrets**

   - Store credentials (DB password, Mistral API key) in environment variables or a secure secret store.
   - Don’t push `.env` with real secrets to GitHub.

3. **Input Validation**

   - If your scraping endpoint or AI endpoint accepts user input (like query params), apply basic input validation to prevent injection attacks or resource exhaustion.

4. **Minimal Attack Surface**

   - Only expose the routes you need (`/scrape`, `/promotions`, etc.).
   - Return generic error messages (avoid exposing sensitive details in logs or error responses).

5. **CORS Controls**

   - If you want to restrict who can call your backend, configure CORS to only allow requests from the official frontend domain (for a more secure environment).

6. **Logs & Monitoring**
   - Even at MVP stage, consider enabling basic logs on Cloud Run or attach a monitoring tool to watch for abnormal spikes or errors.

By focusing on these quick security wins (HTTPS, no secrets in code, minimal endpoints), you’ll reduce the chance of data leaks and keep the MVP agile while still addressing fundamental security concerns.

---

## 4. Task Overview Example

| Task ID | Description                                        | Priority | Est. Hours |
| ------- | -------------------------------------------------- | -------- | ---------- |
| B-TEST1 | Unit test scraping logic & handle invalid HTML     | High     | 4          |
| B-TEST2 | DB integration test (insert/fetch promotions)      | High     | 3          |
| B-TEST3 | AI pipeline test with mock responses               | Medium   | 3          |
| B-TEST4 | End-to-end /scrape & /promotions tests in FastAPI  | Medium   | 3          |
| F-TEST1 | Snapshot & prop tests for React promotion card     | Medium   | 2          |
| F-TEST2 | E2E test: confirm promotions appear on the UI      | Medium   | 3          |
| F-TEST3 | Check for mixed-content requests, only HTTPS calls | High     | 2          |
| SEC1    | Enforce environment variables for secrets          | High     | 2          |
| SEC2    | Basic CORS & input validation checks               | Medium   | 2          |

_(These are sample tasks—adjust as needed for your workflow.)_

---

## Conclusion

1. **Backend**: Emphasize **unit tests** for scraping and AI logic, plus **integration tests** for DB inserts and endpoints.
2. **Frontend**: Aim for **component tests** plus an **end-to-end** pass that ensures real data flows from the API.
3. **Security**: Focus on **HTTPS**, **no secrets in code**, **basic CORS**, and minimal input validation. These quick measures boost MVP reliability and reduce potential vulnerabilities.

With these tests and security steps, your MVP remains **lean** while providing a **foundational safety net** for future growth.
