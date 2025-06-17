**FastAPI City Temperature Management API**

REST API for managing cities and getting current temperature data from OpenWeatherMap.

Requirements:
- Python 3.10+.
- Libraries: `fastapi`, `qlalchemy`, `aiosqlite`, `httpx`.
- OpenWeatherMap API key

**Startup instructions**

Add your OpenWeatherMap API key to the .env:
- OPENWEATHER_API_KEY=_________________

To run the app, use
- bash:

python -m app.main

The application will be available at: http://127.0.0.1:8080

API documentation:
- Swagger UI: http://127.0.0.1:8080/docs
- ReDoc: http://127.0.0.1:8080/redoc

***Design Decisions*** 
1. Architecture 
- Modular Structure:
  - Separation of concerns (routers, models, services). 
  - Async SQLAlchemy for database operations.
- Layered Design:
  - `routers/` (API endpoints) -> `crud.py` (business logic) -> `models.py` (database models)
2. Key Technologies
- FastAPI: For high-performance API with automatic docs (Swagger/ReDoc).
- SQLite + AsyncSQLAlchemy: Lightweight async database interactions. 
- Pydantic V2: Data validation and serialization.
- HTTPX: Async HTTP requests to OpenWeatherMap API.
3. API Features
- Cities CRUD: RESTful endpoints for city management.
- Temperature Sync:
  - Async background task to fetch/update temperatures.
  - Historical data storage in SQLite.

***Why This Works***
- Clear separation of concerns. 
- Async-first for performance.
- Minimal dependencies for easy maintenance.
