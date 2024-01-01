## FastAPI City and Temperature management API

FastAPI application that manages city data and their corresponding temperature data. The application have two main components (apps):

1. A CRUD (Create, Read, Update, Delete) API for managing city data.
2. An API that fetches current temperature data for all cities in the database and stores this data in the database. This API should also provide a list endpoint to retrieve the history of all temperature data.

### Part 1: City CRUD API

1. Defined a Pydantic model `City` with the following fields:
    - `id`: a unique identifier for the city.
    - `name`: the name of the city.
    - `additional_info`: any additional information about the city.
 
2. Implemented the following endpoints:
    - `POST /cities`: Create a new city.
    - `GET /cities`: Get a list of all cities.
    - `GET /cities/{city_id}`: Get the details of a specific city.
    - `PUT /cities/{city_id}`: Update the details of a specific city.
    - `DELETE /cities/{city_id}`: Delete a specific city.

### Part 2: Temperature API

1. Defined a Pydantic model `Temperature` with the following fields:
    - `id`: a unique identifier for the temperature record.
    - `city_id`: a reference to the city.
    - `date_time`: the date and time when the temperature was recorded.
    - `temperature`: the recorded temperature.
2. Implemented an endpoint `POST /temperatures/update` that fetches the current temperature for all cities in the database from [Weather API](https://www.weatherapi.com/). Using an async function to fetch the temperature data, data will be stored in the `Temperature` table.
3. Implemented the following endpoints:
    - `GET /temperatures`: Get a list of all temperature records.
    - `GET /temperatures/?city_id={city_id}`: Get the temperature records for a specific city.

### Run application

1. Clone the repository:
```bash
   git clone git@github.com:MKeSiMu/py-fastapi-city-temperature-management-api.git
   cd py-fastapi-city-temperature-management-api
```
2. Set up a virtual environment and install dependencies:
```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Initialize the SQLite database and apply database migrations:
```bash
   alembic upgrade head
```
4. Run the FastAPI application:
```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```
The API will be accessible at http://localhost:8000.