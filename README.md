# City Temperature API

FastAPI application for managing cities and their temperature history.

## Setup

```bash
pip install -r requirements.txt
```

Create `.env` with your WeatherAPI key:
WEATHER_API_KEY=fd8e7ef7ddab447d9d5213028262306

## Run

```bash
uvicorn app.main:app --reload
```

Docs: http://127.0.0.1:8000/docs

## Endpoints

### Cities
- `POST /cities/` — create city
- `GET /cities/` — list all cities
- `GET /cities/{id}` — get city
- `PUT /cities/{id}` — update city
- `DELETE /cities/{id}` — delete city

### Temperatures
- `POST /temperatures/update` — fetch & store current temps for all cities
- `GET /temperatures/` — list all records
- `GET /temperatures/?city_id=1` — filter by city

## Design choices
- SQLite + aiosqlite for async I/O
- WeatherAPI.com for free weather data
- Cascade delete: removing a city removes its temperature history
- `lifespan` handler creates tables on startup (no Alembic needed for this scope)