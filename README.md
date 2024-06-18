# FastAPI City and Temperature Data Management

## Description

This FastAPI application manages city data and their corresponding temperature data. It includes two main components:

1. CRUD API for managing city data.
2. API for fetching and storing current temperature data for all cities in the database.

## Requirements

- Python 3.8+
- FastAPI
- Uvicorn
- SQLAlchemy
- Databases
- Pydantic
- HTTPX
- SQLite
- Alembic

## Installation


1. Install dependencies

```bash
pip install -r requirements.txt
```

2. Run the database migrations:

```bash
alembic upgrade head
```

3. Run the FastAPI application:

```bash
./run.sh
```
or
```bash
uvicorn main:app --reload
```

## Design Choices

- **FastAPI**: Chosen for its high performance, ease of use, and automatic generation of interactive API documentation.
- **SQLAlchemy**: Used as the ORM for managing the SQLite database, providing an efficient way to handle database operations and migrations.
- **Alembic**: Utilized for handling database migrations to ensure the database schema remains in sync with the models.


## Assumptions and Simplifications

- **SQLite**: Used for simplicity and ease of setup. In a production environment, a more robust database system (e.g., PostgreSQL) would be preferable.
- **Synchronous API for Alembic**: Alembic migrations are handled using the synchronous SQLite driver to avoid issues with asynchronous operations during migration.
