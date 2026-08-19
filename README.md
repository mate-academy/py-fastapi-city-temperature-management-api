# City Temperature Management API

A FastAPI app for managing cities and tracking their temperatures using an external weather API.

## Tech Stack

- FastAPI
- SQLAlchemy
- Alembic
- Pydantic
- httpx
- SQLite
- Open-Meteo API (geocoding + weather, no key required)

## Setup & Running

1. Create a virtual environment and activate it:
```bash
   python -m venv venv
   venv\Scripts\activate
```

2. Install dependencies:
```bash
   pip install -r requirements.txt
```

3. Run migrations:
```bash
   alembic upgrade head
```

4. Start the server:
```bash
   uvicorn main:app --reload
```

5. Open docs at: http://127.0.0.1:8000/docs

## Endpoints

- `GET /cities/` — list all cities
- `GET /cities/{city_id}/` — get a single city
- `POST /cities/` — create a city
- `DELETE /cities/{city_id}/` — delete a city
- `GET /temperatures/` — list all temperature records
- `GET /temperatures/?city_id={id}` — list temperature records for a specific city
- `POST /temperatures/update` — fetch current temperature for all cities and store it

## Design Choices

- City coordinates are looked up dynamically via the Open-Meteo geocoding API instead of being stored on the `City` model, so no schema changes were needed.
- `POST /temperatures/update` fetches data for all cities concurrently using `asyncio.gather`; database writes happen sequentially afterward to avoid sharing one session across concurrent coroutines.
- `Depends(get_db)` is used across all endpoints for database session management.
- Cities that can't be resolved by the geocoding API are silently skipped during `/temperatures/update`.
- No pagination on list endpoints.
- No automated tests.