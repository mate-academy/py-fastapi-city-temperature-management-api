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

## Deliverables

Please submit the following:

- The complete source code of your application.
- A README file that includes:
    - Instructions on how to run your application.
    - A brief explanation of your design choices.
    - Any assumptions or simplifications you made.

Good luck!


FastAPI application for managing city data and tracking their temperature history. The app consists of two main components: a CRUD API for cities and an API that fetches and stores current temperature data via the Open-Meteo external service.

## Setup and Run Instructions

```bash
# 1. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\\Scripts\\activate           # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the application
uvicorn app.main:app --reload

# 4. Open the documentation
# Swagger UI:  http://127.0.0.1:8000/docs
# ReDoc:       http://127.0.0.1:8000/redoc
```

## Endpoints

### Cities

| Method | Path | Description |
|---|---|---|
| POST | /cities/ | Create a new city |
| GET | /cities/ | Get a list of all cities |
| GET | /cities/{city_id} | Get details of a specific city |
| PUT | /cities/{city_id} | Update details of a specific city |
| DELETE | /cities/{city_id} | Delete a specific city |

### Temperatures

| Method | Path | Description |
|---|---|---|
| POST | /temperatures/update | Fetch current temperature for all cities and store it in the history |
| GET | /temperatures/ | Get a list of all temperature records |
| GET | /temperatures/?city_id={city_id} | Get temperature history for a specific city |

## Tech Stack

- FastAPI + Pydantic
- SQLAlchemy + SQLite
- httpx (async client for Open-Meteo)
- uvicorn[standard]

## Design Choices

- The project is split into routers, models, schemas, and database logic to keep the code clean and easy to maintain.
- `Depends(get_db)` is used to manage the database session safely for each request.
- Open-Meteo was chosen because it is free and does not require an API key.
- `httpx.AsyncClient` is used to fetch temperature data asynchronously, as required by the task.

## Assumptions and Simplifications

- Temperature is fetched by city name, so cities with the same name are not separated.
- Authentication is not included.
- Tables are created automatically on startup, without migrations.
- SQLite is used for simplicity.
