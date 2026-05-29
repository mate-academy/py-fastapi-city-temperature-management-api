# City Temperature Management API
FastAPI-app for managing data about cities and their temperature.
## Features
- CRUD operations for all cities (Create, Read, Update, Delete)
- you can get current temperatures for all cities from WeatherAPI
- saving data about temperature records


## Installation
```bash
pip install fastapi uvicorn sqlalchemy httpx pydantic
```

## Run
```bash
uvicorn router:app --reload
```
 
## Endpoints
- GET /cities/ - list of all cities
- POST /cities/ - create a new city
- PUT /cities/{city_id}/ - update a specific city
- GET /cities/{city_id}/ - details about specific city
- DELETE /cities/{city_id}/ - delete a specific city
- GET /temperatures/ - list of all temperature records
- POST /temperatures/update/ - get the temperature records for all cities
- GET /temperatures/?city_id={city_id} - get the temperature records for a specific city


## Technologies
- FastAPI
- SQLAlchemy
- SQLite
- httpx (async HTTP клієнт)