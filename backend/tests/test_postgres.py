import os
import psycopg2
from app.core.config import DB_URL  # new import


def test_connection():
    conn = psycopg2.connect(DB_URL)
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    version = cursor.fetchone()
    print("Connected to:", version)
    cursor.close()
    conn.close()


def test_table_exists():
    conn = psycopg2.connect(DB_URL)
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_name = 'promotions'
        );
    """
    )
    exists = cursor.fetchone()[0]
    if exists:
        print("Table 'promotions' exists.")
    else:
        print("Table 'promotions' does not exist.")
    cursor.close()
    conn.close()


if __name__ == "__main__":
    test_connection()
    test_table_exists()
