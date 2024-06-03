This API facilitates city management operations (Create, Read, Update, Delete) and enables access to city temperatures via integration with a third-party weather service (WeatherAPI).
Setup Instructions:
   1. Set up a Python virtual environment: python -m venv venv
   2. Activate the virtual environment: source venv\bin\activate
   3. Install required dependencies: pip install -r requirements.txt  
   4. Initialize Alembic for database migration: alembic init alembic
   5. Generate a revision for database schema: alembic revision --autogenerate -m "Provide name"
   6. Apply database migrations: alembic upgrade head
   7. Start the server with automatic reloading: uvicorn main:app --reload
API Endpoints
City:
POST /cities/ - Create a new city
GET /cities/ - Retrieve a list of all cities
GET /cities/{city_id}/ - Retrieve details of a chosen city by id
PUT /cities/{city_id}/ - Update details of a chosen city by id
DELETE /cities/{city_id}/ - Delete a specific city entry by id
Temperature:
GET /temperatures/ - Retrieve a list of all temperature records
GET /temperatures/{city_id}/ - Retrieve temperature records for a specific city