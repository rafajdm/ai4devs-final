# App-wide configuration settings
import os

# Construct DB_URL from individual env variables if not already set
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "dbname")
DB_USER = os.getenv("DB_USER", "user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
# Updated connection string format
DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY", "")

# NOTE: Database interactions now use psycopg2 with raw SQL queries.
# ... other configuration constants
