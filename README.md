# City Temperature Management API

A FastAPI application for managing cities and collecting current temperature data.

The application provides a CRUD API for cities and an API for fetching and storing current temperature data using the Open-Meteo service.

## Features

* Create, read, update and delete cities.
* Store city coordinates for weather requests.
* Fetch current temperature for all stored cities.
* Store temperature history in SQLite.
* Retrieve all temperature records.
* Filter temperature records by city.
* Asynchronous HTTP requests using `httpx`.
* Automatic API documentation with Swagger UI.
* Dependency Injection for database sessions.
* SQLAlchemy ORM with SQLite.

## Project Structure

```text
py-fastapi-city-temperature-management-api/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   │
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── cities.py
│   │   └── temperatures.py
│   │
│   └── services/
│       ├── __init__.py
│       └── weather.py
│
├── test_weather.py
├── cities.db
├── .gitignore
└── README.md
```

## Technologies

* Python 3.11+
* FastAPI
* Uvicorn
* SQLAlchemy
* SQLite
* Pydantic
* HTTPX
* Open-Meteo API

## Installation

Clone the repository and open the project directory:

```bash
cd py-fastapi-city-temperature-management-api
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment.

### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

### Git Bash

```bash
source .venv/Scripts/activate
```

Install the dependencies:

```bash
pip install fastapi uvicorn sqlalchemy httpx
```

## Running the Application

Start the development server:

```bash
python -m uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

ReDoc documentation:

```text
http://127.0.0.1:8000/redoc
```

## API Endpoints

### Cities

#### Create a city

```text
POST /cities/
```

Example request:

```json
{
  "name": "Erfurt",
  "additional_info": "Germany",
  "latitude": 50.9848,
  "longitude": 11.0299
}
```

#### Get all cities

```text
GET /cities/
```

#### Get a specific city

```text
GET /cities/{city_id}
```

#### Update a city

```text
PUT /cities/{city_id}
```

#### Delete a city

```text
DELETE /cities/{city_id}
```

### Temperatures

#### Update temperatures

```text
POST /temperatures/update
```

This endpoint:

1. Retrieves all cities from the database.
2. Uses their latitude and longitude.
3. Sends asynchronous requests to Open-Meteo.
4. Retrieves the current temperature.
5. Stores the result in the `temperatures` table.
6. Returns the newly created temperature records.

#### Get temperature history

```text
GET /temperatures
```

#### Get temperatures for a specific city

```text
GET /temperatures?city_id=1
```

## Database

The application uses SQLite.

The database file is:

```text
cities.db
```

The application contains two main tables.

### City

```text
id
name
additional_info
latitude
longitude
```

### Temperature

```text
id
city_id
date_time
temperature
```

Each temperature record belongs to a city through the `city_id` foreign key.

One city can therefore have many temperature records, which allows the application to maintain temperature history.

## Weather Service

The application uses the Open-Meteo API to retrieve current temperature data.

No API key is required.

The weather requests are implemented asynchronously using:

```python
httpx.AsyncClient
```

Multiple city weather requests are processed concurrently using `asyncio.gather()`.

## Design Choices

The application is divided into separate layers.

### `models.py`

Contains SQLAlchemy database models.

### `schemas.py`

Contains Pydantic schemas used for request validation and API responses.

### `crud.py`

Contains database operations such as creating, reading, updating and deleting records.

### `routers/`

Contains FastAPI route handlers.

* `cities.py` handles city endpoints.
* `temperatures.py` handles temperature endpoints.

### `services/weather.py`

Contains communication with the external weather API.

This separation keeps the application easier to understand, test and maintain.

### `database.py`

Contains the SQLAlchemy engine, session factory and FastAPI database dependency.

## Error Handling

The API returns `404 Not Found` when a requested city does not exist.

If the external weather service cannot be reached or returns an error, the temperature update endpoint returns an appropriate `502 Bad Gateway` response.

## Testing

The weather service can also be tested separately using:

```bash
python test_weather.py
```

The test performs an asynchronous request to Open-Meteo and prints the current temperature and timestamp.

Example output:

```text
Temperature: 20.8 °C
Date time: 2026-08-19T10:45
```

## Assumptions and Simplifications

* SQLite is used because this is a small educational project.
* City coordinates are stored directly in the database instead of implementing geocoding.
* Open-Meteo is used as the external weather provider because it does not require an API key.
* Temperature values are stored in Celsius.
* Database migrations are not included because the project is intended as a small educational application.
* The application stores every temperature update as a new record to preserve historical data.

## Example Workflow

Create a city:

```text
POST /cities/
```

Then update temperatures:

```text
POST /temperatures/update
```

Finally retrieve the history:

```text
GET /temperatures
```

or filter it:

```text
GET /temperatures?city_id=1
```

## License

This project was created as an educational FastAPI project.

