# City Temperature Management API

This is a FastAPI-based API for managing city temperatures.

## Table of Contents

- [Description](#description)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Endpoints](#endpoints)

## Description

The City Temperature Management API provides endpoints to manage city temperature data. It uses FastAPI for its backend and SQLAlchemy for interacting with the database.

## Features

- Add cities you want
- Retrieve a list of city temperatures
- Update city temperatures

## Requirements

- Python >= 3.7
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)

## Installation

1. Clone this repository:
    ```bash
   git clone https://github.com/your-username/your-project.git
2. Create a virtual environment and activate it:
    ```
   python -m venv venv
    ```
    - On Windows:
    ```
    venv/scripts/activate
    ```
    - On MacOS:
    ```
    source venv/bin/activate
    ```
3. Install dependencies:
    ```
    pip install -r requirements.txt
    ```
4. Set up your environment variables. Create a .env file in the root directory and add your environment variables following .env.example

5. Run migrations:
   ```
   alembic upgrade head
   ```

7. Run the FastAPI development server:
   ```
   uvicorn main:app --reload
   ```

##   Usage
Open your browser and go to http://127.0.0.1:8000/docs to access the interactive API documentation.

You can test the various endpoints using the Swagger UI or the ReDoc documentation.

## Endpoints
### Cities:
- GET /api/v1/cities/: Get a list of cities and their temperatures.
- POST /api/v1/cities/: Create new city instance.
- GET /api/v1/cities/{city_id}/: Get detail page for city.
- PUT /api/v1/cities/{city_id}/: Update the temperature data of a specific city.
- DELETE /api/v1/cities/{city_id}/: Delete chosen city.
### Temperature:
- GET /api/v1/temperatures/: Get list of updated temperatures of cities in DB.
- POST /api/v1/temperatures/update/: Update temperatures for all cities in DB

## Code design
To improve performance of app all IO bound operations made asynchrony.To create asynchrony engine for DB function do_run_migrations created and run_migrations_online function rewrote.
