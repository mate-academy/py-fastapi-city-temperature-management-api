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

## Project Setup

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
uvicorn app.main:app --reload
```

Open the interactive API docs:

```text
http://127.0.0.1:8000/docs
```

## API Endpoints

### Cities

- `POST /cities` - create a city
- `GET /cities` - list all cities
- `GET /cities/{city_id}` - get one city
- `PUT /cities/{city_id}` - update one city
- `DELETE /cities/{city_id}` - delete one city

Example city payload:

```json
{
  "name": "Kyiv",
  "additional_info": "Capital of Ukraine"
}
```

### Temperatures

- `POST /temperatures/update` - fetch and save current temperatures for all cities
- `GET /temperatures` - list all temperature records
- `GET /temperatures?city_id=1` - list temperature records for a specific city

## Design Notes

- The app uses FastAPI routers to separate city and temperature endpoints.
- SQLite is configured in `app/database.py`.
- SQLAlchemy models are defined in `app/models.py`.
- Pydantic schemas are defined in `app/schemas.py`.
- Weather fetching is isolated in `app/services/weather.py`.
- Database tables are created automatically on application startup with `Base.metadata.create_all`.

## Weather API

The project uses Open-Meteo because it does not require an API key:

- Geocoding API: `https://geocoding-api.open-meteo.com/v1/search`
- Forecast API: `https://api.open-meteo.com/v1/forecast`

For each city, the application first resolves coordinates by city name, then requests the current `temperature_2m` value and stores it in the `temperatures` table.

## Assumptions

- City names should be recognizable by the Open-Meteo geocoding API.
- If one city cannot be resolved or fetched, the update endpoint records an error for that city and continues with the others.
- If no city can be updated, the endpoint returns `502 Bad Gateway`.
- The local SQLite database file `city_temperature.db` is ignored by git and recreated automatically when the app starts.
