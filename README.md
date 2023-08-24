# City temperature management api

***
This API provides you with the opportunity to manage cities (CRUD operations) and retrieve their temperatures through a third-party API (WeatherAPI).

***
## Installation
```shell
   1. python -m venv venv
   2. venv\Scripts\activate
   3. pip install -r requirements.txt
   4. Please provide the environment variables that you can find in the env.sample file.
   5. alembic init alembic
   6. alembic revision --autogenerate -m "Provide name"
   7. alembic upgrade head
   8. uvicorn main:app --reload
```
***

## Endpoints
City:
- POST /cities/ - Create a new city
- GET /cities/  -  Get a list of all cities (check docs if you need some limit and skip)
- GET /cities/{city_id}/ - Get the details of a specific city
- PUT /cities/{city_id}/ -  Update the details of a specific city
- DELETE /cities/{city_id}/ - Delete a specific city

Temperature:
- GET /temperatures/ - Get a list of all temperature records(check docs if you need some limit and skip)
- GET /temperatures/{city_id}/ - Get the temperature records for a specific city

# Documentation:
- GET /docs/
***

## Design Choices
- Httpx - Used for asynchronous requests to third-party APIs
- WeatherAPI - Used for fetch temperature for cities
- SQLAlchemy[asyncio] - Utilized for asynchronous database operations
- FastAPI - Used as the primary framework for the project due to its capability to work with asynchronous operations.
