# Weather App

## Description

This project is a web application for managing cities and their temperatures using FastAPI, SQLAlchemy, and a Weather API. The application allows adding, retrieving, updating, and deleting information about cities and their temperatures.

## Technologies

- **FastAPI**: For creating RESTful APIs.
- **SQLAlchemy**: For database operations.
- **httpx**: For asynchronous HTTP requests to the Weather API.
- **Docker**: For containerizing the application.

## How to Run the Application

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yashkunn/py-fastapi-city-temperature-management-api.git

2. **Set up Environment Variables**

   Create a `.env` file in the root of the project and add your API key for the Weather API:

   ```plaintext
   POSTGRES_DB=
   POSTGRES_DB_PORT=
   POSTGRES_USER=
   POSTGRES_PASSWORD=
   POSTGRES_HOST=

   PGADMIN_DEFAULT_EMAIL=
   PGADMIN_DEFAULT_PASSWORD=

   API_KEY=
   ```
3. **Run with Docker Compose**

   Use the following command to start the containers:
    ```bash
    docker-compose up --build
    ```
   
### Access the API
The API will be available at: http://localhost:8000.

## API Endpoints:
- POST /cities: Add a new city.
- GET /cities: Retrieve a list of all cities.
- GET /cities/{city_id}: Get information about a specific city.
- PUT /cities/{city_id}: Update city information.
- DELETE /cities/{city_id}: Delete a city.
- POST /temperatures/update: Update temperatures for all cities.
- GET /temperatures: Retrieve all temperatures.
- GET /temperatures/city: Retrieve temperatures for a specific city.
