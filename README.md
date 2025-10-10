# City & Temperature FastAPI

A small FastAPI service that manages cities (CRUD) and stores temperature history fetched from a public online resource (Open‑Meteo, no API key required).

## Features

- **Cities CRUD**: `POST /cities`, `GET /cities`, `GET /cities/{id}`, `PUT /cities/{id}`, `DELETE /cities/{id}`
- **Temperatures**
  - `POST /temperatures/update` fetches the current temperature for **all** cities and stores a record per city.
  - `GET /temperatures` lists all temperature records (newest first).
  - `GET /temperatures?city_id={id}` filters by a specific city.
- Uses SQLite via SQLAlchemy; tables are auto-created at startup for convenience.
- Async temperature fetching using `httpx` and Open‑Meteo APIs:
  - Geocoding: `https://geocoding-api.open-meteo.com/v1/search?name={city}`
  - Weather: `https://api.open-meteo.com/v1/forecast?latitude=..&longitude=..&current=temperature_2m`

## Quickstart

1. **Create & activate a virtual environment (recommended)**

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Run the API**

```bash
uvicorn app.main:app --reload
```

Open: <http://127.0.0.1:8000/docs>

## Example workflow

```bash
# Create two cities
curl -X POST http://127.0.0.1:8000/cities -H "Content-Type: application/json" -d '{"name":"Kyiv"}'
curl -X POST http://127.0.0.1:8000/cities -H "Content-Type: application/json" -d '{"name":"Berlin","additional_info":"capital of Germany"}'

# Update temperatures (fetches for all cities)
curl -X POST http://127.0.0.1:8000/temperatures/update

# List temperatures
curl http://127.0.0.1:8000/temperatures

# Filter by city
curl "http://127.0.0.1:8000/temperatures?city_id=1"
```

## Design Choices & Notes

- **Open‑Meteo** is used because it's free and keyless. We first geocode the city name to `(lat, lon)`, then request `current=temperature_2m` to read the current temperature in °C. The code also accepts the legacy `current_weather.temperature` in case of API differences.
- **Dependency Injection**: DB session provided via a `get_db` dependency so handlers stay clean and testable.
- **Error Handling**: You get `400` if you try to add a duplicate city name, `404` for missing entities, and `400` when updating temperatures with no cities present.
- **Persistence**: SQLite file `app.db` is created in the project root. Delete it to start fresh.
- **Migrations**: For a small assignment, `Base.metadata.create_all` is used. In production, you should add Alembic migrations.

## Project Structure

```
fastapi_city_temps/
├─ app/
│  ├─ routers/
│  │  ├─ cities.py
│  │  └─ temperatures.py
│  ├─ __init__.py
│  ├─ database.py
│  ├─ main.py
│  ├─ models.py
│  └─ schemas.py
├─ requirements.txt
└─ README.md
```

## Assumptions & Simplifications

- City **name is unique** to avoid duplicates; in real apps consider (name, country) uniqueness.
- Temperature unit is °C from Open‑Meteo. Time is stored as UTC.
- For clarity, `POST /temperatures/update` performs lookups sequentially; for many cities, consider parallelism (e.g., `asyncio.gather`) and backoff/retry.
- No authentication; add it if deploying externally.
