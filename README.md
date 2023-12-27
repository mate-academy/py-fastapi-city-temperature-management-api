## FastAPI City Temperature Management API
Welcome to the FastAPI City Temperature Management API! This API allows you to interact with city data and temperature records effortlessly.


### City Operations
1. Add a New City
2. Get a List of Cities
3.  Get City Details
4. Update City Details
5. Delete a City

### Temperature Operations

1. Update Temperature Records
2. Get a List of Temperature Records 
3. Get Temperature Records for a Specific City


### How to Use

1. Install Dependencies: Run pip install -r requirements.txt to install the required dependencies.
2. Create and activate venv:
- python -m venv venv
- venv\Scripts\activate (on Windows)
- source venv/bin/activate (on macOS)
- pip install -r requirements.txt
3. Run migrations:
- alembic upgrade head
4. Use [Weather API](https://www.weatherapi.com/docs/) for getting api key and add it in .env
5. Run the Application: Start the FastAPI application using the command uvicorn main:app --reload
6. Explore the API:

Use Swagger UI or ReDoc for interactive API documentation.
Make requests to the API endpoints using your preferred tool or programming language.

