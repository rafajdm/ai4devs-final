import os
import psycopg2
from app.core.config import DB_URL  # new import


def get_promotions(page: int, page_size: int):
    offset = (page - 1) * page_size
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    query = """
    SELECT id, restaurant_name, logo_path, applicable_days_text, discount_rate, address,
           valid_from, valid_until, valid_period_text, source, region, ai_summary, created_at
    FROM promotions
    ORDER BY created_at DESC
    OFFSET %s LIMIT %s
    """
    cur.execute(query, (offset, page_size))
    rows = cur.fetchall()
    promotions = []
    for row in rows:
        promotions.append({
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
        })
    cur.close()
    conn.close()
    return promotions
