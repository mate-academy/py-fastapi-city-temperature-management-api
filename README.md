# City Temperature Management API

A FastAPI service that manages cities and tracks their temperature history. It exposes a
CRUD API for city records and a second API that fetches the current temperature for every
stored city from [WeatherAPI.com](https://www.weatherapi.com/) and persists it as a time
series.

Built on a fully async stack: FastAPI, SQLAlchemy 2.0 (async ORM), SQLite via `aiosqlite`,
Alembic migrations, and `httpx` for outbound requests.

---

## Table of contents

- [Requirements](#requirements)
- [Getting started](#getting-started)
- [API reference](#api-reference)
- [Project structure](#project-structure)
- [Design choices](#design-choices)
- [Assumptions and simplifications](#assumptions-and-simplifications)

---

## Requirements

- Python 3.12+
- A free API key from [weatherapi.com](https://www.weatherapi.com/signup.aspx)

---

## Getting started

### 1. Clone the repository

```bash
git clone https://github.com/omerlenko/py-fastapi-city-temperature-management-api.git
cd py-fastapi-city-temperature-management-api
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv

# Linux / macOS
source .venv/bin/activate

# Windows (PowerShell)
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy the example file and fill in your API key:

```bash
cp .env.example .env
```

`.env` holds two settings:

| Variable | Description | Example |
| --- | --- | --- |
| `DATABASE_URL` | Async SQLAlchemy database URL | `sqlite+aiosqlite:///./app.db` |
| `WEATHER_API_KEY` | Your WeatherAPI.com key | `1a2b3c4d5e...` |

### 5. Apply database migrations

```bash
alembic upgrade head
```

This creates `app.db` with the `cities` and `temperatures` tables.

### 6. Run the server

```bash
uvicorn main:app --reload
```

The API is now available at `http://127.0.0.1:8000`.

Interactive documentation:

- Swagger UI — <http://127.0.0.1:8000/docs>
- ReDoc — <http://127.0.0.1:8000/redoc>

---

## API reference

### Cities

| Method | Endpoint | Description | Success |
| --- | --- | --- | --- |
| `POST` | `/cities/` | Create a new city | `201` |
| `GET` | `/cities/` | List cities (paginated) | `200` |
| `GET` | `/cities/{city_id}/` | Retrieve a single city | `200` |
| `PATCH` | `/cities/{city_id}/` | Partially update a city | `200` |
| `DELETE` | `/cities/{city_id}/` | Delete a city and all of its temperature records | `204` |

Query parameters for the list endpoint: `skip` (default `0`), `limit` (default `10`).

**Create a city**

```bash
curl -X POST http://127.0.0.1:8000/cities/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Kyiv", "additional_info": "Capital of Ukraine"}'
```

```json
{ "id": 1, "name": "Kyiv", "additional_info": "Capital of Ukraine" }
```

### Temperatures

| Method | Endpoint | Description                                                            | Success |
| --- | --- |------------------------------------------------------------------------| --- |
| `POST` | `/temperatures/update/` | Fetch and store the current temperature for every city in the database | `200` |
| `GET` | `/temperatures/` | List temperature records (paginated)                                   | `200` |
| `GET` | `/temperatures/?city_id={id}` | List temperature records for one city                                  | `200` |

Query parameters for the list endpoint: `city_id`, `skip` (default `0`), `limit` (default `10`).

**Refresh temperatures**

```bash
curl -X POST http://127.0.0.1:8000/temperatures/update/
```

The response summarises the run rather than dumping the records:

```json
{ "created": 3, "ignored": 1, "failed": 0 }
```

- `created` — new readings written to the database
- `ignored` — readings already stored for that city and timestamp
- `failed` — cities whose upstream request failed (details are logged server-side)

**Read temperature history**

```bash
curl "http://127.0.0.1:8000/temperatures/?city_id=1"
```

```json
[
  {
    "id": 1,
    "date_time": "2026-08-20T14:30:00",
    "temperature": 23.4,
    "city": { "id": 1, "name": "Kyiv", "additional_info": "Capital of Ukraine" }
  }
]
```

### Error responses

| Status | When |
| --- | --- |
| `404` | The requested `city_id` does not exist |
| `409` | A city with that name already exists |
| `422` | Request body or query parameters fail validation |

---

## Project structure

The project follows FastAPI's recommended package-per-domain layout. Each domain package
owns its own models, schemas, data access, and routes, which keeps the two "apps"
independent and makes the codebase easy to extend.

```
.
├── city/                  # City domain
│   ├── models.py          # SQLAlchemy ORM model
│   ├── schemas.py         # Pydantic request/response models
│   ├── crud.py            # Database operations
│   └── router.py          # HTTP endpoints
├── temperature/           # Temperature domain
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   ├── client.py          # WeatherAPI.com HTTP client
│   └── router.py
├── alembic/               # Migration environment and revisions
├── config.py              # Settings loaded from .env
├── database.py            # Engine, session factory, declarative Base
├── dependencies.py        # Shared injectable dependencies
└── main.py                # Application entry point
```

---

## Design choices

**Async end to end.** The service is I/O-bound — it talks to a database and an external
weather API — so every layer is asynchronous: `AsyncSession` for the ORM, `aiosqlite` as
the driver, and `httpx.AsyncClient` for outbound calls.

**Separate CRUD layer.** Routers handle HTTP concerns (status codes, error translation)
and delegate all database work to `crud.py`. This keeps endpoints thin and makes the data
access functions reusable across domains — the temperature router, for example, reuses
`city.crud.get_cities`.

**Dependency injection throughout.** Reusable `Annotated` aliases keep signatures readable:

- `DbDep` provides a per-request database session that is always closed.
- `ClientDep` supplies the shared HTTP client.
- `CityDep` resolves a path parameter to a `City` and raises `404` if it does not exist,
  so the three city-detail endpoints never repeat that lookup.

**One shared HTTP client.** The `httpx.AsyncClient` is created once in the application
lifespan and reused for every request, so connections are pooled instead of paying for a
new TLS handshake per city.

**Concurrent fetching that tolerates partial failure.** `/temperatures/update/` requests
all cities concurrently with `asyncio.gather(..., return_exceptions=True)`. A single city
failing — an unrecognised name, a rate limit, a network blip — is counted, logged, and
skipped; the successful readings are still saved. All inserts are staged and committed in
a single transaction at the end.

**Idempotent updates.** A `UniqueConstraint` on `(city_id, date_time)` means the same
reading cannot be stored twice. Since WeatherAPI refreshes roughly every 15 minutes,
calling the endpoint repeatedly reports readings as `ignored` instead of creating
duplicates.

**Cascading deletes.** `City.temperatures` is configured with
`cascade="all, delete-orphan"`, so deleting a city removes its readings and never leaves
orphaned rows behind.

**Alembic instead of `create_all`.** Schema changes are versioned and reviewable.
`render_as_batch` is enabled because SQLite cannot alter columns or add constraints in
place, and a metadata naming convention gives every constraint a deterministic name so
those batch migrations stay stable.

**PATCH rather than PUT.** The specification lists `PUT` as optional. `PATCH` was chosen
deliberately: it matches the partial-update semantics of `CityUpdate`, where every field
is optional and only the fields actually sent are modified.

---

## Assumptions and simplifications

- **Data source.** WeatherAPI.com's free tier is used as the online resource. Cities are
  resolved by passing their `name` as the search query, so names must be recognisable to
  the provider (for example `Kyiv`, not `my home town`).
- **Timestamps.** `date_time` is the provider's `last_updated` value, which is the local
  time of the city being queried and carries no timezone offset. Readings for cities in
  different timezones are therefore not directly comparable. A production system would
  normalise these to UTC.
- **Units.** Temperatures are stored in degrees Celsius.
- **City names are unique.** The `name` column carries a unique constraint, and creating a
  duplicate returns `409`. This keeps the mapping between a city record and a weather
  lookup unambiguous.
- **`additional_info` is required.** The field is non-nullable; pass an empty string when
  there is nothing to record.
- **Pagination is always applied.** Both list endpoints default to `limit=10`, so
  retrieving the full history means paging through with `skip` and `limit`.
- **Trailing slashes are canonical.** Routes are registered as `/cities/` and
  `/temperatures/`; FastAPI redirects the slashless forms automatically.
- **Concurrency.** `/temperatures/update/` checks for an existing reading before
  inserting. This assumes the endpoint is not invoked concurrently with itself; the
  database constraint remains the ultimate safeguard.
- **No authentication.** All endpoints are public, which is appropriate for the scope of
  this task.
- **No automated tests.** Testing was outside the scope of the assignment.
