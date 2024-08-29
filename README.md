# FastAPI City and Temperature Management Application

This FastAPI application manages city data and their corresponding temperature records. It consists of two main components:

- **City CRUD API**: Allows the creation, retrieval, updating, and deletion of city records.
- **Temperature API**: Fetches current temperature data for all cities in the database, stores it, and allows retrieval of temperature history.

## Table of Contents
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
  - [City CRUD API](#city-crud-api)
  - [Temperature API](#temperature-api)
- [Design Choices](#design-choices)
- [Assumptions and Simplifications](#assumptions-and-simplifications)

## Installation

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```

2. **Create and Activate a Virtual Environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set Up Environment Variables:** Create a `.env` file in the root directory and add your WeatherAPI key:

    ```bash
    DATABASE_URL=sqlite+aiosqlite:///./test.db
    WEATHER_API_URL=http://api.weatherapi.com/v1/current.json
    API_KEY=your_weatherapi_key_here
    ```

5. **Run Database Migrations:**

    ```bash
    alembic upgrade head
    ```

## Running the Application

1. **Start the FastAPI Server:**

    ```bash
    uvicorn app.main:app --reload
    ```

2. **Access the API Documentation:** Open your browser and navigate to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to explore the automatically generated API documentation.

## API Endpoints

### City CRUD API

- `POST /cities`: Create a new city.
- `GET /cities`: Retrieve a list of all cities.
- `GET /cities/{city_id}`: Retrieve details of a specific city by its ID.
- `PUT /cities/{city_id}`: Update details of a specific city by its ID.
- `DELETE /cities/{city_id}`: Delete a specific city by its ID.

### Temperature API

- `POST /temperatures/update`: Fetch the current temperature for all cities in the database and store this data.
- `GET /temperatures`: Retrieve a list of all temperature records.
- `GET /temperatures/?city_id={city_id}`: Retrieve temperature records for a specific city.

## Design Choices

- **Async Programming:** The application leverages Python's async capabilities (with asyncio and httpx) to handle I/O-bound tasks efficiently, such as fetching data from external APIs.

- **External API Integration:** All interactions with the external weather API (weatherapi.com) are isolated in the `app/services/weather_api.py` module, which makes the code more modular and testable.

- **Dependency Injection:** Used FastAPI's dependency injection system for managing database sessions, ensuring that resources are managed correctly and efficiently.

## Assumptions and Simplifications

- **Single Source for Weather Data:** The application assumes that all temperature data will be fetched from weatherapi.com. It doesn't support multiple sources of weather data.

- **City Name Uniqueness:** It is assumed that city names are unique in the database. This is enforced by handling possible integrity errors during city creation.

- **Simplified Error Handling:** Basic error handling is implemented for database operations and external API requests. The application may be extended to provide more granular and user-friendly error messages.

- **SQLite Database:** The application uses SQLite for simplicity and ease of setup. For a production environment, consider switching to a more robust database solution (e.g., PostgreSQL, MySQL).
