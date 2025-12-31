<img src="photo_2025-12-31_12-36-09.jpg" width="300">

# CITY TEMPERATURE MANAGEMENT API
> This application manages city data and their corresponding temperature data.
> Implemented: 
> CRUD (Create, Read, Update, Delete) API for managing city data.
> List temperatures for all cities
> List temperatures for specific city
> Update current temperature data for all cities in the database
> To get to know in detail you can open a docs after running http://127.0.0.1:8000/docs


## Installing / Getting started
```shell
python -m venv venv
venv\Scripts\activate (on Windows)
pip install -r requirements.txt	
```

## Running

* Copy from .env.sample to .env WHETHER_SERVICE_API_KEY.
This key you can get free https://developer.accuweather.com/home

* Run migrations 
```shell
alembic upgrade head
 ```

* Run server with IDE or with command
```shell
fastapi dev
```

* You can use test data for testing with this cmd
```shell
sqlite3 city_temperature.db .dump > city_temperature_db.sql
```

## Features
* Using Fast API framework
* Pydantic Validation
* Asyncio I/O-bound operations 
* Using SQLAlchemy ORM
* Implement migrations with Alembic