# FastAPI City and Temperature Management App

This FastAPI application allows you to manage city data and corresponding temperature records. It consists of two main components: a city app to manege cities and an app for temperature data.

## Table of Contents
1. [Setup](#setup)
2. [City app](#city-app)
3. [Temperature app](#temperature-app)
4. [Design Choices](#design-choices)
5. [Environmental variables](#environmental-variables)


## Setup

1. Clone this repository to your local machine.
2. Navigate to the project directory.

3. Create a virtual environment:
   `python -m venv venv`

4. Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On macOS and Linux: `source venv/bin/activate`

5. Install the required packages: `pip install -r requirements.txt`
6. Make all migrations: `alembic upgrade head`
7. Start the FastAPI application: `uvicorn main:app --reload`


## City app

### Endpoints
- POST /cities: Create a new city.
- GET /cities: Get a list of all cities.
- GET /cities/{city_id}: Get details of a specific city.
- PUT /cities/{city_id}: Update details of a specific city.
- DELETE /cities/{city_id}: Delete a specific city.


## Temperature app

### Endpoints
- POST /temperatures/update: Fetches the current temperature for all cities in the database from the WeatherAPI and stores it in the Temperature table.
- GET /temperatures: Get a list of all temperature records.
- GET /temperatures/?city_id={city_id}: Get temperature records for a specific city.


## Design Choices
- The application is built using FastAPI, which provides automatic validation, serialization, and interactive documentation.
- SQLite is used as the database backend, managed by SQLAlchemy.
- Pydantic models are used for request and response validation.
- Alembic to migrate models to database
- The temperature update is performed asynchronously using async/await and fetched from WeatherAPI.


## Environmental variables

Rename .env.sample to .env and replace variables below with yours:
- DATABASE_URL
- WEATHER_API_KEY

