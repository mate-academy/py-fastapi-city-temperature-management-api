# City Temperature Management API

A REST API built with FastAPI, SQLAlchemy, and SQLite for managing cities and collecting current temperatures from an online weather service.

## Requirements

- Python 3.13+
- FastAPI
- Uvicorn
- SQLAlchemy
- aiosqlite
- httpx

## Running the application

### 1. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 3. Start the application

Run this command from the project root:

```powershell
python -m uvicorn app.main:app --reload
```

### 4. Open the API documentation

Visit http://127.0.0.1:8000/docs to explore and test the endpoints.

## Design choices

- **FastAPI** provides HTTP routing, request handling, dependency injection, and automatic API documentation.
- **Pydantic** validates request data and defines response structures.
- **SQLAlchemy** manages database models and asynchronous database operations.
- **SQLite** provides lightweight persistent storage without requiring a separate database server.
- **httpx** performs asynchronous HTTP requests to an external weather service.
- **Separation of responsibilities** keeps routes, schemas, database models, database configuration, and CRUD operations in separate modules.

## Temperature updates

The `POST /temperatures/update` endpoint retrieves all cities stored in the database, fetches current weather data for each city from Open-Meteo, saves a temperature record for each successful update, and returns the resulting records.

The weather integration uses city-name geocoding to obtain latitude and longitude before requesting current temperature data.

## Assumptions and simplifications

- Every city is identified by its stored name and is geocoded when weather data is requested.
- City names are assumed to identify the intended location unambiguously. Cities with identical names in different countries may require additional location fields.
- Temperature updates are performed sequentially to keep the implementation simple.
- Weather data availability depends on the external provider and network connectivity.
- The application does not require an API key for the selected Open-Meteo endpoints under their applicable usage terms.
- Authentication, authorization, automated retries, scheduled updates, and database migrations are outside the current scope.
- SQLite is used for local development and demonstration purposes.

## Future improvements

- Store city coordinates to avoid repeated geocoding.
- Fetch weather data concurrently with sensible limits.
- Add automated tests for API endpoints and weather failures.
- Introduce logging, retry handling, and clearer reporting for partial failures.
- Use Alembic for database migrations.