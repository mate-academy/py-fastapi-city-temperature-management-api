## Task Description

You are required to create a FastAPI application that manages city data and their corresponding temperature data. The application will have two main components (apps):

1. A CRUD (Create, Read, Update, Delete) API for managing city data.
2. An API that fetches current temperature data for all cities in the database and stores this data in the database. This API should also provide a list endpoint to retrieve the history of all temperature data.

### Part 1: City CRUD API

1. Create a new FastAPI application.
2. Define a Pydantic model `City` with the following fields:
    - `id`: a unique identifier for the city.
    - `name`: the name of the city.
    - `additional_info`: any additional information about the city.
3. Implement a SQLite database using SQLAlchemy and create a corresponding `City` table.
4. Implement the following endpoints:
    - `POST /cities`: Create a new city.
    - `GET /cities`: Get a list of all cities.
    - **Optional**: `GET /cities/{city_id}`: Get the details of a specific city.
    - **Optional**: `PUT /cities/{city_id}`: Update the details of a specific city.
    - `DELETE /cities/{city_id}`: Delete a specific city.

### Part 2: Temperature API

1. Define a Pydantic model `Temperature` with the following fields:
    - `id`: a unique identifier for the temperature record.
    - `city_id`: a reference to the city.
    - `date_time`: the date and time when the temperature was recorded.
    - `temperature`: the recorded temperature.
2. Create a corresponding `Temperature` table in the database.
3. Implement an endpoint `POST /temperatures/update` that fetches the current temperature for all cities in the database from an online resource of your choice. Store this data in the `Temperature` table. You should use an async function to fetch the temperature data.
4. Implement the following endpoints:
    - `GET /temperatures`: Get a list of all temperature records.
    - `GET /temperatures/?city_id={city_id}`: Get the temperature records for a specific city.

### Additional Requirements

- Use dependency injection where appropriate.
- Organize your project according to the FastAPI project structure guidelines.

## Evaluation Criteria

Your task will be evaluated based on the following criteria:

- Functionality: Your application should meet all the requirements outlined above.
- Code Quality: Your code should be clean, readable, and well-organized.
- Error Handling: Your application should handle potential errors gracefully.
- Documentation: Your code should be well-documented (README.md).

## Deliverables

Please submit the following:

- The complete source code of your application.
- A README file that includes:
    - Instructions on how to run your application.
    - A brief explanation of your design choices.
    - Any assumptions or simplifications you made.

Good luck!

## Running the application

Requires Python 3.10 or newer.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
uvicorn app.main:app --reload
```

The SQLite database (`cities.db`) is created in the current working directory
when the application starts. Interactive API documentation is available at
`http://127.0.0.1:8000/docs`.

## API examples

- `POST /cities` with `{"name": "Kyiv", "additional_info": "Ukraine"}` creates a city.
- `GET /cities` lists cities; `GET /cities/{city_id}` gets one city.
- `PUT /cities/{city_id}` updates supplied city fields.
- `DELETE /cities/{city_id}` deletes the city and its temperature history.
- `POST /temperatures/update` fetches and stores current readings for known cities.
- `GET /temperatures` lists readings; `GET /temperatures?city_id=1` filters by city.

## Design choices and assumptions

SQLAlchemy models define the SQLite tables, while Pydantic schemas validate
requests and serialize responses. FastAPI dependencies provide a database
session per request. City names are unique because temperature lookup uses the
city name for geocoding. Temperature updates use the Open-Meteo geocoding and
forecast APIs, require no API key, and skip cities that cannot be resolved or
whose upstream request fails. The recorded timestamp and temperature come from
the provider's current observation; the temperature is in Celsius. Deleting a
city also deletes its temperature history.
