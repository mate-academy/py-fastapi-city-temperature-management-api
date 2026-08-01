# City & Temperature Management API

A FastAPI application for managing city data and tracking temperature history for each city, using data fetched from the OpenWeatherMap API.

The project has two main components:

1. **City CRUD API** — create, read, update, and delete cities.
2. **Temperature API** — fetch the current temperature for every stored city from OpenWeatherMap, save it to the database, and browse the resulting history.

## Tech Stack

- **FastAPI** — web framework
- **SQLAlchemy** — ORM
- **PostgreSQL** — database
- **Alembic** — database migrations
- **httpx** — async HTTP client for calling the OpenWeatherMap API
- **Docker / Docker Compose** — containerization

## Getting Started

### 1. Get an OpenWeatherMap API key

The temperature-update endpoint fetches live weather data from [OpenWeatherMap](https://openweathermap.org/), which requires a free API key:

1. Go to [openweathermap.org](https://openweathermap.org/) and create a free account.
2. Once logged in, open **API keys** in your account menu.
3. Copy the default key that's generated for you (or create a new one).
4. It may take a few minutes for a newly created key to become active.

### 2. Configure environment variables

Copy the sample env file and fill in your own values:

```bash
cp .env_sample .env
```

`.env` should contain:

```
POSTGRES_DB=your_db_name
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password
POSTGRES_HOST=db
POSTGRES_PORT=5432

OPEN_WEATHER_MAP_KEY=your_openweathermap_api_key
```

`POSTGRES_HOST` should stay as `db` — that's the name of the database service inside Docker Compose.

### 3. Run with Docker

```bash
docker-compose up --build
```

This single command will:

- build the application image,
- start a PostgreSQL container and wait until it's ready to accept connections,
- automatically apply all Alembic migrations,
- start the API server.

Once it's running, open the interactive API docs:

```
http://localhost:8000/docs
```

All endpoints (`/cities`, `/temperatures`) can be explored and tested directly from there.

## Design Decisions

**Structure by domain, not by file type.** The project is split into two self-contained apps, `city/` and `temperature/`, each with its own `models.py`, `schemas.py`, `crud.py`, and `router.py`. Keeping everything related to a single domain together (instead of one big `models.py` for the whole project, one big `routes.py`, etc.) keeps each app understandable on its own and makes it easy to add more apps later without touching existing ones.

**Sync database access, async only where it's actually needed.** SQLAlchemy sessions and all CRUD functions are synchronous — the database layer doesn't need `async`/`await` for anything. The only place that genuinely benefits from being asynchronous is the call to the external OpenWeatherMap API (`fetch_temperature`), since that's the one operation that actually waits on network I/O. Mixing a sync DB session with an `async def` endpoint is fully supported by FastAPI, so there was no need to rewrite the whole app around `AsyncSession` just for one HTTP call.

**`database.py` vs. `dependencies.py`.** Database configuration (engine, session factory, declarative `Base`) lives in `database.py`, while the `get_db` dependency used by every route lives separately in `dependencies.py`. This keeps "how to connect to the database" and "how a request borrows a database session" as two distinct concerns.

**PostgreSQL + Docker instead of plain SQLite.** SQLite alone would have satisfied all the functional requirements of this assignment — the reason for adding PostgreSQL and Docker Compose was purely to practice a more production-like setup (a real client-server database, containerized services, environment-based configuration) rather than any technical limitation of SQLite/SQLAlchemy.

## Error Handling

- **404 Not Found** — returned by `GET /cities/{city_id}`, `PUT /cities/{city_id}`, and `DELETE /cities/{city_id}` when the requested city doesn't exist.
- **400 Bad Request** — returned by `POST /cities/` when trying to create a city with a name that already exists (`name` is a unique column).
- **Graceful handling of unknown cities during a temperature update.** `POST /temperatures/update` fetches weather for every city in the database. If OpenWeatherMap can't find a city (e.g. a typo in its name) or returns any other error status, that city is skipped instead of failing the whole request. The response reports which cities were updated successfully and which ones failed:

```json
{
  "updated": ["Kyiv", "Lviv"],
  "failed": ["Asdfqwertyxyz"]
}
```

## Assumptions & Simplifications

- No authentication/authorization — any client can create, update, or delete cities.
- No automated test suite; the API was tested manually through the Swagger UI (`/docs`).
- OpenWeatherMap is the only weather data source, with no fallback provider if it's unavailable.
