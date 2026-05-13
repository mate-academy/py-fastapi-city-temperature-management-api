## City temperature service

A FastAPI application that manages cities and fetches their current temperatures from WeatherAPI

## Features
- City endpoint with full crud capabilities
- Fetching current temperatures for all cities in the database
- Getting all temperature records or filtered by city id

## How to run

Prerequisites

- Docker and Docker Compose installed
- A free API key from weatherapi.com

```    
    git clone https://github.com/dmitriy-kds/py-fastapi-city-temperature-management-api/
    cd py-fastapi-city-temperature-management-api
    cp .env.sample .env
    # fill in the environmental variables in .env
    docker compose up --build
```

The API will be available at http://localhost:8000
Interactive API docs (Swagger UI) are at http://localhost:8000/docs

## Design Choices
Async SQLAlchemy
The application uses AsyncSession with aiosqlite for all database operations, keeping the FastAPI event loop unblocked during I/O
    
Concurrent Temperature Fetching
POST /temperatures/update uses asyncio.gather to fetch temperatures for all cities concurrently rather than sequentially. This makes the endpoint significantly faster when many cities are stored

Docker
For easier interoperability and sharing

Layered Architecture
The project follows a clear separation of concerns:
- Models: SQLAlchemy ORM definitions
- Schemas: Pydantic models for request/response validation
- CRUD: database operations, isolated from HTTP logic
- Routers: HTTP endpoints, only handle request/response concerns

Settings via Pydantic BaseSettings
All configuration (API key, database URL, weather API URL) is loaded from environment variables through a Settings class, validated on startup

## Assumptions and Simplifications

- SQLite is used as the database for simplicity. For a production deployment, switching to PostgreSQL is recommended
- City names stored in the database are assumed to be recognizable by WeatherAPI (e.g. "London", "Paris"). If a city name is not found, the endpoint returns a 404 error for that city
- Each call to POST /temperatures/update adds new temperature records — it does not overwrite existing ones. This preserves historical data
- No authentication is implemented on the API endpoints
