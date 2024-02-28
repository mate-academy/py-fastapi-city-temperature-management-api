# City Temperature Management API

This FastAPI application created for managing city data and their corresponding temperature data.
The application consists of two main apps:
- City CRUD API: A CRUD (Create, Read, Update, Delete) API for managing city data.
###### py-fastapi-city-temperature-management-api > src > city
- Temperature API: An API that fetches current temperature data for all cities in the database and stores this data in the database.

###### py-fastapi-city-temperature-management-api > src > temperature

## Design Choices

- **Project structure**: I choose project structure by [this](https://github.com/zhanymkanov/fastapi-best-practices?tab=readme-ov-file#1-project-structure-consistent--predictable) best practices, because the structure is consistent, straightforward, and has no surprises.
- **SQLite**: The application employs SQLite as its database engine for the sake of simplicity and straightforward setup. Nevertheless, it is readily customizable to integrate with other databases supported by SQLAlchemy.
- **Weather API**: [Weather API](https://www.weatherapi.com/) is used to fetch current temperature data for cities.

 
# How to Run

1. Create a virtual environment: `python -m venv venv`
2. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - MacOS/Linux: `source venv/bin/activate`
3. Install requirements: `pip install -r requirements.txt`
4. Run the FastAPI application: `uvicorn src.main:app --reload`

# Documentation

FastApi provides Swagger documentation for the API.
You can access it by this url: http://127.0.0.1:8000/docs/
