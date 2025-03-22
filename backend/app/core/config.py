# App-wide configuration settings
import os

# Construct DB_URL from individual env variables if not already set
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "dbname")
DB_USER = os.getenv("DB_USER", "user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_URL = os.getenv(
    "DB_URL", f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"
)

# New block: use Cloud SQL socket if CLOUD_SQL_CONNECTION_NAME is provided (production)
CLOUD_SQL_CONNECTION_NAME = os.getenv("CLOUD_SQL_CONNECTION_NAME", None)
if CLOUD_SQL_CONNECTION_NAME:
    DB_URL = os.getenv(
        "DB_URL",
        f"postgresql://{DB_USER}:{DB_PASSWORD}@/{DB_NAME}?host=/cloudsql/{CLOUD_SQL_CONNECTION_NAME}",
    )

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY", "")

# NOTE: Database interactions now use psycopg2 with raw SQL queries.
# ... other configuration constants
