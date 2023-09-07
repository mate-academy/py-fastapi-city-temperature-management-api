# City temperature mangement

Project for managing cities(CRUD), getting and updating temperature records for every city in DB

## Installation

- Python 3.7+ must be installed (3.9+ prefer)
- Clone this repo on your PC
- Sign up on https://www.weatherapi.com/ and get API_KEY

```shell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create .env file in project root directory with variables from .env.sample

```shell
alembic init alembic
alembic revision --autogenerate -m "Name commit" # Input name you want
alembic upgrade head
uvicorn main:app --reload # Run server
```

## Using

For access endpoints you can use Postman or visit http://127.0.0.1:8000/docs/ and use Swagger documentation page

## Endpoints

### Cities:

- GET /cities/: Get a list of cities and their temperatures.
- POST /cities/: Create new city instance.
- GET /cities/{city_id}/: Get detail page for city.
- DELETE /cities/{city_id}/: Delete chosen city.

### Temperature:

- GET /temperatures/: Get list of updated temperatures of cities in DB.
- POST //temperatures/update/: Update temperatures for all cities in DB

## Technologies used

- FastAPI framework
- SQLAlchemy # ORM
- Weather API # service for getting info for updating temperature records in DB
