Temperature Management API

A simple API built with FastAPI for managing cities and their temperature history.

The application uses SQLite and SQLAlchemy to store data and Open-Meteo API to get current temperatures.

Features

* Create, update, delete and view cities.
* Get temperature records for all cities or a specific city.
* Fetch current temperatures from Open-Meteo.
* Store temperature history in the database.

Installation

Install dependencies:

pip install -r requirements.txt

Run the application:

uvicorn main:app --reload

Open Swagger documentation:

http://127.0.0.1:8000/docs

Notes

Each city needs a name, additional information and coordinates (latitude and longitude) to fetch weather data.

Temperature records are saved in SQLite, so previous measurements remain in the database.