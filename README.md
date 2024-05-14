# Temperature Management API

API service for managing cities and temperatures using `www.weatherapi.com`. 
This project uses FastApi, SQLAlchemy, Alembic and SQLit

## Technologies Used
- **FastAPI**: Python framework used for building web APIs.
- **SQLAlchemy**: SQL toolkit and Object-Relational Mapping (ORM) library for Python.
- **SQLite**: Lightweight relational database management system used for local development.
- **httpx**: Asynchronous HTTP client for making HTTP requests.
- **dotenv**: Python module for parsing `.env` files to load environment variables.

## Installation
1. Clone this repository to your local machine.
2. Navigate to the project directory.
3. Install dependencies using `pip install -r requirements.txt`.
4. Create a `.env` file in the root directory and add your API key for the weather service:
5. Run the application using `uvicorn main:app --reload`.

## Features

### City Management
- **POST /cities/**: Create a new cities to the database with their respective information.
- **GET /cities/**: Retrieves a list of all cities stored in the database.
- **GET /cities/{city_id}/**: Fetches detailed information about a specific city based on its unique identifier.
- **PUT /cities/{city_id}/**: Enables users to update the information of an existing city.
- **DELETE /cities/{city_id}/**: Deletes a city from the database.

### Temperature Management
- **GET /temperatures/**: Retrieves a list of all temperatures stored in the database.
- **GET /temperatures/?city_id={city_id}**: Fetches information about a temperature records for a specific city.
- **POST /temperatures/update**: Fetches the current temperature for all cities in the database from using a third-party weather API.
