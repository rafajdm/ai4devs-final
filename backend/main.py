from fastapi import FastAPI
from scraper import scrape_santander_promotions
from dotenv import load_dotenv
import os
from fastapi.responses import JSONResponse
import psycopg2
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables from a .env file
load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/scraped_data", StaticFiles(directory="scraped_data"), name="scraped_data")


# Helper to fetch promotions from PostgreSQL
def get_promotions():
    # Use environment variables for connection
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
    )
    cur = conn.cursor()
    # Updated query based on documentation in product-overview.md
    query = """
    SELECT id, restaurant_name, logo_path, applicable_days_text, discount_rate, address, 
           valid_from, valid_until, valid_period_text, source, region, ai_summary, created_at 
    FROM promotions
    """
    cur.execute(query)
    rows = cur.fetchall()
    promotions = []
    for row in rows:
        promotions.append(
            {
                "id": row[0],
                "restaurant_name": row[1],
                "logo_path": row[2],
                "applicable_days_text": row[3],
                "discount_rate": row[4],
                "address": row[5],
                "valid_from": row[6],
                "valid_until": row[7],
                "valid_period_text": row[8],
                "source": row[9],
                "region": row[10],
                "ai_summary": row[11],
                "created_at": row[12],
            }
        )
    cur.close()
    conn.close()
    return promotions


@app.get("/")
def read_root():
    return {"message": "Hello, world!"}


@app.get("/scrape")
def trigger_scrape():
    # Trigger the scraping process when this endpoint is accessed
    scrape_santander_promotions()
    return {"message": "Scrape triggered."}


@app.get("/promotions")
def promotions():
    data = get_promotions()
    from fastapi.encoders import jsonable_encoder

    return JSONResponse(content=jsonable_encoder(data))


if __name__ == "__main__":
    import uvicorn

    # Use the PORT from environment variables if available, default to 8000
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
