# 🏙️ City and Temperature Management FastAPI Application
___

This FastAPI application is a powerful tool for managing city data and temperature records efficiently. It consists of two main components: a CRUD API for city data and an API for fetching and recording temperature data for cities. I've included everything you need to know to start this project.

## 🚀 Features
___
- City CRUD API:
  - Create, Read, Update, and Delete city-data.
  - Retrieve details of specific cities.
- Temperature API:
  - Fetch and store current temperature data for all cities concurrently (using `async`/`await`).
  - Retrieve all temperatures.
  - Retrieve temperature records for a specific city.

## 🛠️ Getting Started
___
- Python 3 should be installed
- Register an account on https://www.weatherapi.com/ and get your API key
- Create a `.env` file with your API key inside using the `.env.sample` file

### 📦 Installation
___
```bash
git clone https://github.com/eduardhabryd/py-fastapi-city-temperature-management-api.git
cd py-fastapi-city-temperature-management-api
pip install -r requirements.txt
alembic upgrade head
uvicorn main:app --reload
```

## 📚 Documentation
___
Please take a look at the API documentation for details on available endpoints, request/response formats, and examples. The documentation can be accessed at http://localhost:8000/docs when the application is running.

