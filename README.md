# City Temperature Management API

A FastAPI application that manages a list of cities and stores their temperature history. Current temperatures are fetched asynchronously from [WeatherAPI.com](https://www.weatherapi.com/) and saved to a SQLite database.

## Features

- CRUD API for cities (`POST`, `GET`, `DELETE`)
- Async endpoint that fetches the current temperature for **all** cities and stores it
- Temperature history endpoints, with optional filtering by city
- SQLAlchemy 2.0 ORM models with Alembic migrations
- Dependency injection for the database session
- Pydantic schemas for request/response validation

## Tech Stack

- Python 3.12+
- FastAPI
- SQLAlchemy 2.0 + SQLite
- Alembic (migrations)
- httpx (async HTTP client)
- python-dotenv
- [uv](https://docs.astral.sh/uv/) (dependency management)

## Project Structure

```
.
├── alembic/                 # Migration environment and versions
├── alembic.ini
├── pyproject.toml
├── .env                     # Local environment variables (not committed)
├── .env.sample             # Example environment file
├── .python-version
├── README.MD
├── uv.lock
└── src/
    ├── main.py              # FastAPI app and routes
    ├── py_fasatapi_city_temperature_management_api
    ├── crud/
    │   ├── cities.py        # City database operations
    │   └── temperatures.py  # Temperature database operations
    ├── schemas/             # Pydantic models
    │   ├── cities.py        
    │   └── temperatures.py 
    ├── db/
    │   ├── session.py       # Engine, session factory, get_db dependency
    │   │── base.py
    │   └── models/
    │       ├── cities.py    # City ORM model
    │       └── temperatures.py  # Temperature ORM model
    └── services.py       # Async client for the external weather API
```

## Getting Started

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd py-fastapi-city-temperature-management-api
```

### 2. Install dependencies

```bash
uv sync
```

### 3. Configure environment variables

Create a `.env` file in the project root:

```
DATABASE_URL=sqlite:///./city_temperature.db
WEATHER_API_KEY=your_weatherapi_key
```

Get a free API key by signing up at [weatherapi.com](https://www.weatherapi.com/).

### 4. Apply database migrations

```bash
uv run alembic upgrade head
```

### 5. Run the application

```bash
uv run uvicorn main:app --reload --app-dir src
```

The API is now available at `http://127.0.0.1:8000`.
Interactive docs (Swagger UI): `http://127.0.0.1:8000/docs`

## API Endpoints

### Cities

| Method | Path                | Description                | Success | Errors   |
|--------|---------------------|----------------------------|---------|----------|
| POST   | `/cities/`          | Create a new city          | 201     | 400 if the city already exists |
| GET    | `/cities/`          | List all cities            | 200     |          |
| GET    | `/cities/{city_id}/`| Get a specific city        | 200     | 404      |
| DELETE | `/cities/{city_id}/`| Delete a city              | 204     | 404      |

Example request body for `POST /cities/`:

```json
{
  "name": "Paris",
  "additional_info": "Capital of France"
}
```

### Temperatures

| Method | Path                          | Description                                          |
|--------|-------------------------------|------------------------------------------------------|
| POST   | `/temperatures/update/`       | Fetch the current temperature for all cities and store it |
| GET    | `/temperatures/`              | List all temperature records                         |
| GET    | `/temperatures/?city_id={id}` | List temperature records for one city (404 if the city does not exist) |

Example response from `POST /temperatures/update/`:

```json
{
  "updated": 2,
  "failed": ["Atlantis"]
}
```

`failed` contains the names of cities for which the weather API returned no data (unknown city, invalid key, network error, etc.).

## Design Choices

- **Layered structure.** Routes live in `main.py`, database access in `crud/`, ORM models in `db/models/`, Pydantic schemas in `schemas.py`, and the external API call in `services/weather.py`. Each layer has one responsibility, which keeps the routes thin and makes the weather provider easy to swap or mock.
- **Dependency injection.** The database session is provided through `Depends(get_db)` (wrapped in the `SessionDP` annotated alias), so each request gets its own session that is closed afterwards.
- **Async temperature fetching.** `POST /temperatures/update/` uses `httpx.AsyncClient` with `asyncio.gather`, so requests for all cities run concurrently instead of one after another.
- **Partial failures are tolerated.** If the weather API fails for one city, that city is reported in `failed`, while temperatures for the other cities are still saved.
- **One timestamp per update.** All records created by a single update call share the same UTC `date_time`, so a batch is easy to identify.
- **WeatherAPI.com as the data source.** It accepts a city name directly, so no coordinates or geocoding step are needed.
- **Alembic migrations** are used instead of `create_all()`, so schema changes are versioned.
- **Cascade delete.** Deleting a city also deletes its temperature records (`cascade="all, delete-orphan"` on the relationship).
- **Separate create/read schemas.** `CityCreate` is used for input and `City` (with `id`) for output.

## Assumptions and Simplifications

- City names are unique. Creating a duplicate returns `400`.
- City names are sent to the weather API as-is. Ambiguous names (for example "Springfield") resolve to whatever the provider matches first.
- Temperatures are stored in degrees Celsius.
- The database layer is synchronous. Only the external HTTP calls are async, since they are the slow part. A fully async setup would need `AsyncSession` and an async driver.
- The optional `PUT /cities/{city_id}` endpoint is not implemented.
- There is no authentication, pagination, or rate limiting on the API itself.
- The free WeatherAPI.com plan has a monthly call quota, and each update call makes one request per city.
- Routes are defined with trailing slashes. FastAPI redirects requests without a trailing slash to the slash version.

## Development Notes

Create a new migration after changing the models:

```bash
uv run alembic revision --autogenerate -m "describe change"
uv run alembic upgrade head
```

Quick manual test in `/docs`:

1. `POST /cities/` with a real city name, for example "Paris"
2. `POST /temperatures/update/` returns `{"updated": 1, "failed": []}`
3. `GET /temperatures/?city_id=1` shows the new record
4. `DELETE /cities/1/` returns `204`, and a second call returns `404`
