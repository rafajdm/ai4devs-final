import os
import psycopg2
from app.core.config import DB_URL  # new import
import logging


def get_promotions(
    page: int, page_size: int, restaurant_name: str = None, region: str = None
):
    offset = (page - 1) * page_size
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    base_query = """
    SELECT id, restaurant_name, logo_path, applicable_days_text, discount_rate, address,
           valid_from, valid_until, valid_period_text, source, region, ai_summary, created_at,
           days_of_week
    FROM promotions
    """
    filters = []
    params = []
    if restaurant_name:
        filters.append("LOWER(restaurant_name) LIKE %s")
        params.append(f"%{restaurant_name.lower()}%")
    if region:
        filters.append("region ILIKE %s")
        params.append(region)
    if filters:
        base_query += " WHERE " + " AND ".join(filters)
    base_query += " ORDER BY created_at DESC OFFSET %s LIMIT %s"
    params.extend([offset, page_size])
    logging.info(f"Executing query: {base_query} with params: {params}")
    cur.execute(base_query, params)
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
                "days_of_week": row[13],
            }
        )
    cur.close()
    conn.close()
    return promotions


def get_promotion_by_id(promotion_id: int):
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    query = """
    SELECT id, restaurant_name, logo_path, applicable_days_text, discount_rate, address,
           valid_from, valid_until, valid_period_text, source, region, ai_summary, created_at,
           days_of_week
    FROM promotions
    WHERE id = %s
    """
    cur.execute(query, (promotion_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()

    if row is None:
        return None

    return {
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
        "days_of_week": row[13],
    }
