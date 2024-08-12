# FastAPI City Temperature Management API

This FastAPI application manages city and temperature data using an SQLite database. 
It includes endpoints for creating, reading, updating, and deleting cities, 
as well as fetching and storing temperature data from an external weather API.

## Installation

1. Clone the repository:

    ```shell
    git clone https://github.com/dvkim28/py-fastapi-city-temperature-management-api.git
    cd fastapi-city-temperature-management
    ```

2. Set up a virtual environment:

    ```shell
    python -m venv venv
    source venv/bin/activate
    ```

3. Install dependencies:

    ```shell
    pip install -r requirements.txt
    ```

## Configuration

Ensure to set up your environment variables in .env 

```
WEATHER_API_KEY=your_weather_api_key_here
DATABASE_URL=sqlite:///./cities.db
```

## Running the Application

```shell
uvicorn app.main:app --reload
```

This command starts the server at http://127.0.0.1:8000.

## Endpoints
 - POST /cities: Create a new city.
 - GET /cities: Get a list of all cities.
 - GET /cities/{city_id}: Get details of a specific city.
 - DELETE /cities/{city_id}: Delete a specific city.
 - GET /temperatures: Get a list of all temperature records.
 - GET /temperatures/?city_id={city_id}: Get temperature records for a specific city.