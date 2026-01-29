# FastAPI City Temperature Management API

A modern FastAPI application for managing cities and their temperature records with real-time weather data integration.

## Tech Stack

- **FastAPI** - Modern web framework
- **SQLAlchemy 2.0** - Async ORM
- **Alembic** - Database migrations
- **SQLite** - Database
- **Pydantic** - Data validation
- **uvicorn** - ASGI server

## Prerequisites

- Python 3.13+
- SQLite
- [uv](https://github.com/astral-sh/uv) package manager

## Installation

### 1. Install uv
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Clone the repository
```bash
git clone https://github.com/Taras-Ivashchuk/py-fastapi-library-management-api
cd py-fastapi-city-temperature-management-api
```

### 3. Install dependencies
```bash
uv sync
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
# Database
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/dbname

# API Configuration
API_PREFIX=/api/v1

# Weather API
WEATHER_API_KEY=your_weather_api_key_here
```

**Get a free WeatherAPI key:** [https://www.weatherapi.com/](https://www.weatherapi.com/)

### 5. Set up the database

```bash

# Run migrations
alembic upgrade head
```

### 6. Run the application

```bash
# Development mode with auto-reload
fastapi dev main.py

# Production mode
uvicorn main:app --host 0.0.0.0 --port 8000
```

The API will be available at: **http://127.0.0.1:8000**

## API Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI**: http://127.0.0.1:8000/docs

## API Endpoints

### Cities

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/cities/` | Create a new city |
| `GET` | `/api/v1/cities/` | List all cities |
| `GET` | `/api/v1/cities/{id}/` | Get city by ID |
| `PUT` | `/api/v1/cities/{id}/` | Update city |
| `DELETE` | `/api/v1/cities/{id}/` | Delete city |

### Temperatures

| Method | Endpoint                          | Description                              |
|--------|-----------------------------------|------------------------------------------|
| `GET` | `/api/v1/temperatures/`           | Get all temperature records              |
| `GET` | `/api/v1/temperatures/{city_id}/` | Get temperatures for specific city by ID |
| `POST` | `/api/v1/temperatures/update`     | Fetch latest temperatures for all cities |


## Project Structure

```
py-fastapi-city-temperature-management-api/
├── alembic/                # Database migrations
│   └── versions/
├── city/                   # City module
│   ├── models.py
│   ├── schemas.py
│   ├── services.py
│   └── router.py
├── temperature/            # Temperature module
│   ├── models.py
│   ├── schemas.py
│   ├── services.py
│   └── router.py
├── core/                   # Core configuration
│   ├── config.py
│   └── database.py
├── main.py                # Application entry point
├── alembic.ini            # Alembic configuration
├── pyproject.toml         # Project dependencies
├── .env                   # Environment variables (not in git)
└── README.md
```