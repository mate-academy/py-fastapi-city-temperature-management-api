# City Temperature API

A FastAPI application for managing cities and storing their temperature
history.

The project contains two API areas:

- CRUD endpoints for cities.
- Temperature endpoints that fetch current weather data and store it in
  SQLite.

## Technologies

- FastAPI
- SQLAlchemy ORM
- SQLite
- Pydantic
- HTTPX
- Open-Meteo API

Open-Meteo is used because it provides geocoding and current temperature
data without requiring an API key.

## Project structure

```text
fastapi-city-temperature-api/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── dependencies.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── cities.py
│   │   └── temperatures.py
│   └── services/
│       ├── __init__.py
│       └── weather.py
├── .gitignore
├── requirements.txt
└── README.md
```

## Installation

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the application

From the project root:

```bash
uvicorn app.main:app --reload
```

The application will be available at:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

## City API

### Create a city

```http
POST /cities
```

Example JSON:

```json
{
  "name": "Tallinn",
  "additional_info": "Capital of Estonia"
}
```

### List cities

```http
GET /cities
```

Pagination is available:

```text
GET /cities?skip=0&limit=20
```

### Get one city

```http
GET /cities/{city_id}
```

### Update a city

```http
PUT /cities/{city_id}
```

Example JSON:

```json
{
  "name": "Tallinn",
  "additional_info": "Updated information"
}
```

### Delete a city

```http
DELETE /cities/{city_id}
```

Deleting a city also deletes its stored temperature records.

## Temperature API

### Update temperatures

```http
POST /temperatures/update
```

The endpoint:

1. Reads all cities from SQLite.
2. Resolves city coordinates using Open-Meteo Geocoding API.
3. Fetches current temperature asynchronously.
4. Stores successful results in the `temperatures` table.
5. Returns stored records and any city-specific errors.

### List temperature history

```http
GET /temperatures
```

Pagination:

```text
GET /temperatures?skip=0&limit=100
```

### Filter by city

```text
GET /temperatures?city_id=1
```

## Design choices

SQLAlchemy is used synchronously for SQLite because the database work is
small and simple. External weather requests are asynchronous, as required
by the task, and are executed concurrently with `asyncio.gather`.

The city table stores only the fields required by the task. Coordinates
are resolved from the city name when temperature data is requested, so
latitude and longitude do not need to be stored.

Separate routers are used for cities and temperatures. Database session
management is implemented as a FastAPI dependency.

## Error handling

The API returns:

- `404` when a requested city does not exist.
- `409` when a city name conflicts with an existing unique city.
- `400` when temperature update is requested with no cities.
- `502` when no temperature can be fetched from the external provider.

If temperature fetching fails only for some cities, successful
temperatures are still stored and the response contains an `errors`
list.

## Assumptions and simplifications

- City names are unique.
- Open-Meteo's first geocoding result is considered the intended city.
- Temperature values are stored in degrees Celsius.
- External weather data is fetched only when
  `POST /temperatures/update` is called.
- Database migrations are not used; tables are created automatically on
  application startup.
