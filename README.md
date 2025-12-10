City Temperature Management APIWelcome to the City Temperature Management API! 
This is a RESTful web application built with FastAPI that allows you to 
manage a city directory and automatically track their temperatures using 
external meteorological services.
Project OverviewThe application consists of two main modules:City CRUD: 
A complete API for managing cities (create, read, update, delete).
Temperature Service: A module for collecting and storing weather data. 
It is integrated with the Open-Meteo API to fetch real-time temperatures.
Tech StackPython 3.10+FastAPI: Modern, fast (high-performance) web framework for building 
APIs.SQLAlchemy: ORM for working with the SQLite database.Pydantic: 
For data validation and serialization.Alembic: For database migrations.HTTPX: 
Asynchronous client for making external HTTP requests.Docker & Docker Compose: 
For containerization and easy deployment.
How to Run the ProjectYou can run the project locally or using Docker.

🔹 Option 1: Local SetupClone the repository:git clone <your-repo-url>
cd py-fastapi-city-temperature-management-api
Create and activate a virtual environment:python -m venv venv

# For macOS/Linux:

source venv/bin/activate

# For Windows:

.\venv\Scripts\activate

Install dependencies:pip install -r requirements.txt

# Or if using Poetry:

poetry install

Apply database migrations (Alembic):alembic upgrade head

Run the server:uvicorn main:app --reload

The server will be available at: http://127.0.0.1:8000

🔹 Option 2: Run with DockerIf you have Docker and Docker Compose installed
:docker-compose up --build -d
📚 API DocumentationOnce the server is running, you can access the interactive 
API documentation (Swagger UI) at:👉 http://127.0.0.1:8000/docsMain Endpoints
CitiesMethodURLDescriptionGET/cities/Get a list of all cities (with pagination).
POST/cities/Create a new city.
GET/cities/{id}/Get detailed information about a specific city.
PUT/cities/{id}/Update city information.
DELETE/cities/{id}/Delete a city.
TemperaturesMethodURLDescription
GET/temperatures/
Get temperature history (can be filtered by city_id).
POST/temperatures/update/Magic! 
Updates temperatures for ALL cities by fetching data from Open-Meteo.
Design Decisions & Assumptions1. 
Database ArchitectureWe use SQLite for simplicity of deployment and testing.
The cities table stores basic information.
The temperatures table has a Foreign Key linking to cities, 
allowing us to keep a history of measurements for each city.2. 
Weather Data Fetching (Open-Meteo)Open-Meteo API was chosen for fetching weather data.Why? 
It is a free API that does not require an API key, simplifying the review process.
How it works? 
The /temperatures/update/ endpoint works in two steps:
First, it queries the Geocoding API to find coordinates (latitude/longitude) 
based on the city name.Then, it uses these coordinates to fetch the current 
temperature.3. AsynchronyDatabase operations (crud.py) are implemented 
synchronously because sqlite and the standard SQLAlchemy Session operate in 
blocking mode. FastAPI efficiently handles this in a thread pool.External 
requests to the weather API are implemented asynchronously (async/await) using 
the httpx library. This is critical to prevent blocking the server 
while waiting for responses from the external service when updating weather for multiple cities.4. 
ValidationPydantic schemas (schemas.py) are used for strict validation of 
input and output data, ensuring data integrity.
TestingTo run tests, use pytest. Make sure you have installed the testing dependencies.pytest
Developed as part of a FastAPI homework assignment.