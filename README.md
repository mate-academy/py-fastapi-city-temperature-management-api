# City Temperature Manager

This application is a FastAPI application that manages city data and their corresponding temperature data. It consists of two main features:

1. A CRUD (Create, Read, Update, Delete) API for managing city data.
2. An API that fetches current temperature data for all cities in the database and stores this data in the database, providing the history of all temperature data.

## Quickstart

To run the app:
1. https://github.com/bythewaters/py-fastapi-city-temperature-management-api
2. cd train_station_api
3. python3 -m venv venv
4. source venv/bin/activate
5. Install the requirements with `pip install -r requirements.txt`.
6. Open .env_sample and change environment variables on yours !Rename file from .env_sample to .env
7. Run the server with `uvicorn main:app --reload`.

## Features

### City CRUD API

Manages city data with the following endpoints:

- `POST /cities`: Create a new city.
- `GET /cities`: Get a list of all cities.
- `GET /cities/{city_id}`: Get the details of a specific city (optional).
- `PUT /cities/{city_id}`: Update the details of a specific city (optional).
- `DELETE /cities/{city_id}`: Delete a specific city.

### Temperature API

Fetches and provides temperature data with the following endpoints:

- `GET /update_temperature/`: Fetch the current temperature for all cities in the database and store the data.
- `GET /temperatures`: Get a list of all temperature records.
- `GET /temperatures/{city_id}`: Get the temperature records for a specific city.
