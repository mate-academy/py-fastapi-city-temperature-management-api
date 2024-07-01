# City Temperature Management API

This is a FastAPI application designed to manage city data and their corresponding temperature data. The application has two main components:

1. A CRUD (Create, Read, Update, Delete) API for managing city data.
2. An API that fetches current temperature data for all cities in the database and stores this data. It also provides an endpoint to retrieve the history of all temperature data.

## Features

- Create, read, update, and delete city data.
- Fetch and store current temperature data for all cities.
- Retrieve temperature history for all cities or for a specific city.

## Installation

1. Clone the repository and create a new branch:
    ```sh
    https://github.com/oleksandra-shershen/py-fastapi-city-temperature-management-api.git
    cd py-fastapi-city-temperature-management-api
    git checkout -b new-branch
    ```

2. Set environment variables:
    - Copy and rename the `.env.sample` file to `.env`.
    - Open the `.env` file and edit the environment variables.
    - Save the `.env` file securely.
    - Make sure the `.env` file is in `.gitignore`.

3. Create and activate a virtual environment:

    On Windows:
    ```sh
    python -m venv venv
    venv\Scripts\activate
    ```

    On UNIX or macOS:
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

4. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

5. Run the project:
    ```sh
    uvicorn main:app --reload
    ```

6. Go to the site: [http://localhost:8000](http://localhost:8000)

## API Endpoints
Visit the detailed Swagger documentation at `http://localhost:8000/docs`.

### I. Cities

- `POST /cities`: Create a new city.
- `GET /cities`: Get a list of all cities.
- `GET /cities/{city_id}`: Get the details of a specific city.
- `PUT /cities/{city_id}`: Update the details of a specific city.
- `DELETE /cities/{city_id}`: Delete a specific city.

### II. Temperatures

- `POST /temperatures/update`: Create new temperature records for all cities in the database.
- `GET /temperatures`: Get a list of all temperature records.
- `GET /temperatures/?city_id={city_id}`: Get the temperature records for a specific city.

## Design Choices

- The application is structured according to FastAPI project structure guidelines, ensuring clear separation of concerns and easy maintainability.
- Dependency injection is used to manage database sessions, which helps in writing clean and testable code.
- Asynchronous programming is used for fetching temperature data to ensure non-blocking operations and better performance.

## Assumptions and Simplifications

- The temperature data is fetched from a placeholder online resource. In a real-world application, this would be replaced with an actual weather API.
- Error handling is implemented for common scenarios, such as trying to create a city that already exists or fetching temperature data for a non-existent city.
