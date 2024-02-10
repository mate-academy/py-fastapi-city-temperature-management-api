# City Temperature Manager

FastAPI application that manages city data and their corresponding temperature data. It consists of two main features:

1. A CRUD (Create, Read, Update, Delete) API for managing city data.
2. An API that fetches current temperature data for all cities in the database and stores this data in the database, providing the history of all temperature data.


### Installing using GitHub

   ```bash
   git clone https://github.com/lobodInI/py-fastapi-city-temperature-management-api.git
   cd py-fastapi-city-temperature-management-api
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
   Configure Environment Variables:
- Create a .env file in the project root.
- Make sure it includes all the variables listed in the .env.sample file.
- Ensure that the variable names and values match those in the sample file.
   ```bash
   set API_KEY=API_KEY
   alembic upgrade head
   ```
  
Run the Server:
```bash
 uvicorn main:app --reload
```

### City CRUD API

Manages city data with the following endpoints:
- `POST /cities/`: Create a new city.
- `GET /cities/`: Get a list of all cities.
- `GET /cities/{city_id}/`: Get the details of a specific city (optional).
- `PUT /cities/{city_id}/`: Update the details of a specific city (optional).
- `DELETE /cities/{city_id}/`: Delete a specific city.


### Temperature API

Fetches and provides temperature data with the following endpoints:

- `GET /update_temperature/`: Fetch the current temperature for all cities in the database and store the data.
- `GET /temperatures/`: Get a list of all temperature records.
- `GET /temperatures/{city_id}/`: Get the temperature records for a specific city.