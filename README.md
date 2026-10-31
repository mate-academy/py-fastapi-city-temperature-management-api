# City Temperature Management API

A FastAPI application for managing cities and keeping a history of their current temperatures.

## Setup and run

Requires Python 3.10 or newer. From the project directory:

```bash
python -m venv venv
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs for interactive API documentation. SQLite database `db.sqlite3` and its tables are created automatically on startup. Run tests with `python -m pytest`.

## API

- `POST /cities`: create a city, e.g. `{"name": "Kyiv", "additional_info": "Ukraine"}`. `additional_info` is optional.
- `GET /cities`: list cities.
- `DELETE /cities/{city_id}`: delete a city and its temperature history; returns 404 if it does not exist.
- `POST /temperatures/update`: fetch and save one reading per city; returns the created readings. An empty city list returns an empty list.
- `GET /temperatures`: list all readings; `?city_id=1` filters by city. Each record includes its city ID, time and temperature.

## Design and assumptions

SQLAlchemy models store cities and readings in SQLite. Pydantic schemas validate requests and serialize ORM objects; FastAPI dependencies provide database sessions and an HTTP client. Tables are created on startup; this simple project does not include migrations.

Open-Meteo geocoding resolves each city by name, and the first result is used when names are ambiguous. The forecast API supplies the current temperature in degrees Celsius and its observation time in UTC. Requests for cities run asynchronously. All readings are collected before a single database commit: if any lookup or weather request fails, the endpoint returns 502 and saves none of that update. An unknown city also causes 502. Existing history remains intact. Duplicate city names are allowed and each city receives its own record.

Tests use an isolated in-memory database and controlled HTTP responses, so they do not depend on the external service.
