# FastAPI City Temperature Management API

This project is a FastAPI application that manages city data and their corresponding temperature data. The application
includes two main components (apps):

1. A CRUD API for managing city data.
2. An API that fetches current temperature data for all cities in the database and stores this data. It also provides an
   endpoint to retrieve the history of all temperature data.

## Setup

### Prerequisites

- Python 3.7+
- `pip` (Python package installer)
- SQLite database

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-repo/fastapi-city-temperature-management-api.git
   cd fastapi-city-temperature-management-api

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt

4. **Set up the database:**
   ```bash
   alembic upgrade head

5. **Set up environment variables:**
   - Create a .env file in the root directory of your project and add the following environment variables:
   ```
   WEATHER_API_KEY=your_weather_api_key
   WEATHER_API=https://api.weatherapi.com/v1/current.json (or any another)
   ```

### Running the Application

- To run the FastAPI application, use the following command:
    ```bash
    uvicorn main:app --reload --log-level debug

## API Endpoints

### City CRUD API

- POST /cities: Create a new city.
- GET /cities: Get a list of all cities.
- GET /cities/{city_id}: Get the details of a specific city.
- PUT /cities/{city_id}: Update the details of a specific city.
- DELETE /cities/{city_id}: Delete a specific city.

### Temperature API

- POST /temperatures/update: Fetch current temperature for all cities and store in the database.
- GET /temperatures: Get a list of all temperature records.
- GET /temperatures/?city_id={city_id}: Get temperature records for a specific city.

## Design Choices
- FastAPI: Chosen for its high performance and ease of use in building APIs.
- SQLAlchemy and AsyncSession: Used for database interactions to leverage asynchronous capabilities and efficient database handling.
- Pydantic Models: Used for data validation and serialization.
- HTTPX: Used for making asynchronous HTTP requests to fetch temperature data.
- Tenacity: Used to implement retry logic for HTTP requests to handle transient errors.

## Assumptions and Simplifications
- SQLite: Chosen for simplicity and ease of setup. For production, consider using a more robust database like PostgreSQL.
- Weather API: Assumes an external weather API is available and provides the necessary endpoints and responses.
- Error Handling: Basic error handling is implemented. For production, consider more comprehensive error logging and monitoring.

## Thanks

Thank you for using the FastAPI City Temperature Management API. If you have any questions or feedback, feel free to
reach out!

Contact: [vitalinamalynovska@gmail.com](mailto:vitalinamalynovska@gmail.com).