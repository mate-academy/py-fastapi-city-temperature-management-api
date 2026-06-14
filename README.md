# City Temperature API

## Installation

```bash
pip install -r requirements.txt
```

## Run

```bash
uvicorn app.main:app --reload
```

## Swagger

http://127.0.0.1:8000/docs

## Features

### Cities

- POST /cities
- GET /cities
- DELETE /cities/{id}

### Temperatures

- POST /temperatures/update
- GET /temperatures
- GET /temperatures?city_id=1

## Design choices

- FastAPI for REST API.
- SQLAlchemy ORM.
- SQLite database.
- Open-Meteo API for weather data.
- Async HTTP requests with httpx.
