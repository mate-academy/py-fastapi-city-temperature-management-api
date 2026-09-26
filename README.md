# City Temperature Management API

A FastAPI application that manages cities and their temperature history. It exposes:

- A CRUD API for cities (SQLite via SQLAlchemy, async).
- A temperature API that fetches the current temperature for every stored city from an online
  service, persists each reading, and lets you browse the full history.

## Tech stack

- Python 3.13
- FastAPI
- SQLAlchemy 2.0 (async) + `aiosqlite` driver
- Pydantic v2
- `httpx` (async HTTP client)
- [wttr.in](https://wttr.in) as the external weather source

## Project structure

```
.
├── main.py               # FastAPI app, lifespan, router registration
├── database.py           # async engine, Base, session factory, table creation
├── dependencies.py       # get_session dependency (DI)
├── requirements.txt
├── city/
│   ├── models.py         # SQLAlchemy City model
│   ├── schemas.py        # Pydantic schemas
│   ├── crud.py           # DB operations
│   └── router.py         # HTTP endpoints
└── temperature/
    ├── models.py         # SQLAlchemy Temperature model
    ├── schemas.py        # Pydantic schemas
    ├── crud.py           # DB operations
    ├── utils.py          # async wttr.in client
    └── router.py         # HTTP endpoints
```

## Installation

```bash
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

## Running

```bash
uvicorn main:app --reload
```

The database file (`database.db`) and its tables are created automatically on startup.
Interactive docs: http://127.0.0.1:8000/docs

## Endpoints

### Cities

| Method | Path                | Description                       | Success | Errors |
|--------|---------------------|-----------------------------------|---------|--------|
| POST   | `/cities`           | Create a city                     | 201     | 422    |
| GET    | `/cities`           | List all cities                   | 200     |        |
| GET    | `/cities/{city_id}` | Get a single city                 | 200     | 404    |
| DELETE | `/cities/{city_id}` | Delete a city                     | 204     | 404    |

### Temperatures

| Method | Path                          | Description                                          | Success | Errors |
|--------|-------------------------------|------------------------------------------------------|---------|--------|
| POST   | `/temperatures/update`        | Fetch the current temperature for all cities and save | 201   |        |
| GET    | `/temperatures`               | List all temperature records                         | 200     |        |
| GET    | `/temperatures?city_id={id}`  | List temperature records for one city                | 200     |        |

## Design choices

- **Feature-first layout.** Each domain (`city`, `temperature`) owns its models, schemas, CRUD and
  router. Shared infrastructure (database, session dependency) lives in the project root.
- **Layered flow.** `router` handles HTTP concerns and validation, `crud` handles persistence,
  `schemas` define the API contract, `models` define the database tables. Routers never build SQL
  themselves — they call `crud`.
- **Full async.** `create_async_engine` + `AsyncSession` are used so that both database access and
  the weather HTTP request are non-blocking. The exact requirement of the task (an async function
  to fetch temperature data) is implemented in `temperature/utils.py`.
- **Dependency injection.** `get_session` yields one `AsyncSession` per request and always closes
  it, and is wired into endpoints with `Depends`.
- **Table creation on startup.** A `lifespan` handler calls `Base.metadata.create_all`, which is the
  modern replacement for the deprecated `@app.on_event("startup")`.
- **External data source.** `wttr.in` was chosen because it needs no API key and accepts a city
  name directly (`https://wttr.in/Kyiv?format=j1`), avoiding a separate geocoding step.

## Assumptions and simplifications

- A city is looked up in the weather service by its `name` only (no geocoding or coordinates).
- `date_time` is the server's UTC time at the moment of the fetch, not a timestamp returned by the
  weather service.
- There is no authentication and no pagination.
- SQLite foreign keys are not enforced/cascaded, so deleting a city does not remove its temperature
  history.
- `PUT /cities/{city_id}` (marked optional in the task) is not implemented.
- `POST /temperatures/update` fetches cities sequentially. If a single weather request fails, the
  whole update request fails.

## Usage examples

```bash
# Create a city
curl -X POST http://127.0.0.1:8000/cities \
  -H "Content-Type: application/json" \
  -d '{"name": "Kyiv", "additional_info": "capital"}'

# List cities
curl http://127.0.0.1:8000/cities

# Fetch and store the current temperature for all cities
curl -X POST http://127.0.0.1:8000/temperatures/update

# Temperature history
curl http://127.0.0.1:8000/temperatures
curl "http://127.0.0.1:8000/temperatures?city_id=1"
```

## Original task

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
