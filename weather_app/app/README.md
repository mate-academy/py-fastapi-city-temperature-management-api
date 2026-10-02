# City Weather API

A FastAPI application with two components:

1. **City CRUD API** — manage a list of cities.
2. **Temperature API** — fetch the current temperature for every stored
   city from a free online weather service and keep a history of all
   readings.

## Project structure

```
weather_app/
├── .env                  # local environment variables (not committed)
├── .env.example           # template for required environment variables
├── requirements.txt
├── README.md
└── app/
    ├── main.py                # FastAPI app, router registration
    ├── config.py              # centralised settings (pydantic-settings)
    ├── database.py             # SQLAlchemy engine/session (SQLite)
    ├── models.py                # SQLAlchemy ORM models (City, Temperature)
    ├── schemas.py                # Pydantic request/response schemas
    ├── crud.py                    # Data-access layer (DB queries)
    ├── routers/
    │   ├── cities.py           # /cities endpoints
    │   └── temperatures.py     # /temperatures endpoints
    └── services/
        └── weather.py          # Async client for the external weather API
```

## How to run

```bash
# 1. Create a virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Copy the environment template and adjust if needed
cp .env.example .env            # Windows: copy .env.example .env

# 4. Run the app
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.
Interactive docs (Swagger UI) are auto-generated at `http://127.0.0.1:8000/docs`.

A SQLite file `weather.db` is created automatically in the project root
on first run — no separate database setup is required.

## Configuration

All configuration is centralised in `app/config.py` via `pydantic-settings`
and loaded from environment variables / a local `.env` file. See
`.env.example` for the full list of variables (database URL, external
weather API endpoints, request timeout). Nothing else in the codebase
reads `os.environ` directly — changing the database or the weather
provider's base URL is a config change, not a code change.

## Endpoints

### Cities

| Method | Path             | Description                          |
|--------|------------------|---------------------------------------|
| POST   | `/cities`        | Create a city (`name` must be unique) |
| GET    | `/cities`        | List all cities                       |
| GET    | `/cities/{id}`   | Get a single city                     |
| PUT    | `/cities/{id}`   | Partially update a city               |
| DELETE | `/cities/{id}`   | Delete a city (and its temperature history) |

### Temperatures

| Method | Path                          | Description                                   |
|--------|-------------------------------|------------------------------------------------|
| POST   | `/temperatures/update`        | Fetch & store the current temperature for every city |
| GET    | `/temperatures`               | List all temperature records (newest first)   |
| GET    | `/temperatures?city_id={id}`  | List temperature records for one city          |

Example flow:

```bash
curl -X POST localhost:8000/cities \
  -H "Content-Type: application/json" \
  -d '{"name": "Kyiv", "additional_info": "Capital of Ukraine"}'

curl -X POST localhost:8000/temperatures/update

curl "localhost:8000/temperatures?city_id=1"
```

## Design choices

- **Centralised settings (`app/config.py`).** A single `Settings` object,
  injected via a cached `get_settings()`, loaded from environment
  variables / `.env`. This keeps the database URL, external API URLs and
  timeouts out of the codebase, so switching environments (dev/test/prod)
  or weather providers is a config change, not a code change.

- **SQLite + SQLAlchemy.** SQLite needs no server and ships with Python,
  which keeps the project runnable with zero external setup. The
  SQLAlchemy layer (`database.py`, `models.py`) doesn't hard-code
  anything SQLite-specific, so swapping to Postgres/MySQL later is just
  a `DATABASE_URL` change.

- **Pydantic schemas are separate from the ORM models.** `models.py`
  describes storage, `schemas.py` describes the API contract
  (`*Create` / `*Update` / read schema). This keeps the API shape free
  to diverge from the DB shape later (e.g. hiding a column, adding a
  computed field) without touching the database layer.

- **`crud.py` as a data-access layer.** Route handlers stay focused on
  HTTP concerns (status codes, validation, 404s); actual queries live in
  one place, which also makes them easy to unit-test in isolation from
  FastAPI.

- **Dependency injection.** The DB session is provided via FastAPI's
  `Depends(get_db)`, which is what makes `crud.py` testable with an
  injected test session instead of a hard-coded global connection.

- **Open-Meteo as the weather source.** Chosen specifically because it
  requires **no API key**, so the grader can run `POST
  /temperatures/update` immediately without signing up for anything.
  Since our `City` model stores a name rather than coordinates, the
  service first calls Open-Meteo's geocoding endpoint to resolve the
  city name to latitude/longitude, then calls the forecast endpoint for
  the current temperature. Both endpoint URLs live in `config.py`, so
  swapping to another provider only requires editing `services/weather.py`
  and the relevant settings — nothing in the routers or CRUD layer
  depends on which provider is used.

- **Async fetching, resilient to partial failure.** `update_temperatures`
  uses a single shared `httpx.AsyncClient` for the whole batch (reusing
  connections) and fetches cities one at a time, but if one city's name
  can't be geocoded or its request fails, that city is recorded in the
  response's `failed` list and the loop continues — one bad city name
  doesn't block updates for the rest.

- **Error handling.** Creating a duplicate city name returns `409`;
  looking up/updating/deleting a non-existent city returns `404`;
  external fetch failures are caught per-city rather than raising an
  unhandled exception. Deleting a city cascades to delete its
  temperature history (`cascade="all, delete-orphan"` on the
  relationship), so there are no orphaned temperature rows left behind.

## Assumptions & simplifications

- City `name` is treated as the lookup key sent to the weather API, so
  it must be a real, geocodable place name (and is enforced unique in
  the DB — two cities with the same name would be ambiguous to update
  independently).
- `date_time` on a temperature record is the server's timestamp at the
  moment it fetched the reading (UTC), not a timestamp returned by the
  weather provider — Open-Meteo's "current weather" endpoint doesn't
  return a separate observation time in a convenient format, so using
  our own fetch time is simpler and accurate enough for this use case.
- No authentication/authorization — out of scope per the task
  description, but would be the first thing to add before any real
  deployment.
- Tables are created via `Base.metadata.create_all()` on startup rather
  than via migrations (e.g. Alembic). Fine for this exercise; a longer-
  lived project should use migrations instead so schema changes are
  tracked and reversible.
- `POST /temperatures/update` updates **every** city in the database in
  one call, per the task description, rather than taking a city filter —
  that felt like the more faithful reading of "fetches current
  temperature data for all cities in the database."
