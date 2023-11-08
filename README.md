# City Temperature Management API
FastAPI application that manages city data and their corresponding temperature data. The application has two main components (apps):
1. A CRUD (Create, Read, Update, Delete) API for managing city data.
2. An API that fetches current temperature data for all cities in the database and stores this data in the database. This API also provides a list endpoint to retrieve the history of all temperature data.

## Installation
```shell
git clone https://github.com/artur-leleiko/py-fastapi-city-temperature-management-api.git
cd py-fastapi-city-temperature-management-api
python -m venv venv
venv\Scripts\activate (on Windows)
source venv/bin/activate (on macOS)
pip install -r requirements.txt
create .env file by .env.sample
run -m uvicorn main:app --reload
```

## Technologies
- **FastApi:** A modern, fast (high-performance), web framework for building APIs.
- **SQLAlchemy:** A Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL.
- **Pydantic:** A Python library that provides an easy and convenient way to validate and manipulate data.
- **SQLite:** An in-process library that implements a self-contained, serverless, zero-configuration, transactional SQL database engine.

## Features
- **City Management:** You can add, update, retrieve, and delete city information. Each city can have a name and additional information associated with it.
- **Temperature Record:** The API allows you to fetch the current temperature for cities using an external weather API and store this data in the database.
