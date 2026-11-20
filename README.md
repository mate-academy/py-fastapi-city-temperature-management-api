# City Temperature Management API

A FastAPI application with two apps: a CRUD API for cities and a temperature API that fetches the current temperature for every city from [WeatherAPI.com](https://www.weatherapi.com/) and keeps the history in the database.

**Tech stack:** FastAPI, async SQLAlchemy 2 + aiosqlite (SQLite), Alembic, Pydantic Settings, httpx.

## Running locally

Requires Python 3.12 and a free WeatherAPI.com key.

```bash
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.sample .env               # then put your key into WEATHER_API_KEY
alembic upgrade head
uvicorn main:app --reload
```

Swagger UI: http://127.0.0.1:8000/docs

### Environment variables

| Variable | Required | Description |
|---|---|---|
| `WEATHER_API_KEY` | yes | WeatherAPI.com key |
| `URL_WEATHER` | yes | `https://api.weatherapi.com/v1/current.json` |
| `DATABASE_URL` | no | Defaults to `sqlite+aiosqlite:///./city_temperature_management.db` |

The app does not start if a required variable is missing.

## Endpoints

| Method | Path | Description |
|---|---|---|
| POST | `/cities/` | Create a city (400 if the name is taken) |
| GET | `/cities/` | List all cities |
| GET | `/cities/{city_id}/` | Get one city (404 if missing) |
| PUT | `/cities/{city_id}/` | Update a city (404 / 400) |
| DELETE | `/cities/{city_id}/` | Delete a city with its history (204) |
| POST | `/temperatures/update/` | Fetch and store current temperatures |
| GET | `/temperatures/` | List all temperature records |
| GET | `/temperatures/?city_id={id}` | Records for one city (404 if missing) |

## Design choices

- **Two apps, one layout.** `city/` and `temperature/` each have `models`, `schemas`, `crud` and `router`. Routers handle HTTP (status codes, 404/400), CRUD functions only talk to the database.
- **Dependency injection.** `get_db` in `dependencies.py` yields an `AsyncSession` per request via `Depends`.
- **Async all the way.** Async SQLAlchemy with aiosqlite; Alembic uses the async template and reads the same `DATABASE_URL` from settings.
- **Concurrent weather requests.** `POST /temperatures/update/` opens one `httpx.AsyncClient` and requests all cities at once with `asyncio.gather`. Each city's coroutine returns a ready `Temperature` object or `None`; the successful ones are saved with a single commit.
- **Weather client is separate.** `temperature/weather_api.py` only knows the external API (city name in, temperature or `None` out), not the database models.
- **Cascade delete.** The `City.temperatures` relationship uses `cascade="all, delete-orphan"`, so deleting a city removes its temperature history.
- **No N+1 / implicit IO.** Temperature records are loaded together with their city (`selectinload`), which the nested city in the response needs under `AsyncSession`.
- **No extra index on `temperature.city_id`.** The table is written to on every update; an index can be added with a migration if filtering by city becomes a hot path.

## Assumptions and simplifications

- Temperature is the current value in °C (`current.temp_c`). `date_time` is the server time when the record was created.
- WeatherAPI.com resolves cities by name, so an ambiguous name may match a different place (e.g. "Atlantis" exists in Florida and in South Africa).
- If the weather request for a city fails (unknown city name, timeout of 7 s, network error, unexpected response body), that city is skipped and the other cities are still saved.
- City names are unique. `PUT` replaces both fields.
