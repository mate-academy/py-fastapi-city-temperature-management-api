# City Temperature Management API

This is a FastAPI-based REST application that manages a list of cities and asynchronously fetches their current temperatures using the external [WeatherAPI](https://www.weatherapi.com/).

##  How to Run the Application

### Prerequisites
- Python 3.9+ (Tested on 3.13)
- A valid free API key from WeatherAPI.

### Step-by-Step Instructions

1. **Set up the project directory:**
   Ensure all project files (`app/` folder, `requirements.txt`) are in your working directory.

2. **Set up the Environment Variables:**
   Create a file named `.env` in the root directory of the project and add your WeatherAPI key:
   ```env
   WEATHER_API_KEY=your_actual_api_key_here
   ```

3. **Install Dependencies:**
   Run the following command in your terminal to install the required packages:
   ```
   pip install -r requirements.txt
   ```
4. **Start the Server:**
   Launch the FastAPI application using Uvicorn:
   ```
   uvicorn app.main:app --reload
   ```

5. **Access the API:**
   Open your browser and navigate to the interactive Swagger UI documentation:
   https://www.google.com/search?q=http://127.0.0.1:8000/docs

   Here you can interactively test all endpoints (e.g., add a city via POST /cities/, then update temperatures via POST /temperatures/update).

##  Design Choices

- **FastAPI:** High performance, native async support, and built-in Swagger UI.
- **Modular Structure:** Code is divided into `models`, `schemas`, `services`, and `routers` for readability and scalability.
- **Async Fetching:** Concurrent API requests using `httpx.AsyncClient` and `asyncio.gather()` to minimize execution time.
- **SQLite + SQLAlchemy:** Zero-configuration setup for easy local testing, with ORM for relational mapping and cascading deletes.

##  Assumptions and Simplifications

- **City Names:** Expects valid English names (e.g., "Kyiv"). Invalid or unfound cities are gracefully skipped and reported.
- **Database:** SQLite is used for simplicity and local evaluation instead of a production-ready DB like PostgreSQL.
- **Security:** No authentication/authorization is implemented to focus purely on core requirements.
- **Timezones:** All timestamps are strictly stored in UTC.