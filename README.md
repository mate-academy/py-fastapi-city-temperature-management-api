# City Temperature Management API

A FastAPI application that manages city data and temperature records.

## Features
- CRUD operations for cities
- Temperature data storage and retrieval
- Async SQLite database
- Automatic API documentation

## Installation
```bash
python -m venv .venv
source .venv/bin/activate
pip install fastapi sqlalchemy aiosqlite uvicorn
```

## RUN
```bash
uvicorn main:app --reload
```

## API Endpoints

### Cities

    POST /cities/ - Create city

    GET /cities/ - List all cities

    GET /cities/{id} - Get city by ID

    DELETE /cities/{id} - Delete city

### Temperatures

    POST /temperatures/ - Create temperature record

    GET /temperatures/ - List all temperatures

    GET /temperatures/?city_id={id} - Filter by city
