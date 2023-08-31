# City temperature mangement

Project for managing cities(CRUD), getting and updating temperature records for every city in DB


## Installation
- Python 3.7+ must be installed (3.9+ prefer)
- Clone this repo on your PC
- Sign up on https://www.weatherapi.com/ and get API_KEY

```shell
python -m venv venv # Create virtual environment
venv\Scripts\activate # Activate venv for Windows
venv/bin/activate # Activate venv for MacOS
pip install -r requirements.txt # Install needed dependencies
```
Create .env file in project root directory with variables from .env.sample
```shell
alembic init alembic # Initiate alembic
alembic revision --autogenerate -m "Name commit" # Input name you want
alembic upgrade head # Apply migrations for DB
uvicorn main:app --reload # Run server
```

## Using

For access endpoints you can use Postman or visit http://127.0.0.1:8000/docs/ and use Swagger documentation page

## Endpoints

List of all endpoints you can find at:\
http://127.0.0.1:8000/docs/  Swagger documentation\
http://127.0.0.1:8000/redoc/ Redoc documentation

## Technologies used

- FastAPI framework
- SQLAlchemy # ORM
- Weather API # service for getting info for updating temperature records in DB