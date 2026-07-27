1. How to run my application.

use command in the terminal: uvicorn main:app --reload

2. My project structure. The main directory of my project /py-fastapi-city-temperature-management-api/. It's include list of config files and directories:

    - /city_api -- directory include all config files only for City table. 
        There are:
            - city_models.py -- This file only defines the Pydantic `City` model.
            - city_schemas.py -- This file contains all the schemas for the `City` model.
            - city_crud.py -- This file contains a set of functions for implementing endpoints related to the `City` model.
            - city_router.py - routers for implementing `City` model endpoints.

    - /temperature_api -- directory include all config files only for City table. 
        There are:
            - temp_models.py -- This file only defines the Pydantic `Temperature` model.
            - temp_schemas.py -- This file contains all the schemas for the `Temperature` model.
            - temp_crud.py -- This file contains a set of functions for implementing endpoints related to the `Temperature` model.
            - temp_router.py - routers for implementing `Temperature` model endpoints.

    - /db/databasem.py -- DB engine initialization.
    - db_settings.py -- Database settings. DATABASE_URL and other configuration values (such as PROJECT_NAME) are defined here using Pydantic's BaseSettings, with support for overriding values via a .env file. If the project needs to work with multiple databases in the future, the connection settings for them should be added to this file as well.
    - dependencies.py -- Shared FastAPI dependencies. Loads environment variables from .env (including OPENWEATHER_API_KEY, used for requests to the weather service) and defines get_db, a dependency that provides a database session per request via Depends(get_db), ensuring the session is properly closed after each request regardless of whether an error occurs.
    - weather_api.py -- Handles integration with the external OpenWeatherMap service. get_weather_for_city performs a single async request to fetch current weather data for one city. create_temperature_from_list takes a list of cities from the database, fetches weather data for all of them concurrently using asyncio.gather, and stores a new Temperature record for each city that returned a successful response.
    - main.py -- Application entry point. Creates the FastAPI app instance and registers the routers from each API module (city_router and temp_router), so their endpoints become part of the application.
