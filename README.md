## City Temperature Management App

This is a FastAPI application that allows you to manage city data and temperature records. 
The application consists of two main components:

CRUD API for managing city data.
Temperature API for fetching and storing temperature data for cities.

## How to install

Clone this repository:

git clone https://github.com/yourusername/py-fastapi-city-temperature-management-api.git
cd city-temperature-app

## Accessing the Application

You can now access the FastAPI application by opening your web browser and navigating 
to http://localhost:8000. You will be able to interact with the API using the Swagger 
UI provided by FastAPI by http://localhost:8000/docs/.


## Endpoints

### City CRUD API

- POST /cities: Create a new city.
- GET /cities: Get a list of all cities.
- GET /cities/{city_id}: Get the details of a specific city.
- PUT /cities/{city_id}: Update the details of a specific city.
- DELETE /cities/{city_id}: Delete a specific city.
- 
### Temperature API

- POST /temperatures/update: Fetch current temperature data for 
all cities and store it in the database.
- GET /temperatures: Get a list of all temperature records.
- GET /temperatures/?city_id={city_id}: Get the temperature records 
for a specific city.

### User
- POST / login (with JWT)
- POST / Logout (with JWT)
- POST / register

## WeatherAPI Integration
- The application uses the OpenweathermapAPI to fetch temperature data. 
Your API key is read from the .env file automatically.

