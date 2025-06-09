# City Temperature Management API

## Description
The FastAPI application that manages city data and its corresponding temperature data.

### Includes:
1. The API for managing city data:
- read all cities
- create new city
- get city  by id
- delete city by id
- update city by id

2. The API for get i managing information about weather in diferent cities: 
- read saved information  temperature data for all cities in the database
- ability of get saved temperature data for a specific city (by its ID)
- retrieves the current temperature data for all cities in the database from APIWeather and stores that data in the database

## The project structure:
```
city_temperature_management_api
├── alembic/
├── data/ (for ..db)
├── src
│   └── cities
│   │   ├── __init___.py
│   │   ├── crud.py
│   │   ├── models.py
│   │   ├── router.py
│   │   ├── schemas.py
│   └── temperature
│   │   ├── __init___.py
│   │   ├── crud.py
│   │   ├── models.py
│   │   ├── router.py
│   │   ├── schemas.py
│   │   └── utils.py
│   ├── database.py
│   ├── dependencies.py
│   ├── settings.py
│   └── main.py
├── alembic.ini
├── Dockerfile
├── docker-compose.yml
├── .env
├── .gitignore
├── README.md
└── requirements.txt
```


## How to run the application?

### Running with one simple command
run:    `docker-compose up --build`
open:   [FastAPI app](http://127.0.0.1:8000/docs/)


### Step by step instructions:
1. Create a file .env and fill it out according to the env.sample
2. Create & activate venv:
    `python -m venv venv`
    `source venv/Scripts/activate`
3. Settings up dependencies:
    `pip install -r requirements.txt`
4. Do migrations:
    `alembic revision --autogenerate -m "Initial migration"`
    `alembic upgrade head`
5. Run the application:
    `uvicorn src.main:app --reload`
6. open:   [FastAPI app](http://127.0.0.1:8000/docs/)
