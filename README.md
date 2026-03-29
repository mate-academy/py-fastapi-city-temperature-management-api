# py-fastapi-city-temperature-management-api

A FastAPI REST API for managing cities and tracking their temperature history using data fetched from an external weather service.

## Tech Stack

- **FastAPI** — web framework
- **SQLAlchemy v2** (async) + **SQLite** — database
- **Alembic** — migrations
- **Pydantic v2** — data validation
- **aiohttp** — async HTTP client for weather fetching
- **uvicorn** — ASGI server

## Project Structure

```
src/
├── core/           # App config (settings via python-dotenv)
├── db/             # Database setup, migrations
├── models/         # SQLAlchemy ORM models (City, Temperature)
├── routers/        # Route handlers (cities, temperatures)
├── schemas/        # Pydantic schemas
├── services/       # Business logic
├── dependencies.py # Shared dependencies (DB session injection)
└── main.py         # App entrypoint
```

## Setup & Running

```bash
# 1. Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Set your weather API key in .env

# 4. Apply migrations
alembic upgrade head

# 5. Run the server
uvicorn src.main:app --reload
```

API docs available at: `http://localhost:8000/docs`

## API Endpoints

### Cities
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/cities` | Create a city |
| `GET` | `/cities` | List all cities |
| `GET` | `/cities/{city_id}` | Get a city |
| `PUT` | `/cities/{city_id}` | Update a city |
| `DELETE` | `/cities/{city_id}` | Delete a city |

### Temperatures
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/temperatures/update` | Fetch & store current temps for all cities |
| `GET` | `/temperatures` | List all temperature records |
| `GET` | `/temperatures/?city_id={id}` | Filter records by city |

## Design Choices

- **Async throughout** — all DB operations and external API calls use `async/await` for non-blocking I/O.
- **Service layer** — business logic is separated from routers into dedicated service modules.
- **Dependency injection** — DB session is injected via `Depends()` to keep handlers clean and testable.
- **External weather data** — temperatures are fetched from [OpenWeather](https://openweathermap.org/) (free, no API key required) using city coordinates resolved via geocoding.

## Assumptions

- SQLite is sufficient for the scope of this task (easily swappable to PostgreSQL via the connection string).
- `POST /temperatures/update` fetches data for **all** cities currently in the DB in a single async batch.
- Temperature is stored in **Celsius**.