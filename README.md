# City and Temperature Data Management Application

This FastAPI application is designed to manage city data and their corresponding temperature data. It uses Alembic for database migrations, SQLAlchemy as the database ORM, and Pydantic for request and response validation. This README will guide you through the steps to set up and run the application.

## Prerequisites

Before you can run the application, make sure you have the following prerequisites installed on your system:

- Python 3.7 or higher
- pip (Python package manager)
- A virtual environment tool like virtualenv or conda (optional but recommended)

## Get Started

Follow these steps to set up and run the application:

### 1. Clone the Repository
```bash 
git clone https://github.com/aarrtemm/py-fastapi-city-temperature-management-api.git
cd py-fastapi-city-temperature-management-api
```

### 2. Create a Virtual Environment (optional but recommended)
It's a good practice to create a virtual environment to isolate the project dependencies.

```bash
# Using virtualenv
virtualenv venv

# Activate the virtual environment
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 3. Install Dependencies
Use pip to install the required Python packages

```bash 
pip install -r requirements.txt
```

### 4.Configuration
Open the `database.py` file and configure the application settings as needed. You may specify the database connection details, API base URL, and other parameters. Also in the `.env` file, do not forget to insert the `API KEY` from the weatherapi website

### 5. Set Up the Database with Alembic
Initialize the database and create the necessary tables using Alembic for database migrations.

```bash
# Initialize Alembic
alembic init alembic

#initialize first migration
alembic revision --autogenerate -m "Initial" 

# Run database migrations
alembic upgrade head
```

### 6. Run the Application
Start the FastAPI application by running the following command:
```bash
uvicorn main:app --reload
```
The --reload flag enables automatic code reloading during development. You can access the API documentation at http://localhost:8000/docs in your web browser.

### 7. API Usage
You can use the Swagger UI or ReDoc documentation provided by FastAPI to interact with the API. The API endpoints are documented, and you can test and use the application from there.


# API Endpoints
The following API endpoints are available for managing city and temperature data:

- **GET/cities**: Retrieve a list of all cities.
- **POST/cities**: Create a new city
- **GET/cities/{city_id}**: Retrieve a city by id
- **DELETE/cities/{city_id}**: Delete a city
- **PUT/cities/{city_id}**: Update a city
- **POST/temperatures/update**: Update temperature for all cities
- **GET/temperatures/**: Retrieve a list of all temperatures for all city

# Example API Requests
Here are some example API requests you can make using tools like curl, Postman, or your favorite HTTP client:

- Create a new city record:
```http request
POST http://localhost:8000/cities

{
    "name": "New York",
    "additional_info": "USA",
}
```

- Retrieve city information:
```http request
GET http://localhost:8000/cities/{city_id}
```

- Delete city:
``` http request
DELETE http://localhost:8000/cities/{city_id}
```

- Update city info:
``` http request
PUT http://localhost:8000/cities/{city_id}
{
    "name": "string",
    "additional_info": "string",
}

```

- Update temperatures for all cities:
``` http request
POST http://localhost:8000/temperatures/update
```

- Retrieve list the temperature records for a specific city:
```http request
GET http://localhost:8000/temperatures/?city_id={city_id}
```

Please refer to the Swagger UI or ReDoc documentation for more details on API endpoints and request payloads.

# Closing Notes
You now have the City and Temperature Data Management Application up and running with Alembic, SQLAlchemy, and Pydantic integration. Feel free to explore the API and integrate it into your projects. If you encounter any issues or have questions, please refer to the FastAPI, Alembic, and SQLAlchemy documentation or raise any concerns in the project's issue tracker on GitHub.
