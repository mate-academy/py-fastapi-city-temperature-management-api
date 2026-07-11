# FastAPI City Temperature Management API

## Overview

This project is a FastAPI application for managing cities and their temperature history.

Features:
- CRUD operations for cities
- Temperature update using an external weather API
- Temperature history with optional filtering by city

## Technologies

- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- HTTPX
- Uvicorn

## Project Structure

```
app/
├── routers/
│   ├── cities.py
│   └── temperatures.py
├── services/
│   └── weather.py
├── crud.py
├── database.py
├── dependencies.py
├── main.py
├── models.py
└── schemas.py
```

## Installation

Clone the repository:

```bash
git clone <repository_url>
cd py-fastapi-city-temperature-management-api
```

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the application

```bash
uvicorn app.main:app --reload
```

Open Swagger UI:

```
http://127.0.0.1:8000/docs
```

## API Endpoints

### Cities

- POST `/cities`
- GET `/cities`
- GET `/cities/{city_id}`
- PUT `/cities/{city_id}`
- DELETE `/cities/{city_id}`

### Temperatures

- POST `/temperatures/update`
- GET `/temperatures`
- GET `/temperatures?city_id={city_id}`

## Design Choices

- FastAPI routers are used to separate API endpoints.
- SQLAlchemy ORM is used for database operations.
- SQLite is used as the project database.
- Dependency Injection is implemented using `Depends(get_db)`.
- Weather data is fetched asynchronously using `httpx.AsyncClient`.

## Assumptions

- Open-Meteo API is used as the weather provider.
- City coordinates are stored in a predefined dictionary.
- If weather data cannot be retrieved for a city, that city is skipped and processing continues.