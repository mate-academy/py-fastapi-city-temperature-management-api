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

## Solution

A REST API built with FastAPI, SQLAlchemy 2 and SQLite for managing cities
and their temperature history. Current temperatures are fetched asynchronously
from the free [Open-Meteo](https://open-meteo.com/) API (no API key needed).

### How to run

1. Clone the repository.
2. Create and activate a virtual environment (Python 3.11+):

```bash
python -m venv .venv
source .venv/bin/activate        # Linux/macOS
.venv\Scripts\activate           # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Apply database migrations (creates `db.sqlite3`):

```bash
alembic upgrade head
```

5. Start the application:

```bash
uvicorn main:app --reload
```

6. Open the Swagger documentation: http://127.0.0.1:8000/docs

Settings can be overridden with environment variables or a `.env` file:

| Variable              | Default                  | Description                          |
|-----------------------|--------------------------|--------------------------------------|
| `DATABASE_URL`        | `sqlite:///./db.sqlite3` | Database used by the app and Alembic |
| `WEATHER_API_TIMEOUT` | `10.0`                   | Open-Meteo request timeout, seconds  |

### Endpoints

| Method   | Path                         | Description                                        |
|----------|------------------------------|----------------------------------------------------|
| `POST`   | `/cities`                    | Create a city                                      |
| `GET`    | `/cities`                    | List all cities                                    |
| `GET`    | `/cities/{city_id}`          | Get a city                                         |
| `PUT`    | `/cities/{city_id}`          | Update a city                                      |
| `DELETE` | `/cities/{city_id}`          | Delete a city (and its temperature records)        |
| `POST`   | `/temperatures/update`       | Fetch current temperatures for all cities and save |
| `GET`    | `/temperatures`              | List all temperature records                       |
| `GET`    | `/temperatures?city_id={id}` | List temperature records of one city               |

`POST /temperatures/update` returns the created records and the names of
the cities whose temperature could not be fetched:

```json
{
  "updated": [
    {"city_id": 1, "temperature": 7.5, "id": 1, "date_time": "2026-11-03T07:27:30.418440"}
  ],
  "failed_cities": ["Qwertyzxcvbnm"]
}
```

### Project structure and design choices

```
city/            # app 1: City CRUD
temperature/     # app 2: temperature fetching and history
  models.py      # SQLAlchemy ORM models
  schemas.py     # Pydantic models for requests and responses
  crud.py        # database operations
  router.py      # API endpoints
  utils.py       # async requests to Open-Meteo (temperature app only)
alembic/         # database migrations
database.py      # engine, session factory, declarative Base
dependencies.py  # get_db and get_http_client dependencies
settings.py      # application settings (pydantic-settings)
main.py          # FastAPI app, includes both routers
```

- The two parts of the task are two separate apps (packages), each with its
  own models, schemas, CRUD functions and router.
- Dependency injection is used for the database session (`get_db`), the
  shared `httpx.AsyncClient` (`get_http_client`) and for loading a city or
  returning 404 (`get_city_or_404`).
- Temperatures for all cities are fetched concurrently with
  `asyncio.gather` through one shared `httpx.AsyncClient`. For each city
  the coordinates are found with the Open-Meteo Geocoding API, then the
  current temperature is requested from the Forecast API.
- A city has a one-to-many relationship with its temperature records;
  deleting a city deletes its records as well.
- The schema is managed with Alembic, which reads the database URL from the
  same settings as the application.

### Error handling

- `404 Not Found` for a missing city (also for `GET /temperatures?city_id=`
  with an unknown city).
- `400 Bad Request` when creating or renaming a city to a name that
  already exists.
- `422 Unprocessable Entity` for invalid input (e.g. an empty name).
- If the temperature of a city cannot be fetched (city not found by the
  geocoding API, network error, timeout, unexpected response), the city is
  listed in `failed_cities`, a warning is logged, and the other cities are
  still updated.

### Assumptions and simplifications

- SQLite is used for simplicity; the database layer is synchronous.
- City names are unique, because the temperature is looked up by name.
  The first geocoding result for the name is used.
- Temperatures are in °C. `date_time` is the time the record was saved,
  stored in UTC.
- Every update creates new records, so the full history is kept.
