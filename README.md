# City Temperature Management API

## Overview

A FastAPI application for managing cities and their temperature records. The application retrieves current temperature data from the Open-Meteo API and stores it in a database.

## How to Run the Application

### 1. Clone the repository

```bash
git clone <repository-url>
cd py-fastapi-city-temperature-management-api
```

### 2. Create and activate a virtual environment

**Windows:**

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply database migrations

```bash
alembic upgrade head
```

### 5. Start the application

```bash
uvicorn main:app --reload
```

The application will be available at:

- API: http://127.0.0.1:8000
- Swagger documentation: http://127.0.0.1:8000/docs

## Design Choices

- **FastAPI** — used to build asynchronous REST API endpoints with automatic OpenAPI documentation.
- **SQLAlchemy** — used as the ORM for database operations and model management.
- **Pydantic** — used for request and response data validation and serialization.
- **Alembic** — used to manage database schema changes through migrations.
- **HTTPX** — used to make asynchronous HTTP requests to the Open-Meteo API.
- **AsyncIO** — used to fetch temperature data for multiple cities concurrently.
- **SQLite** — selected as a lightweight database suitable for this project.

The application separates database models, Pydantic schemas, CRUD operations, and API routes to keep the code organized and maintainable.

## Assumptions and Simplifications

- Each city is identified by its name when retrieving geographic coordinates.
- The application retrieves the current temperature using the Open-Meteo API.
- Temperature records are stored with the city ID and the date and time of retrieval.
- Cities without available geocoding or temperature data are skipped during updates.
- SQLite is used instead of a production database to simplify local development.
- The application uses a single temperature measurement (`temperature_2m`) from Open-Meteo.
