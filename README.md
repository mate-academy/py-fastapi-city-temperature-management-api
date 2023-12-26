## Overview

This FastAPI application manages city data and their corresponding temperature records. It consists of two main components:

1. City CRUD API: Manages city information, allowing users to create, retrieve, update, and delete city data.
2. Temperature API: Fetches and stores current temperature data for all cities in the database. Provides endpoints to retrieve temperature records and history.

### Part 1: City CRUD API

1. Has the next endpoints:
- `POST /cities`: Create a new city.
- `GET /cities`: Get a list of all cities.
- `GET /cities/{city_id}`: Get the details of a specific city.
- `PUT /cities/{city_id}`: Update the details of a specific city.
- `DELETE /cities/{city_id}`: Delete a specific city.

### Part 2: Temperature API

1. Has the next endpoints:
- `POST /temperatures/update`: Fetches current temperature for all cities and stores in the database.
- `GET /temperatures`: Get a list of all temperature records.
- `GET /temperatures/?city_id={city_id}`: Get the temperature records for a specific city.

### How to Run

- `git clone https://github.com/Script1988/py-fastapi-city-temperature-management-api.git`
- `python -m venv venv`
- `venv\Scripts\activate (on Windows)`
- `source venv/bin/activate (on macOS)`
- `pip install -r requirements.txt`
- use `uvicorn main:app --reload` to start the server
- access the API documentation at `http://127.0.0.1:8000/docs` to interact with the API.
