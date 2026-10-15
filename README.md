# City Temperature Management API

A FastAPI application that manages cities and collects their current temperatures
from the [Open-Meteo](https://open-meteo.com/) public API.

It consists of two apps:

- **cities** — CRUD API for city data;
- **temperatures** — fetches the current temperature for every city in the database,
  stores it, and exposes the history of all records.

## Tech stack

- **FastAPI** — web framework
- **SQLAlchemy 2.x (async)** + **aiosqlite** — ORM and SQLite driver
- **Alembic** — database migrations
- **httpx** — async HTTP client for the weather API
- **pydantic-settings** — configuration from environment variables / `.env`

## How to run

```bash
git clone <repository-url>
cd py-fastapi-city-temperature-management-api

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirements.txt

alembic upgrade head             # creates the SQLite database and tables
uvicorn main:app --reload
```

The API is available at http://127.0.0.1:8000, interactive docs at
http://127.0.0.1:8000/docs.

### Configuration

Settings are read from environment variables or an optional `.env` file:

| Variable       | Default                                      |
|----------------|----------------------------------------------|
| `DATABASE_URL` | `sqlite+aiosqlite:///./cities_temperature.db` |

## API endpoints

### Cities

| Method | Path                  | Description                                     |
|--------|-----------------------|-------------------------------------------------|
| POST   | `/cities/`            | Create a city (201; 400 if name already exists) |
| GET    | `/cities/`            | List all cities                                 |
| GET    | `/cities/{city_id}/`  | City details including its temperature history  |
| PUT    | `/cities/{city_id}/`  | Update a city                                   |
| DELETE | `/cities/{city_id}/`  | Delete a city together with its temperatures    |

Example request body:

```json
{
  "name": "Kyiv",
  "additional_info": "Capital of Ukraine"
}
```

### Temperatures

| Method | Path                            | Description                                         |
|--------|---------------------------------|-----------------------------------------------------|
| POST   | `/temperatures/update/`         | Fetch current temperature for all cities and store it |
| GET    | `/temperatures`                 | List all temperature records                        |
| GET    | `/temperatures?city_id={id}`    | Temperature records for a specific city             |

Example response of `POST /temperatures/update/`:

```json
{
  "updated": ["Kyiv", "Lviv"],
  "failed": [
    {"city": "Qwerty", "error": "Coordinates for city 'Qwerty' not found"}
  ]
}
```

## Project structure

```
.
├── main.py              # app creation, routers registration
├── settings.py          # configuration (pydantic-settings)
├── database.py          # async engine, session factory, declarative Base
├── dependencies.py      # shared dependencies (get_db)
├── cities/
│   ├── models.py        # SQLAlchemy City model
│   ├── schemas.py       # Pydantic schemas
│   ├── crud.py          # database operations
│   ├── utils.py         # get_city_or_404 dependency
│   └── router.py        # HTTP endpoints
├── temperatures/
│   ├── models.py        # SQLAlchemy Temperature model
│   ├── schemas.py       # Pydantic schemas
│   ├── crud.py          # database operations
│   ├── services.py      # temperature update logic
│   └── router.py        # HTTP endpoints
├── weather_api/
│   └── weather.py       # Open-Meteo client
└── alembic/             # migrations
```

## Design choices

- **App-per-domain structure.** `cities` and `temperatures` each have their own
  models, schemas, CRUD and router, as recommended by the FastAPI project structure
  guidelines.
- **Layered responsibilities.** Routers only handle HTTP; `crud.py` only talks to
  the database; `weather_api` only talks to the external API and knows nothing about
  the database; `temperatures/services.py` combines them.
- **Fully async stack.** Async SQLAlchemy sessions and an async `httpx` client, so
  requests to the weather API do not block the event loop.
- **Concurrent temperature fetching.** `POST /temperatures/update/` fetches all
  cities at once with `asyncio.gather` using a single shared `httpx.AsyncClient`
  (connection pooling), so the total time is close to that of a single request
  instead of growing with the number of cities.
- **Partial failures do not break the update.** `return_exceptions=True` collects
  errors per city; successful results are saved and failed cities are reported
  in the response.
- **Single transaction for the update.** All new temperature records are saved with
  one commit — either the whole batch is stored or none of it.
- **The DB session is not shared between concurrent tasks.** Only HTTP requests run
  concurrently; writing to the database happens afterwards, because `AsyncSession`
  is not safe for concurrent use.
- **Dependency injection.** The database session is provided to endpoints via
  `Depends(get_db)` (the `DbSession` alias); the session is closed and rolled back
  on errors automatically. Loading a city by `city_id` is also a dependency
  (`get_city_or_404`), so endpoints receive a ready `City` object or a 404 is
  returned before the endpoint runs.
- **Open-Meteo as the weather source.** It is free and requires no API key, so the
  project runs without any registration. A city name is first resolved to
  coordinates with the Open-Meteo Geocoding API, then the current temperature is
  requested from the Forecast API.
- **Migrations with Alembic** instead of `create_all`, so the schema can evolve
  without recreating the database.

## Assumptions and simplifications

- A city is identified in the weather API **by its name**; the first geocoding
  result is used. Cities with ambiguous names (e.g. several "Springfield"s) may
  resolve to a different place than intended.
- City names are unique.
- Temperature is stored in **degrees Celsius** (Open-Meteo default).
- `date_time` is the moment the update was performed, stored and returned in
  **UTC** (e.g. `2026-10-15T14:26:54Z`); converting to local time is up to the
  client. All records from one update share the same timestamp. SQLite does not
  store timezone information, so the schema marks values read from the database
  as UTC explicitly.
- Deleting a city also deletes its temperature history.
- `PUT` performs a full update: fields that are not sent are reset to their
  defaults (`additional_info` becomes `null`).
- No pagination, authentication or background scheduling — temperatures are
  updated only when `POST /temperatures/update/` is called.
