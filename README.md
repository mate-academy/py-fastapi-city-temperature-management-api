# City & Temperature Management API

FastAPI application with two parts: a CRUD API for managing cities and an
API that fetches current temperatures for all stored cities and keeps
their history.

## How to run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

The API docs (Swagger UI) are available at http://127.0.0.1:8000/docs

The SQLite database (`sql_app.db`) and its tables are created
automatically on the first start.

## Endpoints

### Cities
- `POST /cities/` - create a city
- `GET /cities/` - list all cities
- `GET /cities/{city_id}` - get a city
- `PUT /cities/{city_id}` - update a city
- `DELETE /cities/{city_id}` - delete a city

### Temperatures
- `POST /temperatures/update` - fetch current temperatures for all cities
  and store them
- `GET /temperatures` - list all temperature records
- `GET /temperatures?city_id=1` - list records for a specific city

## Design choices

- Async SQLAlchemy 2.0 with aiosqlite; the database is a SQLite file
  `sql_app.db`.
- The project is split into two packages, `city` and `temperature`, each
  with its own models, schemas, CRUD functions and router.
- The database session is provided through FastAPI dependency injection
  (`get_db`).
- Temperatures are fetched from the free Open-Meteo API (no API key
  needed). A city is first geocoded by name, then its current temperature
  is requested. Requests for all cities run concurrently with
  `asyncio.gather`.

## Assumptions and simplifications

- City names are unique.
- If a city cannot be found or the weather API fails for it, that city is
  skipped, and the response of `POST /temperatures/update` reports how
  many cities were updated and skipped.
- Deleting a city also deletes its temperature history.
- Tables are created on application startup; database migrations are not
  used.
