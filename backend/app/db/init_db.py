import psycopg2
from dotenv import load_dotenv
from app.core.config import DB_URL  # new import for unified DB URL

# Load environment variables from .env file
load_dotenv()

# SQL statement to create the promotions table
create_table_query = """
CREATE TABLE IF NOT EXISTS promotions (
    id SERIAL PRIMARY KEY,
    restaurant_name VARCHAR NOT NULL,
    logo_path VARCHAR,
    applicable_days_text VARCHAR,
    discount_rate VARCHAR,
    address VARCHAR,
    valid_from DATE,
    valid_until DATE,
    valid_period_text VARCHAR,
    source VARCHAR NOT NULL,
    region VARCHAR,
    ai_summary TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""


def init_db():
    try:
        # Use DB_URL from config.py
        connection = psycopg2.connect(DB_URL)
        cursor = connection.cursor()
        cursor.execute(create_table_query)
        connection.commit()
        print("Table 'promotions' created successfully or already exists.")
    except Exception as error:
        print(f"Error while creating table: {error}")
    finally:
        if connection:
            cursor.close()
            connection.close()


if __name__ == "__main__":
    load_dotenv()  # ensure env variables are loaded
    init_db()
