# City Temperature API with FastAPI
This project implements a FastAPI application to manage city data and their corresponding temperature information.

## Features:

* CRUD API for managing cities (Create, Read, Update, Delete)
* Fetches current temperature data for all cities and stores it in the database
* Retrieves historical temperature data for a city or all cities

## Project Structure:

The project follows the recommended FastAPI application structure.

## Dependencies:

* FastAPI
* Pydantic
* SQLAlchemy

## Database:

* SQLite

## Running the Application:

1. Install dependencies:
```Bash
pip install -r requirements.txt
```

2. Apply migrations.
```bash
alembic upgrade head
```

3. Run the application:

```Bash
python.exe -m uvicorn main:app --reload 
```

## API Endpoints:

### Part 1: City CRUD API

* POST /cities - Creates a new city.
* GET /cities - Retrieves a list of all cities.
* GET /cities/{city_id} - Gets the details of a specific city by ID.
* PUT /cities/{city_id} - Updates the details of a specific city.
* DELETE /cities/{city_id} - Deletes a city by ID.

### Part 2: Temperature API

* POST /temperatures/update - Fetches current temperature data for all cities asynchronously and stores it in the database.
* GET /temperatures - Retrieves a list of all temperature records.
* GET /temperatures/?city_id={city_id} - Gets the temperature records for a specific city.

## Design Choices:

* Pydantic models are used for data validation and serialization.
* SQLAlchemy provides an object-relational mapper for interacting with the database.
* Dependency injection is used to manage database connections.
* Weather API is used to get data about the current weather for fetched cities.

## Documentation:

This API is documented with Swagger API for better understanding and usability.
