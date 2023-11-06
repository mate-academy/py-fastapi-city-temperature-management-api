# 🏙️ City and Temperature Management FastAPI Application
___

This FastAPI application is a powerful tool for managing city data and temperature records efficiently. It consists of two main components: a CRUD API for city data and an API for fetching and recording temperature data for cities. Below, you'll find everything you need to know to get started with this project.

## 🚀 Features
___
- City CRUD API:
  - Create, Read, Update, and Delete city data.
  - Retrieve details of specific cities.
- Temperature API:
  - Fetch and store current temperature data for all cities.
  - Retrieve temperature records for a specific city.
- Dependency Injection: Efficient use of dependency injection.
- Project Structure: Organized according to FastAPI project structure guidelines.
- Error Handling: Graceful handling of potential errors.
- Clean Code: Well-documented, clean, and readable code.

## 🛠️ Getting Started
___
- Python 3 should be installed
- Register account on https://www.weatherapi.com/ and get your API key
- Create `.env` file with your API key inside using `.env.sample` file

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
Please refer to the API documentation for details on available endpoints, request/response formats, and examples. The documentation can be accessed at http://localhost:8000/docs when the application is running.

