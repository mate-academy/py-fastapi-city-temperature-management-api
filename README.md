# City Temperature Management API

A FastAPI app that manages cities and stores a history of their temperatures.
Current temperatures come from [Open-Meteo](https://open-meteo.com/), which is
free and needs no API key.

## How to run

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env               # sets DATABASE_URL (SQLite by default)
uvicorn main:app --reload
```

Open http://127.0.0.1:8000/docs for interactive Swagger docs.
Tables are created automatically on startup.

## Endpoints

| Method | Path                            | Description                                  |
|--------|---------------------------------|----------------------------------------------|
| POST   | `/cities`                       | Create a city                                |
| GET    | `/cities`                       | List cities (`skip`, `limit`)                |
| GET    | `/cities/{city_id}`             | Get one city                                 |
| PUT    | `/cities/{city_id}`             | Update a city (partial updates allowed)      |
| DELETE | `/cities/{city_id}`             | Delete a city and its temperature records    |
| POST   | `/temperatures/update`          | Fetch and store current temperature for all cities |
| GET    | `/temperatures`                 | List temperature records, newest first (`skip`, `limit`) |
| GET    | `/temperatures?city_id={id}`    | Temperature records for one city             |

Example:

```bash
curl -X POST localhost:8000/cities/ -H "Content-Type: application/json" \
     -d '{"name": "Kyiv", "additional_info": "Capital of Ukraine"}'
curl -X POST localhost:8000/temperatures/update
curl "localhost:8000/temperatures/?city_id=1"
```

## Project structure

```
main.py                 # app factory: routers + table creation on startup
dependencies.py         # get_db session dependency (DbSession alias)
database/               # engine, session factory, declarative Base
models/                 # SQLAlchemy models: City, Temperature
schemas/                # Pydantic schemas for requests/responses
cities/                 # city router + CRUD functions
temperatures/           # temperature router, CRUD, async weather client
```

## Design choices

- **Split by feature.** Each app (`cities`, `temperatures`) has its own router
  and CRUD module, following FastAPI's "bigger applications" layout. Models and
  schemas live in shared packages so both apps can use them.
- **Dependency injection.** `get_db` yields one session per request.
  `get_city_or_404` is a dependency too, so the get/update/delete routes share
  the same lookup and 404 handling.
- **Async fetching.** `POST /temperatures/update` uses `httpx.AsyncClient` and
  `asyncio.gather` to query all cities concurrently instead of one by one.
- **Partial failure is OK.** If some cities can't be resolved (typo, network
  error), the others are still saved. The response lists both `updated` and
  `failed` cities. Only if *every* city fails does the endpoint return 502.
- **Error handling.** 404 for unknown cities, 400 for duplicate city names,
  422 for invalid input (Pydantic), 502 when the weather service is unusable.
- **Cascading deletes.** Deleting a city deletes its temperature history.
  SQLite foreign keys are switched on for this.

## Assumptions and simplifications

- City names are unique and are looked up by name in Open-Meteo's geocoding
  API; the first match is used. Ambiguous names (e.g. "Paris" in Texas vs
  France) resolve to the most populated match.
- Temperatures are in °C. `date_time` is the observation time reported by
  Open-Meteo, in UTC.
- Tables are created with `Base.metadata.create_all` on startup instead of
  Alembic migrations, to keep the project small.
- The database layer is synchronous SQLAlchemy (fine for SQLite); only the
  external HTTP calls are async.
- No authentication.

---

<details>
<summary>Original task description</summary>

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

</details>
