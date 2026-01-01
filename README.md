# City Temperature Management API

A FastAPI application for managing cities and tracking their temperature history.

The project provides:
- A CRUD API for managing cities
- An API for fetching current temperature data for all cities
- Persistent storage of temperature history
- Graceful error handling and isolated testing

---

## Features

- Create, list, retrieve and delete cities
- Prevent duplicate city creation (returns `409 Conflict`)
- Fetch current temperature for all cities asynchronously
- Store temperature history in a database
- Filter temperature records by city
- SQLite database with SQLAlchemy ORM
- In-memory database for isolated testing
- Automatic API documentation via Swagger (OpenAPI)

---

## Tech Stack

- **Python 3.10+**
- **FastAPI**
- **SQLAlchemy**
- **SQLite**
- **Pydantic**
- **httpx** (async HTTP client)
- **pytest** (testing)

---

## How to run the application

### Clone the repository
```bash
git clone <repository_url>
cd py-fastapi-city-temperature-management-api
```


### Create and activate a virtual environment
* python -m venv venv
* source venv/bin/activate     --- Linux / macOS
* venv\Scripts\activate       --- Windows


### Install dependencies
* pip install -r requirements.txt


### Run the application
* uvicorn main:app --reload


### Open API documentation
* http://127.0.0.1:8000/docs


### Tests
```bash
pytest
```
