# Portfolio Backend API & Interactive Showcase

**Live Demo:** [Please Wait !!!!!]
---

## Project Overview

A production-ready, decoupled RESTful API built to power a developer portfolio. This backend goes beyond basic CRUD operations by implementing a secure, rate-limited interactive API playground. It is designed with enterprise-level architecture, focusing on relational data integrity, security, and performance.

## Tech Stack

* **Framework:** Python, Django, Django REST Framework (DRF)
* **Database:** PostgreSQL (Neon)
* **Security & Throttling:** DRF ScopedRateThrottle, Python Hashlib (IP Sanitization)
* **Server & Deployment:** Gunicorn, WhiteNoise, Render

## Core Features

* **Decoupled Architecture:** Serves as a standalone JSON API ready to be consumed by any modern frontend framework (React/Next.js).
* **Interactive API Playground:** Allows recruiters to test live endpoints directly from the UI.
* **Privacy-First Logging:** Tracks API request latency and telemetry while securely hashing user IP addresses to comply with privacy standards.
* **Advanced Rate Limiting:** Implements `ScopedRateThrottle` to provide generous read-limits for standard portfolio viewing while strictly throttling the interactive playground to prevent DDoS attacks.
* **Slug-Based Routing:** Utilizes dynamic URL slugs for SEO-friendly frontend routing.
* **Automated API Documentation:** Integrates `drf-spectacular` to generate a live, interactive OpenAPI 3.0 schema and Swagger UI for seamless developer onboarding and endpoint testing.
* **Advanced Querying & Pagination:** Protects server memory using global pagination and allows clients to seamlessly filter datasets and perform relational text-based searches using `django-filter` and DRF `SearchFilter`.

## API Endpoints

| Method | Endpoint | Description | Access |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/v1/health/` | Server heartbeat and ISO-8601 timestamp. | Public |
| `GET` | `/api/v1/projects/` | Retrieves a paginated list of published projects. Supports `?search=` and filtering. | Public (Throttled) |
| `GET` | `/api/v1/projects/<slug>/` | Retrieves deep architectural details of a single project. | Public (Throttled) |
| `POST` | `/api/v1/playground/echo/` | Calculates server latency and echoes the JSON payload. | Public (Strictly Throttled) |
| `GET` | `/api/schema/` | Raw OpenAPI 3.0 YAML/JSON schema file. | Public |
| `GET` | `/api/docs/` | Interactive Swagger UI documentation. | Public |


## Local Setup Instructions

**1. Clone the repository**

```bash
git clone [https://github.com/YourUsername/portfolio-backend.git](https://github.com/YourUsername/portfolio-backend.git)
cd portfolio-backend 
```

**2. Set up the Python Virtual Environment**

```bash
python -m venv venv
source venv/bin/activate  
# On Windows: .\venv\Scripts\activate
```

**3. Install Dependencies**

```bash
pip install -r requirements.txt
```

**4. Run database migrations**

```bash
python manage.py migrate
```

**5. Start the development server**

```bash
python manage.py runserver
```
