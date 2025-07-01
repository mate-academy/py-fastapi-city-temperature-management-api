# Fastapi temperature-city-management api

##### This is a simple api that returns by given city id it's weather (temperature). 
##### You can also update temperature data by `/temperature/update/` endpoint.
##### There are also an opportunity to create city, update city, delete city, retrieve city/temperature and get all cities/temperatures.
##### P.S: During city creation will be created also it's temperature but with default temperature value (0). To update it you need to use update endpoint.

### How to start:
1. Install all requirements:
    `pip install -r requirements.txt`

2. Fill in the .env file by given .env.sample.
     (WeatherAPI key)

3. Run migrations and create db:
    `alembic upgrade head`

4. Run uvicorn server:
    `uvicorn main:app --reload`
