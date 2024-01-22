## GetTemperature API

This is a FastAPI application that manages city data and their corresponding temperature data. The application have two main components (apps):

1. A CRUD (Create, Read, Update, Delete) API for managing city data.
2. An API that fetches current temperature data for all cities in the database and stores this data in the database. This API also provide a list endpoint to retrieve the history of all temperature data.

### City API

1. A Pydantic model `City` with the following fields:
    - `id`: a unique identifier for the city.
    - `name`: the name of the city.
    - `additional_info`: any additional information about the city.
2. Endpoints:
    - `POST /cities/`: Create a new city.
    - `GET /cities/`: Get a list of all cities.
    - `GET /cities/{city_id}/`: Get the details of a specific city.
    - `PUT /cities/{city_id}/`: Update the details of a specific city.
    - `DELETE /cities/{city_id}/`: Delete a specific city.

### Temperature API

1. A Pydantic model `Temperature` with the following fields:
    - `id`: a unique identifier for the temperature record.
    - `city_id`: a reference to the city.
    - `date_time`: the date and time when the temperature was recorded.
    - `temperature`: the recorded temperature.
2. Endpoints:
    - `GET /temperatures/`: Get a list of all temperature records.
    - `GET /temperatures/?city_id={city_id}`: Get the temperature records for a specific city.
    - `POST /temperatures/update/` : Fetch the temperature data from the Openweather API for all the cities in your database

### Installation
 ````
 # Copy the repository
 
 git clone https://github.com/nataliia-petrushak/py-fastapi-city-temperature-management-api.git
 
 # Install virtual environment
 
 python -m venv venv
 source venv/bin/activate
 
 # Install all the necessary requirements
 
 pip install requirements.txt
 
 # Make migrations & create tables
 
 alembic revision --autogenerate -m "Create_city_&_temperature_table"
 alembic upgrade head
 
 # Run server
 
 uvicorn src.main:app --reload
 ````

Visit http://127.0.0.1:8000/docs

Have fun!