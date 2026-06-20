# City Temperature Management API

FastAPI application for managing cities and storing temperature history for them.

The project has two main parts:

- City CRUD API
- Temperature API that fetches current weather data from WeatherAPI and saves it to the database

## Technologies

- FastAPI
- SQLAlchemy
- Alembic
- SQLite
- Pydantic
- HTTPX
- WeatherAPI

## Setup

Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```env
WEATHER_API_KEY=your_weatherapi_key
DATABASE_URL=sqlite:///./weather.db
```

`DATABASE_URL` is optional. If it is not provided, the application uses `sqlite:///./weather.db` by default.

Apply database migrations:

```bash
alembic upgrade head
```

Run the application:

```bash
uvicorn main:app --reload
```

The API documentation will be available at:

- `http://127.0.0.1:8000/docs`
- `http://127.0.0.1:8000/redoc`

## API Endpoints

### Cities

Create a city:

```http
POST /cities/
```

Request body:

```json
{
  "name": "Kyiv",
  "additional_info": "Capital of Ukraine"
}
```

Get all cities:

```http
GET /cities/
```

Get one city:

```http
GET /cities/{city_id}/
```

Update a city:

```http
PUT /cities/{city_id}/
```

Delete a city:

```http
DELETE /cities/{city_id}/
```

### Temperatures

Fetch current temperatures for all cities and save them to the database:

```http
POST /temperatures/update/
```

Get all temperature records:

```http
GET /temperatures/
```

Get temperature records for a specific city:

```http
GET /temperatures/?city_id=1
```

## Design Choices

The project is split into separate `city` and `temperature` modules. Each module contains its own SQLAlchemy model, Pydantic schemas, CRUD logic, and router where needed.

Database access is handled through FastAPI dependency injection with `get_db`, so endpoints do not create database sessions directly.

Application settings are loaded from environment variables with Pydantic Settings. The project reads values from a `.env` file and caches the settings object with `lru_cache`.

The weather API call is isolated in `weather.py`. The `fetch_temperature` function is asynchronous because it performs an external HTTP request with `httpx.AsyncClient`.

The application uses synchronous SQLAlchemy sessions for database operations. Because of that, database calls use regular `db.add`, `db.commit`, and `db.refresh` without `await`.

## Assumptions and Simplifications

- Weather data is fetched from WeatherAPI.
- Temperature is stored in Celsius using the `current.temp_c` field.
- The stored timestamp comes from WeatherAPI's `current.last_updated` field.
- City names are unique.
- If there are no cities, `POST /temperatures/update/` returns `404`.
- If the external weather provider fails, the endpoint returns an error instead of saving partial data.

## Original Task

The original task text was moved to `TASK.md`.
