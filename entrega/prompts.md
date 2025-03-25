> Tengo 3 conversaciones muy largas con ChatGPT (4o, o1, o3-mini-high) que fui realizando desde febrero, le pedi que me hiciera un breve resumen para este archivo. No me deja exportar el chat seguramente porque hay imagenes y modificaicones de código usando `Work with visual studio code`. También tengo chats con Copilot 4o, o1 y o3-mini y un chat con DiagramsGPT para generar una arquitectura en imagen utilizando de entrada mi documentación principal [product-overview.md](./docs/product-overview.md). Mi verdadero flujo de trabajo fue conversar con ChatGPT y generar todos los documentos en la carpeta `./docs/` y conforme me fueran surgiendo necesidades utilizar este contexto para generar nuevos documentos que me ayudasen a hacer un plan de implementación para resolverlas. Estos planes de implementación los fui realizando una vez generado el documento con Copilot + Copilot Edits.

## Indice

1. [Descripción general del producto](#1-descripción-general-del-producto)
2. [Arquitectura del Sistema](#2-arquitectura-del-sistema)
   1. [Diagrama de arquitectura](#21-diagrama-de-arquitectura)
   2. [Descripción de componentes principales](#22-descripción-de-componentes-principales)
   3. [Descripción de alto nivel del proyecto y estructura de ficheros](#23-descripción-de-alto-nivel-del-proyecto-y-estructura-de-ficheros)
   4. [Infraestructura y despliegue](#24-infraestructura-y-despliegue)
   5. [Seguridad](#25-seguridad)
   6. [Tests](#26-tests)
3. [Modelo de Datos](#3-modelo-de-datos)
4. [Especificación de la API](#4-especificación-de-la-api)
5. [Historias de Usuario](#5-historias-de-usuario)
6. [Tickets de Trabajo](#6-tickets-de-trabajo)
7. [Pull Requests](#7-pull-requests)

## 1. Descripción general del producto

1. **Prompt:**
   "Organize this starting info and ask me any questions you think you need so we can start debating about it."
   _– Initiated the conversation about project requirements and objectives._

2. **Prompt:**
   "Creating a `Project Requirements` documentation."
   _– Laid the groundwork for detailed requirements._

3. **Prompt:**
   "Your support as a product expert defining this project features and objectives and deciding an MVP scope."
   _– Focused on defining key features and the scope of the MVP._

---

## 2. Arquitectura del Sistema

### **2.1. Diagrama de arquitectura:**

1. **Prompt:**
   "Let's start working on our tech stack document."
   _– Initiated the discussion on choosing the right technology stack._

2. **Prompt:**
   "Is Python our preferred language for this project? Let's discuss our scraping options considering also optimizing resources."
   _– Drove the conversation on selecting Python and cost-effective scraping techniques._

3. **Prompt:**
   "Break down AWS vs GCP."
   _– Helped compare deployment options and justify choosing a platform._

### **2.2. Descripción de componentes principales:**

1. **Prompt:**
   "What options do we have for scraping? How cost-effective is each option?"
   _– Evaluated various scraping approaches and their costs._

2. **Prompt:**
   "We need around 50k pageviews monthly; we need to slowly start rolling the improvements that will make the site cost more."
   _– Considered scalability and gradual improvements._

3. **Prompt:**
   "Consider a cheapest alternative but thinking about migrating to something within our control at a future iteration."
   _– Focused on an economical initial setup with future migration plans._

### **2.3. Descripción de alto nivel del proyecto y estructura de ficheros**

1. **Prompt:**
   "Let's try and break down this PoC in tasks, sort of like Jira tickets."
   _– Initiated the task breakdown for the PoC implementation._

2. **Prompt:**
   "Minimize the PoC tech stack to a 2-day implementation."
   _– Focused on reducing complexity for rapid prototyping._

3. **Prompt:**
   "Scraping within this PoC should be only manually triggered. We don't need a JSON export, just store the scraped data in a table."
   _– Defined the MVP's minimal requirements for scraping._

### **2.4. Infraestructura y despliegue**

1. **Prompt:**
   "Let's start with a low-cost MVP deployment and plan a migration to Google Cloud later."
   _– Directed the choice of a low-cost initial deployment strategy._

2. **Prompt:**
   "How would we configure our scraping and AI processing to be cost-effective while running on the cloud?"
   _– Focused on cost optimization for cloud resources._

3. _(Outdated Prompt)_ "Let's set up a GitHub Actions deployment into AWS using Terraform."
   _– This prompt is less relevant now since the focus shifted to Google Cloud Run; consider updating any references to AWS._

### **2.5. Seguridad**

1. **Prompt:**
   "Should we add API authentication for admin actions (e.g., reprocessing)?"
   _– Explored initial ideas for securing critical endpoints._

2. **Prompt:**
   "Should manual scraping triggers be restricted to admin roles only?"
   _– Considered role-based access for sensitive actions._

3. **Prompt:**
   "What security concerns should we consider for handling scraped promotional data?"
   _– Addressed data integrity and exposure risks._

### **2.6. Tests**

1. **Prompt:**
   "Should we log scraping statistics (e.g., number of promotions scraped per session)?"
   _– Initiated the discussion on monitoring and logging for the scraping process._

2. **Prompt:**
   "Implement a logging and monitoring strategy for scraping operations."
   _– Focused on the need for visibility into scraping performance._

3. **Prompt:**
   "What would be a good test approach for verifying the correctness of the extracted data?"
   _– Guided the formulation of unit and integration tests for the backend._

---

### 3. Modelo de Datos

1. **Prompt:**
   "How should we structure our database tables for scraped data and extracted promotions?"
   _– Laid the groundwork for the database schema design._

2. **Prompt:**
   "Should we store raw HTML, structured JSON, or both?"
   _– Discussed data storage strategies for flexibility and performance._

3. **Prompt:**
   "How do we optimize for storing large amounts of scraped data while keeping queries fast?"
   _– Addressed performance considerations in database design._

---

### 4. Especificación de la API

1. **Prompt:**
   "How should our scraping API be structured?"
   _– Focused on designing a clean and minimal API for scraping operations._

2. **Prompt:**
   "Implement API endpoints for listing, viewing, and reprocessing scraped pages."
   _– Defined the key endpoints (`/promotions`, `/scrape`, `/ai-process`)._

3. **Prompt:**
   "Should we have an admin API for viewing logs and manual reprocessing?"
   _– Considered additional API endpoints for management purposes._

---

### 5. Historias de Usuario

1. **Prompt:**
   "Should the frontend allow filtering promo data based on extracted discount details?"
   _– Explored potential UI features for enhanced user experience (though not implemented in the MVP)._

2. **Prompt:**
   "What would be the ideal user experience for browsing scraped promotions?"
   _– Helped define the requirements for a minimal yet effective user interface._

3. **Prompt:**
   "How should a user trigger a manual scrape from the UI?"
   _– Defined the interaction for admin users to initiate scraping._

---

### 6. Tickets de Trabajo

1. **Prompt:**
   "Let's try and break down this PoC in tasks, sort of like Jira tickets."
   _– Initiated the breakdown of work items into actionable tasks._

2. **Prompt:**
   "Create structured tickets for each step of the PoC implementation."
   _– Led to the formation of detailed work tickets (e.g., setting up scraping, storing data, etc.)._

3. **Prompt:**
   "Prioritize the first essential development steps before frontend work."
   _– Helped in organizing and prioritizing tasks to focus on backend functionality first._

---

### 7. Pull Requests

_(Note: No additional prompts were provided in this conversation specifically for Pull Requests. The process was implied within the context of work tickets and task breakdowns.)_
