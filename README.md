# 🌡️ City & Temperature management
FastAPI application that manages city data and their corresponding temperature data. The application have two main components (apps):

1. A CRUD (Create, Read, Update, Delete) API for managing city data.
2. An API that fetches current temperature data for all cities in the database and stores this data in the database. This API also provide a list endpoint to retrieve the history of all temperature data.


## ⚙️ Installation
Python 3.7+ must be installed
- Clone this repo on your 
```shell
git clone https://github.com/innyshka/py-fastapi-city-temperature-management-api.git
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```
- Sign up on https://www.weatherapi.com/ and get API_KEY
- Create .env file in project root directory with variables from .env.sample
- Run server
```shell
alembic init alembic # Initiate alembic
alembic upgrade head # Apply migrations for DB
uvicorn main:app --reload # Run server
```
## 📍 Endpoints
- **/city** - you can get list of all cities (also you can create a new city) 
- **/cities/{city_id}** - you can get the details of a specific city (also you can update and delete)
- **/temperatures/update** - you can update the current temperature for all cities in the database from an [online resource ](https://www.weatherapi.com/)
- **/temperatures** - you can get a list of all temperature records
- **/temperatures/?city_id={city_id}** - you can get the temperature records for a specific city
## 📃 Documentation 
For access endpoints you can visit http://127.0.0.1:8000/docs/ and use Swagger documentation page

## 🗃️ Technologies:
- Fast API
- SQLAlchemy
- Weather API