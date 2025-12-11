## Task Description

You are required to create a FastAPI application that manages city data and their corresponding temperature data. The application will have two main components (apps):

1. A CRUD (Create, Read, Update, Delete) API for managing city data.
2. An API that fetches current temperature data for all cities in the database and stores this data in the database. This API should also provide a list endpoint to retrieve the history of all temperature data.

### Part 1: City CRUD API

1. Create a new FastAPI application.
2. Define a Pydantic model `City` with the following fields:
    - `id`: a unique identifier for the city.
    - `name`: the name of the city.
    - `additional_info`: any additional information about the city.
3. Implement a SQLite database using SQLAlchemy and create a corresponding `City` table.
4. Implement the following endpoints:
    - `POST /cities`: Create a new city.
    - `GET /cities`: Get a list of all cities.
    - **Optional**: `GET /cities/{city_id}`: Get the details of a specific city.
    - **Optional**: `PUT /cities/{city_id}`: Update the details of a specific city.
    - `DELETE /cities/{city_id}`: Delete a specific city.

### Part 2: Temperature API

1. Define a Pydantic model `Temperature` with the following fields:
    - `id`: a unique identifier for the temperature record.
    - `city_id`: a reference to the city.
    - `date_time`: the date and time when the temperature was recorded.
    - `temperature`: the recorded temperature.
2. Create a corresponding `Temperature` table in the database.
3. Implement an endpoint `POST /temperatures/update` that fetches the current temperature for all cities in the database from an online resource of your choice. Store this data in the `Temperature` table. You should use an async function to fetch the temperature data.
4. Implement the following endpoints:
    - `GET /temperatures`: Get a list of all temperature records.
    - `GET /temperatures/?city_id={city_id}`: Get the temperature records for a specific city.

### Additional Requirements

- Use dependency injection where appropriate.
- Organize your project according to the FastAPI project structure guidelines.

## Evaluation Criteria

Your task will be evaluated based on the following criteria:

- Functionality: Your application should meet all the requirements outlined above.
- Code Quality: Your code should be clean, readable, and well-organized.
- Error Handling: Your application should handle potential errors gracefully.
- Documentation: Your code should be well-documented (README.md).

## Deliverables

Please submit the following:

- The complete source code of your application.
- A README file that includes:
    - Instructions on how to run your application.
    - A brief explanation of your design choices.
    - Any assumptions or simplifications you made.

Good luck!

---

## How to Run the Application

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Navigate to the project directory:
   ```bash
   cd py-fastapi-city-temperature-management-api
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. (Optional) Set up OpenWeatherMap API key for real temperature data:
   ```bash
   export OPENWEATHER_API_KEY="your_api_key_here"
   ```
   
   You can get a free API key from [OpenWeatherMap](https://openweathermap.org/api).
   If no API key is set, the application will use mock temperature data (20.5°C) for demonstration purposes.

### Running the Application

Start the FastAPI server using uvicorn:

```bash
uvicorn app.main:app --reload
```

The application will be available at:
- API: http://localhost:8000
- Interactive API documentation (Swagger UI): http://localhost:8000/docs
- Alternative API documentation (ReDoc): http://localhost:8000/redoc

### Database

The application uses SQLite database (`city_temperature.db`). The database file will be created automatically when you first run the application.

## Design Choices

### Project Structure

The project follows FastAPI best practices with a modular structure:

```
app/
├── __init__.py
├── main.py
├── database.py
├── models.py
├── schemas.py
├── routers/
│   ├── cities.py
│   └── temperatures.py
└── services/
    └── temperature_service.py
```

### Key Design Decisions

1. **Dependency Injection**: Used FastAPI's `Depends()` for database session management, following the dependency injection pattern.

2. **Async/Await**: Implemented async functions for fetching temperature data from external APIs to ensure non-blocking I/O operations.

3. **Error Handling**: 
   - Proper HTTP status codes (404 for not found, 400 for bad requests)
   - Descriptive error messages
   - Validation of input data using Pydantic models

4. **Database Relationships**: 
   - Used SQLAlchemy relationships with cascade delete (when a city is deleted, its temperature records are also deleted)
   - Foreign key constraints for data integrity

5. **API Design**:
   - RESTful endpoint naming
   - Query parameters for filtering (city_id in temperatures endpoint)
   - Pagination support (skip/limit parameters)

6. **Temperature Service**:
   - Separated external API integration into a service module
   - Graceful fallback to mock data when API key is not available
   - Error handling for network failures

## Assumptions and Simplifications

1. **Temperature API**: 
   - Uses OpenWeatherMap API for fetching real temperature data
   - Falls back to mock temperature (20.5°C) if no API key is provided
   - In production, you should set up a valid API key

2. **Database**:
   - Uses SQLite for simplicity (easy to set up and test)
   - Database file is created automatically in the project directory
   - For production, consider using PostgreSQL or another production-ready database

3. **Authentication/Authorization**: 
   - Not implemented (as not specified in requirements)
   - For production, add authentication middleware

4. **Rate Limiting**: 
   - Not implemented
   - Consider adding rate limiting for production use

5. **Caching**: 
   - Not implemented
   - Could be added to reduce external API calls

6. **Logging**: 
   - Basic error logging (print statements)
   - For production, use proper logging framework
