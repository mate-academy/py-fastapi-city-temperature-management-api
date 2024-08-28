# City temperature API

An FastAPI application that manages city data and their corresponding temperature data.

### Features
1. A CRUD (Create, Read, Update, Delete) API for managing city data.
2. An API that fetches current temperature data for all cities in the database and stores this data in the database. This API also provides a list endpoint to retrieve the history of all temperature data.

### How to run
1. Sign up to OpenWeather service https://home.openweathermap.org/users/sign_up and get API key here https://home.openweathermap.org/api_keys
2. Rename .env.example to .env
3. Replace <WEATHER_API_KEY> with API key from step 1
4. Create empty file city_temperature.db in the same directory as .env file
5. Run `docker-compose up --build -d` or if you're using docker-compose-v2 `docker compose up --build -d`
6. Open browser http://localhost:8000/docs (here you can find documentation about all endpoints)

### P.S.
This API uses OpenWeather API to get current temperature for cities:
1. https://openweathermap.org/current uses to get current temperature (in .env file variable API_WEATHER_URL)
2. https://openweathermap.org/api/geocoding-api uses to get coordinates of the city (in .env file variable API_GEO_URL)