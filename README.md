# City Temperature Management API

A FastAPI application that manages city data and collects current temperature
data for those cities from an external weather service.

The project is split into two parts:

1. **City CRUD API** — create, read, update and delete cities.
2. **Temperature API** — fetch the current temperature for every city in the
   database (asynchronously) and store the history of all measurements.

## Features

- Full CRUD for cities.
- Asynchronous fetching of current temperatures for all cities at once.
- Temperature history with filtering by city.
- Interactive documentation at `/docs` (Swagger) and `/redoc`.

## Tech stack

- FastAPI
- SQLAlchemy (SQLite)
- httpx (async HTTP client)
- Uvicorn

## Installation and running

1. Clone the repository:

   ```bash
   git clone <your-repo-url>
   cd py-fastapi-city-temperature-management-api
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate        # on Windows: venv\Scripts\activate
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:

   ```bash
   uvicorn main:app --reload
   ```

5. Open the interactive docs in your browser:

   ```
   http://127.0.0.1:8000/docs
   ```

## Endpoints

### Cities

| Method | Path                 | Description                 |
|--------|----------------------|-----------------------------|
| POST   | `/cities/`           | Create a new city           |
| GET    | `/cities/`           | List all cities             |
| GET    | `/cities/{city_id}`  | Get a single city by id     |
| PUT    | `/cities/{city_id}`  | Update a city               |
| DELETE | `/cities/{city_id}`  | Delete a city               |

### Temperatures

| Method | Path                            | Description                                   |
|--------|---------------------------------|-----------------------------------------------|
| POST   | `/temperatures/update/`         | Fetch and store current temperatures          |
| GET    | `/temperatures/`                | List all temperature records                  |
| GET    | `/temperatures/?city_id={id}`   | List temperature records for a specific city  |

## Typical usage

1. Create a few cities via `POST /cities/` (e.g. London, Kyiv, Paris).
2. Call `POST /temperatures/update/` — the app fetches the current temperature
   for every city and stores it.
3. View the history via `GET /temperatures/`, or filter it by city with
   `GET /temperatures/?city_id=1`.

## Design choices

- **Weather service: Open-Meteo.** Chosen because it is free and requires no
  API key, which keeps setup simple and avoids storing secrets.
- **Name → coordinates → temperature.** Open-Meteo's forecast endpoint works
  with coordinates, not city names. So each update first calls the Open-Meteo
  geocoding endpoint to turn a city name into coordinates, then calls the
  forecast endpoint. This keeps the `City` model limited to the fields required
  by the task (`name`, `additional_info`) — coordinates are not stored.
- **Asynchronous fetching with `asyncio.gather`.** Fetching weather is an
  IO-bound task (most of the time is spent waiting for the network). All cities
  are fetched concurrently, so updating N cities takes roughly the time of the
  slowest request instead of the sum of all of them.
- **Project structure.** The two parts are organised as separate packages
  (`city/` and `temperature/`), each with its own `models`, `schemas`, `crud`
  and `router`. They are wired together in `main.py` via `include_router`.
- **Dependency injection.** Database sessions are provided through FastAPI's
  `Depends(get_db)`, so endpoints never create or close sessions manually.

## Assumptions and simplifications

- **Synchronous database inside an async fetch.** The database layer uses
  synchronous SQLAlchemy with SQLite. Since SQLite queries here are small and
  local, they don't meaningfully block the event loop, so a fully async
  database driver was considered out of scope for this task.
- **Graceful skipping.** If a city cannot be found by the geocoding service, or
  a request fails or times out, that city is simply skipped rather than failing
  the whole update. The other cities are still processed and stored.
- **Timestamp.** `date_time` is recorded as the server's local time at the
  moment the temperature is stored.
