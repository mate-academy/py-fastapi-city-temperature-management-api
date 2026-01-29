# City Temperature Management API

A FastAPI application that manages city data and stores temperature records for those cities.

---

## Features

- CRUD operations for cities
- Temperature data storage and retrieval
- Async SQLite database using SQLAlchemy
- Automatic API documentation via Swagger UI

---

## Installation

Create and activate a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate   # Linux / macOS
# .venv\Scripts\activate    # Windows
pip install -r requirements.txt
```

## Database Setup
```bash
alembic upgrade head
```

## Run app
```bash
uvicorn main:app --reload
```
## Server runs at http://127.0.0.1:8000

## Api Endpoints
POST   /cities/          - Create city
GET    /cities/          - List all cities
GET    /cities/{id}      - Get city by ID
PUT    /cities/{id}      - Update city
DELETE /cities/{id}      - Delete city
POST   /cities/          - Create city

GET    /cities/          - List all cities
GET    /cities/{id}      - Get city by ID
PUT    /cities/{id}      - Update city
DELETE /cities/{id}      - Delete city

