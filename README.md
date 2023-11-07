# City Temperature API
The City Temperature Update API is a powerful and flexible web service designed to provide real-time temperature data for cities around the world. The application has two main components:

1. A CRUD (Create, Read, Update, Delete) API for managing city data.
2. An API that fetches current temperature data for all cities in the database and stores this data in the database. This API should also provide a list endpoint to retrieve the history of all temperature data.


## Installation
Python 3.7+ must be installed
```shell
git clone https://github.com/Barsh4ec/py-fastapi-city-temperature-management-api
python -m venv venv
source venv\Scripts\activate  # On unix like systems use `venv/bin/activate`
pip install -r requirements.txt
```
- Sign in on https://www.weatherapi.com/ and generate API Key
- Create .env file in project root similar to .env.sample and fill your data
- Run server
```shell
alembic init alembic # Initiate alembic
alembic upgrade head # Apply migrations for DB
uvicorn main:app --reload # Run server
```


### City endpoints
- `POST /cities`: Create a new city.
- `GET /cities`: Get a list of all cities.
- `GET /cities/{city_id}`: Get the details of a specific city.
- `PUT /cities/{city_id}`: Update the details of a specific city.
- `DELETE /cities/{city_id}`: Delete a specific city.

### Temperature endpoints
- `POST /temperatures/update` that fetches the current temperature for all cities in the database from an online resource https://www.weatherapi.com/.
- `GET /temperatures`: Get a list of all temperature records.
- `GET /temperatures/?city_id={city_id}`: Get the temperature records for a specific city.


