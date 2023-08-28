# City Temperature Management API

## Table of Contents
 1. [Introduction](#introduction)
 2. [Requirements](#requirements)
 3. [Installation](#installation)
 4. [Used technologies](#used-technologies)
 5. [Endpoints](#endpoints)


## Introduction
City Temperature Management API is provided 
for receiving actual temperature for required city.

## Requirements
* python 3.8+
* pip

## Installation
1. Clone this repository:
    ```https://github.com/Kirontiko/py-fastapi-city-temperature-management-api.git```
2. Create virtual environment and activate it:
   * Tooltip for windows:
     - ```python -m venv venv``` 
     - ```venv\Scripts\activate```
   * Tooltip for mac:
     - ```python -m venv venv```
     - ```source venv/bin/activate```
3. Install dependencies:
    - ```pip install -r requirements.txt```

4. Apply all migrations in database:
   - ```alembic upgrade head```

5. Run app
   - ```uvicorn main:app --reload```

## Used technologies

- FastAPI
- Httpx
- SQLAlchemy[async]
- WeatherAPI

Endpoints

City:

## Endpoints
City:
- POST /cities/ - Create a new city
- GET /cities/ -  Get a list of all cities (you can set limit and skip for page)
- GET /cities/{city_id}/ - Get the details of a specific city
- PUT /cities/{city_id}/ -  Update the details of a specific city
- DELETE /cities/{city_id}/ - Delete a specific city

Temperature:
- POST /temperatures/update/ - update temperature records for all cities
- GET /temperatures/ - Get a list of all temperature records(check docs if you need some limit and skip)
- GET /temperatures/{city_id}/ - Get the temperature records for a specific city

Documentation:
- GET docs/


