# Cities Weather Management

This project is a web application that allows users to manage cities and retrieve temperature information for different locations. The application uses FastAPI to create a RESTful API and SQLAlchemy for database interactions.

## Features

- Add new cities.
- Retrieve a list of cities.
- Update city information.
- Delete cities.
- Get temperatures for all cities or a specific city.
- Automatically update temperatures for all cities.

## Technologies

- [FastAPI](https://fastapi.tiangolo.com/) - A web framework for building APIs.
- [SQLAlchemy](https://www.sqlalchemy.org/) - ORM for database operations.
- [SQLite](https://www.sqlite.org/index.html) - An embedded relational database.
- [Asyncio](https://docs.python.org/3/library/asyncio.html) - A library for writing asynchronous code in Python.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Narberal90/py-fastapi-city-temperature-management-api.git
   cd py-fastapi-city-temperature-management-api
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Linux/Mac
   venv\Scripts\activate     # For Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the server:
   ```bash
   uvicorn main:app --reload
   ```

## Usage

- **Add City:**
  - POST /cities/
  - Request body:
    ```json
    {
      "name": "Kyiv"
    }
    ```

- **Get List of Cities:**
  - GET /cities/

- **Get City Information:**
  - GET /cities/{city_id}

- **Update City Information:**
  - PUT /cities/{city_id}
  - Request body:
    ```json
    {
      "name": "Updated City Name"
    }
    ```

- **Delete City:**
  - DELETE /cities/{city_id}

- **Get Temperatures:**
  - GET /temperatures/
  - Query parameter `city_id` can be used to get temperature for a specific city.

