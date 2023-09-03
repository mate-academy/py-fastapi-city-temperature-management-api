## City temperature management API

### Description

The FastAPI application manages city data and their corresponding temperature data. 
The application have two main apps: City & Temperature.

1. City API provides managing city data.
2. Temperature API fetches current temperature data for all cities in the database from external Weather API and stores this data in the database.
API provides the endpoint to retrieve the temperature by the city id and by the date.

### Endpoints for City API:

- POST /cities: create a new city.
- GET /cities: get a list of all cities.
- GET /cities/{city_id}: get the details of a specific city.
- PUT /cities/{city_id}: update the details of a specific city.
- DELETE /cities/{city_id}: delete a specific city.

### Endpoints for Temperature API

- POST /temperatures/update: fetches the current temperature for all cities in the database from [Weather API](https://www.weatherapi.com/). 
Store this data in the `Temperature` table.
- GET /temperatures: get a list of all temperature records.
- GET /temperatures/?city_id={city_id}: get the temperature records for a specific city.
- GET /temperatures/?date={date}: get the temperature records by date ("YYYY-MM-DD").


## Installation instruction
+ python -m venv venv
+ venv\Scripts\activate (on Windows)
+ source venv/bin/activate (on macOS)
+ pip install -r requirements.txt
+ Create and run migrations:
   - alembic init alembic
   - alembic revision --autogenerate -m "Initial migration"
   - alembic upgrade head
+ Run server: uvicorn main:app --reload

### Configuration
The project uses environment variables for configuration. 
Please follow these steps to set up the required configuration files.

The .env file is used to store sensitive information and configuration variables that are necessary for the project to function properly.

The .env.sample file serves as a template or example for the .env file. It includes the necessary variables and their expected format, but with placeholder values.
 
 To configure the project:

- Locate the .env.sample file in the project's root directory.
- Duplicate the .env.sample file and rename the duplicated file to .env.
- Open the .env file and replace the placeholder values with the actual configuration values specific to your setup.
