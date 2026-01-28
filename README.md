# City Temperature Management API
This API manages a list of cities and automatically fetches current weather data using the Open-Meteo service.

## How to Run the Application
### 1. Environment Setup
````
# Create a virtual environment
python -m venv .venv

# Activate the environment (Windows)
.venv\Scripts\activate
# Activate the environment (Mac/Linux)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
````
### 2. Database Migrations
The project uses SQLite and Alembic for database schema management.

````
# Run migrations to create tables
alembic upgrade head
````
3. Start the Server
````
uvicorn main:app --reload
````
The API documentation (Swagger UI) will be available at: http://127.0.0.1:8000/docs

## Design Choices
- Modular Architecture: The project is divided into two main modules: cities and temperatures. Each module contains its own models, schemas, and routing logic to ensure maintainability and separation of concerns.

- Asynchronous Implementation: The application utilizes SQLAlchemy (AsyncSession) and httpx for non-blocking I/O operations. This ensures the server remains responsive while waiting for database or external API responses.

- Pydantic V2: Data validation and serialization are handled by Pydantic, ensuring strict type checking and consistent API responses.

- Relational Mapping: A One-to-Many relationship is established between cities and temperature records. Cascading deletes (all, delete-orphan) are implemented to ensure data integrity when a city is removed.

## Assumptions and Simplifications
- Open-Meteo API: This service was chosen because it does not require an API key, simplifying the initial setup and testing process.

- Database: SQLite is used as the database engine to eliminate the need for external database server configuration while providing full relational functionality.

- Timestamping: Temperature records use the server's local time (datetime.now) for storage.

- Error Handling: If the external weather service fails for a specific city due to incorrect coordinates, the system logs the error and continues processing other cities rather than failing the entire request. "