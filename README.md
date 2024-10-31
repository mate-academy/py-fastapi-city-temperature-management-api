# City Temperatures API

## Description of the project

This project is a FastAPI application that manages city data and updates temperature data for each city using an external weather API. The application is asynchronous and uses SQLAlchemy to interact with the SQLite database.

## Functional capabilities
1. CRUD API for managing city data: allows you to create, retrieve, update and delete information about cities.
2. Temperature Data API: Automatically updates temperature data for all cities in the database and stores temperature history for later analysis.

## Requirements

- Python 3.8+
- FastAPI
- SQLAlchemy
- uvicorn to launch the application.

## Setting up and Launching the Application
1. Clone the repository:
    - git clone https://github.com/HalynaRohatska/py-fastapi-city-temperature-management-api

2. Creating a virtual environment (optional):
    - python -m venv venv
    - source venv/bin/activate  or `venv\Scripts\activate`  for Windows

3. Installing dependencies:
    - pip install -r requirements.txt

4. Setting environment variables: Create an .env file in the root of the project and add settings like:
    - WEATHER_API_KEY=your_api_key_here

5. Applying migrations: Before starting the program, you need to create tables in the database by applying migrations:
    - alembic revision --autogenerate -m "Initial migration"
    - alembic upgrade head

6. Launching the application: Run the command to launch the application at http://127.0.0.1:8000:
    - uvicorn main:app --reload

## Principles of Design
- Asynchrony: used for fast processing of requests, especially when retrieving data from the Weather API.
- SQLAlchemy ORM: for database interaction, allowing easy work with database models.
- Dependencies: FastAPI handles dependencies for database sessions, ensuring stable query performance.

## Endpoints

### City API
- POST /cities: Create a new city.
- GET /cities: Get a list of all cities.
- GET /cities/{city_id} (optional): Get information about a specific city.
- PUT /cities/{city_id} (optional): Update information about a specific city.
- DELETE /cities/{city_id}: Delete a city.

### Temperature API
- GET /temperatures: Get temperature history.
- GET /temperatures/?city_id={city_id}: Get temperature data for a specific city.
- POST /temperatures/update: Update temperature data for all cities using the external weather API.

