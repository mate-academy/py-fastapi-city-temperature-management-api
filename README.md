# City Temperature Management API

A RESTful API built with FastAPI, SQLAlchemy, and SQLite for managing cities and tracking their temperature history.

The application allows users to create, retrieve, update, and delete cities. It also fetches current temperature data from the Open-Meteo API and stores the results in a local SQLite database.

## Technologies

- Python 3.10+
- FastAPI
- SQLAlchemy 2.0
- Pydantic
- SQLite
- HTTPX
- Uvicorn
- Open-Meteo API

## Project Structure

```text
app/
├── __init__.py
├── main.py
├── database.py
├── models.py
├── schemas.py
├── crud.py
├── dependencies.py
├── routers/
│   ├── __init__.py
│   ├── cities.py
│   └── temperatures.py
└── services/
    ├── __init__.py
    └── weather.py

.gitignore
README.md
```

### File Descriptions

- `main.py` — initializes the FastAPI application and registers routers.
- `database.py` — configures the SQLite database and SQLAlchemy session factory.
- `models.py` — defines the City and Temperature database models.
- `schemas.py` — contains Pydantic models for data validation and serialization.
- `crud.py` — implements database operations.
- `dependencies.py` — manages database sessions through dependency injection.
- `routers/cities.py` — handles city-related endpoints.
- `routers/temperatures.py` — handles temperature-related endpoints.
- `services/weather.py` — fetches temperature data from Open-Meteo.

## Installation and Setup

### 1. Clone the Repository

Clone the project repository from GitHub and navigate to the project directory.

```bash
git clone https://github.com/annababoi/py-fastapi-city-temperature-management-api.git
cd py-fastapi-city-temperature-management-api
```

### 2. Create a Virtual Environment

```bash
python3 -m venv .venv
```

Activate the virtual environment.

On macOS/Linux:

```bash
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
python -m pip install fastapi sqlalchemy pydantic httpx "uvicorn[standard]"
```

### 4. Run the Application

From the project root directory, execute:

```bash
python -m uvicorn app.main:app --reload
```

The application will be available at:

http://127.0.0.1:8000

### 5. Open API Documentation

FastAPI automatically generates interactive API documentation.

Swagger UI:

http://127.0.0.1:8000/docs

ReDoc:

http://127.0.0.1:8000/redoc

You can use Swagger UI to test all API endpoints directly in your browser.

## API Endpoints

### City Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/cities` | Create a new city |
| GET | `/cities` | Retrieve a list of cities |
| GET | `/cities/{city_id}` | Retrieve a city by ID |
| PUT | `/cities/{city_id}` | Update a city's details |
| DELETE | `/cities/{city_id}` | Delete a city |

### Temperature Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/temperatures/update` | Fetch and save current temperatures for all cities |
| GET | `/temperatures` | Retrieve temperature history |
| GET | `/temperatures?city_id=1` | Retrieve temperature history for a specific city |

## Usage Examples

### Create a City

**POST /cities**

Request body:

```json
{
  "name": "Lviv",
  "additional_info": "Ukraine"
}
```

Example response:

```json
{
  "id": 1,
  "name": "Lviv",
  "additional_info": "Ukraine"
}
```

The `additional_info` field is optional.

### Get All Cities

**GET /cities**

Returns a list of cities stored in the database.

The endpoint supports pagination using the `skip` and `limit` query parameters.

Example:

```text
GET /cities?skip=0&limit=10
```

### Get a Specific City

**GET /cities/1**

Returns information about the city with ID 1.

If the city does not exist, the API returns HTTP 404.

### Update a City

**PUT /cities/1**

Request body:

```json
{
  "name": "Kyiv",
  "additional_info": "Capital of Ukraine"
}
```

Updates the information associated with the specified city.

### Delete a City

**DELETE /cities/1**

Deletes the specified city.

Returns HTTP 204 when the operation is successful.

