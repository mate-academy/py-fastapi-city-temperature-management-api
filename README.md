# City Temperature Management API

FastAPI application for managing cities and storing current temperature records for those cities.

## Requirements

- Python 3.13
- SQLite

## Installation

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

## Database Setup

Run Alembic migrations before starting the API:

```powershell
alembic upgrade head
```

This creates the SQLite database file `cities.db` with the `cities`, `temperatures`, and `alembic_version` tables.

## Run Application

Start the FastAPI server:

```powershell
uvicorn main:app --reload
```

Open the API documentation:

```text
http://127.0.0.1:8000/docs
```

## API Endpoints

City endpoints:

- `POST /cities`: create a city.
- `GET /cities`: list all cities.
- `GET /cities/{city_id}`: get one city.
- `PUT /cities/{city_id}`: update one city.
- `DELETE /cities/{city_id}`: delete one city.

Temperature endpoints:

- `POST /temperatures/update`: fetch current temperature for all saved cities and store records.
- `GET /temperatures`: list all temperature records.
- `GET /temperatures/?city_id={city_id}`: list temperature records for one city.

## Design Choices

The project is split into two domain packages:

- `city`: city models, schemas, CRUD operations, and FastAPI routes.
- `temperature`: temperature models, schemas, CRUD operations, weather client, and FastAPI router.

SQLite is used as the database, SQLAlchemy is used for ORM models and database sessions, and Alembic is used for schema migrations. FastAPI dependency injection provides a database session per request.

Temperature updates use Open-Meteo:

- Geocoding API resolves city names to coordinates.
- Forecast API returns the current `temperature_2m` value.

## Assumptions and Simplifications

- City names are resolved by the first Open-Meteo geocoding result.
- Temperature values are stored in Celsius.
- `POST /temperatures/update` processes cities sequentially.
- If a weather provider request fails, the endpoint returns `502 Bad Gateway`.
- Authentication and rate limiting are not implemented.
- SQLite is used for local development and evaluation.
