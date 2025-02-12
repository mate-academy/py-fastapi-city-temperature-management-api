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


# City Temperature Management API

This is a FastAPI-based project for managing city temperature data and fetching weather information from an external weather service.

## Requirements
- Python 3.13
- standart db SQLite, you can use PostgreSQL or another supported database (add environment to .env)
- **Weather API Key**: Required to fetch real-time weather data. You need to set `API_WEATHER_KEY`. you can take key here [OpenWeather](https://home.openweathermap.org/api_keys)

---

## Installation and Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <project-folder>
```

### 2. Create and Activate a Virtual Environment
```bash
# Create the virtual environment
python -m venv .venv

# Activate the virtual environment
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## Configuration

### 4. Set the Required Environment Variables
This project requires an API key for fetching weather data. Set your key in the environment variable `API_WEATHER_KEY`:

#### **On Windows**:
```bash
set API_WEATHER_KEY=yourkey
```

#### **On Linux/macOS**:
```bash
export API_WEATHER_KEY=yourkey
```

> Replace `yourkey` with the actual API key you obtained from the weather service.[OpenWeather](https://home.openweathermap.org/api_keys)

---

## Database Setup

### 5. Create Migrations
If this is the first time running the project or the database structure has been updated, create migration files:
```bash
alembic revision --autogenerate -m "initial migration"
```

### 6. Apply Migrations
Apply the migrations to create or update the database schema:
```bash
alembic upgrade head
```

---

## Run the Project

### 7. Start the Server
Start the FastAPI application using `uvicorn`:
```bash
python -m uvicorn main:app --reload     
```

The API will be accessible at:  
[http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## Weather API Integration

### How to Obtain the API Key
To use the weather API, go to your chosen weather service provider (e.g., OpenWeather, WeatherAPI, etc.), sign up, and generate an API key.

Set the `API_WEATHER_KEY` environment variable as described above before starting the project.

---

## Additional Information

### Testing the API
Visit the Swagger UI for API documentation and testing:  
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### Deactivating Virtual Environment
When done, deactivate the virtual environment with:
```bash
deactivate
```

---

Enjoy working with the City Temperature Management API!