### Update Temperatures

**POST /temperatures/update**

This endpoint:

1. Retrieves all cities from the SQLite database.
2. Finds their geographical coordinates using the Open-Meteo Geocoding API.
3. Fetches current temperatures asynchronously.
4. Stores the retrieved data in the Temperature table.
5. Returns the number of successfully saved temperature records.

Example response:

```json
{
  "updated": 3
}
```

Each successful request creates new temperature records, allowing the application to maintain temperature history.

### Get Temperature History

**GET /temperatures**

Returns temperature records ordered from newest to oldest.

Example response:

```json
[
  {
    "id": 1,
    "city_id": 1,
    "date_time": "2026-10-30T12:00:00",
    "temperature": 12.5
  }
]
```

To filter records by city:

```text
GET /temperatures?city_id=1
```

## Design Choices

### FastAPI

FastAPI was selected because it supports automatic data validation, dependency injection, asynchronous endpoints, and interactive API documentation.

### SQLite and SQLAlchemy

SQLite provides a lightweight database without requiring an external database server.

SQLAlchemy ORM simplifies database operations by allowing Python classes to represent database tables.

The application uses two database models:

- `City` — stores information about cities.
- `Temperature` — stores temperature measurements associated with cities.

The models have a one-to-many relationship: one city can have multiple temperature records.

### Pydantic

Pydantic models validate incoming request data and serialize API responses.

Separate schemas are defined for creating, updating, and reading city data.

### Dependency Injection

Database sessions are managed using FastAPI's `Depends` mechanism.

Each request receives a database session, which is closed when the request finishes.

This approach improves code organization and makes database operations easier to maintain.

### Modular Project Structure

The application separates API routes, database operations, Pydantic schemas, and external API interactions into dedicated modules.

This separation makes the code easier to read, test, and extend.

### Asynchronous HTTP Requests

HTTPX AsyncClient is used to make asynchronous requests to the Open-Meteo API.

Asynchronous HTTP requests allow the application to wait for external API responses without blocking the event loop.

### Temperature History

Temperature measurements are stored as separate database records.

Instead of overwriting previous values, every successful update adds a new record.

This allows users to retrieve historical temperature data for individual cities.

## Assumptions and Simplifications

- SQLite is used for local development.
- City names are used to retrieve geographical coordinates.
- The first matching location returned by Open-Meteo is selected.
- Temperature values are stored in degrees Celsius.
- Temperature timestamps are requested in UTC.
- Every successful temperature update creates a new database record.
- Temperature updates are triggered manually through the API.
- The application does not include automatic scheduled updates.
- If weather data cannot be retrieved for a city, the error is logged and that city is skipped.
- The application does not implement user authentication.
- An internet connection is required to retrieve current weather data.
- The database is created locally when the application starts.

## Error Handling

The application uses FastAPI's HTTP exception handling and Pydantic validation.

Common HTTP status codes:

| Status Code | Description |
|-------------|-------------|
| 200 | Successful request |
| 201 | Resource successfully created |
| 204 | Resource successfully deleted |
| 404 | Requested city does not exist |
| 422 | Request data fails validation |

External weather API errors are logged, and processing continues with the remaining cities when possible.

## External API

Weather data is provided by Open-Meteo:

https://open-meteo.com/

The application uses two Open-Meteo services:

1. **Geocoding API** — converts city names into geographical coordinates.
2. **Forecast API** — retrieves current temperature data for the specified coordinates.

Open-Meteo provides weather data without requiring an API key for non-commercial use.

## Possible Future Improvements

The application could be extended with:

- Automatic scheduled temperature updates.
- More advanced city search and filtering.
- Additional weather information, such as humidity and wind speed.
- PostgreSQL support.
- Automated tests using pytest.
- Docker containerization.
- User authentication.

## Author

**Anna Baboi**

Educational project developed as part of Python and FastAPI practice at Mate Academy.