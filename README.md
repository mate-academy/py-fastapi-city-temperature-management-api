# City Temperature Management API

## Installation
1. `python -m venv venv`
2. `pip install -r requirements.txt`
3. Configure .env file
4. Create .env file with settings using .env.sample
* Get your API key from https://www.weatherapi.com/
* Setup database url, api url and api key from the [Weather API](https://www.weatherapi.com/docs/)
5. Run those commands:
    > alembic revision --autogenerate -m "Initial migration"

    > alembic upgrade head

    > uvicorn app.main:app --reload


## Overview

1. City CRUD API for managing city data
2. Temperature API for obtaining and updating data
2. An API that fetches current temperature data for all cities in the database and stores this data in the database. This API should also provide a list endpoint to retrieve the history of all temperature data.
This project is a Weather API service that allows users to manage cities and record temperatures for those cities. The project is built using SQLAlchemy for database interactions and follows a typical CRUD (Create, Read, Update, Delete) pattern.

##  Structure

* Application is located in the `app` directory, in the `core` directory there are files with settings and database initialization
* Routers for CityAPI and TemperatureAPI are split into two files in the `routers` directory
* API for working with third-party weather service is in the `api` directory.
* The `alimbic` directory has been renamed to `migrations` for convenience.
* .env file is used to store sensory information and is located in the root of the project.