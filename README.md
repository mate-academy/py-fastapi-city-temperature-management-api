# City Temperature Management API
A RESTful API for managing city data and tracking their corresponding temperature records. The API allows users to create and manage cities, fetch the current temperature for all cities, and view the history of recorded temperatures.

## Features

### City Management:

- Provides CRUD operations for city data.

### Temperature Management:

- Fetches the current temperature for all cities in the database.
- Stores temperature records in the database.
- Allows retrieval of historical temperature data for all cities or specific cities.

### Swagger Documentation:

Auto-generated API documentation using Swagger/Redoc.

## Technologies
- **FastAPI** - A modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.
- **SQLAlchemy** - A powerful SQL toolkit and Object-Relational Mapping (ORM) library for Python.
- **SQLite** - A C-language library that implements a small, fast, self-contained, high-reliability, full-featured, SQL database engine.
- **HTTPX** - An HTTP client for Python, with async support.
- **Tenacity** - A Python library for retrying operations that might fail, helping to handle transient errors.
- **Swagger** - An open-source software framework backed by a large ecosystem of tools that helps developers design, build, document, and consume RESTful web services.

## How to launch locally:
1. Clone the repository:
```
git clone https://github.com/your-repo/fastapi-city-temperature-management-api.git
```
2. Navigate to the project directory:
```
cd fastapi-city-temperature-management-api
```
3. Create and activate a virtual environment:
```
python -m venv venv

source venv/bin/activate  # For Mac OS/Linux

venv\Scripts\activate  # For Windows
```
4. Install the required dependencies:
```
pip install -r requirements.txt
```
5. Create a .env file and define environmental variables following the example:
```
WEATHER_API_KEY=your_weather_api_key
WEATHER_API=https://api.weatherapi.com/v1/current.json
```
6. Set up the database:
```
alembic upgrade head
```
7. Run the development server:
```
uvicorn main:app --reload --log-level debug
```
## API Endpoints:

### City CRUD API:

1. POST /cities: Create a new city.

- URL: http://127.0.0.1:8000/cities/
- Description: Adds a new city to the database.

2. GET /cities: Retrieve a list of all cities.

- URL: http://127.0.0.1:8000/cities/
- Description: Returns a list of all cities in the database.

3. GET /cities/{city_id}: Retrieve details of a specific city.

- URL: http://127.0.0.1:8000/cities/{city_id}/
- Description: Fetches the details of a specific city by its ID.

4. PUT /cities/{city_id}: Update details of a specific city.

- URL: http://127.0.0.1:8000/cities/{city_id}/
- Description: Updates the information of a specific city identified by its ID.

5. DELETE /cities/{city_id}: Delete a specific city.

- URL: http://127.0.0.1:8000/cities/{city_id}/
- Description: Removes a specific city from the database.

### Temperature API
1. POST /temperatures/update: Fetch current temperature data for all cities and store it in the database.

- URL: http://127.0.0.1:8000/temperatures/update/
- Description: Retrieves current temperatures for all cities and saves the data to the database.

2. GET /temperatures: Retrieve a list of all temperature records.

- URL: http://127.0.0.1:8000/temperatures/
- Description: Provides a list of all recorded temperature data in the database.

3. GET /temperatures/?city_id={city_id}: Retrieve temperature records for a specific city.

- URL: http://127.0.0.1:8000/temperatures/?city_id={city_id}
- Description: Returns temperature records associated with a specific city ID.

### API Documentation
1. Swagger Documentation: Interactive API documentation.

- URL: http://127.0.0.1:8000/docs/
- Description: Provides an interactive interface to explore and test the API endpoints.

2. ReDoc Documentation: Alternative API documentation interface.

- URL: http://127.0.0.1:8000/redoc/
- Description: Offers a different style of API documentation, focusing on a clean and easy-to-read layout.

## How to access
To use the API, simply navigate to the appropriate endpoints listed above.

### Swagger Documentation:

Access the auto-generated documentation at http://127.0.0.1:8000/docs/ to interact with the API directly through your web browser.






