
# City Temperature Management API

A REST API built with FastAPI to manage cities and track their temperature history.

The application uses SQLite as the database, SQLAlchemy ORM for database operations, and Open-Meteo API to fetch current temperatures.

## Technologies

- Python 3.10+
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- HTTPX
- Uvicorn
- Open-Meteo API

## Features

- Create, retrieve, update, and delete cities.
- Fetch current temperatures for all saved cities.
- Store temperature history in SQLite.
- Filter temperature records by city.
- Asynchronous HTTP requests to Open-Meteo.
- Automatic API documentation with Swagger UI.
- Basic error handling.

## Project Structure

```text
app/
├── routers/
│   ├── __init__.py
│   ├── cities.py
│   └── temperatures.py
├── services/
│   ├── __init__.py
│   └── weather.py
├── __init__.py
├── database.py
├── main.py
├── models.py
└── schemas.py

requirements.txt
README.md
.gitignore
```

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd py-fastapi-city-temperature-management-api
```

2. Create a virtual environment:

```bash
python -m venv .venv
```

3. Activate it on Windows:

```powershell
.\.venv\Scripts\activate
```

4. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

5. Run the application:

```bash
uvicorn app.main:app --reload
```

6. Open API documentation:

http://127.0.0.1:8000/docs

## API Endpoints

### Cities

| Method | Endpoint | Description |
|---|---|---|
| POST | /cities | Create a city |
| GET | /cities | List all cities |
| GET | /cities/{city_id} | Retrieve a city |
| PUT | /cities/{city_id} | Update a city |
| DELETE | /cities/{city_id} | Delete a city |

### Temperatures

| Method | Endpoint | Description |
|---|---|---|
| POST | /temperatures/update | Fetch and save current temperatures |
| GET | /temperatures | List temperature history |
| GET | /temperatures?city_id=1 | Filter records by city |

## Example Usage

Create a city:

POST /cities

```json
{
  "name": "Krakow",
  "additional_info": "City in southern Poland"
}
```

Update temperature data:

POST /temperatures/update

Example response:

```json
[
  {
    "id": 1,
    "city_id": 1,
    "date_time": "2026-10-21T10:30:00",
    "temperature": 12.5
  }
]
```

The values above are examples, not live weather data.

## Design Choices

- FastAPI provides automatic request validation and API documentation.
- SQLite is used for simple local data storage.
- SQLAlchemy ORM manages database models and relationships.
- Pydantic schemas validate input and serialize output.
- APIRouter separates city and temperature endpoints.
- Dependency injection manages database sessions.
- HTTPX and asyncio provide asynchronous weather requests.
- Temperature records are retained to preserve historical data.

## Assumptions and Simplifications

- City names must be unique.
- Coordinates are obtained from Open-Meteo Geocoding API.
- The first geocoding match is used when multiple cities have the same name.
- Temperatures are measured in degrees Celsius.
- Measurement timestamps are stored in UTC without timezone information.
- If weather retrieval fails for any city, the entire update request fails.
- Deleting a city also deletes its temperature history.
- Database tables are created automatically at application startup.
- Database migrations, authentication, and scheduled updates are not implemented.
- An internet connection is required to update temperatures.
