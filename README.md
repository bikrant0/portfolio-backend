# Portfolio Backend API & Interactive Showcase

**Live Demo:** [Please Wait !!!!!]
### Have some patience for this.. 
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

## API Endpoints

| Method | Endpoint | Description | Access |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/v1/health/` | Server heartbeat and ISO-8601 timestamp. | Public |
| `GET` | `/api/v1/projects/` | Retrieves a list of all published projects. | Public (Throttled) |
| `GET` | `/api/v1/projects/<slug>/` | Retrieves deep architectural details of a single project. | Public (Throttled) |
| `POST` | `/api/v1/playground/echo/` | Calculates server latency and echoes the JSON payload. | Public (Strictly Throttled) |

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
