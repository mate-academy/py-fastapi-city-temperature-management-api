# City Temperature Management API

A REST API built with **FastAPI**, **SQLAlchemy**, and **SQLite** for managing cities and tracking their temperature history. The application provides CRUD operations for cities and allows users to fetch and store current temperatures for all cities in the database.

## Features

### City Management

- Create a new city.
- Retrieve a list of all cities.
- Retrieve a specific city by ID.
- Delete a city.

### Temperature Management

- Fetch current temperatures for all cities from an external weather API.
- Store temperature records in the database with timestamps.
- Retrieve all temperature records.
- Filter temperature history by city ID.
- Use asynchronous functions to fetch weather data.

## Technologies

- **Python** — programming language.
- **FastAPI** — web framework for building REST APIs.
- **SQLAlchemy** — ORM for database operations.
- **SQLite** — database for storing cities and temperature records.
- **Pydantic** — request validation and response serialization.
- **Alembic** — database migrations.
- **httpx** — asynchronous HTTP requests to the external weather API.
- **Uvicorn** — ASGI server.

## Installation and Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd <project-directory>
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
```

On Windows:

```powershell
.venv\Scripts\activate
```

On macOS or Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
DATABASE_URL=sqlite+aiosqlite:///./db.sqlite3
API_KEY=your_weather_api_key
```

Replace `your_weather_api_key` with a valid API key from the weather provider used by the application.

Keep `.env` out of version control. Do not commit real API keys or other secrets.

### 5. Apply database migrations

If the project uses Alembic:

```bash
alembic upgrade head
```

If migrations have not been created yet, generate the initial migration and apply it:

```bash
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

### 6. Run the application

```bash
uvicorn main:app --reload
```

The API will be available at:

`http://127.0.0.1:8000`

## API Documentation

FastAPI automatically generates interactive API documentation.

- **Swagger UI:** `http://127.0.0.1:8000/docs`
- **ReDoc:** `http://127.0.0.1:8000/redoc`

Use these interfaces to explore endpoints and send requests.

## API Endpoints

### Cities

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/cities` | Create a city |
| `GET` | `/cities` | Retrieve all cities |
| `GET` | `/cities/{city_id}` | Retrieve a city by ID |
| `DELETE` | `/cities/{city_id}` | Delete a city |

Example request to create a city:

```json
{
  "name": "London",
  "additional_info": "Capital of the United Kingdom"
}
```

### Temperatures

| Method | Endpoint                   | Description |
|---|----------------------------|---|
| `POST` | `/temperatures/update/`    | Fetch and store current temperatures for all cities |
| `GET` | `/temperatures`            | Retrieve all temperature records |
| `GET` | `/temperatures/?city_id=1` | Retrieve temperature records for a specific city |

Example temperature record:

```json
{
    "temperature": 20,
    "date_time": "2026-10-20T23:42:29",
    "id": 1,
    "city": {
      "name": "city",
      "additional_info": "none",
      "id": 1
    }
  }
```

The temperature value and timestamp above are illustrative.

## Usage Example

### 1. Create a city

Send a `POST` request to `/cities`:

```json
{
  "name": "Paris",
  "additional_info": "Capital of France"
}
```

### 2. Retrieve temperature history

Send a `GET` request to `/temperatures` to retrieve all stored records.

To retrieve records for a specific city, use:

```text
GET /temperatures?city_id=1
```

Each update adds new records rather than overwriting previous measurements, preserving the temperature history.

## Design Choices

- **Separation of concerns:** City and temperature functionality are organized into separate modules.
- **SQLAlchemy ORM:** Database tables and relationships are represented as Python models.
- **Pydantic schemas:** Input data is validated and output data is serialized using dedicated schemas.
- **Dependency injection:** FastAPI dependencies provide database sessions to endpoint handlers.
- **Asynchronous operations:** Async SQLAlchemy sessions and asynchronous HTTP requests help avoid blocking during I/O operations.
- **SQLite:** A lightweight database suitable for a small application and local development.
- **Database migrations:** Alembic manages schema changes and keeps the database structure consistent.
- **Temperature history:** Every successful update creates a new record associated with its city.

## Assumptions and Simplifications

- Each city is identified by a unique database ID.
- Temperature records reference cities through `city_id`.
- The external weather provider returns the current temperature for a requested city.
- The API key is supplied through an environment variable rather than hardcoded in the source code.
- SQLite is used for simplicity and local development.
- Historical temperature records are retained until explicitly deleted or the database is reset.

## License

This project was created for educational purposes.
