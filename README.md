# City Temperature Management API

FastAPI application for managing cities and storing temperature history fetched from [Open-Meteo](https://open-meteo.com/).

## Features

- Full CRUD for cities (`POST`, `GET`, `PUT`, `DELETE`)
- Async temperature update for all cities via Open-Meteo geocoding + forecast APIs
- Temperature history listing with optional `city_id` filter
- SQLite persistence through SQLAlchemy
- Dependency injection for database sessions and city lookups

## Requirements

- Python 3.10+

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
uvicorn app.main:app --reload
```

Open interactive docs at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

## API overview

### Cities

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/cities` | Create a city |
| `GET` | `/cities` | List all cities |
| `GET` | `/cities/{city_id}` | Get a city |
| `PUT` | `/cities/{city_id}` | Update a city |
| `DELETE` | `/cities/{city_id}` | Delete a city (cascades temperatures) |

### Temperatures

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/temperatures/update` | Fetch current temperature for every city and store records |
| `GET` | `/temperatures` | List temperature history |
| `GET` | `/temperatures?city_id={id}` | List temperatures for one city |

### Example

```bash
curl -X POST http://127.0.0.1:8000/cities \
  -H "Content-Type: application/json" \
  -d '{"name": "Kyiv", "additional_info": "Capital of Ukraine"}'

curl -X POST http://127.0.0.1:8000/temperatures/update

curl http://127.0.0.1:8000/temperatures?city_id=1
```

## Tests

```bash
pytest
```

Weather HTTP calls are mocked in unit tests. Network access is not required to run the suite.

## Design choices

- Project layout follows the FastAPI [Bigger Applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/) guide: `app/main.py`, `app/dependencies.py`, and `APIRouter` modules under `app/routers/`.
- SQLAlchemy models and Pydantic schemas live in dedicated modules, matching the FastAPI SQL databases tutorial.
- Database access uses a sync SQLAlchemy session injected via `Depends(get_db)`. Async I/O is reserved for Open-Meteo requests through `httpx.AsyncClient` and `asyncio.gather`, as required by the assignment.
- Open-Meteo is used because it needs no API key: city names are geocoded, then current `temperature_2m` is fetched with `timezone=Europe/Kyiv`.
- Partial weather failures (unknown city names) do not fail the whole `/temperatures/update` request. Successful readings are stored and failed cities are reported in `errors`. A total provider outage returns HTTP 502.
- Optional city endpoints (`GET`/`PUT` by id) are implemented to complete the CRUD surface.

## Assumptions and simplifications

- City names are unique.
- Request bodies for city creation omit `id`; the database assigns it. Response schemas still match the assignment fields for `City` and `Temperature`.
- Tables are created on application startup with `Base.metadata.create_all`. Alembic migrations are not included.
- SQLite file path is `./db.sqlite3` (ignored by git).
- Temperature timestamps are stored as timezone-aware datetimes in `Europe/Kyiv`.
