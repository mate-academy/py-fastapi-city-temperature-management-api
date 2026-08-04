Cities & Temperature API
FastAPI application for managing city data and tracking their current temperatures using an external weather service.

(a) Instructions to Run
Install dependencies:
Make sure you have Python installed, then run the following command in your terminal to install the required packages:

pip install fastapi uvicorn sqlalchemy httpx

Run the server:
Start the FastAPI application using Uvicorn:

uvicorn main:app --reload

Note: The database tables are created automatically on startup, so no manual database migrations are needed.

Access the API Documentation:
Open your browser and navigate to http://127.0.0.1:8000/docs to test endpoints via the interactive Swagger UI.

(b) Design Choices
Project Structure: Follows FastAPI best practices by using APIRouter to separate endpoints into a routers directory (cities.py and temperatures.py). This modularity ensures the application is scalable and maintainable.

Database Layer: Utilizes SQLite with SQLAlchemy 2.0 modern syntax (Mapped and mapped_column). Database interactions are isolated in a dedicated crud.py file to separate business logic from routing.

Dependency Injection: Depends(get_db) is utilized across all endpoints to ensure safe database session management (automatically opening and closing connections).

Cascade Deletion: Configured cascade="all, delete-orphan" on the City model. If a city is deleted via the API, its associated temperature history is automatically removed to maintain database integrity.

(c) Assumptions & Simplifications
External API Choice: Used the free Open-Meteo API (Geocoding API + Weather Forecast API) for the async temperature update task because it is reliable and requires no API keys or authentication.

Database Migrations: Assumed that a complex migration setup (like Alembic) is not strictly required for this specific task scope, hence the automatic creation on startup.
