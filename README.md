# FastAPI Temperature-manager

## Description:
FastAPI application for manage temperature in choosen cities.
Asynchronous FastAPI application using **async SQLAlchemy** and **async Alembic** for database access and migrations.

Endpoints:

Manage cities:
1. Add city
2. List of all cities in database
3. Get city by id
4. Update city by id
5. Remove from base city by id

Manage temperatures
1. Update temperatures for all cities (168 records per city, 24*7)
2. List of all temperatures
3. List of temperatures by city_id
4. Flush all records in temperatures

Stack:
1. FastAPI
2. SQLAlchemy(ORM)
3. Pydantic
4. Alembic

## How to install and run:
1. Clone repository:
`git clone https://github.com/AndS9/py-fastapi-city-temperature-management-api.git`
2. Init virtual enviroment and run it:
`python -m venv .venv`

    Start venv:
    on macOs/linux  `source .venv/bin/activate`,       
    on Windows      `soucre .venv/Scripts/activate` or `.\ venv\Scripts\activate.ps1`

3. Install requiring packages
`pip install -r requirements.txt`
4. Optional: Change path to database in app.settings(line 7)
```
7 line   DATABASE_URL: str | None = 'sqlite+aiosqlite:///./my_database.db'

```
5. initalize database with:
`alembic upgrade head`
6. Run application from app directory
`fastapi dev main.py` 