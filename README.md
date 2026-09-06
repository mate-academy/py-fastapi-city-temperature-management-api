# City Temperature Management API

FastAPI application for managing cities and their temperature data.

## Features

* CRUD operations for cities
* Get temperature records
* Update temperatures from Open-Meteo API
* Async database and HTTP requests
* Concurrent requests with `asyncio.gather()`

## Run

Install dependencies:

```bash
pip install -r requirements.txt
```

Run migrations:

```bash
alembic upgrade head
```

Start the application:

```bash
uvicorn main:app --reload
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

## Design Choices

* **FastAPI** — REST API
* **SQLAlchemy + SQLite** — database
* **Alembic** — database migrations
* **Pydantic** — data validation
* **httpx + asyncio** — asynchronous API requests
* **Open-Meteo** — weather data provider

## Assumptions

Each temperature update creates a new database record, allowing temperature history to be stored. Authentication is not implemented because it is outside the assignment scope.
