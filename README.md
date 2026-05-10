# City Temperature API
___
## Description
This app stores information about cities and their temperatures in the database. The data are getting from the [Weather API](https://www.weatherapi.com/).\
The next available endpoints are:
- GET `/cities` - to see the list of all cities in the database;
- GET `/cities/{city_id}` - to the specific city by its id;
- POST `/cities` - to create a new city;
- PUT `/cities/{city_id}` - to update the specific city by its id;
- DELETE `/cities/{city_id}` - to remove the specific city by its id;
- GET `/temperatures` - to see the list of all records about temperatures;
- GET `/temperatures/?city_id={city_id}` - to see the list of records about temperatures filtered by city id;
- POST `/temperatures/update` - to add new records about temperatures in the cities in the database.
___
## Instructions
To run this application follow the next steps:
1. Register in the [Weather api](https://www.weatherapi.com/) and copy the api key;
2. Make file `.env` and add the environment variable `API_KEY` according to `.env-example`;
3. Apply migrations using a command `alembic upgrade head`;
4. Run the application using a command `python -m uvicorn app.main:app --reload`.
5. Visit the address `http://127.0.0.1:8000/docs/` to see the documentation and use all endpoints.
___
## About development
I used the service [Weather api](https://www.weatherapi.com/) because it gives more detailed information about the temperature of city and not only.\
To get the information from this service I used the external module [requests](https://requests.readthedocs.io/en/latest/) because it's very easy to make HTTP requests.
