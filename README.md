# FastAPI City Temperature Management API

This project is a FastAPI application that manages cities and stores historical temperature data for them.  
It consists of two main parts:

1. **City CRUD API** – for managing cities.
2. **Temperature API** – for asynchronously fetching and storing temperature data for all cities.

---

## Features

### City API
- Create a city
- List all cities
- Retrieve a city by ID
- Update city details
- Delete a city

### Temperature API
- Fetch current temperature for **all cities** asynchronously and store it
- Retrieve temperature history
- Filter temperature history by `city_id`

---

## Tech Stack

- **FastAPI**
- **SQLAlchemy 2.0 (async)**
- **SQLite** with `aiosqlite`
- **httpx** for async HTTP requests
- **Pydantic v2**
- **Uvicorn**

---

## Project Structure

app/
├── main.py
├── core/
│ └── config.py
├── db/
│ ├── base.py
│ └── session.py
├── models/
│ ├── city.py
│ └── temperature.py
├── schemas/
│ ├── city.py
│ └── temperature.py
├── crud/
│ ├── city.py
│ └── temperature.py
└── api/
└── routers/
├── cities.py
└── temperatures.py
tests/


---

## How to Run the Application

### 1. Create virtual environment and install dependencies

#### Using `pip`
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt

Using uv

uv venv
uv pip install -r requirements.txt

2. Configure environment variables

Create a .env file in the project root:

DATABASE_URL=sqlite+aiosqlite:///./app.db
OPEN_METEO_TIMEOUT_SECONDS=10

3. Start the API

uvicorn app.main:app --reload

Open Swagger UI:

http://127.0.0.1:8000/docs

API Overview
City endpoints

    POST /cities

    GET /cities

    GET /cities/{city_id}

    PUT /cities/{city_id}

    DELETE /cities/{city_id}

Temperature endpoints

    POST /temperatures/update

    GET /temperatures

    GET /temperatures?city_id={city_id}

Design Choices

    Async SQLAlchemy is used throughout the application to ensure non-blocking database access.

    Dependency Injection is implemented using FastAPI dependencies (get_db) to manage AsyncSession lifecycle.

    SQLite was chosen for simplicity and ease of setup, as required by the task.

    Open-Meteo API is used as a temperature provider because:

        it is free,

        does not require an API key,

        provides reliable current temperature data.

    Each city stores latitude and longitude as explicit fields, which allows accurate temperature fetching.

Assumptions and Simplifications

    Cities must have latitude and longitude to fetch temperature data.

    Only current temperature is stored (no forecasts).

    Temperature updates are triggered manually via an API endpoint.

    SQLite is sufficient for the scope of this task; in production, PostgreSQL and Alembic migrations would be preferable.

    No authentication or authorization is implemented, as it was not required by the task.

Example Workflow

    Create a city using POST /cities with name and coordinates.

    Call POST /temperatures/update to fetch and store temperatures for all cities.

    Retrieve temperature history using:

        GET /temperatures

        GET /temperatures?city_id=1

Notes

This project focuses on correctness, clarity, and best practices rather than production-ready infrastructure.
