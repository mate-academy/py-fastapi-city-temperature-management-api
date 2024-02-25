# City Temperature Management API

This FastAPI application manages city data and their corresponding temperature data. It consists of two main components:

1. **City CRUD API**: Manages city data including creating, reading, updating, and deleting cities.
2. **Temperature API**: Fetches current temperature data for all cities and provides endpoints to retrieve temperature history.

## Design Choices

- **SQLite Database**: SQLite is used as the database engine for simplicity and ease of setup. However, the application can be easily adapted to use other databases supported by SQLAlchemy.

- **OpenWeatherMap API**: The OpenWeatherMap API is used to fetch current temperature data for cities. It provides a simple and free-to-use API for weather data.

# Installation

## Using GitHub

1. Ensure you have Python 3 installed.
2. Clone the repository:

   ```bash
   git clone https://github.com/goldenuni/py-fastapi-city-temperature-management-api.git
   cd py-fastapi-city-temperature-management-api

# How to Run

1. Create a virtual environment: `python -m venv venv`
2. Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On macOS: `source venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Run the FastAPI application: `uvicorn main:app --reload`

Explore the API using the provided Swagger UI and refer to the documentation for detailed instructions. 🌟

You can access the API documentation at http://127.0.0.1:8000/docs in your web browser.