# FastAPI City Temperature Management API

## Overview

This FastAPI application manages city data and their corresponding temperature data. It provides two main components:

1. A CRUD API for managing city data.
2. An API that fetches current temperature data for all cities in the database from WeatherAPI and stores this data. If returned data has city name that is not equal to requested, it won`t be saved. It also provides a list endpoint to retrieve the history of all temperature data.

## Instructions

### Running the Application

1. **Clone the Repository**:
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2. **Create and Activate a Virtual Environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set Up the Database**:
    ```bash
    alembic upgrade head
    ```

5. **Run the Application**:
    ```bash
    uvicorn main:app --reload
    ```

6. **Set Environment Variables**:
    - **WEATHER_API_KEY**: Set this to your weather API key.

### Usage

1. **City CRUD API**:
    - **Create a new city**:
        ```bash
        POST "http://127.0.0.1:8000/cities"
        ```
    - **Get a list of all cities**:
        ```bash
        GET "http://127.0.0.1:8000/cities"
        ```
    - **Get the details of a specific city** (Optional):
        ```bash
        GET "http://127.0.0.1:8000/cities/{city_id}"
        ```
    - **Update the details of a specific city** (Optional):
        ```bash
        PUT "http://127.0.0.1:8000/cities/{city_id}"
        ```
    - **Delete a specific city**:
        ```bash
        DELETE "http://127.0.0.1:8000/cities/{city_id}"
        ```

2. **Temperature API**:
    - **Fetch and store the current temperature for all cities**:
        ```bash
        POST "http://127.0.0.1:8000/temperatures/update"
        ```
    - **Get a list of all temperature records**:
        ```bash
        GET "http://127.0.0.1:8000/temperatures"
        ```
    - **Get the temperature records for a specific city**:
        ```bash
        GET "http://127.0.0.1:8000/temperatures/?city_id={city_id}"
        ```

## Design Choices

1. **FastAPI**: Chosen for its performance and ease of use, FastAPI allows for the rapid development of APIs and supports asynchronous programming.
2. **SQLAlchemy**: Used for ORM to interact with the SQLite database, providing a flexible and powerful toolkit for database management.
3. **Pydantic**: Utilized for data validation and settings management, ensuring that data used in the application is correct and validated.
4. **HTTPX**: Chosen for making asynchronous HTTP requests to fetch weather data due to its compatibility with FastAPI and async features.

## Assumptions and Simplifications

1. **Weather Data Source**: It is assumed that the weather API used will provide the necessary data in a predictable and reliable format.
2. **Simplified City Data Model**: The city model only includes `id`, `name`, and `additional_info`. Real-world applications might require more detailed fields.
3. **Error Handling**: Basic error handling is implemented. More comprehensive error handling and logging might be necessary for a production environment.
4. **Single Weather API Key**: It is assumed that a single API key with sufficient quota is available for fetching temperature data. Rate limiting and key rotation are not handled.
5. **Local SQLite Database**: For simplicity, a local SQLite database is used. In a production environment, a more robust database system (like PostgreSQL) might be preferred.
