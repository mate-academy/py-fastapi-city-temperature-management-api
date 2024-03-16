# City-temperature-api

## How to run the application

```bash
# Clone the repository
git clone https://github.com/antonnech2309/py-fastapi-city-temperature-management-api.git

# Install the required packages
pip install -r requirements.txt

# Make migrations
alembic upgrade head

# Run the application
uvicorn main:app --reload
```

Also you need to register on [weatherapi.com](https://www.weatherapi.com/) and get your API key. Then you need to 
create a `.env` file in the root of the project and add there your 
API key like in `.env-sample` file.

## Design choices

- I used FastAPI as the web framework because it is easy to use and has a lot of features.
- I used SQLite as the database because it is easy to use and does not require any additional setup.
- I used SQLAlchemy as the ORM because it is easy to use and integrates well with FastAPI.
- I used Pydantic for data validation and serialization because it is easy to use and integrates well with FastAPI.
- I used Alembic for database migrations because it is easy to use and integrates well with SQLAlchemy.

## Assumptions and simplifications

- I used the weatherapi.com API to fetch the current temperature data for all cities in the database.