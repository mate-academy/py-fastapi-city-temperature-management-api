# FastAPI City Temperature Management API

A FastAPI application for managing cities and storing their temperature history.

The application uses Open-Meteo to receive the current temperature for every city stored in the database.

## Run

Docker must be installed.

```bash
docker compose up --build
```

The API will be available at:

```text
http://localhost:8000
```

Swagger documentation:

```text
http://localhost:8000/docs
```

To stop the application:

```bash
docker compose down
```

The SQLite database is stored in a Docker volume, so data remains after the container is restarted.

## Design Choices

- FastAPI and asynchronous SQLAlchemy are used for API and database operations.
- HTTPX is used to obtain city coordinates from Open-Meteo Geocoding API.
- Open-Meteo is used to obtain current temperature data.
- `asyncio.gather()` fetches temperatures for all cities concurrently.
- Every update creates a new temperature record to preserve history.
- Cities and temperatures have a one-to-many relationship.
- Temperature records are deleted automatically when their city is deleted.
- Alembic is used for database migrations.

## Assumptions and Simplifications

- Each city is identified by its name, which is used to request coordinates from the external geocoding API.
- Every temperature update creates a new record instead of overwriting previous data.
- If data retrieval fails for one city, the update continues for the remaining cities and stores the error message.
- Temperature updates are triggered manually through the API.
- Authentication, scheduled updates, and retry logic are not implemented.