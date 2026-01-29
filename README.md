# City Temperature Tracker API

A FastAPI-based application designed to manage city data and track their corresponding temperature records. It leverages asynchronous operations for efficient external API calls and robust database interactions.

## Tech Stack
1) Framework: FastAPI
2) Database: SQLAlchemy 2.0 (Async) with SQLite and Alembic (for migrations)
3) Package Manager: uv (Astral)
4) HTTP Client: httpx (Async)
5) External Weather API: WeatherAPI.com

### 🚀 Features

-   **City Management:** Full CRUD (Create, Read, Update, Delete) operations for cities, including optional additional information for disambiguation.
-   **Automated Temperature Updates:** Fetches current temperature for all registered cities from an external weather API.
-   **Temperature History:** Provides endpoints to retrieve a list of all temperature records, with filtering options by city.
-   **Asynchronous Processing:** Utilizes `httpx` and `asyncio` for non-blocking external API calls and database operations, enhancing performance.
-   **City Name Refinement:** Automatically refines user-provided city names using the external weather API to ensure consistency and correctness.

### 🏗 Project Structure

The project follows a modular "app" structure for clear separation of concerns and scalability:

- `app/`
    - `city/`           # City CRUD logic
        - `models.py`       # SQLAlchemy ORM model for City
        - `schemas.py`      # Pydantic schemas for City
        - `crud.py`         # Database operations (Create, Read, Update, Delete) for cities
        - `router.py`       # API endpoints for city management
    - `temperature/`    # Temperature tracking logic
        - `models.py`       # SQLAlchemy ORM model for Temperature
        - `schemas.py`      # Pydantic schemas for Temperature
        - `crud.py`         # Database operations (Create, Read, Update) for temperatures
        - `router.py`       # API endpoints for temperature management and updates
    - `services/`       # External API integrations and business logic
        - `city_weather_service.py` # Handles interaction with WeatherAPI.com for city lookup and temperature fetching
    - `__init__.py`
    - `main.py`         # Main FastAPI application entry point, includes all routers

- `core/`           # Core configurations and utilities (e.g., database session, settings)
- `alembic/`        # Alembic migration scripts
- `pyproject.toml`  # Project metadata and dependencies (managed by uv)
- `uv.lock`         # Locked dependencies by uv
- `README.md`       # Project documentation (this file)
- `.env.sample`     # Example environment variables

### 🛠 Setup & Installation

#### Clone the repository

```sh
git clone <your-repo-url>
cd py-fastapi-city-temperature-management-api
```

#### Install dependencies

This project uses `uv` for dependency management, which is highly recommended for its speed and efficiency.

**Using `uv` (Recommended):**
You do not need to create a virtual environment manually. `uv` will create one for you in a `.venv` directory and sync all dependencies from your `pyproject.toml` and `uv.lock`.

```sh
uv sync
```

**Using `pip` (Alternative):**
If you prefer to use `pip`, first create and activate a virtual environment:

```sh
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

Then, install the dependencies from `requirements.txt`:

```sh
pip install -r requirements.txt
```

#### Environment Variables

Create a `.env` file in the project root based on `.env.sample` and fill in the required values (e.g., your WeatherAPI.com key).

```
# .env file
WEATHERAPI_KEY=your_weatherapi_key
WEATHERAPI_URL=http://api.weatherapi.com/v1
DATABASE_URL=sqlite+aiosqlite:///./city-temperature.db
```

#### Run Database Migrations

This project uses Alembic for database migrations. After setting up your environment and before running the application, you need to apply the migrations:

```sh
alembic upgrade head
```

If you make changes to the SQLAlchemy models, you'll need to generate a new migration script:

```sh
alembic revision --autogenerate -m "Your description of the changes"
```

#### Running the Application

Use `uv run` to ensure the application executes within the managed environment.

```sh
uv run uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`. You can access the interactive Swagger documentation at `http://127.0.0.1:8000/docs` (or ReDoc at `http://127.0.0.1:8000/redoc`).

# API Endpoints

## City

| Endpoint                | Method   | Description                                    |
|:------------------------|:---------|:-----------------------------------------------|
| `/cities/`              | `POST`   | Create a new city. Refines name using WeatherAPI.com. |
| `/cities/`              | `GET`    | List all cities.                               |
| `/cities/{city_id}/`    | `GET`    | Get details of a specific city.                |
| `/cities/{city_id}/`    | `PUT`    | Update city information. Refines name if `name` is updated. |
| `/cities/{city_id}/`    | `DELETE` | Remove a city and its associated temperature records. |

## Temperature

| Endpoint                | Method   | Description                                    |
|:------------------------|:---------|:-----------------------------------------------|
| `/temperatures/update/` | `POST`   | Triggers an asynchronous update of current temperatures for all registered cities. |
| `/temperatures/`        | `GET`    | Get all temperature records. Supports optional filtering by `city_id`. |

# 💡 Design Choices & Assumptions

1.  **External Weather API (WeatherAPI.com):** Chosen for its simplicity and direct city name search capabilities. The `FindCityService` refines city names based on its search results.
2.  **Concurrency (`asyncio.gather`):** In `update_cities_temperatures`, `asyncio.gather` is used to concurrently fetch temperature data for multiple cities from WeatherAPI.com, significantly improving performance.
3.  **Asynchronous Database (SQLAlchemy 2.0 & `AsyncSession`):** SQLite with SQLAlchemy 2.0's asynchronous capabilities is used to ensure database operations are non-blocking, maintaining the responsiveness of the FastAPI application.
4.  **Robust Error Handling:** Custom `HTTPException`s are raised for scenarios like city not found (`404`), external API errors (`502`), or service unavailability (`503`), providing clear messages to API consumers.
5.  **City Name Refinement Logic:** The `FindCityService` refines city names using the external API. When `additional_info` is provided, it attempts to find a more specific match (e.g., by country). If `additional_info` is *not* provided, it defaults to the *first* result returned by the external API's search endpoint.
    *   **Implication for Uniqueness:** The `name` field in the database is unique *after* refinement. This means two different user inputs (e.g., "London" and "London, UK") might resolve to the same refined name ("London, United Kingdom") and cause a `409 Conflict` (IntegrityError) if that refined name already exists. Users should be aware of this behavior and utilize `additional_info` for disambiguation when necessary to ensure distinct city entries.
6.  **Optional `additional_info` and Nullability:** The `additional_info` field in the `City` model is now optional at the Pydantic level and nullable at the database level, preventing `IntegrityError` when not provided.
7.  **Temperature Update Pagination:** The `POST /temperatures/update` endpoint uses `skip` and `limit` when fetching the list of cities. This implies that if there are more cities than the `limit`, not all cities will be updated in a single call. To update all cities, the client would need to make repeated calls with adjusted `skip`/`limit` or the implementation should be adjusted to fetch all cities.