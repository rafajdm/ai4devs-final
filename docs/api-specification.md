# Promo-Finder MVP API Specification

This document describes the available API endpoints for the Promo-Finder MVP.

---

## Overview

The API is built with **FastAPI** and serves three core endpoints:

1. **`/promotions`**
2. **`/scrape`**
3. **`/ai-process`**

Below is a detailed description of each, including methods, expected payloads, and sample responses.

---

## 1. `/promotions`

### **Endpoint**

```
GET /promotions
```

### **Description**

Returns a list of stored promotions from the database, possibly including AI-generated summaries.

### **Request Parameters**

None (for the MVP, there is no pagination, filtering, or sorting).

### **Response** (example for `GET /promotions`)

- **Status 200**: Each promotion object includes:
  - `id`, `restaurant_name`, `days_of_week`, `ai_summary`, etc.

### **Example Response**

```json
[
  {
    "id": 1,
    "restaurant_name": "Sample Restaurant",
    "logo_path": "/images/sample-logo.png",
    "applicable_days_text": "Mon-Fri",
    "discount_rate": "20%",
    "address": "123 Main St, Santiago",
    "valid_from": "2025-03-08",
    "valid_until": "2025-03-31",
    "valid_period_text": "Valid throughout March",
    "source": "Santander Chile",
    "region": "Metropolitana",
    "created_at": "2025-03-07T10:15:30",
    "days_of_week": "1,2,3",
    "ai_summary": "AI-processed description or details"
  }
]
```

---

## 2. `/scrape`

### **Endpoint**

```
POST /scrape
```

### **Description**

Manually triggers the scraping process for the target website (<https://banco.santander.cl/beneficios>), parses the promotional data, and stores the results in the database.

### **Request Body**

None (the MVP does not require additional parameters to start the scrape).

### **Response**

- **Status 200**: Scrape triggered successfully. The response may include a simple confirmation message.
- **Status 500**: If the scraping process encounters an error.

### **Example Response**

```json
{
  "message": "Scraping initiated. Check logs or /promotions to see new data."
}
```

---

## 3. `/ai-process`

### **Endpoint**

```
POST /ai-process
```

### **Description**

`POST /ai-process` finalizes complex parsing via AI, storing results in fields like `ai_summary` and updating relevant columns (e.g., `days_of_week`).

### **Request Body**

None (MVP does not specify partial AI processing — it processes all unprocessed promotions).

### **Response**

- **Status 200**: AI processing triggered successfully. May include a result count of updated promotions.
- **Status 500**: If the AI processing encounters an error.

### **Example Response**

```json
{
  "message": "AI processing completed.",
  "processed_count": 12
}
```

---

## Error Handling

| Error Code | Description                                      |
| ---------- | ------------------------------------------------ |
| 400        | Bad Request - Usually malformed input            |
| 404        | Not Found - Invalid endpoint or resource missing |
| 500        | Internal Server Error - Uncaught server errors   |

## Authentication & Security (MVP)

- There is **no authentication** in this MVP.
- For a production environment, consider adding API keys or other secure mechanisms.

## Further Extensions

1. **Pagination & Filtering** on `/promotions`
2. **Partial scraping** for different sub-pages or institutions
3. **AI customization** (handling only certain promotion IDs, etc.)
4. **User accounts** and advanced **security features**

---

## Conclusion

This **API specification** outlines the key endpoints for scraping promotions, retrieving stored promotion data, and performing basic AI-driven text processing. The MVP design intentionally keeps endpoints and request/response structures simple, with room for growth in future versions.
