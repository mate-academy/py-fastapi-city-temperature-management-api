## City Temperature Management API

API for managing city temperatures

1. A CRUD (Create, Read, Update, Delete) API for managing city data.
2. An API that fetches current temperature data for all cities in the database and stores this data in the database. This API should also provide a list endpoint to retrieve the history of all temperature data.

## Installation
1. Python 3.7+
2. Clone repo
3. Sign up on https://www.weatherapi.com/ and get API_KEY


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