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


---

# Weather API

FastAPI application that manages cities and stores their temperature history.
Temperatures are fetched from the Open-Meteo API.

## How to run

1. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   venv\Scripts\activate        # Linux/Mac: source venv/bin/activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Start the server from the project root:

   ```bash
   uvicorn app.main:app --reload
   ```

4. Open the interactive docs: http://127.0.0.1:8000/docs

The SQLite database file `weather.db` is created automatically on first start.

## Endpoints

### Cities
- `POST /cities` create a city
- `GET /cities` list cities
- `GET /cities/{city_id}` get one city
- `PUT /cities/{city_id}` update a city
- `DELETE /cities/{city_id}` delete a city (its temperature records are deleted too)

### Temperatures
- `POST /temperatures/update` fetch current temperature for all cities and store it
- `GET /temperatures` list all temperature records
- `GET /temperatures?city_id={city_id}` list records of one city

## Project structure

```
app/
├── main.py          application entry point
├── database.py      engine, session, get_db dependency
├── city/            models, schemas, crud, router for cities
└── temperature/     models, schemas, crud, router, service for temperatures
```

## Design choices

- The project is split by domain (`city`, `temperature`), each with the same
  layers: models, schemas, crud, router. This keeps related code together.
- Database access is isolated in `crud.py`; routers only handle HTTP.
- Database sessions are provided through FastAPI dependency injection (`get_db`).
- Open-Meteo is used because it is free and needs no API key. It works with
  coordinates, so each city is first resolved through its geocoding API.
- Temperatures are fetched with `httpx.AsyncClient` and `asyncio.gather`,
  so all cities are requested concurrently.
- `service.py` only talks to the external API and does not touch the database.
- City names are unique; duplicates return 400, missing cities return 404.
- A failure for one city (not found, network error) does not break the update
  for the other cities.

## Assumptions and simplifications

- Database work is synchronous (SQLAlchemy); only the external requests are async.
- Tables are created with `create_all`, no migrations (Alembic) are used.
- Times are stored in UTC without timezone info.
- Temperature is in degrees Celsius.
- City names are expected in English, because the geocoder finds them best.
- Cities that cannot be found by the geocoder are skipped during the update.
- Every call to `POST /temperatures/update` adds new records (history is kept).
