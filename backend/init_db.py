import psycopg2
from psycopg2 import sql
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database connection parameters
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

# SQL statement to create the promotions table
create_table_query = """
CREATE TABLE IF NOT EXISTS promotions (
    id SERIAL PRIMARY KEY,
    restaurant_name VARCHAR NOT NULL,
    logo_path VARCHAR NOT NULL,
    valid_dates VARCHAR NOT NULL,
    discount_rate VARCHAR NOT NULL,
    address VARCHAR NOT NULL,
    expiration_date VARCHAR,
    source VARCHAR NOT NULL,
    ai_summary TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""


def init_db():
    try:
        # Connect to PostgreSQL
        connection = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
        )
        cursor = connection.cursor()

        # Execute the create table query
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
    init_db()
