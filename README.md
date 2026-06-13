Markdown

# City Weather Management API

This is a professional FastAPI application designed to manage city records and track their real-time temperature historical data using asynchronous external API integration.

## Tech Stack

- **FastAPI** (High-performance Python web framework)
- **SQLAlchemy ORM** (Database toolkit and Object-Relational Mapper)
- **SQLite** (Lightweight, file-based SQL database)
- **Pydantic v2** (Data validation and settings management)
- **HTTPX** (Fully featured async HTTP client for Python)
- **Open-Meteo API** (Free, registration-free external weather data provider)

## Installation & Setup

Follow these steps to set up and run the application locally on your machine:

1. **Navigate to the Project Directory:**
   ```bash
   cd py-fastapi-city-temperature-management-api
2. **Set up a Virtual Environment:**
    python -m venv .venv
3. **Activate the Virtual Environment:**
    Windows:
    .venv\Scripts\activate
    macOS/Linux:
    source .venv/bin/activate
4. **Install Dependencies:**
    pip install -r requirements.txt
5. **Run the Application Server:**
    uvicorn app.main:app --reload
6. **Access Interactive API Documentation:**
    Open your browser and navigate to: http://127.0.0.1:8000/docs (Swagger UI).

## Architectural & Design Decisions
1. Modular Directory Structure: The project is strictly separated into independent domain          components: cities and temperatures. Each module encapsulates its own routes, schemas, models, and database logic (crud.py). This guarantees scalability and high maintainability.
2. Database Integrity & Cascades:
The City and Temperature database tables share a standard One-to-Many relationship. A strict foreign key constraint with ondelete="CASCADE" is implemented on the temperatures table. Therefore, if a city is deleted, its entire temperature log history is automatically wiped out, eliminating orphaned data.
3. Asynchronous Non-blocking Operations:
The POST /temperatures/update endpoint is designed as an asynchronous route (async def). It utilizes httpx.AsyncClient to securely fetch geolocation coordinates and actual weather stats from Open-Meteo sequentially without blocking the event loop or other API requests.

## Assumptions & Simplifications
    Name-Based Geocoding: It is assumed that the name provided when creating a city matches a recognizable global location (e.g., "Kyiv", "London", "New York") in English, so the automated geocoder can dynamically retrieve proper GPS coordinates.

    Strict Adherence to Schemas: Following the rigid assignment schema properties, the temperature history output tracks specific reference identifiers via city_id (integer) instead of joining plain text location strings directly into the default layout response.

    Timezone Standardization: All captured historical measurements are saved using standard UTC    timestamps (datetime.utcnow) to enforce consistency across different regional locations.