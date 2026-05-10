# City Temperature Management API

A FastAPI-based application that manages cities and tracks their current temperatures using external Weather API.

## How to Run

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Dolteriska/py-fastapi-city-temperature-management-api
   cd py-fastapi-city-temperature-management-api
   
2. **Setup a virtual environment**:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt

4. **Configuration**:
   Rename .env.sample file to .env in the root directory and add your WeatherAPI key:
   ```bash
   DATABASE_URL=sqlite+aiosqlite:///./weather.db
   WEATHER_API_KEY=your_actual_api_key_here

5. **Run migrations**:
   ```bash
   alembic upgrade head
   
6. **Run the application**:
   ```bash
   uvicorn app.main:app --reload
   
Access the API documentation at http://127.0.0.1:8000/docs

**Design Choices**:
Layered Architecture: I separated the logic into Models (DB structure), Schemas (Pydantic validation), Repositories (DB queries), and Services (Business logic). This makes the code modular and easy to test.

**Async Stack**: Used SQLAlchemy with aiosqlite and httpx for the weather client to ensure the application remains non-blocking and high-performing.

**Dependency Injection**: Utilized FastAPI's Depends for managing service and repository lifecycles.

**Assumptions & Simplifications**
Weather Provider: I used WeatherAPI.com as the primary data source.

**Error Handling**: If the external API fails for a specific city during a bulk update, the system logs the error and continues with the next city instead of failing the entire request.

**SQLite**: For simplicity and ease of review, SQLite is used as the database.
   
