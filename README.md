# City Temperature Management API

## How to run

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
uvicorn main:app --reload
```

API docs: http://127.0.0.1:8000/docs

## Design choices

- Two apps, `cities` and `temperatures`, each with its own `models`, `schemas`, `crud` and `router`.
- Async SQLAlchemy with SQLite (`aiosqlite`); the schema is managed by Alembic migrations.
- The DB session is injected via `Depends(get_db)`; a city is loaded via the `get_city_or_404` dependency.
- Temperatures come from the Open-Meteo API (free, no API key): a geocoding request resolves the city name to coordinates, then a forecast request returns the current temperature.
- `POST /temperatures/update/` fetches all cities concurrently with `asyncio.gather` through one shared `httpx.AsyncClient`.
- A failure for one city does not stop the update: successful results are saved in one commit, failed cities are listed in the response.

## Assumptions and simplifications

- A city is looked up in the weather API by name; the first geocoding result is used.
- City names are unique.
- Temperature is in °C.
- `date_time` is the time of the update, in UTC.
- Open-Meteo refreshes current data every 15 minutes, so repeated updates within that interval return the same value.
- Deleting a city deletes its temperature records.
- `PUT` replaces all fields of a city.
- No pagination, authentication or scheduled updates.
