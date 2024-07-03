# City Temperature Management API

This project implements a FastAPI application to manage city data and temperature data.

## Requirements

- Python 3.7+
- FastAPI
- SQLAlchemy
- SQLite
- httpx

## Installation

1. Clone the repository:
    ```bash
    git clone <URL>
    ```

2. Navigate to the project directory:
    ```bash
    cd my_city_temperature_app
    ```

3. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```

4. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

5. Run the application:
    ```bash
    uvicorn main:app --reload
    ```

## Usage

- POST `/cities/`: Create a new city.
- GET `/cities/`: Get a list of all cities.
- GET `/cities/{city_id}`: Get details of a specific city.
- DELETE `/cities/{city_id}`: Delete a specific city.
- POST `/temperatures/update`: Update the temperature for all cities.
- GET `/temperatures/`: Get a list of all temperature records.
- GET `/temperatures/?city_id={city_id}`: Get temperature records for a specific city.

## Design and Justification

- FastAPI is used for rapid development and support for asynchronous functions.
- SQLAlchemy is used for ORM and managing the SQLite database.
- httpx is used for asynchronous HTTP requests.

## Assumptions

- The application uses WeatherAPI to fetch temperature data.
- The API key for WeatherAPI should be specified in `weather_service.py`.

## Additional Notes

- Ensure that you have an API key from WeatherAPI or any other weather data provider you choose to use.
- The `requirements.txt` file should contain all necessary dependencies to run the application.

Example `requirements.txt`:
```plaintext
fastapi
sqlalchemy
httpx
uvicorn
pydantic
