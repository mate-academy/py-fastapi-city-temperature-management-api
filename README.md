# City and Temperature Management API

This FastAPI application manages city and temperature data. It is organized into two main components:

1. **City CRUD API**: For creating, reading, updating, and deleting city records.
2. **Temperature API**: For fetching current temperature data for cities and storing it in the database, as well as retrieving historical temperature records.

## Requirements

- Python 3.7+
- FastAPI
- SQLAlchemy
- SQLite
- `httpx` for async HTTP requests

## Installation

1. **Clone the repository:**

   ```bash
   git clone git@github.com:saywin/py-fastapi-city-temperature-management-api.git
   cd city-temperature-management-api

2. **Virtual environment and install dependencies:**

   ```bash
   python -m venv .venv
   source .venv/bin/activate # On MacOS use
   .venv\Scripts\activate  # On Windows use
   pip install -r requirements.txt

3. **Run the application:**

   ```bash
   uvicorn app.main:app --reload
   
4. **Access the API documentation:**

   http://127.0.0.1:8000/docs
   