# City Temperature API

An asynchronous FastAPI application for managing cities and collecting their current temperatures from an external weather service.

## Features

- Create, read, update, and delete cities
- Fetch current temperatures for all stored cities
- Store temperature history in SQLite
- Filter temperature records by city
- Asynchronous database and HTTP operations
- Automatic cascade deletion of related temperature records
- Interactive API documentation

## Tech Stack

- Python 3.12+
- FastAPI
- SQLAlchemy Async
- SQLite with `aiosqlite`
- Alembic
- HTTPX
- WeatherAPI
- Pydantic

## Installation

The project uses [uv](https://docs.astral.sh/uv/) for dependency management.

Install the project dependencies:

```bash
uv sync
```

Create a `.env` file based on `.sample.env`:

```env
WEATHER_API_KEY=your_weather_api_key
```

A free API key can be obtained from [WeatherAPI](https://www.weatherapi.com/).

## Database Setup

Apply all database migrations:

```bash
uv run alembic upgrade head
```

## Running the Application

Start the development server:

```bash
uv run uvicorn app.main:app --reload
```

The application will be available at:

- API: http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Running Tests

```bash
uv run pytest
```

## API Endpoints

### Cities

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/cities` | Create a city |
| `GET` | `/cities` | Get all cities |
| `GET` | `/cities/{city_id}` | Get a city by ID |
| `PUT` | `/cities/{city_id}` | Update a city |
| `DELETE` | `/cities/{city_id}` | Delete a city |

Example request:

```json
{
  "name": "Kyiv",
  "additional_info": "Capital of Ukraine"
}
```

### Temperatures

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/temperatures/update` | Fetch and store temperatures for all cities |
| `GET` | `/temperatures` | Get complete temperature history |
| `GET` | `/temperatures?city_id={city_id}` | Filter temperature records by city |

Temperatures are stored in degrees Celsius.

## Design Choices

- Database operations use SQLAlchemy `AsyncSession`.
- Weather requests are performed asynchronously with HTTPX.
- Requests for multiple cities are executed concurrently.
- Alembic manages the database schema.
- SQLite foreign keys are enabled explicitly.
- Deleting a city also deletes its temperature history through `ON DELETE CASCADE`.
- Database operations are rolled back when an error occurs.

## Project Structure

```text
app/
├── cities/
│   ├── models.py
│   ├── router.py
│   └── schemas.py
├── temperature/
│   ├── models.py
│   ├── router.py
│   ├── schemas.py
│   └── services.py
├── db/
│   └── database.py
└── main.py

alembic/
└── versions/
```

## Assumptions and Simplifications

- City names must be recognized by WeatherAPI.
- Temperature values are stored in Celsius.
- A single failed weather request prevents the update operation from being completed.
- SQLite is used because the project is intended for educational and local use.
