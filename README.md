# Async City & Temperature API

FastAPI project for managing cities and temperature history. Fully asynchronous and using the real [WeatherAPI](https://www.weatherapi.com/).

## Structure

```
app/
├── main.py
├── database.py
├── core/config.py
├── city/          # CRUD for cities
├── temperature/   # Temperature + API integration
└── __init__.py
.env               # secrets (WEATHER_API_KEY)
```

## Installation

```bash
git clone <repo-url>
cd <project>
python -m venv .venv
# Linux / Mac
source .venv/bin/activate
# Windows
.venv\Scripts\activate
pip install -r requirements.txt
```

## Configuration

Create a `.env` file:

```env
WEATHER_API_KEY=your_weatherapi_key
```

## Running the Application

After activating the virtual environment and installing dependencies, run:

```bash
uvicorn app.main:app --reload
```

This will start the FastAPI server at `http://127.0.0.1:8000`. The `--reload` flag enables automatic reload on code changes for development purposes.

## Endpoints

### Cities

* `POST /cities` — add a city
* `GET /cities` — list all cities
* `DELETE /cities/{city_id}` — delete a city

### Temperatures

* `POST /temperatures/update` — update temperatures for all cities
* `GET /temperatures` — get all temperature records
* `GET /temperatures?city_id={id}` — get temperature history for a specific city

## Design Choices

* **Async-first approach**: All API calls and database interactions are asynchronous to prevent blocking and improve performance.
* **FastAPI + Uvicorn**: Modern, lightweight ASGI framework and server for async capabilities.
* **SQLAlchemy Async + SQLite**: Simple async ORM integration for demonstration and local storage. Can be replaced with PostgreSQL for production.
* **WeatherAPI integration**: Fetches real-time temperature data for cities.
* **Lifespan event handlers**: Used instead of deprecated `on_event` for startup/shutdown database setup.
* **Environment variables**: API keys and sensitive data are stored in `.env` to avoid hardcoding.

## Assumptions

* City names provided by users are valid and recognizable by WeatherAPI. Invalid city names will result in HTTP 400 errors.
* SQLite is sufficient for development/testing purposes; production usage would require a more robust database.
* Timezone-aware datetimes are used for temperature records (UTC) to maintain consistency.
* Users will run the server in a terminal where `.env` can be loaded using `python-dotenv`.
* No authentication or user management is implemented; API is open for demonstration purposes.

## Features

* Fully asynchronous (`asyncio`, `httpx`, `SQLAlchemy Async`)
* Real WeatherAPI integration
* Lifespan used instead of deprecated `on_event`
* SQLite for simplicity
* `.env` for storing API keys
