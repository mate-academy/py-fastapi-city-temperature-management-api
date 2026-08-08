# City Temperature Management API

FastAPI application for managing cities and storing their temperature history.
The service provides CRUD operations for cities, retrieves current weather from
Weatherstack, and saves every retrieved value as a separate temperature record.

## Features

- Create, list, retrieve, update, and delete cities.
- Fetch the current temperature for every city stored in the database.
- Use asynchronous HTTP requests when communicating with Weatherstack.
- Store temperature history instead of overwriting previous measurements.
- List all temperature records or filter them by city.
- Generate and apply database schema changes with Alembic.
- Validate request and response data with Pydantic.
- Interactive OpenAPI documentation provided by FastAPI.

## Technology stack

- Python 3.12+
- FastAPI
- SQLAlchemy 2.0
- Pydantic 2
- Alembic
- SQLite
- HTTPX
- Weatherstack API

## Project structure

```text
.
├── alembic/                       # Alembic environment and migrations
│   ├── versions/
│   └── env.py
├── city_crud_api/
│   ├── api/
│   │   ├── crud.py                # City database operations
│   │   ├── router.py              # City endpoints
│   │   └── schemas.py             # City Pydantic schemas
│   └── models.py                  # City SQLAlchemy model
├── db/
│   └── engine.py                  # Shared engine, session, and Base
├── temperature_api/
│   ├── crud.py                    # Temperature database operations
│   ├── get_temp.py                # Async Weatherstack client
│   ├── models.py                  # Temperature SQLAlchemy model
│   ├── router.py                  # Temperature endpoints
│   └── schemas.py                 # Temperature Pydantic schemas
├── .env.sample                    # Environment variable template
├── alembic.ini
├── main.py                        # FastAPI application entry point
└── requirements.txt
```

## Database design

The application uses one SQLite database with two related tables:

- `cities`: `id`, `name`, and optional `additional_info`.
- `temperatures`: `id`, `city_id`, `date_time`, and `temperature`.

`temperatures.city_id` is a foreign key referencing `cities.id`. The column is
indexed because temperature history is frequently filtered by city. The database
sets `date_time` when a temperature record is inserted.

## Installation and startup

### 1. Clone the repository

```bash
git clone --branch develop https://github.com/Lemonch1ks/py-fastapi-city-temperature-management-api.git
cd py-fastapi-city-temperature-management-api
```

### 2. Create a virtual environment

Windows PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Linux or macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Copy `.env.sample` to `.env`.

Windows PowerShell:

```powershell
Copy-Item .env.sample .env
```

Linux or macOS:

```bash
cp .env.sample .env
```

Set your Weatherstack API key in `.env`:

```dotenv
WEATHER_API_KEY=your_weatherstack_api_key
BASE_WEATHER_API_URL=http://api.weatherstack.com/
```

The application adds `/current` to the configured base URL. The `.env` file is
ignored by Git and must not be committed.

### 5. Apply migrations

```bash
python -m alembic upgrade head
```

This command creates `db.sqlite3` and the `cities`, `temperatures`, and
`alembic_version` tables.

### 6. Run the application

```bash
python -m uvicorn main:app --reload
```

The API is available at <http://127.0.0.1:8000>.

- Swagger UI: <http://127.0.0.1:8000/docs>
- ReDoc: <http://127.0.0.1:8000/redoc>

## API endpoints

### Cities

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/cities` | Create a city |
| `GET` | `/cities` | List all cities |
| `GET` | `/cities/{city_id}` | Retrieve a city |
| `PUT` | `/cities/{city_id}` | Update a city |
| `DELETE` | `/cities/{city_id}` | Delete a city |

Create a city:

```bash
curl -X POST http://127.0.0.1:8000/cities \
  -H "Content-Type: application/json" \
  -d '{"name":"Poltava","additional_info":"Ukraine"}'
```

Example response:

```json
{
  "name": "Poltava",
  "additional_info": "Ukraine",
  "id": 1
}
```

### Temperatures

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/temperatures/update` | Fetch and store current temperatures for all cities |
| `GET` | `/temperatures` | List all temperature records |
| `GET` | `/temperatures?city_id={city_id}` | List temperature records for one city |

Fetch and save current temperatures:

```bash
curl -X POST http://127.0.0.1:8000/temperatures/update
```

Filter temperature history by city:

```bash
curl "http://127.0.0.1:8000/temperatures?city_id=1"
```

Example temperature record:

```json
{
  "id": 1,
  "city_id": 1,
  "date_time": "2026-08-08T20:30:00",
  "temperature": 21.0
}
```

## Design choices

- A single FastAPI application includes separate city and temperature routers.
- Both components share one SQLAlchemy `Base`, session dependency, and SQLite
  database because temperature records reference cities.
- Router, schema, model, and CRUD responsibilities are kept in separate modules.
- `get_db` uses FastAPI dependency injection to provide and close a database
  session for every request.
- Weatherstack calls use `httpx.AsyncClient` and `await`, so waiting for the
  external API does not block the event loop.
- Weather requests are awaited one at a time to remain compatible with
  Weatherstack free-tier rate limits.
- Every update creates a new row in `temperatures`, preserving historical data.
- Alembic manages schema creation and future database changes.

## Error handling

- Unknown city IDs return `404 Not Found`.
- Invalid request bodies and query parameters return FastAPI validation errors.
- Missing Weatherstack settings, network failures, and provider errors return
  `502 Bad Gateway` from the update endpoint.
- Provider error responses do not expose the API key.

## Assumptions and simplifications

- SQLite is sufficient for this task and local development.
- Weatherstack's default temperature unit is used.
- City names are passed directly to Weatherstack and are not geocoded separately.
- City names are not required to be unique.
- Authentication and authorization are outside the task scope.
- Database operations use a synchronous SQLAlchemy session; only external
  weather requests are asynchronous, as required by the task.

## Migration commands

Create a migration after changing SQLAlchemy models:

```bash
python -m alembic revision --autogenerate -m "describe the change"
```

Apply all migrations:

```bash
python -m alembic upgrade head
```

Revert the latest migration:

```bash
python -m alembic downgrade -1
```
