# City Temperature Management API

A FastAPI application that manages a list of cities and stores their current temperature, fetched from an external weather service.

## Tech stack

- **FastAPI** for the web API
- **SQLAlchemy 2.0** for the ORM, with **SQLite** as the database
- **Alembic** for migrations
- **Pydantic** for request and response schemas
- **httpx** with **asyncio** for async calls to [weatherapi.com](https://www.weatherapi.com/)
- **uv** for dependency management

## Setup

1. Install [uv](https://docs.astral.sh/uv/), then install dependencies:
   ```bash
   uv sync
   ```
2. Create a `.env` file based on `.env.sample`:
   ```env
   DATABASE_URL=sqlite:///./db.sqlite
   WEATHER_API_KEY=your_weatherapi_key
   ```
   You can get a free API key at weatherapi.com.
3. Apply the migrations:
   ```bash
   uv run alembic upgrade head
   ```
4. Start the server:
   ```bash
   uv run uvicorn main:app --reload
   ```

The interactive docs are at http://127.0.0.1:8000/docs.

## Endpoints

### Cities

| Method | Path | Description |
|---|---|---|
| POST | `/cities` | Create a city |
| GET | `/cities` | List all cities |
| GET | `/cities/{city_id}` | Get one city |
| DELETE | `/cities/{city_id}` | Delete a city |

### Temperatures

| Method | Path | Description |
|---|---|---|
| POST | `/temperatures/update` | Fetch the current temperature for every city and store it |
| GET | `/temperatures` | List all temperature records |
| GET | `/temperatures?city_id={id}` | List records for one city |

## Project structure

```
cities/          # City model, schemas, CRUD, routes
temperatures/    # Temperature model, schemas, CRUD, routes, weather API client
alembic/         # Migrations
database.py      # Engine, session, Base, get_db_session dependency
main.py          # App creation and router registration
```

Each app is a separate package with its own `models.py`, `schemas.py`, `crud.py` and `routers.py`. `database.py` holds the shared `Base`, so all tables live in one metadata object.

## Design choices

- **Layered structure.** Routes handle HTTP, CRUD functions handle the database, and `weather_client.py` handles the external API. Only the route that calls the weather API and the client are async. The CRUD layer, schemas and models are plain sync code.
- **Concurrent fetching.** `POST /temperatures/update` uses `asyncio.gather` with a shared `httpx.AsyncClient`, so requests for all cities run concurrently instead of one by one.
- **Separate schemas.** Pydantic schemas are kept separate from SQLAlchemy models, so the API contract doesn't depend on the database structure.
- **Migrations with Alembic.** The schema is managed through migrations instead of `create_all`.
- **Configuration in `.env`.** The database URL and API key are not hard-coded.