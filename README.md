# City Weather Management API #

A FastAPI-based application for managing city data and tracking their current temperatures using external weather services.

## 🚀 Getting Started ##
1. Environment Setup
Create a .env file in the root directory and add your OpenWeatherMap API key:
```bash
WEATHER_API_KEY=your_api_key_here
DATABASE_URL=sqlite+aiosqlite:///./proj_db.db
```

3. Installation
Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Database Migrations
Initialize the database schema using Alembic:

```bash
alembic upgrade head
```
4. Running the Application
Start the Uvicorn server:

```bash
uvicorn main:app --reload
```

Access the interactive API documentation (Swagger UI) at: http://127.0.0.1:8000/docs


## 🛠 Design Choices ##
- **Asynchronous Architecture:** Utilized SQLAlchemy with aiosqlite and httpx to ensure the application remains responsive while performing I/O operations (DB queries and external API calls).

- **Domain-Driven Structure:** Organized the project into two main modules (city and temperature). Each module encapsulates its own models, schemas, and logic for better maintainability.

- **Pydantic V2:** Leveraged Pydantic for robust data validation and settings management.

- **Dependency Injection:** Implemented FastAPI's Depends for database session management to ensure clean resource handling and easier testing.

## 📝 Assumptions & Simplifications ##
- **Weather Service:** The application uses OpenWeatherMap. It assumes city names in the database are provided in English for accurate API matching.

- **Timezones:** All temperature records are stored with a UTC timestamp using func.now().

- **Error Handling:** If the external API fails for a specific city, that record is skipped, and the process continues for the remaining cities.