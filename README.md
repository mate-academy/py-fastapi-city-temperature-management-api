# City Temperature Management API
> A FastAPI-based service for managing and monitoring city temperatures

System of managing cities and temperatures. 
This system allows users to retrieve current temperature information for all 
cities listed in the table, store it in the database and view detailed information.

## Description

### The API allows users to:
- create, view (list and retrieve), update and delete cities in the city table,
- update the current temperature information for all cities in the city table,
- browse the history of temperature data for all cities or a specific city.

## Installing using GitHub

```shell

git clone https://github.com/TetyanaPavlyuk/py-fastapi-city-temperature-management-api.git
cd py-fastapi-city-temperature-management-api
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
Sign Up on https://www.weatherapi.com/

Copy your API Key on https://www.weatherapi.com/my/

Copy `.env.sample` to `.env`:
```shell

cp .env.sample .env
```
Populate the .env file with the required environment variables.

Apply migrations:

```shell

alembic upgrade head 
```

Run server:
```shell

uvicorn main:app --reload
```

## Features
* Comprehensive API documentation available at `/docs` for easy integration and usage.  
* Built with asynchronous programming to ensure high performance:  
  - Asynchronous API calls and database operations optimize response times.  
  - Designed to handle high loads efficiently, making the system scalable for real-time data processing.
* Dependency injection implemented for managing database sessions via `Depends(get_db)`.  
