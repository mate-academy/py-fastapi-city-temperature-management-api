# FastAPI City Temperature Management

Welcome to the FastAPI City Temperature Management application! This application is designed to manage city data and corresponding temperature records with a clean and efficient API.

## Part 1: City CRUD API

### Endpoints
- **Create City:** `POST /cities`
- **Get Cities:** `GET /cities`
- **Delete City:** `DELETE /cities/{city_id}`

## Part 2: Temperature API

### Endpoints
- **Fetch Temperature For All Cities:** `POST /temperatures/update`
- **Get Temperatures:** `GET /temperatures`
- **Get City Temperatures:** `GET /temperatures/{city_id}`

## Additional Features

- Dependency injection was used to organize the code efficiently.
- The FastAPI project structure guidelines have been followed for clarity.
- Asynchronous functions are used to obtain temperature data to improve performance.

## Getting Started

1. Clone this repository.
```bash
git clone https://github.com/AndriyKy/py-fastapi-city-temperature-management-api.git && cd py-fastapi-city-temperature-management-api
```
2. Create a virtual environment and install dependencies.
```bash
python3.11 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
```
3. Run the migration: `alembic upgrade head`.
4. Run the FastAPI server: `uvicorn src.main:app --reload`.

Explore the powerful features of this FastAPI application for managing city and temperature data effortlessly!
