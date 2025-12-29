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

## Weather Cities API

A backend service for managing cities and logging their temperature in real time.
Temperatures are automatically fetched from OpenStreetMap (Nominatim) and Open-Meteo APIs.


### Features

- Cities create, read, delete
- Automatic current temperature fetching
- Temperature history logging
- Get latest temperature for a city
- Temperature history per city
- Async integration with external APIs
- Clean Architecture (routers / crud / services / models / schemas)


### Tech Stack
- Python 3.13+
- FastAPI
- SQLAlchemy 2.0
- SQLite (easily replaceable with PostgresSQL)
- Open-Weather API
- httpx

###  Installation

```bash
git clone https://github.com/bashyrov/py-fastapi-city-temperature-management-api.git
cd py-fastapi-city-temperature-management-api
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Run

```bash
python -m uvicorn main:app --reload
```

#### Swagger UI:

http://127.0.0.1:8000/docs


### Cities

#### Create a new city
```code
POST /cities/
```
```json
{
  "name": "Tokyo",
  "additional_info": ""
}
```

#### Delete a city
```code
DELETE /cities/{city_id}
```

#### Get all cities
```code
GET /cities/
```
```json
[
  {
    "id": 1,
    "name": "Tokyo",
    "additional_info": ""
  }
]
```

### Temperatures
#### Update temperatures for all cities

```code
POST /temperatures/update
```

#### Get temperature for all cities

```code
GET /temperatures/
```

#### Get temperature for a specific city

```code
GET /temperatures/{city_id}
```

