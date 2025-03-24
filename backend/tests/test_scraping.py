import os
import pytest
from bs4 import BeautifulSoup
import logging  # added logging

logging.basicConfig(level=logging.INFO)  # added logging configuration

from app.scraping.scraper import (
    extract_promotions_from_html,
    extract_promotion_detail_from_html,
)


# Test for the base layout using the local santander.html asset
def test_extract_promotions_base():
    asset_path = os.path.join(
        os.path.dirname(__file__), "assets", "santander_base", "santander.html"
    )
    logging.info("Loading base asset from %s", asset_path)  # logging added
    with open(asset_path, "r", encoding="utf-8") as f:
        html = f.read()
    soup = BeautifulSoup(html, "html.parser")
    promotions = extract_promotions_from_html(soup)
    # Assert that at least one promotion was extracted and key fields exist
    assert isinstance(promotions, list)
    assert len(promotions) > 0
    for promo in promotions:
        assert "restaurant_name" in promo
        assert promo["restaurant_name"] != "No name"


# Test for the detail layout using the local santander_detail.html asset
def test_extract_promotion_detail():
    asset_path = os.path.join(
        os.path.dirname(__file__), "assets", "santander_detail", "santander_detail.html"
    )
    logging.info("Loading detail asset from %s", asset_path)  # logging added
    with open(asset_path, "r", encoding="utf-8") as f:
        html = f.read()
    soup = BeautifulSoup(html, "html.parser")
    detail = extract_promotion_detail_from_html(soup)
    # Assert that detail extraction returns non-default values for address and validity
    assert "address" in detail
    assert detail["address"] != "No address"
    assert "valid_period_text" in detail
    assert detail["valid_period_text"] != "No valid period"
