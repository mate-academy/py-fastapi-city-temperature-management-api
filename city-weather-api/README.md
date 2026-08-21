# City Temperature Management API

FastAPI application for managing cities and storing their temperature history.

## How to run

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
uvicorn app.main:app --reload
```

Open Swagger documentation:

`http://127.0.0.1:8000/docs`

## Design

- FastAPI — REST API
- SQLite — database
- SQLAlchemy — database operations
- Pydantic — data validation
- HTTPX — asynchronous HTTP requests
- Open-Meteo — current temperature data

The application provides CRUD operations for cities and stores temperature history.

## Assumptions

City coordinates and current temperatures are retrieved using the Open-Meteo API.