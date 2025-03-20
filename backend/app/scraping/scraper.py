import os
import requests
import json
from bs4 import BeautifulSoup, Tag  # modified import
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time  # Add this import
from typing import Optional  # add this import if not already present
from typing import cast  # ensure cast is imported
import psycopg2  # new import for database storage
from app.core.config import DB_URL  # new import

# Configure logging to output debug messages to the console
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

TARGET_URL = "https://banco.santander.cl/beneficios"


def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # Update the chromedriver path to the one installed in the container
    service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


def store_promotions(promos):
    try:
        conn = psycopg2.connect(DB_URL)
        with conn:
            with conn.cursor() as cur:
                # Create table if it does not exist
                cur.execute(
                    """
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
                    )
                    """
                )
                for promo in promos:
                    cur.execute(
                        """
                        INSERT INTO promotions (
                            restaurant_name, 
                            logo_path, 
                            applicable_days_text, 
                            discount_rate, 
                            address, 
                            valid_from, 
                            valid_until, 
                            valid_period_text, 
                            source, 
                            region, 
                            ai_summary
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """,
                        (
                            promo.get("restaurant_name"),
                            promo.get("logo_path"),
                            promo.get("applicable_days_text"),
                            None,  # discount_rate
                            promo.get("address"),
                            None,  # valid_from
                            None,  # valid_until
                            promo.get("valid_period_text"),
                            promo.get("source"),
                            promo.get("region"),
                            None,  # ai_summary
                        ),
                    )
                conn.commit()
    except Exception as e:
        logging.error(f"Database error: {e}")


def scrape_santander_promotions():
    logging.info("Starting the scraper, accessing website...")
    driver = setup_driver()
    driver.get(TARGET_URL)
    logging.info(f"Accessed website: {TARGET_URL}")

    try:
        logging.info("Clicking on the 'Sabores' category...")
        sabores_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "div.cat-nav-item.cat-sabores")
            )
        )
        sabores_button.click()
        logging.info("Clicked 'Sabores'")
        time.sleep(1.5)  # Add delay after click

        # Wait for the page to load after clicking
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.row.total.mini"))
        )

        page_source = driver.page_source
    except Exception as e:
        logging.error(f"Error interacting with the page: {e}")
        driver.quit()
        return

    # Parse the page content with BeautifulSoup
    soup = BeautifulSoup(page_source, "html.parser")
    main_div = soup.find("div", class_="row total mini")
    if not main_div or not isinstance(main_div, Tag):
        logging.warning("Main div not found or invalid. Check the URL and selectors.")
        driver.quit()
        return

    promos = main_div.select("div.discount.border-full")
    if not promos:
        logging.warning("No promotions found. Check the URL and selectors.")
        driver.quit()
        return

    logging.info(f"Looping for {len(promos)} promotions")
    results = []
    for idx, promo in enumerate(promos, start=1):
        logging.info(f"Getting promotion {idx}...")
        # -- Image capture block using Selenium --
        try:
            # Locate the image element for the current promotion using its index
            img_element = driver.find_element(
                By.XPATH,
                f"(//div[contains(@class, 'discount border-full')]//figure//img)[{idx}]",
            )
            screenshot_path = os.path.join(
                "scraped_data/logos", img_element.get_attribute("src").split("/")[-1]
            )
            img_element.screenshot(screenshot_path)
            logo_path = screenshot_path
            logging.info(
                f"Promotion {idx}: Image captured via Selenium screenshot: {screenshot_path}"
            )
        except Exception as e:
            logging.error(f"Promotion {idx}: Failed to capture image via Selenium: {e}")
            logo_path = "No logo"

        # -- Text extraction block --
        # Use a CSS selector to target the div with multiple classes that contains the text data
        text_div = promo.select_one("div.d-flex.flex-column.justify-content-center")
        if text_div:
            p_tags = text_div.find_all("p")
            restaurant_name = (
                p_tags[0].get_text(strip=True) if len(p_tags) > 0 else "No name"
            )
            applicable_days_text = (
                p_tags[1].get_text(strip=True) if len(p_tags) > 1 else "No dates"
            )
            if len(p_tags) > 2:
                spans = p_tags[2].find_all("span")
                # The second span contains the region text
                region = (
                    spans[1].get_text(strip=True) if len(spans) > 1 else "No region"
                )
            else:
                region = "No region"
        else:
            restaurant_name = "No name"
            applicable_days_text = "No dates"
            region = "No region"
        logging.info(f"Promotion {idx}: Scraping preview")

        # Replace interactive click using BeautifulSoup with Selenium's method:
        try:
            mas_info_button = driver.find_element(
                By.XPATH,
                f"(//div[contains(@class, 'discount-btn-mas-info')]//p[contains(text(), 'Más información')])[{idx}]",
            )
            # Scroll the element into view
            driver.execute_script("arguments[0].scrollIntoView(true);", mas_info_button)
            time.sleep(0.5)  # Small delay to let scrolling finish
            # Use JavaScript to click the button instead
            driver.execute_script("arguments[0].click();", mas_info_button)
            logging.info(f"Promotion {idx}: Scraping detail")
            time.sleep(1.5)  # Add delay after click

            # Wait for the overlay to appear
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "detail-promo"))
            )
            logging.info(f"Promotion {idx}: Detail overlay found")

            detail_promo = driver.find_element(By.ID, "detail-promo")

            # Extract address from the third <li> inside the description div
            description_div = detail_promo.find_element(By.CLASS_NAME, "description")
            li_elements = description_div.find_elements(By.TAG_NAME, "li")
            address = li_elements[2].text if len(li_elements) >= 3 else "No address"

            # Extract valid_period_text from the <p> element with class 'bg-primary-sky'
            valid_period_element = detail_promo.find_element(
                By.CSS_SELECTOR, "p.bg-primary-sky"
            )
            valid_period_text = valid_period_element.text.replace(
                "Vigencia:", ""
            ).strip()

            # Wait for the close button to be clickable and then click it
            close_button = WebDriverWait(detail_promo, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".close.cursor-pointer"))
            )
            close_button.click()
            time.sleep(1.5)  # Add delay after click
            logging.info(f"Promotion {idx}: Closed detail")
        except Exception as e:
            logging.error(f"Error extracting additional data: {e}")
            address = "No address"
            valid_period_text = "No valid period"

        promo_data = {
            "restaurant_name": restaurant_name,
            "logo_path": logo_path,
            "applicable_days_text": applicable_days_text,
            "region": region,
            "address": address,
            "valid_period_text": valid_period_text,
            "source": "Santander Chile",
        }
        results.append(promo_data)
        break  # Remove this line to scrape all promotions

    driver.quit()
    logging.info(f"Finishing up, extracted {len(results)} promotion(s).")
    if results:
        store_promotions(results)  # store promotions in DB
        logging.info(f"Stored {len(results)} promotion(s) into the database.")

        # Export promotions to a JSON file
        json_folder = "scraped_data/santander"
        if not os.path.exists(json_folder):
            os.makedirs(json_folder)
        json_file = os.path.join(json_folder, "promotions.json")
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=4)
        logging.info(f"Exported promotions to {json_file}")

        for idx, promo in enumerate(results, 1):
            logging.info(f"{idx}. {promo['restaurant_name']} - {promo['logo_path']}")
    else:
        logging.info(
            "No promotions extracted. Verify the page structure and selectors."
        )


if __name__ == "__main__":
    scrape_santander_promotions()
