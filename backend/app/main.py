from fastapi import FastAPI
from app.scraping.scraper import scrape_santander_promotions
from dotenv import load_dotenv
import os
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import promotions, scrape, ai_process  # new

# Load environment variables from a .env file
load_dotenv()

allowed_origins = [os.getenv("FRONTEND_URL", "*")]
app = FastAPI(redirect_slashes=False)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define API prefix
API_V1_PREFIX = "/api/v1"

# Mount static files at root level for easier access
app.mount(
    "/scraped_data",  # Changed from /api/v1/scraped_data to /scraped_data
    StaticFiles(directory="scraped_data"),
    name="scraped_data",
)

# Mount routers with the API prefix
app.include_router(promotions.router, prefix=API_V1_PREFIX)
app.include_router(scrape.router, prefix=API_V1_PREFIX)
app.include_router(ai_process.router, prefix=API_V1_PREFIX)

if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
