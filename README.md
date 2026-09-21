# City Temperature API

FastAPI application for managing cities and storing their temperature history.

The application provides:

* CRUD operations for cities
* Async fetching of current temperature data from an external weather API
* Storage of temperature history in SQLite
* Filtering temperature records by city

## Technologies

* Python
* FastAPI
* SQLAlchemy
* SQLite
* Pydantic
* HTTPX
* Uvicorn
* Open-Meteo API

## Project Structure

```text
project/
├── city/
│   ├── crud.py
│   ├── database.py
│   ├── models.py
│   └── schemas.py
├── main.py
├── requirements.txt
└── README.md
```

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd <repository-folder>
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

If `requirements.txt` is not available yet, install the required packages:

```bash
pip install fastapi uvicorn sqlalchemy httpx
```

## Database

The application uses SQLite.

The database tables are initialized automatically when the application starts:

```python
Base.metadata.create_all(bind=engine)
```

No separate migration command is required for the current version of the project.

The SQLite database file is created automatically if it does not already exist.

## Running the Application

Start the FastAPI development server:

```bash
uvicorn main:app --reload
```

The application will be available at:

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

### Create a city

```http
POST /cities/
```

Example request body:

```json
{
  "name": "Kyiv",
  "additional_info": "Capital of Ukraine"
}
```

### Get all cities

```http
GET /cities/
```

### Get a city by ID

```http
GET /cities/{city_id}/
```

Example:

```http
GET /cities/1/
```

### Update a city

```http
PUT /cities/{city_id}/
```

Example request body:

```json
{
  "name": "Kyiv",
  "additional_info": "Capital and largest city of Ukraine"
}
```

### Delete a city

```http
DELETE /cities/{city_id}
```

Example response:

```json
{
  "detail": "City deleted"
}
```

## Temperatures

### Update temperatures

```http
POST /temperatures/update/
```

This endpoint:

1. Retrieves all cities from the database.
2. Finds coordinates for every city using the Open-Meteo Geocoding API.
3. Fetches the current temperature using the Open-Meteo Weather API.
4. Stores a new temperature record for each successfully processed city.

Temperature fetching is implemented asynchronously using `httpx.AsyncClient`.

Example result:

```json
{
  "detail": "Temperatures updated"
}
```

### Get all temperature records

```http
GET /temperatures/
```

Example response:

```json
[
  {
    "id": 1,
    "city_id": 1,
    "date_time": "2026-09-21T12:00:00",
    "temperature": 18.4
  },
  {
    "id": 2,
    "city_id": 2,
    "date_time": "2026-09-21T12:00:01",
    "temperature": 16.7
  }
]
```

### Filter temperatures by city

```http
GET /temperatures/?city_id={city_id}
```

Example:

```http
GET /temperatures/?city_id=1
```

This returns all stored temperature records for the city with ID `1`.

## Database Design

The application contains two main database models.

### City

Fields:

* `id`
* `name`
* `additional_info`

City names are unique.

### Temperature

Fields:

* `id`
* `city_id`
* `date_time`
* `temperature`

`city_id` is a foreign key referencing `City.id`.

The relationship is one-to-many:

```text
City
  |
  └── many Temperature records
```

A city can therefore have multiple temperature records, which allows the application to store temperature history instead of replacing the previous value.

## Design Choices

### SQLAlchemy and SQLite

SQLite was selected because it is simple to configure and is sufficient for this project.

SQLAlchemy ORM is used to work with the database through Python models instead of writing raw SQL queries.

### Dependency Injection

The database session is provided through FastAPI's `Depends` mechanism.

This allows each endpoint to receive a database session and ensures that the session is closed after the request is completed.

### Async Temperature Fetching

External HTTP requests are performed asynchronously using `httpx.AsyncClient`.

The application first converts a city name into latitude and longitude using the Open-Meteo Geocoding API.

The coordinates are then sent to the Open-Meteo Weather API to retrieve the current temperature.

### Temperature History

Every call to:

```http
POST /temperatures/update/
```

creates new temperature records.

Existing records are not overwritten, which allows the API to preserve temperature history.

## Assumptions and Limitations

* The project uses SQLite and is intended as a simple development or educational application.
* Database migrations are not implemented. Tables are created using `Base.metadata.create_all()`.
* The application uses the first city returned by the geocoding service when several locations have the same name.
* Temperature data depends on the availability of the external Open-Meteo API.
* A city that cannot be found by the geocoding API may be skipped during temperature updates.
* Temperature values are stored as floating-point numbers.
* The current implementation uses synchronous SQLAlchemy database sessions while external HTTP requests are asynchronous.
* Authentication and authorization are not implemented because they are outside the scope of the task.

## API Documentation

FastAPI automatically generates interactive API documentation.

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```
