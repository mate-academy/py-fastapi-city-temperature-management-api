# City Temperature Management API

A FastAPI application for managing cities and storing their current
temperature history.

The application provides CRUD endpoints for cities and allows current
temperature data to be fetched asynchronously from an external weather API
and stored in a SQLite database.

## Features

- Create, retrieve, update, and delete cities.
- Store additional information about cities.
- Fetch current temperatures for all stored cities.
- Fetch temperature data asynchronously.
- Store temperature history in SQLite.
- Filter temperature records by city.
- Interactive Swagger API documentation.

## Technologies

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- HTTPX
- asyncio
- Open-Meteo API

## Project Structure

```text
app/
├── main.py
├── database.py
├── models.py
├── schemas.py
├── crud.py
├── routers/
│   ├── cities.py
│   └── temperatures.py
└── services/
    └── weather.py

```

## Installation

Clone the repository and enter the project directory:

```bash
git clone <repository-url>
cd py-fastapi-city-temperature-management-api
```

Create a virtual environment:

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

Run the FastAPI development server:

```bash
uvicorn app.main:app --reload
```

The application will be available at:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

## API Endpoints

### Cities

- `POST /cities` - create a city.
- `GET /cities` - get all cities.
- `GET /cities/{city_id}` - get a city by ID.
- `PUT /cities/{city_id}` - update a city.
- `DELETE /cities/{city_id}` - delete a city.

### Temperatures

- `POST /temperatures/update` - fetch and store current temperatures for all cities.
- `GET /temperatures` - get all stored temperature records.
- `GET /temperatures?city_id={city_id}` - get temperature history for a specific city.

## Design Choices

The project is split into separate layers:

- `routers` contain FastAPI endpoints.
- `crud.py` contains database operations.
- `models.py` contains SQLAlchemy ORM models.
- `schemas.py` contains Pydantic request and response schemas.
- `services/weather.py` contains communication with the external weather service.
- `database.py` contains database configuration and the database dependency.

Dependency injection is used through `Depends(get_db)` to provide SQLAlchemy
database sessions to API endpoints.

Temperature requests are performed asynchronously using `httpx.AsyncClient`.
Requests for multiple cities are executed concurrently with `asyncio.gather`.

## Weather API

The application uses Open-Meteo.

The city name is converted to latitude and longitude using the Open-Meteo
Geocoding API. The coordinates are then used to request the current
temperature.

No API key is required.

## Database

SQLite is used as the database.

The database file is created automatically when the application starts.

There are two main tables:

- `cities`
- `temperatures`

A city can have multiple temperature records, allowing the application to
keep temperature history.

## Assumptions and Simplifications

- City names are unique.
- Open-Meteo is used as the external weather provider.
- The first geocoding result for a city name is used.
- A new temperature record is stored every time `POST /temperatures/update`
  is called.
- If fetching weather data for one city fails, other cities can still be
  processed.
- SQLite is used because this is a small educational project.
