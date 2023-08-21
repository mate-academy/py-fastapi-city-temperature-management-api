# City temperature management API
***

This API is a simple temperature management system for cities. It allows to create, update, delete and get cities and their temperatures.

## Setup
***
Set your own .env file with corresponding data
```
    cp .env.sample .env
```
Clone the repository
```
    git clone ...
    cd py-fastapi-city-temperature-management-api
```
Run virtual environment
```
    python -m venv venv
    source venv/bin/activate
```
Install the dependencies
```
    pip install -r requirements.txt
```
Initiate alembic migrations
```
    alembic init alembic
    alembic revision --autogenerate -m "init"
    alembic upgrade head
```
Run the server
```
    uvicorn main:app --reload
```

Use the API
- `POST /cities`: Create a new city.
- `GET /cities`: Get a list of all cities.
- `GET /cities/{city_id}`: Get the details of a specific city.
- `PUT /cities/{city_id}`: Update the details of a specific city.
- `DELETE /cities/{city_id}`: Delete a specific city.

- `POST /temperatures/update`: Update temperatures for all cities.
- `GET /temperatures`: Get a list of all temperature records.
- `GET /temperatures/?city_id={city_id}`: Get the temperature records for a specific city.

## Swagger
`GET /docs`: Swagger UI with API documentation.
