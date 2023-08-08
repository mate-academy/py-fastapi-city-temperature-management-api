# FastAPI Application Documentation

This documentation provides an overview of the FastAPI application, its routes, and how to use them.

## Introduction

This FastAPI application provides endpoints for managing cities and temperatures.

## Installation

To run the FastAPI application, follow these steps:
* Fill `.env_sample` up and rename it to `.env`
* `pip install -r requirements.txt`
* `alembic init alembic`
* `alembic revision --autogenerate -m "Initial ab"`
* `alembic upgrade head`
* `uvicorn main:app --reload`

## Endpoints

### Cities

- `GET /cities/`: Get a list of cities.
- `POST /cities/`: Create a new city.
- `DELETE /cities/{city_id}`: Delete a city by ID.

### Temperatures

- `GET /temperatures/`: Get a list of temperatures.
- `GET /temperatures/{city_id}/`: Get temperatures for a specific city.
- `POST /temperatures/update/`: Update temperatures for all cities.

For detailed information about request and response formats, refer to the API documentation:
`GET /docs`

## Dependencies

- FastAPI
- SQLAlchemy
- SQLChemistry
