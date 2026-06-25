# Weather Tracker API

A FastAPI application that manages city data and tracks their corresponding temperature data using asynchronous operations, Dependency Injection, and SQLAlchemy 2.0 with Alembic migrations.

## Project Structure

The project follows a modular layout (domain-driven structure) as recommended by the FastAPI documentation:

```text
weather_tracker/
├── alembic/                  # Database migrations settings and history
├── app/
│   ├── cities/               # City management module (CRUD)
│   │   ├── models.py         # SQLAlchemy domain model
│   │   ├── schemas.py        # Pydantic data validation models
│   │   ├── service.py        # Async database queries
│   │   └── router.py         # API endpoints
│   ├── temperatures/         # Temperature tracking module
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── service.py        # Async API fetching & DB insertion
│   │   └── router.py
│   ├── core/
│   │   └── database.py       # Async engine and session configuration
│   └── main.py               # Application entry point & router registration
├── alembic.ini
└── requirements.txt