# City Temperature API (FastAPI + SQLAlchemy + SQLite)

## What it does
- CRUD for cities
- Fetches current temperature for all cities from Open-Meteo and stores history
- Lists temperature history (optionally filtered by city_id)

## Tech
- FastAPI
- SQLAlchemy ORM (SQLite)
- httpx (async HTTP client)

Weather provider:
- Open-Meteo Geocoding API and Forecast API

## Setup

### 1) Create venv and install deps
python -m venv venv
### Windows:
venv\Scripts\activate

pip install -r requirements.txt

### 2) Configure env (optional)
Create `.env`:
DATABASE_URL=sqlite:///./app.db

### 3) Run
uvicorn app.main:app --reload

Open docs:
http://127.0.0.1:8000/docs

## Endpoints
### Cities
- POST /cities
- GET /cities
- GET /cities/{city_id}
- PUT /cities/{city_id}
- DELETE /cities/{city_id}

### Temperatures
- POST /temperatures/update
- GET /temperatures
- GET /temperatures?city_id=1

## Design choices / simplifications
- SQLite used for simplicity
- City stores only (id, name, additional_info) per task
- Coordinates are resolved on each update via geocoding (no lat/lon stored)
- DB operations are sync (fine for small SQLite demo); async DB can be added later
