# City temperature API

## **Table of Contests**
* [**Introduction**](#introduction)
* [**Requirements**](#requirements)
* [**Installation**](#installation)
* [**Used technologies**](#used-technologies)
* [**Endpoints**](#endpoints)


## Introduction
City Temperature Management API is provided 
for receiving actual temperature for required city.

## Requirements
* python 3.8+
* pip

## Installation
1. Clone this repository:
    ```https://github.com/BogdanFSD/py-fastapi-library-management-api```
2. Create virtual environment and activate it:
     - ```python -m venv venv``` 
     - ```venv\Scripts\activate```

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
