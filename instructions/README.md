# City and Temperature Management API

## Overview

This project is a FastAPI application designed to manage city data and their corresponding temperature data. The application consists of two main components:

1. **City CRUD API**: Manages city data using a CRUD interface.
2. **Temperature API**: Fetches and stores current temperature data for all cities and provides a history of temperature records.

## Features

- CRUD operations for city data.
- Fetch and store current temperature data from an online source.
- Retrieve historical temperature data for each city.

## Technologies Used

- **FastAPI**: A modern, fast web framework for building APIs with Python.
- **SQLAlchemy**: SQL toolkit and Object-Relational Mapping (ORM) system for Python.
- **SQLite**: Lightweight database for data storage.
- **Pydantic**: Data validation and settings management using Python type annotations.
- **Alembic**: Lightweight database migration tool for use with SQLAlchemy.


## Getting Started

### Installation

   ```bash
    pip install -r requirements.txt
    alembic init alembic
    alembic revision --autogenerate -m "Initial migration"
    alembic upgrade head
```
-Create a .env file in the root of the project directory by copying the sample file.

-Open the .env file and specify your API key

#### To start the FastAPI application, run the following command:
   ```bash
    uvicorn app.main:app --reload
```




