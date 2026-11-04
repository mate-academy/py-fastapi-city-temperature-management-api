# City & Temperature Management API

FastAPI app with two parts: a CRUD API for cities and an API that fetches
current temperatures for all stored cities and keeps their history.

## Run

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Docs: http://127.0.0.1:8000/docs

## Endpoints

- `POST /cities/`, `GET /cities/`, `GET /cities/{id}`, `PUT /cities/{id}`, `DELETE /cities/{id}`
- `POST /temperatures/update` - fetch current temperatures for all cities and store them
- `GET /temperatures` - all temperature records
- `GET /temperatures?city_id=1` - records for one city

## Design choices

- Async SQLAlchemy 2.0 + aiosqlite (SQLite file `sql_app.db`).
- Two packages (`city`, `temperature`), each with models/schemas/crud/router.
- DB session is provided through dependency injection (`get_db`).
- Temperatures come from the free Open-Meteo API (no API key). Cities are
  geocoded by name, then requests for all cities run concurrently via `asyncio.gather`.

## Assumptions

- City names are unique.
- If a city can't be found or the API fails for it, that city is skipped
  and the response reports how many were skipped.
- Deleting a city also deletes its temperature history.
- Tables are created on startup (no migrations).