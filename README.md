# City Temperature Management API

A FastAPI application that manages cities and stores their temperature history.
Current temperatures are fetched from [Open-Meteo](https://open-meteo.com) (free, no API key).

## How to run

Requires Python 3.9+.

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.sample .env        # optional, defaults work out of the box
uvicorn app.main:app --reload
```

Open the interactive docs at http://127.0.0.1:8000/docs.
The SQLite database (`city_temperature.db`) and its tables are created on startup.

Run the tests (the weather API is mocked, no network needed):

```bash
pytest
```

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/cities` | Create a city |
| `GET` | `/cities` | List cities (`skip`, `limit`) |
| `GET` | `/cities/{city_id}` | Get one city |
| `PUT` | `/cities/{city_id}` | Update a city (partial: only sent fields change) |
| `DELETE` | `/cities/{city_id}` | Delete a city and its temperature records |
| `POST` | `/temperatures/update` | Fetch and store the current temperature of every city |
| `GET` | `/temperatures/` | List temperature records, newest first (`skip`, `limit`) |
| `GET` | `/temperatures/?city_id={city_id}` | Temperature records of one city |

Example:

```bash
curl -X POST localhost:8000/cities -H "Content-Type: application/json" \
     -d '{"name": "Kyiv", "additional_info": "Capital of Ukraine"}'
curl -X POST localhost:8000/temperatures/update
curl "localhost:8000/temperatures/?city_id=1"
```

## Project structure

```
app/
├── main.py            # app creation, router registration, startup (create tables)
├── config.py          # settings (pydantic-settings, read from env / .env)
├── database.py        # async engine, session factory, declarative Base
├── dependencies.py    # shared dependencies: DB session, HTTP client
├── city/              # City app: models, schemas, crud, router
└── temperature/       # Temperature app: models, schemas, crud, router
    └── weather.py     # async Open-Meteo client
tests/                 # pytest tests with in-memory DB and mocked weather API
```

## Design choices

- **Per-feature packages.** Each app (`city`, `temperature`) has its own SQLAlchemy models,
  Pydantic schemas, CRUD functions and router, following the FastAPI "bigger applications" layout.
- **Fully async.** SQLAlchemy 2.0 async with `aiosqlite` for the DB and `httpx.AsyncClient`
  for the weather API, so the event loop is never blocked.
- **Dependency injection.** The DB session (`get_db`), the HTTP client (`get_http_client`)
  and the "city or 404" lookup (`get_city_or_404`) are FastAPI dependencies, which also
  lets the tests replace the DB and the weather API.
- **Concurrent fetching.** `POST /temperatures/update` requests all cities at once with
  `asyncio.gather`. A failure for one city (unknown name, timeout, bad response) does not
  stop the others: the response lists `updated` records and `failed` cities with a reason.
- **Error handling.** 404 for missing cities, 409 for duplicate city names, 422 for invalid
  input (FastAPI/Pydantic validation). Weather service errors are wrapped in `WeatherServiceError`.
- **Cascade delete.** Deleting a city removes its temperatures (`ON DELETE CASCADE`,
  with SQLite foreign keys turned on).

## Assumptions and simplifications

- City names are unique; the city name is what we look up in Open-Meteo geocoding,
  and the first match is used. Adding a country to `name` is not supported, so
  ambiguous names (e.g. "Paris") resolve to whatever Open-Meteo ranks first (usually the most populous place).
- Temperatures are in °C. `date_time` is the time of measurement reported by
  Open-Meteo, stored and returned in UTC.
- Tables are created with `Base.metadata.create_all` on startup instead of Alembic
  migrations to keep the project small.
- List endpoints are paginated with `skip`/`limit` (default 100).
- No authentication.

---

## Original Task Description

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
