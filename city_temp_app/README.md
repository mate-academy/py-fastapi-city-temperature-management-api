# City Temperature Manager

A FastAPI application to track cities and their historical temperature data using real-time API integration.

## Setup
1. **Install dependencies**:
   ```bash
   pip install fastapi uvicorn sqlalchemy httpx
2. **Access the API**:
   - Swagger UI: `http://127.0.0.1:8000/docs`

## Design Choices
- **FastAPI & SQLAlchemy**: Used for rapid development and clean database management with SQLite.
- **Asynchronous Fetching**: Implemented `httpx` and `asyncio.gather` for parallel API requests to improve performance.
- **Open-Meteo API**: Chosen for weather data as it does not require an API key for public use.

## Assumptions & Simplifications
- **Geocoding**: The application picks the first result from the geocoding search for any given city name.
- **Errors**: If a city is not found, the temperature is recorded as 0.0.
- **Storage**: SQLite is used as a lightweight database solution for this task.
