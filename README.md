# City Temperature API

## Overview

1. The CRUD (Create, Read, Update, Delete) API for managing city and temperature data.
2. An API that fetches current temperature data for all cities in the database and stores this data in the database. This API should also provide a list endpoint to retrieve the history of all temperature data.
This project is a Weather API service that allows users to manage cities and record temperatures for those cities. The project is built using SQLAlchemy for database interactions and follows a typical CRUD (Create, Read, Update, Delete) pattern.

## Features

- **Cities Management**: Add, view, and delete cities.
- **Temperatures Management**: Add and view temperature records for specific cities.

## Installation

```
    git clone https://github.com/yourusername/weather-api.git
    cd weather-api
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
```

2. Env config:  
   You need to register on "http://api.weatherapi.com/v1/current.json"  
   Get your api key and use it in .env file


3. Generate alembic migration and apply it by running following command:
   ```
   alembic revision --autogenerate -m "Initial migration"
   alembic upgrade head
   ```

4. Run the Application:
    ```
    fastapi dev main.py
    ```

    The application will be available at `http://127.0.0.1:8000`.

### Cities

- **GET /cities**: Get a list of all cities.
- **GET /cities/{city_id}**: Get details of a single city by ID.
- **POST /cities**: Add a new city.
- **PUT /cities/{city_id}**: Update information about city.
- **DELETE /cities/{city_id}**: Delete a city by ID.

### Temperatures

- **GET /temperatures**: Get a list of all temperatures.
- **GET /temperatures/{city_id}**: Get temperature for a specific city.
- **POST /temperatures/update**: Update temperatures for all cities by using weather API.

## Design Choices

- **SQLAlchemy ORM**: Used for database interactions due to its flexibility and ease of use with Python.
- **CRUD Operations**: Implemented to provide a clear and simple interface for managing cities and temperatures.
- **Structure**: Correct and readable project structure.

## Assumptions and Simplifications

- **Single Database**: The application assumes a single SQLite database.
- **Error Handling**: Error handling at almost all code.
- **Simplified Data Models**: The data models are kept simple for demonstration purposes. In a real-world scenario, additional fields and validations might be necessary.
- **SOLID**: Code is easy for modify and maintain because of approximation to SOLID principles.

### Project documentation

Documentation is available at: 
```
http://127.0.0.1:8000/docs  
```