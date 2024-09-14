
## FastAPI City and Temperature Management API
This FastAPI application manages city data and temperature records. It includes two main components: a CRUD API for city data and an API for fetching and storing temperature data.

## Instructions to Run the Application
Prerequisites: 
1. Python 3.8+: Make sure you have Python installed. You can download it from python.org.

2. Virtual Environment: It's recommended to use a virtual environment to manage dependencies.

## Setup 
### Clone the Repository:

````
git clone https://github.com/Andrii1000/py-fastapi-city-temperature-management-api
cd py-fastapi-city-temperature-management-api
````

### Create a Virtual Environment:

````

python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
````

#### Install Dependencies:

````
pip install -r requirements.txt
````

#### Setup the Database: 
Ensure you have SQLite configured in your environment. The application will automatically create the database tables on startup.

#### Run the Application:

````
uvicorn main:app --reload
````
The application will be available at http://127.0.0.1:8000.

#### Access the API Documentation:

Swagger UI: http://127.0.0.1:8000/docs

## Design Choices
#### 1. Asynchronous Operations:

- Used AsyncSession and asynchronous HTTP requests to handle operations non-blocking, ensuring better performance for I/O-bound tasks.
#### 2. Separation of Concerns:

- Organized the code into different modules for CRUD operations, API routes, and schemas to maintain a clean architecture and improve maintainability.
#### 3. Pydantic Schemas:

- Used Pydantic models for data validation and serialization to ensure that all data passed through the API conforms to expected formats.
#### 4. Database Setup:

- Used SQLAlchemy for ORM and SQLite as the default database. Alembic is used for managing database migrations.
## Assumptions and Simplifications
#### External API for Temperature Data:

- The temperature API used (WeatherAPI) is assumed to be reliable and available. Error handling for external API failures is minimal.
#### Database Choice:

- SQLite is used as a lightweight database. For production, a more robust database like PostgreSQL might be considered, and configurations should be adjusted accordingly.
#### Basic Error Handling:

- Basic error handling is provided. For a production environment, more comprehensive error handling and logging should be implemented.
#### Authentication and Authorization:

- No authentication or authorization is implemented. For security in a production environment, consider adding authentication mechanisms.
#### API Rate Limiting:

- No rate limiting is applied. If there is a risk of hitting rate limits with the temperature API, consider implementing rate limiting or caching mechanisms.
