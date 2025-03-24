# Project Name

## Description

Promo-Finder MVP is a lightweight application designed to automatically collect promotions from a specific financial institution’s website, process them with an AI agent, and present the results in a minimal React interface. The goal is to demonstrate an end-to-end solution for web scraping, structured data storage, AI-based text summaries, and a simple web front end.

## Folder Structure

A detailed overview of the recommended folder structure and its rationale can be found in the [architectural-pattern.md](./docs/architectural-pattern.md) document. There, you'll see how the backend, frontend, and supporting files are organized, along with an explanation of the layered modular monolith pattern.

## Setting up for Local Development

This section explains how to run the project locally using Docker Compose.

### 1. Prerequisites

1. Have Docker and Docker Compose installed.
2. Clone the repository and navigate to the project root (where `docker-compose.yml` resides).
3. (Optional) Create a `.env` file with environment variables needed for the backend and database.

```env
# Database credentials
DB_HOST=dbhost
DB_NAME=dbname
DB_USER=dbuser
DB_PASSWORD=dbpassword

# Mistral API keys
MISTRAL_API_KEY=apikey
```

### 2. Starting Services

1. Open a terminal in the project root.
2. Run:
   ```bash
   docker-compose up --build
   ```
   - This command builds images for `backend` and `frontend`, pulls the `postgres` image, and starts all containers.
3. Wait for containers to finish starting. Logs will show when services are up.

### 3. Accessing the Application

- **Backend**: Typically accessible at `http://localhost:8000` (or the port specified in your `docker-compose.yml`).
- **Frontend**: Often served at `http://localhost:80` (or another mapped port).
- **Database**: Postgres runs in its own container, so you can connect via `postgres://<user>:<password>@localhost:<mapped_port>/<database>` if needed.

### 4. Stopping Services

Press `Ctrl + C` in the same terminal window to stop containers, or run:

```bash
docker-compose down
```

This ensures everything shuts down cleanly.

## Running Tests

To execute tests in a dockerized environment with logging enabled, run:

```bash
docker-compose run backend pytest --capture=tee-sys --log-cli-level=INFO
```

## Usage

TBD

## Deployment to Google Cloud Run

Below is a quick overview of how to deploy your Dockerized **backend** and **frontend** containers to Google Cloud Run.

### 1. Backend Container

1. **Build** the Docker image (use `--platform=linux/amd64` if on Apple Silicon):
   ```bash
   cd backend
   docker build --platform=linux/amd64 -t promo-finder-backend:latest .
   ```
2. **Tag** the image for Artifact Registry (example using `us-central1`):
   ```bash
   docker tag promo-finder-backend:latest \
       us-central1-docker.pkg.dev/YOUR_PROJECT_ID/promo-finder-repo/promo-finder-backend:latest
   ```
3. **Push** to Artifact Registry:
   ```bash
   docker push us-central1-docker.pkg.dev/YOUR_PROJECT_ID/promo-finder-repo/promo-finder-backend:latest
   ```
4. **Deploy** to Cloud Run:
   ```bash
   gcloud run deploy promo-finder-backend \
       --image us-central1-docker.pkg.dev/YOUR_PROJECT_ID/promo-finder-repo/promo-finder-backend:latest \
       --platform managed \
       --region us-central1 \
       --allow-unauthenticated \
       --set-env-vars DB_HOST=ep-dbhost,DB_NAME=dbname,DB_USER=dbuser,DB_PASSWORD=dbpassword,MISTRAL_API_KEY=mistralapikey,FRONTEND_URL=frontendurl
   ```

### 2. Frontend Container

1. **Build** the Docker image:
   ```bash
   cd frontend
   docker build --platform=linux/amd64 -t promo-finder-frontend:latest .
   ```
2. **Tag** the image:
   ```bash
   docker tag promo-finder-frontend:latest \
       us-central1-docker.pkg.dev/YOUR_PROJECT_ID/promo-finder-repo/promo-finder-frontend:latest
   ```
3. **Push** to Artifact Registry:
   ```bash
   docker push us-central1-docker.pkg.dev/YOUR_PROJECT_ID/promo-finder-repo/promo-finder-frontend:latest
   ```
4. **Deploy** to Cloud Run:
   ```bash
   gcloud run deploy promo-finder-frontend \
       --image us-central1-docker.pkg.dev/YOUR_PROJECT_ID/promo-finder-repo/promo-finder-frontend:latest \
       --platform managed \
       --region us-central1 \
       --allow-unauthenticated
   ```

> **Note**: Ensure each container listens on `$PORT` (often 8080) so Cloud Run’s health checks pass.

---

## Contributing

Guidelines for contributing to the project.

## License

Information about the project's license.
