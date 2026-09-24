# City Temperature Management API

A FastAPI application for managing cities and tracking their temperatures.
It provides CRUD endpoints for cities and an endpoint that fetches the current
temperature for every stored city from an online weather service, storing the
results as a history of temperature records.

## Features

- **City CRUD API**: create, list, retrieve, update, and delete cities.
- **Temperature API**: fetch current temperatures for all cities concurrently
  and browse the stored history, either for all cities or for one city.
- **Fully asynchronous**: async FastAPI endpoints, async SQLAlchemy sessions
  (`aiosqlite`), and async HTTP requests (`httpx`).
- **Database migrations** managed with Alembic.
- **Interactive documentation** generated automatically by FastAPI.

## Tech Stack

| Component | Technology |
|---|---|
| Web framework | FastAPI |
| Data validation | Pydantic v2 |
| ORM | SQLAlchemy 2.0 (async) |
| Database | SQLite via `aiosqlite` |
| Migrations | Alembic |
| HTTP client | `httpx` (async) |
| Weather data | [Open-Meteo](https://open-meteo.com/) (free, no API key) |
| Settings | `pydantic-settings` |

## Project Structure

```
py-fastapi-city-temperature-management-api/
├── alembic/                # Database migrations
│   ├── versions/
│   └── env.py
├── city/
│   ├── crud.py             # Database operations for cities
│   ├── models.py           # SQLAlchemy City table
│   ├── router.py           # /cities endpoints
│   └── schemas.py          # Pydantic request/response models
├── temperature/
│   ├── crud.py             # Database operations for temperatures
│   ├── models.py           # SQLAlchemy Temperature table
│   ├── router.py           # /temperatures endpoints
│   ├── schemas.py          # Pydantic request/response models
│   └── weather.py          # Client for the Open-Meteo API
├── alembic.ini
├── database.py             # Engine, session factory, declarative Base
├── dependencies.py         # FastAPI dependencies (database session)
├── main.py                 # Application entry point
├── settings.py             # Configuration loaded from environment / .env
└── requirements.txt
```

Each feature folder follows the same layering:

- **`models.py`** describes database tables.
- **`schemas.py`** describes the data the API accepts and returns.
- **`crud.py`** contains the queries that read and write the database.
- **`router.py`** defines the HTTP endpoints and maps results to status codes.

## Getting Started

### Prerequisites

- Python 3.12 or newer, **64-bit**. (On Windows, the 32-bit build has no
  prebuilt wheel for `greenlet`, a required dependency of async SQLAlchemy, and
  installation fails without a C++ compiler.)

### Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd py-fastapi-city-temperature-management-api
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv

   # Windows
   .venv\Scripts\activate

   # macOS / Linux
   source .venv/bin/activate
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. (Optional) Create a `.env` file in the project root to override the default
   settings:

   ```env
   DATABASE_URL=sqlite+aiosqlite:///./proj_db.db
   ```

   If no `.env` file exists, the default above is used.

5. Apply the database migrations:

   ```bash
   alembic upgrade head
   ```

6. Start the server:

   ```bash
   uvicorn main:app --reload
   ```

The API is now available at `http://127.0.0.1:8000`.

### Interactive Documentation

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## API Reference

### Cities

| Method | Endpoint | Description | Success |
|---|---|---|---|
| `POST` | `/cities` | Create a new city | `201 Created` |
| `GET` | `/cities` | List all cities | `200 OK` |
| `GET` | `/cities/{city_id}` | Get a specific city | `200 OK` |
| `PUT` | `/cities/{city_id}` | Update a specific city | `200 OK` |
| `DELETE` | `/cities/{city_id}` | Delete a specific city | `204 No Content` |

Requests for a city that does not exist return `404 Not Found`.

**Create a city**

```bash
curl -X POST http://127.0.0.1:8000/cities \
  -H "Content-Type: application/json" \
  -d '{"name": "Kyiv", "additional_info": "Capital of Ukraine"}'
```

Response:

```json
{
  "id": 1,
  "name": "Kyiv",
  "additional_info": "Capital of Ukraine"
}
```

`additional_info` is optional and may be omitted or set to `null`.

**Update a city**

`PUT` replaces the city's data, so all fields must be sent:

```bash
curl -X PUT http://127.0.0.1:8000/cities/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "Kyiv", "additional_info": "Largest city in Ukraine"}'
```

### Temperatures

| Method | Endpoint | Description | Success |
|---|---|---|---|
| `POST` | `/temperatures/update` | Fetch and store current temperatures for all cities | `200 OK` |
| `GET` | `/temperatures` | List all temperature records | `200 OK` |
| `GET` | `/temperatures?city_id={city_id}` | List temperature records for one city | `200 OK` |

**Update temperatures**

```bash
curl -X POST http://127.0.0.1:8000/temperatures/update
```

Response:

```json
{
  "updated": 3,
  "failed": []
}
```

`updated` is the number of new temperature records saved. `failed` lists the
names of cities whose temperature could not be fetched, for example because
the name was not recognized by the weather service or the request timed out.
A failure for one city does not prevent the others from being updated.

**Get temperature records**

```bash
curl "http://127.0.0.1:8000/temperatures?city_id=1"
```

Response:

```json
[
  {
    "id": 1,
    "city_id": 1,
    "date_time": "2026-09-25T14:00:00Z",
    "temperature": 17.3
  }
]
```

Temperatures are in degrees Celsius. Timestamps are stored in UTC.

## How Temperature Updates Work

1. All cities are loaded from the database.
2. For each city, two requests are made to Open-Meteo:
   - the **Geocoding API** converts the city name into coordinates;
   - the **Forecast API** returns the current temperature (`temperature_2m`)
     for those coordinates.
3. The requests for all cities run **concurrently** with `asyncio.gather`, so
   the total time is close to the time needed for a single city rather than
   the sum for all of them. One shared `httpx.AsyncClient` reuses connections.
4. Successful results are saved in one transaction, all with the same
   timestamp, so records from one update can be easily grouped.

## Design Decisions

- **Async throughout.** Fetching weather data is network-bound, so async I/O
  lets the server handle other requests while waiting for responses, and lets
  all city requests run concurrently.
- **Separate schemas and models.** SQLAlchemy models describe storage, and
  Pydantic schemas describe the API contract. This keeps generated fields like
  `id` out of request bodies and lets the response shape differ from the table
  when needed.
- **CRUD layer.** Database queries live in `crud.py` rather than in the
  routers, so they can be reused. For example, the temperature update reuses
  the city listing query.
- **Open-Meteo as the data source.** It is free and needs no API key, which
  makes the project easy to run without extra configuration.

## Limitations and Possible Improvements

- **Ambiguous city names.** Geocoding uses the first match for a name, so a
  name shared by several places (for example "Springfield") may resolve to
  the wrong one. Storing coordinates on the `City` model would fix this and
  also remove one request per city on every update.
- **Deleting a city with temperature records.** Records referencing a deleted
  city should be removed together with it, via a cascade on the relationship.
- **Pagination.** List endpoints return all records, which may become slow as
  the temperature history grows.
- **Tests.** Automated tests for the endpoints, with the weather API mocked,
  would make changes safer.