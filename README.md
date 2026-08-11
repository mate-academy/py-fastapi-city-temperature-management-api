# City & Temperature API

FastAPI application for managing cities and tracking their temperature history.

- **City CRUD API** — create, read, update, and delete cities.
- **Temperature API** — fetch current temperature for all cities from an online
  weather service (wttr.in) and store the history.

## Tech Stack

FastAPI, SQLAlchemy 2.0 (async), SQLite (`aiosqlite`), Pydantic v2, httpx.

## Project Structure

```
.
├── main.py                  # FastAPI app, table creation, router registration
├── database.py               # async engine, AsyncSessionLocal, Base
├── dependencies.py            # get_db() dependency
├── settings.py                 # app config
├── city/
│   ├── models.py               # DBCity
│   ├── schemas.py                # CityCreate, City
│   ├── crud.py                    # DB functions for cities
│   └── router.py                   # /cities endpoints
└── temperature/
    ├── models.py                # DBTemperature
    ├── schemas.py                 # TemperatureCreate, Temperature
    ├── crud.py                      # DB functions for temperature records
    ├── weather_service.py            # calls wttr.in, updates all cities
    └── router.py                      # /temperatures endpoints
```

## Setup & Run

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

pip install fastapi uvicorn "sqlalchemy>=2.0" aiosqlite httpx pydantic

uvicorn main:app --reload
```

Tables are created automatically on startup — no migrations needed.

Open the docs: http://127.0.0.1:8000/docs

## API Endpoints

### Cities

| Method | Path                | Description   |
|--------|---------------------|-----------------|
| POST   | `/cities/`             | Create a city     |
| GET    | `/cities/`               | List all cities    |
| GET    | `/cities/{city_id}`        | Get one city         |
| PUT    | `/cities/{city_id}`          | Update a city           |
| DELETE | `/cities/{city_id}`            | Delete a city              |

### Temperatures

| Method | Path                              | Description                                  |
|--------|-------------------------------------|-------------------------------------------------|
| POST   | `/temperatures/update`                | Fetch current temperature for every city and save it |
| GET    | `/temperatures/`                        | List all temperature records                          |
| GET    | `/temperatures/?city_id={city_id}`        | List temperature records for one city                  |

## Design Notes

- Everything is async end-to-end (DB driver + weather HTTP calls), so
  `POST /temperatures/update` doesn't block while waiting on external requests.
- SQLAlchemy models are prefixed with `DB` (`DBCity`, `DBTemperature`) to avoid
  name clashes with the Pydantic schemas (`City`, `Temperature`).
- `crud.py` functions never raise HTTP errors — they return `None` if a record
  isn't found, and the router turns that into a 404.
- Weather data comes from wttr.in, chosen because it accepts a plain city name
  (no API key, no geocoding step needed).

## Assumptions

- `additional_info` is a required field on `City`.
- City names don't have to be unique.
- `date_time` on a temperature record is the server time at the moment of the
  update call, not the observation time reported by wttr.in.
- No authentication — all endpoints are open.