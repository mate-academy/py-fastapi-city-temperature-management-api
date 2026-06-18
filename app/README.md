# City Temperature API

A FastAPI application that manages cities and their temperature history. Temperature data is fetched asynchronously from [Open-Meteo](https://open-meteo.com/) — a free, open-source weather API that requires no API key.

---

## Table of Contents

- [Project Structure](#project-structure)
- [How to Run](#how-to-run)
- [API Endpoints](#api-endpoints)
- [Design Choices](#design-choices)
- [Assumptions & Simplifications](#assumptions--simplifications)

---

## Project Structure

```
city_temperature_api/
├── app/
│   ├── main.py               # FastAPI app, router registration, lifespan
│   ├── database.py           # SQLAlchemy engine, SessionLocal, get_db dependency
│   ├── models/
│   │   └── models.py         # ORM models: City, Temperature
│   ├── schemas/
│   │   └── schemas.py        # Pydantic v2 request/response schemas
│   ├── crud/
│   │   ├── city.py           # City CRUD helpers
│   │   └── temperature.py    # Temperature CRUD helpers
│   ├── routers/
│   │   ├── cities.py         # /cities endpoints
│   │   └── temperatures.py   # /temperatures endpoints
│   └── services/
│       └── weather.py        # Async weather fetching (geocode + forecast)
├── requirements.txt
└── README.md
```

---

## How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the server

```bash
uvicorn app.main:app --reload
```

The server starts at **http://127.0.0.1:8000**.  
Interactive docs are available at **http://127.0.0.1:8000/docs** (Swagger UI).

> The SQLite database file (`city_temperature.db`) is created automatically in the working directory on first run.

### 3. Quick walkthrough

```bash
# Add a city
curl -X POST http://localhost:8000/cities/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Kyiv", "additional_info": "Capital of Ukraine"}'

# List cities
curl http://localhost:8000/cities/

# Fetch & store current temperatures for all cities
curl -X POST http://localhost:8000/temperatures/update

# Retrieve temperature history
curl http://localhost:8000/temperatures/

# Filter by city
curl "http://localhost:8000/temperatures/?city_id=1"
```

---

## API Endpoints

### Cities

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/cities/` | Create a new city |
| `GET` | `/cities/` | List all cities (paginated) |
| `GET` | `/cities/{city_id}` | Get a specific city |
| `PUT` | `/cities/{city_id}` | Update a city's fields |
| `DELETE` | `/cities/{city_id}` | Delete a city (cascades to temperatures) |

### Temperatures

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/temperatures/update` | Fetch & store current temps for all cities |
| `GET` | `/temperatures/` | List all temperature records (newest first) |
| `GET` | `/temperatures/?city_id={id}` | Filter records by city |

All endpoints support pagination via `skip` / `limit` query parameters.

---

## Design Choices

### Weather data source — Open-Meteo
Open-Meteo provides a free geocoding API and a free weather forecast API. No registration or API key is needed. The flow for each city is:
1. **Geocode** the city name → latitude/longitude via `geocoding-api.open-meteo.com`
2. **Fetch** the current `temperature_2m` (2-metre air temperature in °C) via `api.open-meteo.com`

All cities are fetched **concurrently** with `asyncio.gather`, making `POST /temperatures/update` fast even with many cities.

### Database — SQLite + SQLAlchemy
SQLite was chosen for zero-configuration local development. The SQLAlchemy ORM layer makes it trivial to swap in PostgreSQL or MySQL by changing the `SQLALCHEMY_DATABASE_URL` in `database.py`.

### Cascading deletes
The `City → Temperature` relationship is defined with `cascade="all, delete-orphan"`, so deleting a city automatically removes all its temperature records.

### Dependency injection
`get_db` is used as a FastAPI dependency everywhere a database session is needed. This keeps route handlers clean, ensures sessions are always closed, and makes the code easy to test by overriding the dependency.

### Pydantic v2
All schemas use Pydantic v2 with `model_config = {"from_attributes": True}` (replaces v1's `orm_mode = True`) so ORM objects can be returned directly from route handlers.

### Error handling
- **409 Conflict** when trying to create a city with a duplicate name.
- **404 Not Found** for missing city or city-filtered temperature queries.
- Per-city weather fetch failures are caught and counted; a partial result is still returned rather than failing the whole request.

---

## Assumptions & Simplifications

- **UTC timestamps** — all `date_time` values are stored as naive UTC datetimes.
- **Temperature unit** — Celsius (°C) as returned by Open-Meteo.
- **No authentication** — the API is open; add OAuth2/JWT middleware for production use.
- **SQLite concurrency** — `check_same_thread=False` is safe for development. For production, switch to a server-grade database.
- **City name geocoding** — Open-Meteo returns the first result for a city name. Ambiguous names (e.g. "Springfield") will resolve to whatever Open-Meteo returns first; include a country code in `additional_info` if needed, though the geocoder does not use that field.