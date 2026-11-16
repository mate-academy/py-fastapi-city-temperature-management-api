# City Temperature Management API

FastAPI application for managing cities and keeping a history of their current temperatures.

## Requirements

- Python 3.10 or newer
- Internet access for temperature updates (Open-Meteo; no API key required)

## Run locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open the interactive API documentation at <http://127.0.0.1:8000/docs>.

The app creates `city_temperature.db` in the current working directory on startup. To choose another SQLite file, set `DATABASE_URL`, for example:

```powershell
$env:DATABASE_URL = "sqlite+aiosqlite:///./cities.db"
uvicorn app.main:app --reload
```

## Endpoints

- `POST /cities` — create a city (`name`, optional `additional_info`).
- `GET /cities` — list cities.
- `GET /cities/{city_id}` — get one city.
- `PUT /cities/{city_id}` — update a city's fields.
- `DELETE /cities/{city_id}` — delete a city and its temperature history.
- `POST /temperatures/update` — fetch and save a current reading for every city.
- `GET /temperatures` — list saved readings; optional `city_id` query parameter filters by city.

Example city request:

```json
{
  "name": "Chisinau",
  "additional_info": "Capital of Moldova"
}
```

`POST /temperatures/update` returns counts and per-city errors. A provider failure for one city does not discard successful readings for other cities. Each successful update adds a new history record.

## Design and assumptions

- The project separates database setup, SQLAlchemy models, Pydantic schemas, API routers, and weather-provider access under `app/`.
- SQLAlchemy's async engine and `aiosqlite` are used for database access. The weather requests use async `httpx` calls, with up to ten cities fetched concurrently.
- City names are geocoded using Open-Meteo's geocoding endpoint; the first matching result is used. The app does not store coordinates or ask the user to enter them.
- Open-Meteo's forecast endpoint supplies the current temperature and observation time. Stored times are UTC (SQLite stores them without timezone metadata).
- Temperature history is retained until its city is deleted. There is no authentication, pagination, or background scheduler in this training assignment; updates are triggered through the API endpoint.
