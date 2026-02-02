# City & Temperature Management API (FastAPI)

A FastAPI application that:
1) Manages cities (CRUD).
2) Fetches current temperatures for all stored cities from an online resource and stores them in the database.
3) Provides endpoints to retrieve temperature history (optionally filtered by city).

## Tech Stack
- FastAPI
- Pydantic v2
- SQLAlchemy 2.0 (async)
- Alembic (migrations)
- SQLite
- httpx (async HTTP client)
- uv (dependency management)
- flake8 (lint)

## Project Structure
app/
  api/            # routers/endpoints
  core/           # settings/config
  crud/           # database CRUD logic
  db/             # session/engine
  models/         # SQLAlchemy models
  schemas/        # Pydantic schemas
  services/       # external temperature provider client
alembic/          # database migrations

## Setup

### 1) Install dependencies (uv)
From the project root:
```bash
uv sync --extra dev
```

### 2) Create .env from .env.example if you want to override defaults:
```
DATABASE_URL=sqlite+aiosqlite:///./app.db
TEMPERATURE_PROVIDER_BASE_URL=https://wttr.in
```
### If .env is not provided, the app uses default values.

### 3) Run migrations (Alembic)
If this is the first time running the project:
```bash
uv run alembic upgrade head
```
Note: Migration files are already included in the repository.
If you change models, generate a new migration:
```bash
uv run alembic revision --autogenerate -m "your message"
uv run alembic upgrade head
```

### 4) Run the server
```bash
uv run uvicorn app.main:app --reload
```
Open Swagger UI:
- http://127.0.0.1:8000/docs
- 
### API Endpoints

#### Cities
- POST /cities — create a city
- GET /cities — list all cities
- GET /cities/{city_id} — get city details (implemented)
- PUT /cities/{city_id} — update city (implemented)
- DELETE /cities/{city_id} — delete city
#### Temperatures
- POST /temperatures/update — fetch current temperature for every city and store records
- GET /temperatures — list all temperature records (history)
- GET /temperatures?city_id={city_id} — list temperature records for a specific city
#### Temperature Provider
The app uses the public endpoint:
- wttr.in with JSON format: https://wttr.in/{city}?format=j1
It reads current_condition[0].temp_C.
#### Design Choices & Assumptions
- Async stack: SQLAlchemy async engine (sqlite+aiosqlite) and async HTTP calls (httpx.AsyncClient).
- Unique city name: City.name is unique to prevent duplicates.
- Batch update timestamp: during /temperatures/update the same UTC now timestamp is used for the whole batch.
- Graceful failures: if fetching temperature for a city fails, it is reported in failed_city_ids, while successful cities are still stored.

### 5) Run flake8:
```bash
uv run flake8
```
