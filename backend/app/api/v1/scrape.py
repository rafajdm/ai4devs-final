from fastapi import APIRouter
from app.scraping.scraper import scrape_santander_promotions

router = APIRouter(prefix="/scrape", tags=["scrape"])


@router.get("/")
def trigger_scrape():
    scrape_santander_promotions()
    return {"message": "Scrape triggered."}
