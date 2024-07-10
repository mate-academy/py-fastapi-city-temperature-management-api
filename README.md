# City Temperature Management API

## Overview

This project is a Weather API service that allows users to manage cities and record temperatures for those cities. The project is built using SQLAlchemy for database interactions and follows a typical CRUD (Create, Read, Update, Delete) pattern.

## Features

- **Cities Management**: Add, view, and delete cities.
- **Temperatures Management**: Add and view temperature records for specific cities.

## Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/yourusername/weather-api.git
    cd weather-api
    ```

2. **Create a Virtual Environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
To run this project, you need to set up the environment variables. Create a .env file in the root directory of your project. 

A sample .env.sample file is provided to help you get started.

3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set Up the Database**:
    - Ensure you have a running PostgreSQL instance.
    - Create a database for the project:
        ```sql
        CREATE DATABASE weather_db;
        ```
    - Apply migrations:
        ```bash
        alembic upgrade head
        ```

5. **Run the Application**:
    ```bash
    uvicorn app.main:app --reload
    ```

    The application will be available at `http://127.0.0.1:8000`.

## Endpoints

### Cities

- **GET /cities**: Get a list of all cities with optional pagination (parameters: `skip`, `limit`).
- **GET /cities/{city_id}**: Get details of a single city by ID.
- **POST /cities**: Create a new city.
- **DELETE /cities/{city_id}**: Delete a city by ID.

### Temperatures

- **GET /temperatures**: Get a list of all temperature records with optional pagination (parameters: `skip`, `limit`).
- **GET /temperatures/{city_id}**: Get temperature records for a specific city with optional pagination (parameters: `skip`, `limit`).
- **POST /temperatures**: Create a new temperature record.

## Design Choices

- **SQLAlchemy ORM**: Used for database interactions due to its flexibility and ease of use with Python.
- **CRUD Operations**: Implemented to provide a clear and simple interface for managing cities and temperatures.
- **Pagination**: Added to endpoints to handle large datasets efficiently.

## Assumptions and Simplifications

- **Single Database**: The application assumes a single PostgreSQL database. For a production environment, consider using separate databases for different environments (development, testing, production).
- **Basic Error Handling**: Error handling is minimal and may need to be expanded for production use.
- **Simplified Data Models**: The data models are kept simple for demonstration purposes. In a real-world scenario, additional fields and validations might be necessary.
