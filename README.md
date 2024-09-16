### City Temperature Management API

Application that manages city data and their corresponding temperature data.

### Tech Stack
* **FastAPI**  - modern, fast framework for building APIs with Python
* **SQLAlchemy** - Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL
* **Pydentic** - the most widely used data validation library for Python
* **Alembic** - lightweight database migration tool for SQLAlchemy Database Toolkit for Python
* **SQLite** - small, fast, self-contained, high-reliability, full-featured, SQL database engine, that can be replaced by any SQL Database, f.e. PostgreSQL, etc.
* **httpx** - fully featured HTTP client for Python, which provides sync and async APIs


#### The application has two main components (apps):

1. A CRUD (Create, Read, Update, Delete) API for managing city data.
2. An API that fetches current temperature data for cities and stores this data in the database.


###  1. City CRUD API

    - `POST /cities`: Create a new city.
    - `GET /cities`: Get a list of all cities.
    - `GET /cities/{city_id}`: Get the details of a specific city.
    - `PUT /cities/{city_id}`: Update the details of a specific city.
    - `PATCH /cities/{city_id}`: Partial Update the details of a specific city.
    - `DELETE /cities/{city_id}`: Delete a specific city.

###  2. Temperature API

    - `GET /temperatures`: Get a list of all temperature records.
    - `GET /temperatures/?city_id={city_id}`: Get the temperature records for a specific city.
    - `POST /temperatures/update/?city_id={city_id}`: `: Fetches the current temperature for single city from an online weather resource and stores this data in the database.
    - `POST /temperatures/update`: Fetches the current temperature for all cities in the database from an online weather resource and stores this data in the database.. 

### Additional Features

- This app used in async mode & uses async requests for external API. 
- Used dependency injection for db connection & parameters.
- Used external WeatherAPI.com, that provides access to weather data via a JSON restful API. 
- Handles potential errors.
- API documentation using Swagger UI is accessed at **/docs/**.

## Installation

1. Clone this repository to local 
```
https://github.com/KwintDimon/py-fastapi-city-temperature-management-api
```
2. Create & activate a virtual environment

   - open project folder
   ```
   python -m venv venv
   source venv/bin/activate  # For Mac OS/Linux
   venv\Scripts\activate  # For Windows
   ```
3. Install dependencies:
```
pip install -r requirements.txt
```
4. Make database migration:
```
alembic upgrade head
```
5. Set .env file wit environment variables (such as  .env.sample)
6. Run project:
```
uvicorn main:app --reload 
```

### Contact
Developer contact dimon5555@gmail.com
