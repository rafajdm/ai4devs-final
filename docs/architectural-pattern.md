# Folder Structure & Architectural Pattern

Below is a **folder structure** for the Promo-Finder MVP, along with an overview of the **layered / modular monolith** approach. This structure groups related code logically while remaining lean enough for an MVP.

---

## Folder Structure

```
ai4devs-final/
│
├── backend/                  # Backend root
│   ├── Dockerfile            # Dockerfile for backend
│   ├── requirements.txt      # Python dependencies
│   ├── README.md             # Backend-specific documentation
│   ├── app/                  # Application code (modular structure)
│   │   ├── api/             # FastAPI endpoints (presentation layer)
│   │   │   ├── v1/          # Versioned routes (if needed)
│   │   │   └── __init__.py
│   │   ├── scraping/        # Playwright-based scraping logic
│   │   │   └── __init__.py
│   │   ├── ai/              # LangGraph + Mistral integration
│   │   │   └── __init__.py
│   │   ├── db/              # Database layer
│   │   │   ├── connect.py   # Example for psycopg2 connection logic
│   │   │   ├── queries.py   # Raw SQL queries or helper functions
│   │   │   └── __init__.py
│   │   ├── core/            # Core settings, configs, and utilities
│   │   │   ├── config.py    # App-wide settings (e.g. DB URL)
│   │   │   ├── logger.py    # Logging configuration
│   │   │   └── __init__.py
│   │   ├── main.py          # Entry point for FastAPI (app initialization)
│   │   └── __init__.py
│   ├── tests/               # Backend tests
│   │   ├── test_api.py
│   │   ├── test_scraping.py
│   │   └── __init__.py
│   └── scripts/             # Any standalone scripts for local usage
│       └── __init__.py
│
├── frontend/                 # Frontend root
│   ├── Dockerfile            # Dockerfile for frontend
│   ├── index.html            # HTML template (for Vite or CRA)
│   ├── package.json          # NPM or Yarn configuration
│   ├── vite.config.js        # Vite config (if using Vite)
│   ├── src/                  # Source code for the React app
│   │   ├── assets/           # Static assets (images, fonts, etc.)
│   │   ├── components/       # Reusable components
│   │   │   └── PromotionCard.jsx
│   │   ├── pages/            # Views (formerly pages)
│   │   │   └── Home.jsx
│   │   ├── App.jsx           # Main App component
│   │   └── main.jsx          # Entry point (React DOM rendering)
│   └── public/               # Public folder remains for additional static assets
│
├── docs/                     # Project documentation
│   ├── product-overview.md
│   ├── high-level-requirements.md
│   ├── high-level-architecture.md
│   └── ...                   # Other documentation files
│
├── .gitignore                # Git ignore file
├── docker-compose.yml        # Docker Compose for orchestrating backend & frontend
└── README.md                 # Overall project documentation
```

---

## Architectural Pattern

### Layered / Modular Monolith

1. **API Layer** (`api/`):
   - FastAPI endpoints, responsible for **presentation** and exposing data to the outside world.
   - Could be versioned (`v1/`, `v2/`) for easier maintenance if it grows.

2. **Scraping Subsystem** (`scraping/`):
   - Houses Playwright scripts and related logic for retrieving promotions.
   - Invoked by specific endpoints (e.g., `/scrape`) or background tasks.

3. **AI Subsystem** (`ai/`):
   - LangGraph + Mistral integration to process or enrich scraped data (e.g., generating short summaries).

4. **Database Layer** (`db/`):
   - Contains Python modules for interacting with **PostgreSQL** using **psycopg2** (raw SQL queries).
   - If needed, consider manual migrations or basic SQL scripts for schema changes.
   - Manages connections and queries to **PostgreSQL**.

5. **Core Config** (`core/`):
   - Handles application-wide settings, environment variables (`config.py`), logging config, utility functions.
   - Helps keep “global” logic or constants in one place.

6. **Frontend** (`frontend/`):
   - A simple **React** app (using Vite or CRA) for the UI.
   - **Tailwind CSS** for styling.
   - Displays promotions in a card layout, fetches data via the FastAPI endpoints.

#### Data Flow

1. **Scrape**: User or admin hits a FastAPI endpoint `/scrape`.
2. **Store**: Scraped data is parsed and saved in **PostgreSQL** (`promotions` table, for example).
3. **AI**: An optional step to call LangGraph/Mistral for generating additional text or summaries.
4. **Render**: The React frontend calls the API to fetch the processed promotions, then displays them.

---

## Tips & Notes

- **Expand or Split**: If the project grows, each subsystem (scraping, AI, API) can be split into microservices.
- **Testing**: Keep your backend tests in `tests/`. If you have frontend tests (e.g., Jest, React Testing Library), store them in `frontend/src/__tests__/` or a similar structure.
- **Docs**: Maintain a separate `docs/` folder for product specs, architecture overviews, meeting notes, etc.

---

## Conclusion

This structure provides **clarity, maintainability, and room for expansion**. Each core responsibility (scraping, AI, data handling, UI) is distinctly separated, simplifying both local development and future scaling.
