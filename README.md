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

## How to Run

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
uvicorn main:app --reload
```

The API is available at `http://127.0.0.1:8000`, interactive docs (Swagger) at
`http://127.0.0.1:8000/docs`. The SQLite database (`city_temperature.db`) and
its tables are created automatically on first startup.

## Design Choices

- **Project layout**: `database.py` (engine/session), `models.py` (SQLAlchemy
  ORM), `schemas.py` (Pydantic request/response models), `crud.py`
  (data-access layer), `external.py` (third-party weather API client),
  `main.py` (FastAPI app and routes) — separates persistence, validation and
  HTTP concerns.
- **Weather source**: [Open-Meteo](https://open-meteo.com/) — free, requires
  no API key. A city name is resolved to coordinates via its geocoding API,
  then the forecast API is queried for `current_weather`.
- **Concurrency**: `POST /temperatures/update` fetches every city's
  temperature concurrently with `asyncio.gather`, through a single shared
  `httpx.AsyncClient` injected as a FastAPI dependency, instead of awaiting
  each city's HTTP round trip one at a time.
- **`GET /temperatures/?city_id=...`** is implemented as an optional query
  parameter on `GET /temperatures`, not a separate route, mirroring how
  optional filters are conventionally expressed in FastAPI/REST APIs.
- **Data integrity**: `City.name` is unique; creating or renaming a city to a
  name that already exists returns `400` instead of a raw database error.
  `Temperature` rows cascade-delete with their city (`cascade="all,
  delete-orphan"`) so deleting a city can never leave orphaned temperature
  records.

## Assumptions and Simplifications

- One `Temperature` reading is stored per city per call to
  `POST /temperatures/update` (the endpoint is meant to be invoked
  periodically, e.g. by a scheduler, rather than polling internally).
- If a city's name can't be geocoded, or the weather API call fails, that
  city is skipped for that update cycle rather than failing the whole
  request (`asyncio.gather(..., return_exceptions=True)`).
- No authentication is implemented — out of scope per the task description.
