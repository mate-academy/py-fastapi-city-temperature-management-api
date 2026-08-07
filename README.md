# City Temperature Management API

FastAPI application for managing cities and storing current temperature readings fetched from OpenWeatherMap.

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (recommended) or any compatible package manager
- An [OpenWeatherMap](https://openweathermap.org/api) API key

## Setup

1. Clone the repository and enter the project directory.

2. Install dependencies:

```bash
uv sync
```

3. Create a `.env` file in the project root:

```env
SQLITE_FILE_NAME=sqlite_file
OPENWEATHER_API_KEY=your_openweathermap_api_key
```

4. Apply database migrations:

```bash
uv run alembic upgrade head
```

5. Start the application:

```bash
uv run uvicorn main:app --reload
```

The API is available at `http://127.0.0.1:8000`. Interactive docs: `http://127.0.0.1:8000/docs`.

## API Overview

### Cities

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/city` | Create a city |
| `GET` | `/cities` | List all cities |
| `PATCH` | `/cities/{city_id}` | Update a city |
| `DELETE` | `/cities/{city_id}` | Delete a city |

**Create city example:**

```bash
curl -X POST http://127.0.0.1:8000/city \
  -H "Content-Type: application/json" \
  -d '{"name": "Kyiv", "additional_info": "Capital of Ukraine"}'
```

### Temperatures

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/temperatures` | List all temperature records |
| `GET` | `/temperatures?city_id={id}` | List temperatures for a city |
| `POST` | `/temperatures` | Fetch and store temperatures for cities that do not have a record yet |
| `PATCH` | `/temperatures` | Refresh stored temperatures from OpenWeatherMap |

**Update temperatures example:**

```bash
curl -X PATCH http://127.0.0.1:8000/temperatures
```

## Project Structure

```
├── main.py                 # FastAPI app entry point
├── core/                   # Settings and async DB engine
├── models/                 # SQLAlchemy ORM models
├── schemes/                # Pydantic request/response schemas
├── routers/                # HTTP route handlers
├── services/               # Business logic and external API calls
├── dependecies/            # FastAPI dependency injection helpers
└── alembic/                # Database migrations
```

## Design Choices

- **Layered layout.** Routes stay thin; business logic lives in `services/`, schemas in `schemes/`, and persistence in `models/`. This follows common FastAPI project organization and keeps concerns separated.
- **Async throughout.** SQLAlchemy async sessions (`aiosqlite`) and `aiohttp` are used so database and weather requests do not block the event loop.
- **Dependency injection.** Database sessions and query filters are injected via FastAPI `Depends`, which keeps handlers testable and avoids global session handling.
- **Configuration via settings.** `pydantic-settings` loads `SQLITE_FILE_NAME` and `OPENWEATHER_API_KEY` from `.env`, so secrets and environment-specific values stay out of code.
- **Alembic migrations.** Schema changes are versioned instead of creating tables ad hoc on startup.
- **OpenWeatherMap.** Temperatures are resolved by geocoding the city name, then calling the current weather API with metric units (°C).
- **City uniqueness.** City `name` is unique in the database to avoid duplicate entries for the same place.
- **Partial city updates.** City updates use `PATCH` with optional fields so clients can change only `name` or only `additional_info`.

## Assumptions and Simplifications

- City names are assumed to be resolvable by OpenWeatherMap’s geocoding API. Ambiguous or invalid names may fail when fetching weather.
- Temperature history is simplified: `POST /temperatures` creates at most one record per city; `PATCH /temperatures` updates existing records in place rather than appending a new historical row on every refresh.
- The optional `GET /cities/{city_id}` endpoint was not implemented; list and update/delete by id cover the needed city workflows.
- Temperature update uses `PATCH /temperatures` (and an initial `POST /temperatures`) instead of a single `POST /temperatures/update` endpoint, separating first-time creation from refresh.
- SQLite is used as a local file database, which is enough for development and evaluation but not intended for high-concurrency production use.
- Error handling focuses on missing cities and integrity conflicts; transient OpenWeatherMap failures are not retried automatically.
