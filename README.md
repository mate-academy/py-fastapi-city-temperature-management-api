# City & Temperature Management API
This FastAPI application provides a simple and efficient way to manage city data and their corresponding temperature records. The application is divided into two main components:

- City CRUD API: Manage city data (Create, Read, Update, Delete).
- Temperature API: Fetch and store current temperature data for cities and retrieve temperature data history.

## Installation & Running the Application
To run this application, follow these steps:

### Clone the repository:
```shell
  git clone https://github.com/OlegatorLE/py-fastapi-city-temperature-management-api.git
  cd py-fastapi-city-temperature-management-api
  python -m venv venv
  source venv/bin/activate # or venv\Scripts\activate in Windows
  pip install -r requirements.txt
  create .env file by .env.sample
  uvicorn main:app --reload
```

The API will be available at http://127.0.0.1:8000.

## Design Choices
- FastAPI: Chosen for its high performance and ease of use in building APIs with automatic validation and interactive API documentation.
- SQLAlchemy: Utilized for its ORM capabilities, allowing for easy database interactions and migrations.
- Pydantic: Models were created to ensure robust data validation and serialization.
- SQLite: Selected for its simplicity and zero-configuration for this demonstration.
- Dependency Injection: Implemented for database session management to ensure a clean and efficient way to handle database connections.

## Endpoints
### City CRUD API
POST /cities: Create a new city.
GET /cities: Retrieve a list of all cities.
GET /cities/{city_id}: Retrieve details of a specific city.
PUT /cities/{city_id}: Update details of a specific city.
DELETE /cities/{city_id}: Delete a specific city.

### Temperature API
POST /temperatures/update: Fetch and store current temperature for all cities.
GET /temperatures: Retrieve a list of all temperature records.
GET /temperatures/?city_id={city_id}: Retrieve temperature records for a specific city.

## Features
The Temperature API fetches data from an external service (https://www.weatherapi.com/); error handling is implemented with the assumption that this service can be occasionally unavailable or return errors.
