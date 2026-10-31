# City Temperature Management API

FastAPI + SQLAlchemy (async, SQLite) application:

* `city` — CRUD for cities
* `temperature` — fetches the current temperature of every city from
  [Open-Meteo](https://open-meteo.com/) (no API key) and stores the history

## Run

```bash
uv sync
uv run uvicorn main:app --reload
```

Docs: http://127.0.0.1:8000/docs. Tables are created automatically on startup.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/cities` | create a city |
| GET | `/cities` | list cities |
| GET | `/cities/{city_id}` | city details |
| PUT | `/cities/{city_id}` | update a city |
| DELETE | `/cities/{city_id}` | delete a city (and its temperature history) |
| POST | `/temperatures/update` | fetch & store current temperature for all cities |
| GET | `/temperatures` | all temperature records |
| GET | `/temperatures/?city_id={id}` | records of one city |

## Design choices

* Layers per app: `router` (HTTP) -> `crud` (DB / external API) -> `models`.
* Dependency injection: the DB session comes from `Depends(get_db)`.
* Temperatures for all cities are fetched concurrently with `asyncio.gather` + `httpx.AsyncClient`.
  Open-Meteo needs coordinates, so each city name is geocoded first.

## Assumptions / simplifications

* Cities that Open-Meteo can't find are skipped; if the weather service fails, the endpoint returns 502.
* Tables are created with `create_all` (no migrations); no auth, pagination or tests.
* Deleting a city also deletes its temperature records (done manually in `city/crud.py`).