# Backend

## Description
This directory contains the backend code for the Promo-Finder MVP. It includes the web scraping logic, data processing, and database interactions.

## Setup

### Prerequisites
- Python 3.8+
- Docker (for containerized execution)
- Google Chrome and ChromeDriver (for Selenium)

### Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/your-repo/ai4devs-final.git
   cd ai4devs-final/backend
   ```

2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   Ensure the `.env` file is present at the root level with the following content:
   ```env
   DB_HOST=your_db_host
   DB_NAME=your_db_name
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   MISTRAL_API_KEY=your_mistral_api_key
   ```

4. **Initialize the database:**
   ```sh
   python init_db.py
   ```

### Running the Scraper

1. **Run the scraper:**
   ```sh
   python scraper.py
   ```

### Dockerized Execution

1. **Build the Docker image:**
   ```sh
   docker build -t promo-finder-backend .
   ```

2. **Run the Docker container:**
   ```sh
   docker run --env-file ../.env promo-finder-backend
   ```

## Files

- `scraper.py`: Contains the web scraping logic.
- `init_db.py`: Initializes the PostgreSQL database.
- `requirements.txt`: Lists the Python dependencies.
- `Dockerfile`: Dockerfile for containerizing the backend.

## License
Information about the project's license.
