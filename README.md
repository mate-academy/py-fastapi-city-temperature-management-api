# Weather API
The Weather API stands as a versatile and robust web service 
crafted to deliver real-time temperature information for global cities.
The system comprises two primary modules:

1. A CRUD (Create, Read, Update, Delete) API for managing city data.
2. An API that fetches current temperature data for all cities in the database and stores this data in the database. This API should also provide a list endpoint to retrieve the history of all temperature data.


## Installation
Ensure Python 3.7+ is installed. Follow these steps:

```shell
git clone https://github.com/Barsh4ec/py-fastapi-city-temperature-management-api
python -m venv venv
source venv/bin/activate # for MacOS
venv\Scripts\activate # for Windows
pip install -r requirements.txt
```

You should:
* Sign in at https://www.weatherapi.com/, generate an API Key.
* Create a .env file in the project root, similar to .env.sample, and fill in your data.
* Initialize and run migrations:

```shell
alembic init alembic
alembic upgrade head
uvicorn main:app --reload
```
* Run server:

```shell
uvicorn main:app --reload
```


### City endpoints
* `POST /cities`: Create a new city.
* `GET /cities`: Get a list of all cities.
* `GET /cities/{city_id}`: Get the details of a specific city.
* `PUT /cities/{city_id}`: Update the details of a specific city.
* `DELETE /cities/{city_id}`: Delete a specific city.

### Temperature endpoints
* `GET /temperatures`: Get a list of all temperature records.
* `GET /temperatures/?city_id={city_id}`: Get the temperature records for a specific city.

