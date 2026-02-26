## Project Description

A FastAPI application that manages city data and their corresponding temperature data. 
The application will have two main components (apps):

1. City - for managing city data.
2. Temperature - API that fetches current temperature data for all cities in the database and stores this data in the database. Also provides a list endpoint to retrieve the history of all temperature data.

#### City endpoints
1. GET /cities/ 
2. POST /cities/
3. GET /cities/{city_id}/
4. PUT /cities/{city_id}/
5. DELETE /cities/{city_id}/ 

#### Temperature endpoints
1. GET /temperatures/
2. POST /temperatures/update
3. GET /temperatures/?city_id={city_id}


### Technologies used
- FastAPI with async endpoints
- SQLAlchemy 2.0
- async_sessionmaker
- Pydantic v2
- pydantic-settings
- Alembic async migrations
- httpx for external API calls


### How to run
- Clone the repo
- Create .venv and activate it
- Install requirements
- Create .env file with WEATHER_API_KEY and DATABASE_URL
- Run migrations
- Start the server
