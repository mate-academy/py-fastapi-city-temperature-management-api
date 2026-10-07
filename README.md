# City and Temperature Management API

A FastAPI application designed to manage city records and track current weather temperature data fetched automatically from an external weather service (Open-Meteo API).

---

## Tech Stack

- Python 3.11+
- FastAPI — Modern, fast asynchronous web framework
- SQLAlchemy 2.0 (Async) + aiosqlite — Asynchronous ORM with SQLite database
- Pydantic v2 — Data validation and serialization
- HTTPX — Asynchronous HTTP client for external API requests
- Uvicorn — ASGI server

---

## Project Structure

app/
├── __init__.py
├── main.py
├── api/
│   ├── __init__.py
│   ├── dependencies.py      # Database session dependency
│   ├── cities.py            # /cities router
│   └── temperatures.py      # /temperatures router
├── crud/
│   ├── __init__.py
│   ├── city.py              # City CRUD database operations
│   └── temperature.py       # Temperature database operations
├── db/
│   ├── __init__.py
│   ├── engine.py            # Async engine and session setup
│   └── models.py            # SQLAlchemy models
└── schemas/
    ├── __init__.py
    ├── city.py              # Pydantic models for City
    └── temperature.py       # Pydantic models for Temperature

---

## Setup and Execution Instructions

### Step 1: Set up the environment

Create and activate a virtual environment:
python -m venv .venv

On Linux/macOS:
source .venv/bin/activate

On Windows (Git Bash):
source .venv/Scripts/activate

On Windows (CMD):
.venv\Scripts\activate

Install required dependencies:
pip install -r requirements.txt

### Step 2: Run the application

uvicorn app.main:app --reload

The application will be running at http://127.0.0.1:8000.

### Step 3: Interactive API Documentation

Swagger UI: http://127.0.0.1:8000/docs
ReDoc: http://127.0.0.1:8000/redoc

---

## API Endpoints

Cities API (/cities):
- POST /cities — Create a new city record
- GET /cities — Retrieve a list of all cities
- GET /cities/{city_id} — Retrieve details for a specific city
- PUT /cities/{city_id} — Update details of a specific city
- DELETE /cities/{city_id} — Delete a specific city (cascades to related temperature records)

Temperatures API (/temperatures):
- POST /temperatures/update — Fetch and save the current temperature for all cities in the database via the Open-Meteo API
- GET /temperatures — Retrieve history of all temperature records
- GET /temperatures?city_id={city_id} — Retrieve temperature records for a specific city

---

## Design Choices and Architecture

1. Concurrent Async Requests:
Fetching weather data for multiple cities sequentially would cause performance bottlenecks. By combining httpx.AsyncClient with asyncio.gather(), weather forecasts for all cities are fetched concurrently in parallel, significantly reducing response time.

2. Open-Meteo External Weather API:
Selected Open-Meteo API as the weather provider because it is free, reliable, requires no API key registration, and provides both Geocoding and Forecast endpoints.

3. Graceful Error Handling:
By specifying return_exceptions=True in asyncio.gather(), any failure while retrieving temperature for a single city (e.g., city name not found by geocoding) is caught safely without stopping the updates for other valid cities.

4. Database Cascade and Foreign Keys in SQLite:
SQLite disables Foreign Key constraints by default. A database connection event listener (PRAGMA foreign_keys=ON) is attached to the SQLAlchemy engine to guarantee foreign key constraint enforcement and cascade deletion (ON DELETE CASCADE) when a city is removed.

---

## Assumptions and Simplifications

- Geocoding Matching: The first result returned by the geocoding service is assumed to be the correct match for the given city name.
- Temperature Units: All temperature values are recorded and stored in Celsius (°C).
