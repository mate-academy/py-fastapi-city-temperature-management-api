# City Temperature Management API

A robust FastAPI application designed to manage city records and track real-time temperature history using asynchronous SQLAlchemy and external weather API integration.

## 🚀 Getting Started

### Prerequisites
Ensure you have Python 3.8+ installed.

### Installation
1. **Clone the repository** (or navigate to the project folder):
   ```bash
   cd py-fastapi-city-temperature-management-api
Install dependencies:

Bash

pip install fastapi uvicorn sqlalchemy aiosqlite httpx pydantic
Running the Application
Start the Uvicorn server with hot reload enabled:

Bash

uvicorn main:app --reload
API Documentation
Once the server is running, access the interactive Swagger UI documentation at: 👉 http://127.0.0.1:8000/docs

🏗️ Design Choices & Architecture
Asynchronous Execution: The project leverages AsyncSession from SQLAlchemy, aiosqlite, and httpx for non-blocking I/O operations, ensuring high performance during concurrent API requests.

External API Integration: Open-Meteo was selected as the weather data provider. It offers high accuracy and allows for coordinate-based weather fetching without the need for API keys.

Resilient Error Handling: To meet production-grade requirements, the application implements safe JSON parsing using the .get() method. This prevents KeyError crashes if the external API returns unexpected or incomplete payloads.

Session Management: Configured expire_on_commit=False in the async_sessionmaker. This ensures that city objects remain accessible within the service layer after database commits, preventing MissingGreenlet exceptions during async iterations.

✅ Features Implemented
City CRUD: Full Create, Read, and Delete functionality for city management.

Automated Weather Updates: A specialized POST /temperatures/update endpoint that asynchronously fetches and stores current weather data for all registered cities.

Temperature History: Comprehensive history tracking with support for filtering records by city_id.

Dependency Injection: Utilizes FastAPI's dependency injection system for database session management.

🛠️ Project Structure
main.py: Application entry point and API routing.

models.py: SQLAlchemy database models.

schemas.py: Pydantic models for data validation and serialization.

crud.py: Database abstraction layer (Create, Read, Delete logic).

services.py: External API integration and business logic for weather updates.

database.py: Database connection and session configuration.
