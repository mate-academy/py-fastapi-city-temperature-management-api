### API for City Tempreture managment
This API provides a comprehensive solution for managing temperature data across various cities.
## API have two main parts:
* A City API for managing city data.
```shell
    - `POST /cities`: Create a new city.
    - `GET /cities`: Get a list of all cities.
    - `GET /cities/{city_id}`: Get the details of a specific city.
    - `PUT /cities/{city_id}`: Update the details of a specific city.
    - `DELETE /cities/{city_id}`: Delete a specific city.
```
* A Temperature API that fetches current temperature data for all cities in the database and stores this data in the database. This API should also provide a list endpoint to retrieve the history of all temperature data.
```shell
    - `POST /temperatures/update`: that fetches the current temperature for all cities in the database from openweathermap.org API
    - `GET /temperatures`: Get a list of all temperature records.
    - `GET /temperatures/?city_id={city_id}`: Get the temperature records for a specific city.
```
## Instalation
```shell
    # clone repo
    git clone https://github.com/Judviii/py-fastapi-city-temperature-management-api.git
    cd py-fastapi-city-temperature-management-api
    
    # Create venv

    # on macOS
    python3 -m venv venv
    source venv/bin/activate
    # on Windows
    python -m venv venv
    venv\Scripts\activate

    # install requirements.txt
    pip install -r requirements.txt

    # make migration 
    alembic upgrade head
    # do not forget to set .env file wit environment variables
    # use .env.sample as example

    # Run project
    uvicorn main:app --reload
   
    (API will be available at http://127.0.0.1:8000/)
```

## Additional Features
* Used external openweathermap.org that provides access to weather data via API.
* Used dependency injection where its makes sense for db connection & some parameters.
* Used async requests for external APIs.
* Handles potential errors.
* API documentation using Swagger UI (available at http://127.0.0.1:8000/docs/)
## Tech Stack

* **FastAPI**: A modern, fast framework for building APIs with Python, supporting asynchronous programming and automatic documentation generation.
* **SQLAlchemy**: A powerful SQL toolkit and Object Relational Mapper (ORM) for Python that gives developers full SQL flexibility.
* **Pydantic**: The most widely used data validation library for Python, providing a simple and intuitive way to validate and serialize data.
* **Alembic**: A lightweight database migration tool that integrates with SQLAlchemy, simplifying schema management and versioning.
* **SQLite**: A lightweight, fast, self-contained, high-reliability relational database engine that can be replaced with other SQL databases, such as PostgreSQL.
* **httpx**: A fully featured HTTP client for Python that provides both synchronous and asynchronous APIs for easy HTTP requests.
