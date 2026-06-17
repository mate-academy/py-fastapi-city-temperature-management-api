# City Temperature Management API

A RESTful API built with FastAPI that manages cities and their current temperatures fetched from an external weather service.

## Tech Stack

- **FastAPI** — web framework
- **SQLAlchemy** (async) — ORM
- **Alembic** — database migrations
- **Pydantic** — data validation and serialization
- **aiosqlite** — async SQLite driver
- **httpx** — async HTTP client for external API calls

---

## Project Structure

```
py-fastapi-city-temperature-management-api/
│
├── app/
│   ├── city/
│   │   ├── crud.py       # DB operations for City
│   │   ├── models.py     # SQLAlchemy City model
│   │   ├── router.py     # City endpoints
│   │   └── schemas.py    # Pydantic schemas for City
│   │
│   └── temperature/
│       ├── crud.py       # DB operations for Temperature
│       ├── models.py     # SQLAlchemy Temperature model
│       ├── router.py     # Temperature endpoints
│       └── schemas.py    # Pydantic schemas for Temperature
│
├── alembic/              # Database migrations
├── main.py               # FastAPI app entry point
├── database.py           # Async engine, session, Base
├── dependencies.py       # Shared get_db dependency
├── settings.py           # Environment config
├── requirements.txt
└── .env                  # Environment variables (not committed)
```

---

## How to Run

### 1. Clone the repository
```bash
git clone https://github.com/maxmlv/py-fastapi-library-management-api.git
cd py-fastapi-city-temperature-management-api
```

### 2. Create and activate a virtual environment
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Create a `.env` file in the project root
```env
PROJECT_NAME="FastAPI City Temperature Management API"
DATABASE_URL=sqlite+aiosqlite:///./city_temp_db.db
```

### 5. Apply database migrations
```bash
alembic upgrade head
```

### 6. Run the application
```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

Interactive docs (Swagger UI) at `http://127.0.0.1:8000/docs`

---

## API Endpoints

### Cities
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/cities/` | Get all cities |
| `GET` | `/cities/{city_id}` | Get city by ID |
| `POST` | `/cities/` | Create a new city |
| `PUT` | `/cities/{city_id}` | Update city info |
| `DELETE` | `/cities/{city_id}` | Delete a city |

### Temperatures
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/temperatures/` | Get all temperature records |
| `GET` | `/temperatures/?city_id={id}` | Get temperatures for a specific city |
| `POST` | `/temperatures/update` | Fetch and store current temperatures for all cities |

---

## Usage Example

1. Add a city:
```bash
POST /cities/
{
  "name": "Kyiv",
  "additional_info": "Capital of Ukraine"
}
```

2. Fetch current temperatures for all cities:
```bash
POST /temperatures/update
```

3. Get temperatures for a specific city:
```bash
GET /temperatures/?city_id=1
```

---

## Design Choices

**Modular structure** — the project is split into `city` and `temperature` modules under `app/`, each with its own `models.py`, `schemas.py`, `crud.py`, and `router.py`. This keeps each feature self-contained and makes the codebase easier to scale.

**Async SQLAlchemy** — the project uses `create_async_engine` and `async_sessionmaker` throughout, practicing real-world async patterns with FastAPI. All DB operations use `await` and the modern `select()` syntax instead of the legacy `db.query()`.

**Separation of concerns** — `crud.py` only handles database logic and never raises HTTP exceptions. All HTTP status codes and `HTTPException` are handled exclusively in `router.py`. This keeps the DB layer reusable outside of HTTP context.

**Pydantic v2 schemas** — separate schemas for `Create`, `Update`, and `Response` are used for each model, following the DTO pattern. `ConfigDict(from_attributes=True)` enables direct ORM-to-schema serialization.

**External weather API** — temperatures are fetched from [wttr.in](https://wttr.in), which requires no API key and supports querying by city name. The fetch is done with `httpx.AsyncClient` to keep the entire request lifecycle non-blocking.

**Error handling** — the `/temperatures/update` endpoint handles failures per city individually, so a single failed city does not abort the entire batch. Partial results are returned alongside an `errors` list.

---

## Assumptions and Simplifications

- **SQLite** is used as the database for simplicity. Switching to PostgreSQL requires only changing `DATABASE_URL` to `postgresql+asyncpg://...` and installing `asyncpg`.
- City **names are unique** — attempting to create a duplicate city returns `409 Conflict`.
- Temperature records are **append-only** — each call to `POST /temperatures/update` adds new records rather than updating existing ones, preserving historical data.
- The `additional_info` field on City is the only updatable field via `PUT` — the city name is treated as an identifier and is not editable.