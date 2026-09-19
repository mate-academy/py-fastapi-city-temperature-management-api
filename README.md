# City Data & Temperature Management API

A production-ready FastAPI application designed to manage city records and track their historical temperature data using asynchronous requests to the external Open-Meteo API.

---

## Features
- **City CRUD API**: Create, read, update, and delete operations for city entities.
- **Asynchronous Temperature Fetching**: A non-blocking service that looks up city coordinates via geolocation and records the current live temperature in the database.
- **Unified Filtration & Pagination**: Built-in support for paginated temperature reports filterable by specific cities.
- **Automatic Cascades**: Automatic deletion of corresponding temperature logs when a city is removed to ensure database integrity.

---

## Installation & Setup

1. **Clone the project directory** and navigate to its root:
   ```bash
   cd city_weather_app
   ```

2. **Install all required dependencies** using `pip`:
   ```bash
   pip install fastapi uvicorn sqlalchemy httpx
   ```

3. **Start the local development server** via Uvicorn:
   ```bash
   uvicorn main:app --reload
   ```

4. **Access the Interactive API Documentation**:
   Open your browser and head to [http://127.0.0](http://127.0.0) to explore the system via the interactive Swagger UI.

---

## Design Choices & Architecture

- **Clean Project Structure**: The project is split into isolated domains (`models.py`, `schemas.py`, `crud.py`, `main.py`) separating the data representation, request validation, database operations, and application routing to follow clean-code guidelines.
- **Asynchronous HTTP Client (`httpx`)**: Fetching temperature records from an external service can introduce latency. The `/temperatures/update` endpoint relies entirely on an async execution context using `httpx.AsyncClient` to keep the application responsive during API calls.
- **External Data Source**: Open-Meteo API was chosen because it provides a highly reliable, free, and completely keyless global forecast service that aligns well with prototyping needs.
- **Data Safety & Constraints**: The city entity enforces a unique constraint on the `name` column, preventing duplicates. Database schemas utilize strict `ForeignKey` constraints with cascading options (`cascade="all, delete-orphan"`), preventing orphan entries when a city is wiped from the database.

---

## Assumptions & Simplifications

1. **Two-Step Geocoding Pipeline**: Since the database stores only the basic string literal name of a city, the application must perform a two-step lookup per city inside the update script:
   - *Step A:* Resolve the city name into `latitude` and `longitude` coordinates using the Open-Meteo Geocoding engine.
   - *Step B:* Query the exact current temperature of those exact coordinates.
2. **Graceful Fault Tolerance**: If a city name cannot be resolved by the geocoding service (e.g., if typos were inserted into the name field during creation) or if the internet connection drops momentarily, the update function will silently log or skip the specific city record, continuing its workflow for the remaining data pool.
3. **Local Database Configuration**: SQLite is selected for simplicity, running off a single local database file (`weather.db`). Table instances are bootstrapped automatically at runtime using SQLAlchemy's metadata mapping layer (`Base.metadata.create_all`).
