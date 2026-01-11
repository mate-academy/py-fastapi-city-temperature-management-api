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

# City & Temperature Management API

## Description
A **FastAPI** application for managing city data and their corresponding temperature records.
The project has two main components:
- **City CRUD API** — create, read, update, and delete city records.
- **Temperature API** — fetch and store temperature data for cities from an online resource (OpenWeather API).

---

## Installation & Running

### 1. Clone the project
```bash
git clone <repo-url>
cd project

### 2. Install dependencies
pip install -r requirements.txt

### 3. Database setup
SQLite is used by default. The database file is created automatically:
sqlite:///./city_temperature.db

### 4. Configure OpenWeather API
Register at OpenWeather and obtain your API key.
⚠️ Important: Do not hardcode the API key in the source code.
Instead, create a .env file in the project root:
OPENWEATHER_API_KEY=your_api_key_here
and load it in temperature/router.py using python-dotenv.

### 5. Run the server
uvicorn main:app --reload

### 6. Access the API
Swagger UI: http://127.0.0.1:8000/docs
Root endpoint: http://127.0.0.1:8000/

### Endpoints
City API
POST /cities/ — create a new city
GET /cities/ — list all cities
GET /cities/{city_id} — get city details by ID
PUT /cities/{city_id} — update city details
DELETE /cities/{city_id} — delete a city
Duplicate handling: If a city with the same name already exists, the API returns 409 Conflict instead of a server error.

### Temperature API
POST /temperatures/ — manually create a temperature record
GET /temperatures/ — list all temperature records
supports filtering: GET /temperatures?city_id={id}
POST /temperatures/update — fetch and store current temperatures for all cities (async call to OpenWeather API)

### Design Choices
Modern SQLAlchemy 2.0 syntax (Mapped, mapped_column, relationship) for type safety and clarity.
Clear separation into city and temperature packages for modularity.
Asynchronous requests to OpenWeather API implemented with httpx.
Dependency Injection (Depends(get_db)) for database sessions.
SQLite chosen as a lightweight and simple database for this project.

### Assumptions & Simplifications
OpenWeather API (free tier, up to 1000 requests/day) is used as the temperature source.
additional_info field in City is optional and not unique.
Temperature history is stored in the database and accessible via endpoints.
Error handling is basic (e.g., 404 when city is missing; empty list [] when no temperature records exist).
No authentication or advanced business logic implemented, as this is a learning assignment.

### Known limitations
- Database operations are synchronous. FastAPI runs them in a thread pool, but for full non-blocking behavior you should use AsyncSession with an async driver (e.g., aiosqlite).
- Duplicate city names are handled gracefully with 409 Conflict.
- Redundant endpoint /temperatures/by_city/{city_id} removed in favor of query parameter filtering.
