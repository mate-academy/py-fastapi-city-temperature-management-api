# Cities & Temperatures API

A FastAPI application that manages a list of cities and keeps a history of their current temperatures.

- **Cities app** – CRUD API for cities, stored in SQLite.
- **Temperatures app** – fetches the current temperature of every city from the free [Open-Meteo](https://open-meteo.com/) API, stores it, and exposes the history.

## Requirements

- Python 3.10 or newer (the code uses the `X | None` type syntax)
- Internet access (needed only for `POST /temperatures/update`)
- No API key is needed. Open-Meteo is free and keyless.

## How to run

All commands are run from the project root (the folder that contains `app/`).

```bash
# 1. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start the server
uvicorn app.main:app --reload
```

The API is now available at <http://127.0.0.1:8000>.
Interactive documentation (Swagger UI), where every endpoint can be tried out: <http://127.0.0.1:8000/docs>.

The SQLite database file `app.db` and its tables are created automatically on the first start.

### Quick example

```bash
# Add some cities
curl -X POST http://127.0.0.1:8000/cities -H "Content-Type: application/json" \
     -d '{"name": "Budapest", "additional_info": "Capital of Hungary"}'
curl -X POST http://127.0.0.1:8000/cities -H "Content-Type: application/json" \
     -d '{"name": "Vienna"}'

# Fetch and store the current temperature of all cities
curl -X POST http://127.0.0.1:8000/temperatures/update

# Read the history (all cities, or one city)
curl http://127.0.0.1:8000/temperatures
curl "http://127.0.0.1:8000/temperatures?city_id=1"
```

## Endpoints

| Method | Path | Description | Success | Errors |
|---|---|---|---|---|
| POST | `/cities` | Create a city (`name`, optional `additional_info`) | 201 | 409 duplicate name, 422 invalid body |
| GET | `/cities` | List all cities | 200 | |
| GET | `/cities/{city_id}` | Get one city | 200 | 404 |
| PUT | `/cities/{city_id}` | Replace a city's name and info | 200 | 404, 409, 422 |
| DELETE | `/cities/{city_id}` | Delete a city and its temperature history | 204 | 404 |
| POST | `/temperatures/update` | Fetch and store the current temperature of every city | 200 | |
| GET | `/temperatures` | List all temperature records (oldest first) | 200 | |
| GET | `/temperatures?city_id={id}` | List the records of one city | 200 | 404 unknown city |

`POST /temperatures/update` returns a summary, for example:

```json
{
  "updated": 2,
  "failed": [{"city": "Xyzqwkjhg", "reason": "City not found: Xyzqwkjhg"}]
}
```

## Project structure

The layout follows the FastAPI guide
[Bigger Applications – Multiple Files](https://fastapi.tiangolo.com/tutorial/bigger-applications/).

```
.
├── app/
│   ├── __init__.py
│   ├── main.py            # creates the FastAPI app, creates tables, includes the routers
│   ├── database.py        # SQLAlchemy engine, session factory, Base
│   ├── dependencies.py    # get_db dependency (+ the DbSession shortcut)
│   ├── models.py          # SQLAlchemy tables: City, Temperature
│   ├── schemas.py         # Pydantic models: CityCreate, City, Temperature
│   ├── weather.py         # async Open-Meteo client functions
│   └── routers/
│       ├── __init__.py
│       ├── cities.py      # /cities endpoints
│       └── temperatures.py# /temperatures endpoints
├── requirements.txt
└── README.md
```

## Design choices

- **One router per "app".** `routers/cities.py` and `routers/temperatures.py` each use an `APIRouter` with its own prefix and tag. `main.py` only wires everything together.
- **Models and schemas are separate.** SQLAlchemy models (`models.py`) describe the database tables; Pydantic schemas (`schemas.py`) describe what the API accepts and returns. `CityCreate` is the request body (no `id`), `City` is the response. `CityCreate` is also reused as the body of `PUT`.
- **Dependency injection.** Each request gets its own database session through `Depends(get_db)`, which always closes the session afterwards. The `DbSession` alias in `dependencies.py` keeps route signatures short.
- **Async only where it matters.** Fetching temperatures is network-bound, so `POST /temperatures/update` is an `async def` endpoint. It loads the cities, then queries all of them **concurrently** with one shared `httpx.AsyncClient` and `asyncio.gather`, and then writes the results to the database in a single commit. The concurrent tasks only do HTTP; they never touch the database session. All other endpoints are plain `def`, which FastAPI runs in a thread pool.
- **Partial failure is not a total failure.** `gather(..., return_exceptions=True)` means one city that cannot be fetched (not found, timeout, service error) does not stop the others. Those cities are skipped and listed under `failed` in the response. All network and parsing problems are converted into one `WeatherError` with a readable message. Requests have a 10-second timeout.
- **Open-Meteo.** It needs no API key, so the project runs immediately. Because a city has no coordinates, each update first calls the geocoding endpoint (name → latitude/longitude) and then the forecast endpoint (`current=temperature_2m`).
- **Data integrity.** City names are unique (duplicates return 409). Deleting a city also deletes its temperature records (ORM cascade). The city name and info lengths are validated, so bad input returns a clean 422.
- **One endpoint for both temperature lists.** `GET /temperatures` takes an optional `city_id` query parameter. Both `/temperatures` and `/temperatures/` work without a redirect, so the URL form from the task description (`/temperatures/?city_id=1`) is supported as written.

## Assumptions and simplifications

- **Temperature unit and time.** Temperatures are in °C (Open-Meteo's default). `date_time` is the moment the temperature was fetched, in **UTC**, not Open-Meteo's own measurement time. All cities from one update share the same timestamp. SQLite does not store time zones, so the API returns it without a time-zone suffix; treat it as UTC.
- **Geocoding by name, first match only.** The first search result is used. Ambiguous names (for example "Springfield") may resolve to a different city than intended. Coordinates are not stored, so geocoding is repeated on every update (two HTTP requests per city).
- **Update always answers 200.** Even if some or all cities fail, the endpoint returns 200 with the details under `failed`. If there are no cities, it returns `updated: 0` and a message.
- **Unknown city in the filter.** `GET /temperatures?city_id=...` returns 404 if that city does not exist, and an empty list if the city exists but has no records yet.
- **Synchronous database access.** The project uses plain synchronous SQLAlchemy sessions, also inside the one `async` endpoint. This blocks the event loop for a moment, which is negligible for a local SQLite file.
- **No migrations.** Tables are created at startup if they do not exist (`create_all`). If a model changes after `app.db` already exists, delete `app.db` and restart (this removes all data).
- **No authentication, no pagination, no automated tests.** These were left out to keep the scope to the task requirements.

## Possible improvements

- Store latitude/longitude on `City` to skip geocoding on every update.
- Async SQLAlchemy (`aiosqlite`) so database calls do not block the event loop.
- Alembic migrations, pagination on the list endpoints, and configuration through environment variables.
- Automated tests with `pytest`, using dependency overrides for the database and a fake weather client.
- A scheduled job that calls the update automatically.
