# City Temperature Management API

This project implements a FastAPI application for managing cities and storing temperature history for each city.

## Technologies

- Python
- FastAPI
- SQLAlchemy (async)
- SQLite
- Alembic (for database migrations)
- httpx (asynchronous requests to an external API)
- Pydantic

## How to run:

1. Clone repository:

```bash

git clone https://github.com/Iryna802498/py-fastapi-city-temperature-management-api.git
cd py-fastapi-city-temperature-management-api

```

2. Creating and activating a virtual environment:

```bash

python -m venv venv
source venv/bin/activate # for Linux/macOS
venv\Scripts\activate # for Windows

```

3. Install dependencies:

```bash

pip install -r requirements.txt

```

4. Create .env file(Do not forget that .env file not commit to your own repository):

```bash

cp .env.sample .env

```

5. Create migrations:

```bash

alembic upgrade head

```

6. Run server:

```bash

uvicorn main:app --reload

```

## Endpoints

### City

- GET /cities/ - get a list of all cities
- GET /cities/{city_id}/ - get the details of a specific city
- POST /cities/ - create a new city
- PATCH /cities/{city_id}/ - partitional update a specific city
- DELETE /cities/{city_id}/ - delete a specific city

### Temperature

- GET /temperatures/ - get a list of all temperature records
- GET /temperatures/?city_id={city_id} - get the temperature records for a specific city
- POST /temperatures/update/ - obtaining current temperatures for all cities via OpenWeatherAPI and saving them in the database

## Design solutions

- Async SQLAlchemy is used to efficiently work with asynchronous API requests.
- To avoid the N+1 problem, selectinload was used to load related objects.
- Pydantic schemas were used to validate data and return a structured API response.
- The project architecture is organised according to a modular principle (app, city, temperature, dependencies).

## Assumptions and simplifications

- Database: SQLite (for simplicity), in a real project you can use PostgreSQL or another database.
- The current implementation of temperature retrieval does not store the history of requests to the external API, only the last update is stored.
