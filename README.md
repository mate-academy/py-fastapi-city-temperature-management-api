# City Temperature Management API

A FastAPI application for managing cities and tracking the history of their
current temperature readings.

## Features

- **City CRUD** — create, list, retrieve, update, and delete cities.
- **Temperature history** — fetch the current temperature for every stored
  city from a public weather API and persist it, then query the recorded
  history (optionally filtered by city).

## Project Structure

```
app/
├── main.py             # FastAPI app instance, router registration, table creation
├── database.py         # SQLAlchemy engine/session setup and get_db dependency
├── models.py           # SQLAlchemy ORM models (City, Temperature)
├── schemas.py          # Pydantic request/response models
├── weather.py           # Async client for fetching current temperatures
└── routers/
    ├── cities.py        # /cities endpoints
    └── temperatures.py  # /temperatures endpoints
```

## Running the application

1. Create a virtual environment and install dependencies:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate        # Windows
   source .venv/bin/activate     # macOS/Linux
   pip install -r requirements.txt
   ```

2. Start the development server:

   ```bash
   uvicorn app.main:app --reload
   ```

3. Open the interactive API docs at http://127.0.0.1:8000/docs

A SQLite database file (`city_temperature.db`) is created automatically in
the project root on startup — no extra setup required.

## API Overview

| Method | Path                          | Description                              |
|--------|-------------------------------|-------------------------------------------|
| POST   | `/cities`                     | Create a city                             |
| GET    | `/cities`                     | List all cities                           |
| GET    | `/cities/{city_id}`           | Get a single city                         |
| PUT    | `/cities/{city_id}`           | Update a city                             |
| DELETE | `/cities/{city_id}`           | Delete a city                             |
| POST   | `/temperatures/update`        | Fetch & store the current temperature for every city |
| GET    | `/temperatures`               | List all temperature records              |
| GET    | `/temperatures?city_id={id}`  | List temperature records for one city     |

## Design choices

- **SQLite + SQLAlchemy ORM**: simple, file-based, zero-configuration
  persistence that satisfies the task requirements without extra
  infrastructure.
- **Open-Meteo** (`open-meteo.com`) is used as the weather data source: it is
  free, requires no API key, and offers both geocoding (city name → lat/lon)
  and current-weather endpoints, which keeps the assignment runnable
  out-of-the-box for any reviewer.
- **`POST /temperatures/update`** fetches data for every city using a single
  shared `httpx.AsyncClient`, awaiting each request sequentially. If a city's
  name cannot be geocoded or the weather API call fails, that city is skipped
  rather than failing the whole batch, and the endpoint returns the list of
  temperature records that were successfully created.
- **Dependency injection**: the database session is provided via the
  `get_db` FastAPI dependency, used by every router so each request gets an
  isolated session that is properly closed afterward.
- **Router separation**: cities and temperatures are split into separate
  `APIRouter` modules under `app/routers/`, mirroring FastAPI's recommended
  "Bigger Applications" project layout.

## Assumptions / simplifications

- City names are assumed to be geocodable by Open-Meteo's geocoding API (e.g.
  "London", "Kyiv"); ambiguous names resolve to the first/best match.
- City `name` is treated as unique to avoid duplicate weather lookups and
  ambiguous temperature history.
- Temperatures are stored in Celsius, as returned by Open-Meteo's
  `current_weather` field.
- No authentication/authorization is implemented, as it was not part of the
  task requirements.
