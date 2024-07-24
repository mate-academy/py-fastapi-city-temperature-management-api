# City Temperature Management API

## Project Description

The City Temperature Management API is a FastAPI application designed to manage city data and their corresponding temperature data. The application consists of two main components:

1. A CRUD (Create, Read, Update, Delete) API for managing city data.
2. An API that fetches current temperature data for all cities in the database and stores this data. Additionally, it provides an endpoint to retrieve the history of all temperature data.

## Resources

### City

- **id**: a unique identifier for the city.
- **name**: the name of the city.
- **additional_info**: any additional information about the city.

### Temperature

- **id**: a unique identifier for the temperature record.
- **city_id**: a reference to the city.
- **date_time**: the date and time when the temperature was recorded.
- **temperature**: the recorded temperature.

## Components

### City CRUD API

Manage city information (CRUD operations).

#### API Endpoints

- **POST**: `cities/` - Create a new city.
- **GET**: `cities/` - Get a list of all cities.
- **DELETE**: `cities/{city_id}/` - Delete a specific city.

### Temperature API

Fetch and store current temperature data for all cities, and retrieve temperature history.

#### API Endpoints

- **POST**: `temperatures/update/` - Fetch current temperature for all cities and store this data.
- **GET**: `temperatures/` - Get a list of all temperature records.
- **GET**: `temperatures/?city_id={city_id}` - Get the temperature records for a specific city.

## Project Setup

### Prerequisites

- Python 3.9+
- SQLite (or any other preferred database)

### Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/py-fastapi-city-temperature-management-api.git
    cd py-fastapi-city-temperature-management-api
    ```

2. **Create a virtual environment and activate it:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the database:**
    Create the SQLite database and apply the migrations to create the necessary tables:
    ```bash
    alembic upgrade head
    ```

5. **Run the application:**
    ```bash
    uvicorn main:app --reload
    ```

6. **Access the API documentation:**
    Open your browser and navigate to `http://127.0.0.1:8000/docs` to see the interactive API documentation.

## Design Choices

- **FastAPI**: Chosen for its performance and ease of use in creating RESTful APIs.
- **SQLite**: Used as the database for simplicity and ease of setup.
- **SQLAlchemy**: Used as the ORM to interact with the database.
- **httpx**: Used for asynchronous HTTP requests to fetch temperature data.

## Assumptions and Simplifications

- The temperature data is fetched from a weather API using a single API key.
- Basic error handling is implemented to manage common issues such as network errors or invalid data.
- The database setup is simplified to use SQLite, which can be easily switched to another database if needed.

## Directory Structure

```plaintext
py-fastapi-city-temperature-management-api/
├── main.py
├── db/
│   ├── database.py
│   ├── models.py
│   ├── crud.py
│   └── schemas.py
├── city/
│   ├── router.py
├── temperature/
│   ├── router.py
├── alembic/
│   ├── versions/
│   └── env.py
├── requirements.txt
└── README.md
```

## Contact

Maks - [maksymstakhovskyi@yahoo.com](mailto:maksymstakhovskyi@yahoo.com)