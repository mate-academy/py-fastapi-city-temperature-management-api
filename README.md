## City Temperature Management FastAPI Application

This FastAPI application manages city data and their corresponding temperature data.
It consists of two main components: a CRUD API for managing city data and an
API for fetching and storing temperature data.

Installation:

1. Clone the repository:

* ```https://github.com/IhorVoskoboinikov/py-fastapi-city-temperature-management-api```

2. Add venv environment (for windows)

* ```python -m venv venv```
* ```venv\Scripts\activate```

3. Add venv environment (for Linux / macOS)

* ```python3 -m venv venv```
* ```source venv/bin/activate```

4. get API_KEY from Look through [Weather API](https://www.weatherapi.com/docs/) and create .env file as .env.sample
5. Install dependencies
   ```pip install requirements.txt```

6. Create migrations:

* ```alembic revision --autogenerate -m "Initial migration"  ```
* ```alembic upgrade head```

7. Run server:

* ```uvicorn main:app --reload ```

## Usage (local):

1. Go to the URL where the API was
   launched: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs), and use
   the API endpoints.

## Api view:

![img.png](api_demo.png)