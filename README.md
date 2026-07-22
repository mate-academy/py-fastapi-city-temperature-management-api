# Temperature Management API

## How to run
1. Install all dependencies `pip install -r requirements.txt`.
2. Add `.env` file according to `.env.sample` template. Get an API key from  [Free Weather API](https://www.weatherapi.com/).
3. Apply migrations `alembic upgrade head`.
4. Run the server. To access to all endpoints, use `/docs/` url.

## Explanation of my design choices
1. I made a module `utils.py` to store functions that help to reduce code duplication in view functions, especially to handle `HTTPException`.
2. I added dependency injection for database session and query parameter `city_id` to reduce duplication parameters in view functions. 
3. I used resource [Free Weather API](https://www.weatherapi.com/) to get information about weather by city. \
And to make the code be asynchronously I chose the module `httpx`.


## Simplifications I made
The only simplification I made is I didn't implement handling error logic when application is trying to get information about weather by city name that does not exist.
