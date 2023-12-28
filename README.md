## Task Description

FastAPI application that manages city data and their corresponding temperature data.

### Setting up locally

1. Clone the repository to your PC:
- `git clone <link>`
2. Set up venv and activate it:
- `py -m venv venv`
- `source venv/Scripts/activate`
3. Install requirements:
- `pip install -r requirements.txt`
4. Create .env file from .env.sample
5. Run migrations:
- `alembic upgrade head`
6. Run the server:
- `uvicorn main:app --reload`


### Endpoints
City
1. `POST /cities` Create a new city.
2. `GET /cities` Get a list of all cities.
3. `GET /cities/{city_id}` Get the details of a specific city.
4. `PUT /cities/{city_id}` Update the details of a specific city.
5. `DELETE /cities/{city_id}` Delete a specific city.

Temperature
1. `POST /temperatures/update` Fetches the current temperature for all cities in the database from an online resource
2. `GET /temperatures`: Get a list of all temperature records.
3. `GET /temperatures/?city_id={city_id}`: Get the temperature records for a specific city.

### Design Choices
This application consists of two apps: city and temperature. Both of them are asynchronous. Endpoint for collecting temperature data was broken down into a couple of functions in utils.py for simplicity.
