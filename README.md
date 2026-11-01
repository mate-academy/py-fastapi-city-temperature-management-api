# City Temperature Management API

A learning project built with FastAPI to manage cities and store their temperature history.

## Technologies

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- HTTPX
- Open-Meteo API

## Setup and Run

1. Clone the repository and navigate to the project directory.
2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Start the application:

   ```bash
   uvicorn app.main:app --reload
   ```

5. Open the API documentation at `http://127.0.0.1:8000/docs`.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/cities/` | Create a city |
| GET | `/cities/` | Get all cities |
| GET | `/cities/{city_id}` | Get a city by ID |
| DELETE | `/cities/{city_id}` | Delete a city |
| POST | `/temperatures/update` | Fetch and store current temperatures |
| GET | `/temperatures/` | Get temperature history |
| GET | `/temperatures/?city_id={city_id}` | Filter temperature history by city |

## Design Choices

- SQLAlchemy is used for database operations, with SQLite for storage.
- Pydantic schemas validate input and serialize API responses.
- FastAPI dependency injection provides database sessions to endpoints.
- Open-Meteo provides city coordinates and current temperature data.
- HTTPX and `asyncio.gather()` allow temperature requests for multiple cities to run concurrently.

## Assumptions and Simplifications

- City update (`PUT`) is omitted because it is optional in the assignment.
- Each temperature update creates a new historical record.
- If fetching temperature data fails for a city, the update operation returns an error rather than saving a partial batch.
- The SQLite database is created automatically when the application starts.
