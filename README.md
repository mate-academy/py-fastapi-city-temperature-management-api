City Temperature API
This project is a FastAPI application that manages city data and records temperature information for each city. It consists of two main components:

A CRUD API for managing city data.
An API that fetches and stores temperature data for each city from an online weather API.
Features
CRUD Operations for City Data: Add, retrieve, update, and delete cities.
Temperature Data Management: Fetch current temperature for each city, store it in a database, and retrieve historical temperature data.
Getting Started
Prerequisites
Python 3.10+ is required.
Install dependencies from requirements.txt.
Installation
Clone the repository:

bash
Копіювати код
git clone <repository-url>
cd city-temperature-api
Install dependencies:

bash
Копіювати код
pip install -r requirements.txt
Set up the database:

Use SQLite as the database (or configure the connection in settings.py for another database).
Initialize the database tables using Alembic:
bash
Копіювати код
alembic upgrade head
Configure environment variables:

Set up a .env file with the required variables, including DATABASE_URL and the API key for fetching temperature data (if needed).
Run the application:

bash
Копіювати код
uvicorn main:app --reload
API Endpoints
City API
POST /cities: Create a new city.
GET /cities: Retrieve a list of all cities.
GET /cities/{city_id} (optional): Retrieve a specific city’s details.
PUT /cities/{city_id} (optional): Update details of a specific city.
DELETE /cities/{city_id}: Delete a specific city.
Temperature API
POST /temperatures/update: Fetch current temperature for all cities and store it in the database.
GET /temperatures: Retrieve all temperature records.
GET /temperatures/?city_id={city_id}: Retrieve temperature records for a specific city.
Design Choices
Separation of Concerns: City and temperature data are managed in separate modules for clarity and scalability.
Async SQLAlchemy: Used asynchronous database sessions for efficient non-blocking API calls.
External Temperature API: An async function is used to fetch temperature data from an online weather API for each city. Error handling logs any failures and skips to the next city.
Assumptions and Simplifications
Weather API Limitations: For demonstration, assumed an API key-based access to a weather API (e.g., OpenWeatherMap). The project can be expanded with other sources if necessary.
Error Handling: Limited to logging API failures when fetching temperatures, assuming data fetching is not critical to core CRUD operations.
Database: Used SQLite for simplicity, though a production environment should use PostgreSQL or MySQL.
