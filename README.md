
# Temperature Management API

API service for managing cities and temperatures using `www.weatherapi.com`. 
This project uses FastApi, SQLAlchemy, Alembic and SQLite.

## Installing / Getting started

```shell
git clone https://github.com/Anastasia-Su/py-fastapi-city-temperature-management-api.git
cd py-fastapi-city-temperature-management-api
python -m venv venv
venv\Scripts\activate (on Windows)
source venv/bin/activate (on macOS)
pip install -r requirements.txt
```
Create `.env` file based on `.env.sample`.

Create migrations:
```shell
alembic init alembic
alembic revision --autogenerate -m 'initial_migration' 
alembic upgrade head
```
Run the server:
```shell
python -m uvicorn main:app
```

## Features

* CRUD for cities
* Update DB with temperatures
* Get temperatures for all the cities in DB
* Get temperature by city id
* Documentation: `/docs/`
