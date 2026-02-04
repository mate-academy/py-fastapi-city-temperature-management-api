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