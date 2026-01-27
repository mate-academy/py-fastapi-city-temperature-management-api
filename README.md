# City Temperature Tracker API

A FastAPI-based application that manages city data and tracks their historical temperature trends using the Open-Meteo API. This project demonstrates asynchronous database operations with SQLAlchemy and concurrent external API integration.

## Tech Stack
1) Framework: FastAPI
2) Database: SQLAlchemy 2.0 (Async) with SQLite and Alembic
3) Package Manager: uv (Astral)
4) Linting/Formatting: Ruff (PEP 8 compliant)
5) HTTP Client: httpx (Async)

### 🚀 Features

- City Management: Full CRUD (Create, Read, Update, Delete) operations for
  cities.
- Automated Weather Updates: Fetches current weather for all registered cities
  via geocoding and weather APIs.
- Temperature History: View historical temperature data with filtering options.
- Asynchronous Processing: Uses httpx and asyncio for non-blocking API calls.

### 🏗 Project Structure

The project follows a modular "app" structure for scalability:

- src/
- ├── city_app/           # City CRUD logic
- │   ├── models.py       # SQLAlchemy DBCity model
- │   ├── schemas.py      # Pydantic City schemas
- │   ├── crud.py         # DB operations for cities
- │   └── router.py       # API endpoints for cities
- ├── temperature_app/    # Weather tracking logic
- │   ├── models.py       # SQLAlchemy DBTemperature model
- │   ├── services.py     # External API integration (Open-Meteo)
- │   ├── crud.py         # DB operations for temperatures
- │   └── routers.py      # API endpoints for weather updates
- ├── database.py         # DB Engine and Base class
- └── utils.py            # Shared dependencies (get_db)

main.py >> Entry point and router inclusion

# 🛠 Setup & Installation

### Clone the repository

```sh
    git clone <your-repo-url>
    cd city-temperature-tracker
```

### Create and activate virtual environment

```sh
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Install dependencies

```sh
    pip install fastapi[standard] uvicorn sqlalchemy aiolite httpx pydantic
```

### Running the ApplicationBash

```sh
    uvicorn main:app --reload
```

The API will be available at http://127.0.0.1:8000.You can access the
interactive Swagger documentation at http://127.0.0.1:8000/docs

# API EndpointsCity

| Endpoint                | Method   | Description                                    |
|:------------------------|:---------|:-----------------------------------------------|
| `/cities/`              | `POST`   | Create a new city                              |
| `/cities/`              | `GET`    | List all cities                                |
| `/cities/{id}/`         | `GET`    | Get details of a specific city                 |
| `/cities/{id}/`         | `PUT`    | Update city info                               |
| `/cities/{id}/`         | `DELETE` | Remove a cityTemperature                       |
| Endpoint                | Method   | Description                                    |
| `/temperatures/update/` | `POST`   | Triggers a global sync of current temperatures |
| `/temperatures/`        | `GET`    | Get all records (Optional: ?city_id=X)         |
 



  

# 💡Design Choices & Assumptions
1. Open-Meteo API: Chosen because it requires no API key for development. Since Open-Meteo requires latitude/longitude, a Geocoding step was implemented in services.py to translate city names into coordinates automatically.
2. Concurrency: In update_cities_temperature, I used asyncio.gather. This allows the application to fire off all network requests simultaneously rather than waiting for each city one-by-one, significantly improving performance.
3. Database: Used SQLite with SQLAlchemy 2.0 syntax. I utilized AsyncSession to ensure the application remains non-blocking during I/O operations.
4. Error Handling: Implemented custom exception helpers to ensure 404s and 400s are returned with clear messages if a city is missing or an API call fails.