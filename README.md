This API facilitates city management operations (Create, Read, Update, Delete) and enables access to city temperatures via integration with a third-party weather service (WeatherAPI).
Setup Instructions:
   1. Set up a Python virtual environment: python -m venv venv
   2. Activate the virtual environment: source venv\bin\activate
   3. Install required dependencies: pip install -r requirements.txt
   4. Configure environment variables using details provided in the env.sample file.
   5. Initialize Alembic for database migration: alembic init alembic
   6. Generate a revision for database schema: alembic revision --autogenerate -m "Provide name"
   7. Apply database migrations: alembic upgrade head
   8. Start the server with automatic reloading: uvicorn main:app --reload
API Endpoints
City Operations:
POST /cities/ - Create a new city entry
GET /cities/ - Retrieve a list of all cities (Refer to documentation for pagination options)
GET /cities/{city_id}/ - Retrieve details of a specific city
PUT /cities/{city_id}/ - Update details of a specific city
DELETE /cities/{city_id}/ - Delete a specific city entry
Temperature Retrieval:
GET /temperatures/ - Retrieve a list of all temperature records (Refer to documentation for pagination options)
GET /temperatures/{city_id}/ - Retrieve temperature records for a specific city