# Temperature Management API

FastApi REST Framework API Project
Project Title: FastAPI City Temperature Management 

Project Description:

The FastAPI City Temperature Management project is a web application designed to manage and display temperature data for various cities. 

## Installation

Python 3.10.x must be already installed

```shell
git clone https://github.com/Psheiuk-Nazar/py-fastapi-city-temperature-management-api.git
cd py-fastapi-city-temperature-management-api
pythone -m venv venv
source venv//Scripts//activate
pip install -r requirements.txt
pythone manage.py runserver
```

## Features:
1. **City Management**: Users can add and delete cities from the database.
2. **Temperature Updates**: The application fetches real-time temperature data for each city from an external API and updates it in the database.
3. **Temperature Retrieval**: Users can retrieve temperature data for specific cities.
4. **API Documentation**: The project includes comprehensive API documentation using FastAPI's built-in Swagger UI.

## Technologies Used:

1. **FastAPI**: A modern, fast (high-performance), web framework for building APIs.
2. **SQLAlchemy**: A SQL toolkit and Object-Relational Mapping (ORM) library.
3. **HTTPx**: A fully featured HTTP client for Python 3, which supports both synchronous and asynchronous requests.
4. **Python-dotenv**: A Python module that reads key-value pairs from a .env file and makes them available as environment variables