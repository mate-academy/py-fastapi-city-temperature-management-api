# City Temperature Management API

A FastAPI-based application for managing city data and tracking their current temperatures using an external weather service.

## Features

- **City Management**: Full CRUD operations for cities (Create, Read, Update, Delete).
- **Temperature Tracking**: Fetch current temperatures for all cities from WeatherAPI and update the database.
- **Asynchronous Operations**: Uses `SQLAlchemy` with `aiosqlite` for asynchronous database interactions.
- **External Integration**: Connects with [WeatherAPI.com](https://www.weatherapi.com/) to retrieve current weather data.

## Requirements

- Python 3.10+
- [WeatherAPI.com](https://www.weatherapi.com/) API Key

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd py-fastapi-city-temperature-management-api
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables:**
   Create a `.env` file in the root directory and add your WeatherAPI key:
   ```env
   WEATHER_API_KEY=your_api_key_here
   ```
   (You can use `.sample.env` as a template if it exists).

## Database Setup

This project uses Alembic for database migrations. To initialize the SQLite database and apply migrations, run:

```bash
alembic upgrade head
```

## Running the Application

Start the FastAPI server

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.
You can access the interactive API documentation (Swagger UI) at `http://127.0.0.1:8000/docs`.

## Design Choices

1. **FastAPI & Pydantic**: Leveraged for high performance, automatic documentation, and robust data validation.
2. **Asynchronous Database Access**: Used `SQLAlchemy`'s `AsyncSession` with `aiosqlite` to ensure the application remains responsive during I/O-bound database operations.
3. **Modular Structure**: The project is organized into `city` and `temperature` modules, each with its own models, schemas, and CRUD logic, promoting maintainability.
4. **Dependency Injection**: Used for database session management and pagination parameters, making the code cleaner and easier to test.
5. **External Service Integration**: Encapsulated WeatherAPI logic in `integrations/weatherapi.py` to decouple external dependencies from the core business logic.

## Notes

The original task description mentioned an optional `PUT` endpoint for updates. In this implementation, `PATCH` was used instead, since the update operation is partial rather than a full resource replacement. While this slightly deviates from the wording of the requirement, `PATCH` is a reasonable and semantically appropriate choice for this project.