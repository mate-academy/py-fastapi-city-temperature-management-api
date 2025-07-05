# City Temperature Management API

A FastAPI-based asynchronous REST API for managing temperature records of cities.

## Features

* Create cities, fetch temperature records from www.weatherapi.com
* Asynchronous database operations

## Technologies

* FastAPI
* SQLAlchemy (async)
* Alembic
* Pydantic
* Uvicorn

## Setup
> Before running the application, rename .env.sample to .env and insert your environment-specific data.
```bash
git clone https://github.com/uzlss/py-fastapi-city-temperature-management-api.git
cd py-fastapi-city-temperature-management-api

python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

## API Overview

### Cities

* `POST /cities/` – Create a city
* `GET /cities/` – List cities
* `GET /cities/id/` - Retrieve a city
* `DELETE /cities/id/` - Delete a city

### Temperatures

* `POST /temperatures/bulk/` – Bulk create
* `GET /temperatures/` – List temperatures, filter by city id
