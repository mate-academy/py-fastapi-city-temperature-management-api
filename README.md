## Task Description

You are required to create a FastAPI application that manages city data and their corresponding temperature data. The application will have two main components (apps):

1. A CRUD (Create, Read, Update, Delete) API for managing city data.
2. An API that fetches current temperature data for all cities in the database and stores this data in the database. This API should also provide a list endpoint to retrieve the history of all temperature data.

### Part 1: City CRUD API

1. Create a new FastAPI application.
2. Define a Pydantic model `City` with the following fields:
    - `id`: a unique identifier for the city.
    - `name`: the name of the city.
    - `additional_info`: any additional information about the city.
3. Implement a SQLite database using SQLAlchemy and create a corresponding `City` table.
4. Implement the following endpoints:
    - `POST /cities`: Create a new city.
    - `GET /cities`: Get a list of all cities.
    - **Optional**: `GET /cities/{city_id}`: Get the details of a specific city.
    - **Optional**: `PUT /cities/{city_id}`: Update the details of a specific city.
    - `DELETE /cities/{city_id}`: Delete a specific city.

### Part 2: Temperature API

1. Define a Pydantic model `Temperature` with the following fields:
    - `id`: a unique identifier for the temperature record.
    - `city_id`: a reference to the city.
    - `date_time`: the date and time when the temperature was recorded.
    - `temperature`: the recorded temperature.
2. Create a corresponding `Temperature` table in the database.
3. Implement an endpoint `POST /temperatures/update` that fetches the current temperature for all cities in the database from an online resource of your choice. Store this data in the `Temperature` table. You should use an async function to fetch the temperature data.
4. Implement the following endpoints:
    - `GET /temperatures`: Get a list of all temperature records.
    - `GET /temperatures/?city_id={city_id}`: Get the temperature records for a specific city.

### Additional Requirements

- Use dependency injection where appropriate.
- Organize your project according to the FastAPI project structure guidelines.

## Evaluation Criteria

Your task will be evaluated based on the following criteria:

- Functionality: Your application should meet all the requirements outlined above.
- Code Quality: Your code should be clean, readable, and well-organized.
- Error Handling: Your application should handle potential errors gracefully.
- Documentation: Your code should be well-documented (README.md).

## Deliverables

Please submit the following:

- The complete source code of your application.
- A README file that includes:
    - Instructions on how to run your application.
    - A brief explanation of your design choices.
    - Any assumptions or simplifications you made.

Good luck!

---

# City Temperature Management API

This is a FastAPI application for managing cities and storing temperature history for those cities.

The project has two main parts:

- City CRUD API
- Temperature API that fetches current temperatures from Open-Meteo

## Requirements

- Python 3.11+
- FastAPI
- Uvicorn
- SQLAlchemy
- aiosqlite
- httpx
- Alembic

Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

From inside the project folder:

```bash
uvicorn main:app --reload
```

The API will run at:

```text
http://127.0.0.1:8000
```

Interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## Database

The application uses SQLite with SQLAlchemy's async session support.

The database URL is configured in `database.py`:

```text
sqlite+aiosqlite:///./city_temperature.db
```

If using Alembic, create and apply migrations before running the app:

```bash
alembic revision --autogenerate -m "create city and temperature tables"
alembic upgrade head
```

## API Endpoints

### City Endpoints

Create a city:

```text
POST /cities/
```

Get all cities:

```text
GET /cities/
```

Get one city:

```text
GET /cities/{city_id}
```

Update a city:

```text
PUT /cities/{city_id}
```

Delete a city:

```text
DELETE /cities/{city_id}
```

### Temperature Endpoints

Create a temperature record manually:

```text
POST /temperatures/
```

Get all temperature records:

```text
GET /temperatures/
```

Get temperature records for one city:

```text
GET /temperatures/?city_id={city_id}
```

Fetch and store current temperatures for all cities:

```text
POST /temperatures/update/
```

## Temperature Data Source

The application uses Open-Meteo to fetch real temperature data.

It first uses the Open-Meteo geocoding API to convert a city name into latitude and longitude:

```text
https://geocoding-api.open-meteo.com/v1/search
```

Then it uses the Open-Meteo forecast API to get the current temperature:

```text
https://api.open-meteo.com/v1/forecast
```

No API key is required.

## Design Choices

- FastAPI routers are separated by feature: `city` and `temperature`.
- Pydantic schemas are used for request and response validation.
- SQLAlchemy models are used to define database tables.
- Dependency injection is used for database sessions through `get_db`.
- Temperature records are stored separately from cities so each city can have a temperature history.
- Open-Meteo was chosen because it provides free weather data without requiring an API key.
- Alembic is used to manage database schema migrations.

## Assumptions and Simplifications

- City names are used for geocoding.
- If Open-Meteo returns multiple matches for a city name, the first result is used.
- Temperature values are stored in Celsius.
- Database tables are created and updated through Alembic migrations.
- Error handling is basic and can be improved further for production use.
