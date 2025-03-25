import json
import logging
import psycopg2
import requests
import time
import re
from datetime import datetime
from langgraph.graph import StateGraph
from fastapi import APIRouter
from app.core import config  # adjust import as needed
from typing import TypedDict


class AIProcessState(TypedDict):
    applicable_days_text: str
    valid_period_text: str
    parsed_text: str
    discount_rate: str
    days_of_week: list[int]
    valid_from: str
    valid_until: str


logging.basicConfig(level=logging.INFO)

router = APIRouter(prefix="/ai-process", tags=["ai-process"])  # prefix stays as is


# Regex for extracting dates
DATE_PATTERN = r"(\d{1,2} de [a-zA-Z]+ de \d{4})"

# Mapping of Spanish month names to their numerical equivalents
MONTHS_MAP = {
    "enero": "01",
    "febrero": "02",
    "marzo": "03",
    "abril": "04",
    "mayo": "05",
    "junio": "06",
    "julio": "07",
    "agosto": "08",
    "septiembre": "09",
    "octubre": "10",
    "noviembre": "11",
    "diciembre": "12",
}


def parse_dates(text):
    """Extracts and formats dates from text"""
    # Replace Spanish month names with numerical equivalents
    for month, num in MONTHS_MAP.items():
        text = text.replace(month, num)

    matches = re.findall(DATE_PATTERN, text)
    formatted_dates = []

    for match in matches:
        try:
            parsed_date = datetime.strptime(match, "%d de %m de %Y")
            formatted_dates.append(parsed_date.strftime("%Y-%m-%d"))
        except ValueError:
            logging.warning(f"Failed to parse date: {match}")

    if len(formatted_dates) >= 2:
        return formatted_dates[0], formatted_dates[1]  # valid_from, valid_until
    return "N/A", "N/A"


# Define LangGraph processing steps
def parse_text(state):
    """Function to parse input text"""
    if not state.get("applicable_days_text") or not state.get("valid_period_text"):
        logging.warning("Missing input text fields.")
        return None

    parsed_text = f"{state['applicable_days_text']} {state['valid_period_text']}"
    valid_from, valid_until = parse_dates(parsed_text)

    logging.info(
        f"Parsed text: {parsed_text}, Extracted Dates: {valid_from} - {valid_until}"
    )

    return {
        "parsed_text": parsed_text,
        "valid_from": valid_from,
        "valid_until": valid_until,
    }


def extract_promotion_details(response_text):
    """Extract structured details directly from the JSON response."""
    logging.info("Received response text for extraction.")

    # Extract JSON block if it's wrapped in markdown-style formatting
    json_block_match = re.search(r"```json\s*(\{.*?\})\s*```", response_text, re.DOTALL)
    if json_block_match:
        response_text = json_block_match.group(1).strip()

    logging.info("Extracted JSON block from response: %s", response_text)

    try:
        structured_data = json.loads(response_text)
        logging.info("Extracted structured data: %s", structured_data)

        # Convert days_of_week to numerical representation
        day_mapping = {
            "sunday": 0,
            "monday": 1,
            "tuesday": 2,
            "wednesday": 3,
            "thursday": 4,
            "friday": 5,
            "saturday": 6,
        }
        days_text = structured_data.get("days_of_week", "").lower()
        days_numbers = sorted(
            {
                day_mapping[day.strip()]
                for day in days_text.split(",")
                if day.strip() in day_mapping
            }
        )

        return {
            "discount_rate": structured_data.get("discount_rate", "N/A"),
            "days_of_week": days_numbers if days_numbers else "N/A",
            "valid_from": structured_data.get("valid_from", "N/A"),
            "valid_until": structured_data.get("valid_until", "N/A"),
        }
    except json.JSONDecodeError:
        logging.error(
            "Failed to parse structured response from Mistral. Raw response: %s",
            response_text,
        )
        return {
            "discount_rate": "N/A",
            "days_of_week": "N/A",
            "valid_from": "N/A",
            "valid_until": "N/A",
        }


def call_mistral(state):
    """Function to call Mistral API with updated parameters and extract structured data."""
    if "parsed_text" not in state:
        logging.error("Parsed text missing from state.")
        return state  # Return state to ensure LangGraph continuity

    api_url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {config.MISTRAL_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "mistral-small-2503",
        "messages": [
            {
                "role": "user",
                "content": (
                    f"Extract the structured details from the following text. "
                    f"Provide the discount percentage, days of the week as a comma-separated list (e.g., 'monday, tuesday'), "
                    f"and the validity period in ISO 8601 format (yyyy-MM-dd). "
                    f"Here is the text:\n\n{state['parsed_text']}\n\n"
                    f"Return the output in JSON format like this:\n"
                    f'{{"discount_rate": "X%", "days_of_week": "monday, tuesday", "valid_from": "yyyy-MM-dd", "valid_until": "yyyy-MM-dd"}}'
                ),
            }
        ],
        "max_tokens": 200,
        "temperature": 0.0,
    }

    time.sleep(1)  # Reduce delay to 1 second

    try:
        logging.info("Calling Mistral API with payload: %s", payload)
        response = requests.post(api_url, json=payload, headers=headers)

        if response.status_code == 200:
            result = response.json()
            logging.info("Mistral API raw response: %s", result)

            if "choices" in result and len(result["choices"]) > 0:
                message_content = result["choices"][0]["message"]["content"]
                structured_data = extract_promotion_details(message_content)

                if structured_data:
                    logging.info("Extracted structured data: %s", structured_data)

                    # **Ensure only structured data is returned as final output**
                    return structured_data

        logging.error("Mistral API request failed: %s", response.text)
        return state  # Return the original state to prevent LangGraph failures
    except Exception as e:
        logging.error("Error calling Mistral API: %s", e, exc_info=True)
        return state  # Ensure state is always returned


