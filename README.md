## FastAPI City & Temperature Management API


## Task Description

You are required to create a FastAPI application that manages city data and their corresponding temperature data. The application will have two main components (apps):

1. A CRUD (Create, Read, Update, Delete) API for managing city data.
2. An API that fetches current temperature data for all cities in the database and stores this data in the database. This API should also provide a list endpoint to retrieve the history of all temperature data.

### Part 1: City CRUD API

1. Create a new FastAPI application.
2. Define a Pydantic model `City` with the following fields:
    - `id`: a unique identifier for the city.
    - `name`: the name of the city.
    - `additional_info`: any additional information about the city.
3. Implement a SQLite database using SQLAlchemy and create a corresponding `City` table.
4. Implement the following endpoints:
    - `POST /cities`: Create a new city.
    - `GET /cities`: Get a list of all cities.
    - **Optional**: `GET /cities/{city_id}`: Get the details of a specific city.
    - **Optional**: `PUT /cities/{city_id}`: Update the details of a specific city.
    - `DELETE /cities/{city_id}`: Delete a specific city.

### Part 2: Temperature API

1. Define a Pydantic model `Temperature` with the following fields:
    - `id`: a unique identifier for the temperature record.
    - `city_id`: a reference to the city.
    - `date_time`: the date and time when the temperature was recorded.
    - `temperature`: the recorded temperature.
2. Create a corresponding `Temperature` table in the database.
3. Implement an endpoint `POST /temperatures/update` that fetches the current temperature for all cities in the database from an online resource of your choice. Store this data in the `Temperature` table. You should use an async function to fetch the temperature data.
4. Implement the following endpoints:
    - `GET /temperatures`: Get a list of all temperature records.
    - `GET /temperatures/?city_id={city_id}`: Get the temperature records for a specific city.

### Additional Requirements

- Use dependency injection where appropriate.
- Organize your project according to the FastAPI project structure guidelines.

## Evaluation Criteria

Your task will be evaluated based on the following criteria:

- Functionality: Your application should meet all the requirements outlined above.
- Code Quality: Your code should be clean, readable, and well-organized.
- Error Handling: Your application should handle potential errors gracefully.
- Documentation: Your code should be well-documented (README.md).

## Additional Requirements
- SQLite database with SQLAlchemy ORM.

- Dependency injection for database sessions.

- Async function for fetching temperature data from an online source.

- Project structure follows FastAPI best practices.

## How to Run

1. Clone the repository:

```bash

git clone <your_repo_url>
cd <project_folder>

```

2. Create and activate virtual environment:
```bash

python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Run migrations (if using Alembic):
```bash
alembic upgrade head
```
(If migrations are not used, ensure tables are created at startup with Base.metadata.create_all(bind=engine).)

5. Start the server:
```bash
uvicorn main:app --reload
```

## API Documentation
Once the server is running, visit:

- Swagger UI: http://localhost:8000/docs

- ReDoc: http://localhost:8000/redoc

## Design Choices

- FastAPI was chosen for speed, simplicity, and automatic docs generation.

- SQLAlchemy ORM provides a clean and Pythonic way to handle database models.

- Alembic (optional) is used for database migrations.

- Async temperature fetch to avoid blocking the main thread when calling external APIs.

## Assumptions & Simplifications

- Temperature data is fetched from a free public API (e.g., OpenWeatherMap).

- No authentication or authorization is implemented.

- All cities are assumed to be unique by name.

- Error handling is implemented for common cases (e.g., duplicate cities, missing records).
