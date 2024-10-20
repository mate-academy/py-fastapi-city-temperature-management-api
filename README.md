# Temperature Management Api

This project provides a RESTful API to manage cities and their 
associated temperature data. Built using FastAPI, SQLAlchemy, and Pydantic, 
this API allows users to create, read, update, and delete cities and 
temperature records efficiently.

## Technologies Used

1. FastAPI: A modern web framework for building APIs with Python 3.6+ based on standard Python-type hints.
2. SQLAlchemy: A SQL toolkit and Object-Relational Mapping (ORM) library for Python
3. Pydantic: Data validation and settings management using Python type annotations.
4. Databases: SQLite for local machine.

## Installation

1. Clone the repository: https://github.com/MykhailoIvchenko/py-fastapi-city-temperature-management-api.git.
2. Switch to the project folder ```cd city-temperature-api```.
3. Create a virtual environment: ```python -m venv venv```.
4. Activate the virtual environment:
    - On Windows: ```venv\Scripts\activate```.
    - On macOS and Linux: ```source venv/bin/activate```.
5. Install the required packages:
    ```
   pip install -r requirements.txt
   ```
6. Set up your database in database.py (if necessary) and create the required tables.

## Usage

1. Start the FastAPI server: ```uvicorn main:app --reload```
2. Access the API documentation at http://127.0.0.1:8000/docs.

## API Endpoints
1. Cities:
   1) GET /cities/
      - Retrieve a list of all cities.
      - Query parameters: q (search term), skip (pagination), limit (results limit).
   2) GET /cities/{city_id}/
      - Retrieve a single city by ID.
   3) POST /cities/
      - Create a new city.
      - Request body: { "name": "City Name", "additional_info": "Additional Info" }
   4) PUT /cities/{city_id}
      - Update an existing city by ID.
      - Request body: { "name": "Updated City Name", "additional_info": "Updated Info" }
   5) DELETE /cities/{city_id}
      - Delete a city by ID.
      
2. Temperatures
   1) POST /temperatures/update
      - Update temperatures for all cities.
   2) GET /temperatures
      - Retrieve a list of all temperatures.
      - Query parameters: q (city ID), skip, limit.
   3) GET /temperatures?city_id={city_id}
      - Retrieve temperatures for a specific city by ID.