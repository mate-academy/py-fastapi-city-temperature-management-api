# FastAPI City Temperature Management API

A REST API for managing cities and storing a history of temperatures
fetched from an external weather service ([Open-Meteo](https://open-meteo.com/)).

## Features

- CRUD operations for the `City` entity.
- Retrieving a list of temperatures with filtering by city and pagination.
- `POST /temperatures/update/` — asynchronously queries Open-Meteo for
  **all** cities in the database concurrently (`asyncio.gather`) and stores
  new temperature records.

## Tech Stack

- **FastAPI** — web framework
- **SQLAlchemy 2.0 (async)** — ORM, database access via `AsyncSession`
- **SQLite** (`aiosqlite`) — default database
- **httpx** — asynchronous HTTP client used to call Open-Meteo
- **pydantic-settings** — configuration via `.env`

## Project Structure

The project is organized by domain (each domain is a separate package with
its own `router.py`, `schemas.py`, `crud.py`), following the official
FastAPI guide ["Bigger Applications"](https://fastapi.tiangolo.com/tutorial/bigger-applications/).

```
.
├── main.py               # entry point: creates the app, lifespan event, includes routers
├── settings.py            # application configuration (.env)
├── dependencies.py        # shared dependencies: get_db, pagination
├── requirements.txt
│
├── db/
│   ├── database.py         # async engine, SessionLocal, Base
│   └── models.py            # SQLAlchemy models: City, Temperature
│
├── city/
│   ├── router.py
│   ├── schemas.py
│   └── crud.py
│
└── temperature/
    ├── router.py
    ├── schemas.py
    ├── crud.py
    └── weather.py           # Open-Meteo client (geocoding + forecast)
```

## Installation and Running

### 1. Clone the repository and create a virtual environment

```bash
git clone <repository-url>
cd py-fastapi-city-temperature-management-api.db
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Copy the example file and edit it if needed:

```bash
cp .env.sample .env
```

By default, the application works with SQLite without any extra setup.

### 4. Run the application

```bash
uvicorn main:app --reload
```

Database tables are created automatically on startup (via the `lifespan`
event).

### 5. Open the API documentation

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Main Endpoints

| Method | Path                         | Description                                          |
|--------|-------------------------------|-------------------------------------------------------|
| GET    | `/cities/`                    | List cities (pagination via `skip`, `limit`)            |
| POST   | `/cities/`                    | Create a city                                            |
| GET    | `/cities/{city_id}/`           | Retrieve a city by id                                     |
| PUT    | `/cities/{city_id}/`           | Update a city                                              |
| DELETE | `/cities/{city_id}/`           | Delete a city                                               |
| GET    | `/temperatures/`               | List temperatures (filter by `city_id`, pagination)         |
| POST   | `/temperatures/update/`         | Fetch the current temperature for all cities                |

### Example: seed the database and update temperatures

```bash
curl -X POST http://127.0.0.1:8000/cities/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Kyiv", "additional_info": "Capital of Ukraine"}'

curl -X POST http://127.0.0.1:8000/temperatures/update/
```

## Design Choices

- **Fully asynchronous stack.** SQLAlchemy `AsyncSession` is used instead of
  a synchronous `Session`, and `httpx.AsyncClient` instead of `requests`.
  Since the key operation (`POST /temperatures/update/`) performs a network
  request per city, async allows all cities to be queried **concurrently**
  (`asyncio.gather`) instead of waiting for each request sequentially.

- **`return_exceptions=True` in `asyncio.gather`.** If fetching data for one
  city fails (e.g. the city name cannot be geocoded), this should not fail
  the entire request — the remaining cities are still processed, and the
  failing one is simply skipped.

- **Dependency Injection.**
  - `get_db` manages the database session lifecycle (`Depends`), ensuring
    the session is closed even if an exception occurs inside the endpoint.
  - `PaginationDep` is a shared dependency for `skip`/`limit` with built-in
    validation (`Query(ge=..., le=...)`), reused across both routers
    (`city`, `temperature`) without duplicating the function signature.
  - A single `httpx.AsyncClient` instance is created once at application
    startup (via `lifespan`) and reused across requests, instead of
    creating a new client on every endpoint call.

- **Custom exceptions in the `crud` layer.** Instead of repeating
  "record exists" checks in every route, business logic (e.g.
  `CityNotFoundError`) is encapsulated in `crud.py`. The router only
  translates the exception into the corresponding HTTP status code.

- **Eager loading via `selectinload`.** The `Temperature` schema includes a
  nested `city` object. Since `AsyncSession` does not support implicit lazy
  loading (which raises a `MissingGreenlet` error), related cities are
  explicitly loaded with an extra query directly in `crud.py`.

- **Documented response codes.** Each endpoint declares its possible status
  codes (e.g. `404` for a missing city, `422` for invalid request bodies)
  via the `responses` parameter, so the auto-generated Swagger/ReDoc docs
  reflect real endpoint behavior, not just the happy path.

## Assumptions and Simplifications

- The weather data source is the free, public Open-Meteo API, which
  requires no API key. A city name is first geocoded (via the
  `geocoding-api.open-meteo.com` endpoint), and the current temperature is
  then fetched using the resulting coordinates.
- Each call to `POST /temperatures/update/` creates **new** records in the
  `Temperature` table (a history), rather than overwriting the latest
  existing record — this preserves a temperature history over time.
- If a city name cannot be geocoded (no matching city in Open-Meteo's
  database, or a misspelled name), that city's record is simply skipped
  without failing the whole request.
- Default pagination values: `skip=0`, `limit=10` (maximum `100`).
- Authentication/authorization is not implemented, as it was not required
  by the task.
