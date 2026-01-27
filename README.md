# City Temperature API

FastAPI application for managing cities and their temperature data with asynchronous weather fetching.

## Technology Stack

- **FastAPI** - Web framework
- **SQLAlchemy** - ORM with modern syntax
- **Alembic** - Database migrations
- **Pydantic** - Data validation
- **httpx** - Async HTTP client
- **SQLite** - Database
- **Open-Meteo API** - Free weather data (no API key required)

## Project Structure

```
fastapi-city-temperature/
├── app/
│   ├── main.py              # FastAPI application
│   ├── database.py          # DB configuration
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── crud.py              # Business logic
│   └── routers/
│       ├── cities.py        # City endpoints
│       └── temperatures.py  # Temperature endpoints
├── alembic/                 # Database migrations
├── requirements.txt
└── README.md
```

## Installation & Running

### 1. Setup Environment

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Initialize Database

```bash
# Apply migrations to create tables
alembic upgrade head
```

### 3. Run Application

```bash
uvicorn app.main:app --reload
```

### 4. Access Documentation

- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc

## API Endpoints

### Cities

- `POST /cities` - Create city
- `GET /cities` - List all cities
- `GET /cities/{id}` - Get specific city
- `PUT /cities/{id}` - Update city
- `DELETE /cities/{id}` - Delete city

### Temperatures

- `POST /temperatures/update` - Fetch current temperatures for all cities
- `GET /temperatures` - List temperature records (optional `?city_id=` filter)

### Example Usage

```bash
# Create city
curl -X POST "http://127.0.0.1:8000/cities" \
  -H "Content-Type: application/json" \
  -d '{"name": "Kyiv", "additional_info": "Capital of Ukraine"}'

# Update temperatures
curl -X POST "http://127.0.0.1:8000/temperatures/update"

# Get temperatures
curl "http://127.0.0.1:8000/temperatures?city_id=1"
```

## Design Choices

### 1. Layered Architecture

- **Routers** → HTTP handling
- **CRUD** → Business logic
- **Models** → Data structure
- Provides separation of concerns, testability, and maintainability

### 2. Dependency Injection

- Used `Depends(get_db)` for database session management
- Automatic resource cleanup
- Easy to test and mock

### 3. Async Temperature Fetching

- `asyncio.gather()` for parallel API calls
- Fetches all cities simultaneously (~2s vs ~20s sequential)
- Improves performance and user experience

### 4. SQLAlchemy 2.0 Syntax

- Modern `select()` statements instead of legacy `query()`
- Better type safety and IDE support
- Future-proof and async-ready

### 5. Alembic Migrations

- Version-controlled database schema
- Reversible migrations
- Production-safe incremental updates

### 6. Pydantic Validation

- Automatic request validation
- Auto-generated API documentation
- Type-safe contracts

### 7. Cascade Delete

- Deleting a city automatically removes its temperature records
- Maintains data integrity
- Simplifies code

## Assumptions & Simplifications

### Database

**SQLite** - Simple file-based DB, suitable for development. For production, use PostgreSQL.

### Weather API

**Open-Meteo** - Free API without registration. Limitations:

- Uses first geocoding result (may be incorrect for common city names)
- Rate limit: ~10,000 requests/day
- No API key needed

### Security

**No authentication** - All endpoints public. For production, implement JWT/OAuth2.

### Error Handling

**Basic HTTP exceptions** - Simple error messages. For production, add structured logging and monitoring.

### Pagination

**Simple offset/limit** - Works for small datasets. For large datasets, use cursor-based pagination.

### Geocoding

**First result only** - Assumes city names are unambiguous. For production, store coordinates in database or add country field.

### Concurrency

**Single-process** - SQLite has limited concurrent write support. For production, use PostgreSQL.

### Testing

**Manual only** - No automated tests included. For production, add pytest unit/integration tests.

### Background Tasks

**On-demand updates** - Temperature fetched manually. For production, use Celery/APScheduler for periodic updates.

## Quick Test

```bash
# 1. Create cities
POST /cities {"name": "Kyiv", "additional_info": "Capital"}
POST /cities {"name": "Lviv", "additional_info": "Cultural capital"}

# 2. Update temperatures
POST /temperatures/update

# 3. View results
GET /temperatures
```

## Alembic Commands

```bash
# Create migration after model changes
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Check current version
alembic current

# Rollback
alembic downgrade -1
```

## Troubleshooting

**Port in use:** `uvicorn app.main:app --reload --port 8001`

**Database locked:** `rm cities_temperature.db && alembic upgrade head`

**Module not found:** `pip install -r requirements.txt`

---

**Documentation:** https://fastapi.tiangolo.com/
