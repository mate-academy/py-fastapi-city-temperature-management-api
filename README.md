# City & Temperature FastAPI

This project provides:
1) City CRUD API (SQLite + SQLAlchemy ORM)
2) Temperature API that fetches current temperatures for all cities (async) and stores history.

## Tech
- FastAPI
- SQLAlchemy (SQLite)
- httpx (async HTTP client)
- Open-Meteo APIs (no API key needed)
  - Geocoding: converts city name -> latitude/longitude
  - Forecast: returns current temperature

## Run locally

### 1) Install dependencies
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

pip install -r requirements.txt
2) Start server
uvicorn app.main:app --reload
3) Open docs
Swagger UI: http://127.0.0.1:8000/docs

API endpoints
Cities
POST /cities

GET /cities?skip=0&limit=100

GET /cities/{city_id}

PUT /cities/{city_id}

DELETE /cities/{city_id}

Temperatures
POST /temperatures/update

Fetches current temperatures for ALL cities (async) and saves records.

GET /temperatures?skip=0&limit=100

GET /temperatures?city_id={city_id}

Design choices & assumptions
City model follows the required fields: id, name, additional_info.

Coordinates (lat/lon) are not stored in DB to keep the model minimal.
Instead, the update endpoint uses Open-Meteo Geocoding each time.

Temperature history is stored as rows with date_time set by DB default.

Error handling:

If geocoding fails for a city, the update endpoint reports geocoding_not_found
but continues processing other cities.

Network/API errors are reported per-city in the response.

Notes
SQLite is used with check_same_thread=False for FastAPI usage.

For larger loads, consider:

caching geocoding results (lat/lon) in DB

async DB layer (SQLAlchemy async) or background tasks
