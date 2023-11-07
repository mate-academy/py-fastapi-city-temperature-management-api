# FastAPI City and Temperature Management API

This FastAPI application provides a City and Temperature Management API with endpoints to manage city information and record temperature data.

## How to Run the Application

1. Clone the repository:

   ```bash
   git clone https://github.com/maxkatkalov/py-fastapi-city-temperature-management-api.git
   cd py-fastapi-city-temperature-management-api
   

2. Set up a virtual environment and install dependencies:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use venv\Scripts\activate
   pip install -r requirements.txt
   
3. Initialize the SQLite database and apply database migrations:

   ```bash
   alembic upgrade head

4. Run the FastAPI application:

   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload

The API will be accessible at http://localhost:8000.

## City Management

- A City model with attributes for id, name, and additional_info is defined using Pydantic. 
- The application uses an SQLite database with SQLAlchemy and Alembic for database management. 
- Endpoints are provided to create, retrieve, update, and delete cities. 
- City data is validated using Pydantic models.
## Temperature Management
- A Temperature model with attributes for id, city_id, date_time, and temperature is defined using Pydantic. 
- A corresponding Temperature table in the database is created to store temperature records. 
- An additional endpoint POST /temperatures/update fetches current temperature data for all cities and stores it in the database. 
- Endpoints are provided to retrieve temperature records, optionally filtered by city.

![endpoints.png](demo%2Fendpoints.png)
