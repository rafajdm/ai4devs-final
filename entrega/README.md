## Índice

0. [Ficha del proyecto](#0-ficha-del-proyecto)
1. [Descripción general del producto](#1-descripción-general-del-producto)
2. [Arquitectura del sistema](#2-arquitectura-del-sistema)
3. [Modelo de datos](#3-modelo-de-datos)
4. [Especificación de la API](#4-especificación-de-la-api)
5. [Historias de usuario](#5-historias-de-usuario)
6. [Tickets de trabajo](#6-tickets-de-trabajo)
7. [Pull requests](#7-pull-requests)

---

## 0. Ficha del proyecto

### **0.1. Tu nombre completo:**

    Rafael Jose Diaz Martinez

### **0.2. Nombre del proyecto:**

    Promo-finder MVP

### **0.3. Descripción breve del proyecto:**

    Promo-finder MVP es una aplicación ligera diseñada para recopilar promociones desde el sitio web de una institución financiera. El sistema utiliza un agente de inteligencia artificial para procesar y resumir la información, presentando los resultados a través de una interfaz minimalista en React. Además, se aprovecha un entorno dockerizado para simplificar la configuración y ejecución tanto en desarrollo local como en despliegues.

### **0.4. URL del proyecto:**

El proyecto se ha desplegado en Google Cloud Run, por lo que la URL principal para la aplicación frontend (React) es algo como:

```
https://promo-finder-frontend-xxxxx.run.app
```

El backend (FastAPI) se encuentra igualmente en Cloud Run, con una URL tipo:

```
https://promo-finder-backend-xxxxx.run.app
```

### 0.5. URL o archivo comprimido del repositorio

> URL del repositorio: [https://github.com/rafajdm/ai4devs-final](https://github.com/rafajdm/ai4devs-final)

---

## 1. Descripción general del producto

### **1.1. Objetivo:**

    El objetivo central del proyecto es automatizar la recolección de promociones desde el sitio web de instituciones financieras chilena, procesarlas con ayuda de IA (para resúmenes de texto o normalización de datos) y exhibirlas de manera clara al usuario final.
    Para este MVP se considerara una institución únicamente y se realizaran los procesos de manera manual.

### **1.2. Características y funcionalidades principales:**

    1. Scraping o bajo demanda de la web de la institución.
    2. Almacenamiento estructurado en PostgreSQL.
    3. Procesamiento con IA (Estructurar data desestructurada).
    4. Presentación de la información en un frontend sencillo, con tarjetas de promociones.
    5. Despliegue dockerizado en GCP (Cloud Run) con base de datos en Neon.tech

### **1.3. Diseño y experiencia de usuario:**

    - El usuario accede a un panel (React) donde se listan las promociones.
    - Cada promoción muestra datos clave (descuento, nombre, fechas, dirección, etc.).
    - No se requiere autenticación en el MVP.
    - El diseño usa Tailwind CSS para un estilo rápido y minimalista.

### **1.4. Instrucciones de instalación:**

    1. Local con Docker Compose:
        - Clonar el repositorio, crear un archivo .env con credenciales de DB y API keys.
        - Ejecutar docker-compose up --build.
        - Acceder a http://localhost:80 para el frontend y http://localhost:8000 para el backend (si los mapeos se definieron así).
    2. Despliegue en GCP:
        - Construir imágenes y subirlas a Artifact Registry.
        - Desplegar en Cloud Run con gcloud run deploy ....

---

## 2. Arquitectura del Sistema

### **2.1. Diagrama de arquitectura:**

    A alto nivel:
    - React Frontend → Docker Container en Cloud Run → (peticiones a) FastAPI Backend → (conexión) PostgreSQL en hosting de preferencia.
    - Un módulo de scraping en el backend (Playwright, etc.) se dispara a petición para extraer datos.

### **2.2. Descripción de componentes principales:**

    1. Backend (FastAPI): define endpoints /scrape, /promotions, /ai-process.
    2. Scraping: Módulo que usa Playwright para acceder al sitio, parsear HTML, guardar datos.
    3. AI: Integración con un API de NLP o un modelo (LangGraph + Mistral) para estructurar datos desestructurados.
    4. DB (PostgreSQL): Alojada en Neon Tech (opcionalmente local con Docker Compose).
    5. Frontend (React + Tailwind): UI minimalista que consume la API del backend.

### **2.3. Descripción de alto nivel del proyecto y estructura de ficheros**

    - backend/: Contiene la lógica de FastAPI, scraping, AI, etc.
    - frontend/: Código React.
    - docs/: Documentos de arquitectura, especificaciones, user stories, etc.
    - docker-compose.yml: Orquestación local.
    - Dockerfiles separados para backend y frontend.

### **2.4. Infraestructura y despliegue**

    - Cloud Run para el frontend y backend.
    - Neon Tech free tier para base de datos.
    - Artifact Registry para almacenar imágenes Docker.
    - Variables de entorno en Cloud Run para credenciales y URLs.

### **2.5. Seguridad**

    1. HTTPS nativo en Cloud Run.
    2. No exponer credenciales en el código. Usar variables de entorno.
    3. CORS para limitar origen de peticiones al dominio del frontend.
    4. Scraping: Minimizar la frecuencia y no exceder TOS del sitio.

### **2.6. Tests**

    - Backend: Pruebas unitarias en scraping, AI mock, endpoints de FastAPI. (Por desarrollar)
    - Frontend: Tests de componentes con Jest/React Testing Library y uno o dos tests end-to-end con Cypress. (Por desarrollar)
    - Seguridad: Verificar HTTP -> HTTPS, no exponer secrets.

---

## 3. Modelo de Datos

### **3.1. Diagrama del modelo de datos:**

```
erDiagram
    promotions {
        SERIAL id PK "Unique promotion ID"
        VARCHAR restaurant_name "Name of the restaurant (NOT NULL)"
        VARCHAR logo_path "Path to the restaurant’s logo image"
        VARCHAR applicable_days_text "Plain string for applicable days"
        VARCHAR discount_rate "Promotion discount (e.g., '20%')"
        VARCHAR address "Address or location of the restaurant"
        DATE valid_from "Promotion start date"
        DATE valid_until "Promotion end date"
        VARCHAR valid_period_text "Textual representation of the valid period"
        VARCHAR source "e.g., 'Santander Chile' (NOT NULL)"
        VARCHAR region "Region of the promotion"
        TEXT ai_summary "Generated text from the AI agent"
        TIMESTAMP created_at "Timestamp of insertion"
        VARCHAR days_of_week "Applicable days of the week"
    }
```

### **3.2. Descripción de entidades principales:**

    - Promotions: Almacena la info de cada promoción (nombre, descuento, fechas, etc.).

---

## 4. Especificación de la API

Endpoints principales:

    1. GET /promotions
        - Retorna la lista de promociones en JSON.
    2. POST /scrape
        - Dispara la lógica de scraping (Playwright) y guarda nuevas promos en la DB.
    3. POST /ai-process
        - Llama al servicio de IA para generar ai_summary en cada promo y desestructurar datos.

---

## 5. Historias de Usuario

    1. Scraping & Data Ingestion
        - “Como admin, quiero iniciar un scrape manual… para recopilar datos.”
    2. Visualizar Promociones
        - “Como usuario, quiero ver todas las promociones de forma sencilla…”
    3. AI Summaries
        - “Como usuario, quiero leer un breve resumen de la promoción…”

---

## 6. Tickets de Trabajo

    1. Backend: “Implementar módulo de scraping con Playwright”
    2. Frontend: “Mostrar lista de promociones en tarjetas con React + Tailwind”
    3. Base de datos: “Crear tabla promotions, diseñar migración, etc.”

---

## 7. Pull Requests

**Pull Request 1**

No realizada.

**Pull Request 2**

No realizada.

**Pull Request 3**

No realizada.