# Define LangGraph workflow
graph = StateGraph(state_schema=AIProcessState)
graph.add_node("parse_text", parse_text)
graph.add_node("call_mistral", call_mistral)
graph.set_entry_point("parse_text")
graph.add_edge("parse_text", "call_mistral")

# Ensure LangGraph properly collects and returns the response
graph.set_finish_point(
    "call_mistral"
)  # This should now return structured data correctly

# Compile LangGraph client
langgraph_client = graph.compile()


def call_mistral_api(applicable_days_text: str, valid_period_text: str) -> dict:
    """Uses LangGraph to extract structured data from text input"""
    if not applicable_days_text or not valid_period_text:
        logging.warning("Invalid input to call_mistral_api.")
        return {"error": "Invalid input data."}

    query = {
        "applicable_days_text": applicable_days_text,
        "valid_period_text": valid_period_text,
    }

    logging.info("Sending query to LangGraph: %s", query)
    try:
        response = langgraph_client.invoke(query)
        if response:
            logging.info(
                "LangGraph extracted data: %s",
                json.dumps(response, indent=4, ensure_ascii=False),
            )
            return response  # Ensure the extracted data is correctly returned
        else:
            logging.warning("LangGraph returned no structured data.")
            return {}
    except Exception as e:
        logging.error("Error in LangGraph processing: %s", e, exc_info=True)
        return {}


@router.post("")
def process_ai():
    """Processes promotions using LangGraph and updates the database with AI response."""
    logging.info("Starting AI processing.")

    try:
        with psycopg2.connect(config.DB_URL) as conn:
            with conn.cursor() as cur:
                # Fetch all promotions without an AI summary (removing limit)
                cur.execute(
                    "SELECT id, applicable_days_text, valid_period_text FROM promotions WHERE ai_summary IS NULL;"
                )
                promotions = cur.fetchall()
                logging.info("Fetched %d promotions.", len(promotions))

                for promotion_id, applicable_days_text, valid_period_text in promotions:
                    logging.info("Processing promotion ID: %s", promotion_id)
                    result = call_mistral_api(applicable_days_text, valid_period_text)

                    if result:
                        logging.info(
                            "AI extracted data: %s",
                            json.dumps(result, indent=4, ensure_ascii=False),
                        )

                        # Convert days_of_week list to a comma-separated string
                        days_of_week_str = ",".join(
                            map(str, result.get("days_of_week", []))
                        )

                        # Update database with AI processed data
                        cur.execute(
                            """
                            UPDATE promotions
                            SET discount_rate = %s,
                                days_of_week = %s,
                                valid_from = %s,
                                valid_until = %s,
                                ai_summary = %s
                            WHERE id = %s;
                            """,
                            (
                                result.get("discount_rate"),
                                days_of_week_str,
                                result.get("valid_from"),
                                result.get("valid_until"),
                                json.dumps(result, ensure_ascii=False),
                                promotion_id,
                            ),
                        )
                        conn.commit()
                        logging.info(
                            "Updated promotion ID %s in database.", promotion_id
                        )

                    time.sleep(1)  # Reduce API delay to 1 second

                return {"message": "Processed and updated all promotions."}

    except Exception as e:
        logging.error("Error processing AI: %s", e, exc_info=True)
        return {"error": "An error occurred during AI processing."}


@router.post("/{promotion_id}")
def process_single_promotion(promotion_id: int):
    """Processes a single promotion using LangGraph and updates the database."""
    logging.info(f"Starting AI processing for promotion ID: {promotion_id}")

    try:
        with psycopg2.connect(config.DB_URL) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT applicable_days_text, valid_period_text FROM promotions WHERE id = %s;",
                    (promotion_id,),
                )
                result = cur.fetchone()

                if not result:
                    return {"error": "Promotion not found"}

                applicable_days_text, valid_period_text = result
                result = call_mistral_api(applicable_days_text, valid_period_text)

                if result:
                    days_of_week_str = ",".join(
                        map(str, result.get("days_of_week", []))
                    )

                    cur.execute(
                        """
                        UPDATE promotions
                        SET discount_rate = %s,
                            days_of_week = %s,
                            valid_from = %s,
                            valid_until = %s,
                            ai_summary = %s
                        WHERE id = %s;
                        """,
                        (
                            result.get("discount_rate"),
                            days_of_week_str,
                            result.get("valid_from"),
                            result.get("valid_until"),
                            json.dumps(result, ensure_ascii=False),
                            promotion_id,
                        ),
                    )
                    conn.commit()
                    return {"message": f"Updated promotion ID {promotion_id}"}

                return {"error": "Failed to process promotion"}

    except Exception as e:
        logging.error("Error processing AI: %s", e, exc_info=True)
        return {"error": "An error occurred during AI processing."}
