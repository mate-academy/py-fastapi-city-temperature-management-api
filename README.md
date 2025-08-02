# City Temperature API

## Overview

This application is a FastAPI-based RESTful API for managing cities and their temperature records. It supports creating, reading, updating, and deleting city data, as well as fetching and storing temperature measurements (simulated or from a real source). The project uses async SQLAlchemy with SQLite and Alembic for migrations.

---

## How to Run the Application

### Prerequisites

- Python 3.9+
- [Poetry](https://python-poetry.org/) or `pip`
- SQLite (no extra setup needed, DB file created automatically)

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/xnquaint/py-fastapi-city-temperature-management-api.git
    cd city-temperature-api
    git checkout develop
    ```

2. Create and activate a virtual environment (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/macOS
    .\venv\Scripts\activate   # Windows
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Database Setup & Migrations

Run Alembic migrations to create the database tables:

```bash
alembic upgrade head
````

### Run the FastAPI Server

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.

---

## Design Choices

* **Async SQLAlchemy:** Used `AsyncSession` with `aiosqlite` to allow non-blocking DB operations.
* **Pydantic Schemas:** Separate models for input validation (`Create`, `Update`) and output serialization (`InDB` with `orm_mode=True`).
* **CRUD Layer:** All database operations are abstracted in a `crud.py` for separation of concerns and testability.
* **Single Endpoint with Optional Query Parameter:** Combined multiple GET endpoints for temperatures into one with optional filtering by `city_id` to avoid route ambiguity.
* **Alembic for Migrations:** Enables versioned, controlled schema updates.
* **Dependency Injection:** Used FastAPI's `Depends` for managing DB session lifecycle.

