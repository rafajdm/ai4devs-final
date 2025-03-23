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