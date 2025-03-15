import os
import psycopg2


def test_connection():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "promotions"),
        user=os.getenv("DB_USER", "your_db_user"),
        password=os.getenv("DB_PASSWORD", "your_db_password"),
    )
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    version = cursor.fetchone()
    print("Connected to:", version)
    cursor.close()
    conn.close()


def test_table_exists():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "promotions"),
        user=os.getenv("DB_USER", "your_db_user"),
        password=os.getenv("DB_PASSWORD", "your_db_password"),
    )
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
