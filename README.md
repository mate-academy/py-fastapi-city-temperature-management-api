## City temperature management API

### Description
#### This application that manages city data and their corresponding temperature data.

### Features
- A CRUD (Create, Read, Update, Delete) API for managing city data
- Check whether a city name exists in the WeatherAPI
- Update temperature values for all cities in the database and save them
- Filter temperature values by city_id

### Technologies

- Python
- FastAPI
- SQLite

### Installation

#### 1. Clone the project

```bash
git clone https://github.com/apmaz/py-fastapi-city-temperature-management-api.git
cd py-fastapi-city-temperature-management-api
```

#### 2. Rename `.env.sample` to `.env` and fill in the values:

```bash
mv .env.sample .env

#WEATHER_API
WEATHER_API_KEY=weather_api_key
```
### Documentation
Here are links to the automatically generated API documentation using Swagger. You can explore available endpoints, their parameters, and example requests and responses:

- Swagger: [http://127.0.0.1:8000/docs/](http://127.0.0.1:8000/docs/)  

### Models

City API models:
- `id`: a unique identifier for the city.
- `name`: the name of the city.
- `additional_info`: any additional information about the city.

City API endpoints:
- `POST /cities`: Create a new city.
- `GET /cities`: Get a list of all cities.
- `GET /cities/{city_id}`: Get the details of a specific city.
- `PUT /cities/{city_id}`: Update the details of a specific city.
- `DELETE /cities/{city_id}`: Delete a specific city.


Temperature API models:
- `id`: a unique identifier for the temperature record.
- `city_id`: a reference to the city.
- `date_time`: the date and time when the temperature was recorded.
- `temperature`: the recorded temperature.

Temperature API endpoints:
- `POST /temperatures/update` update temperature for all cities in the database.
- `GET /temperatures`: Get a list of all temperature records.
- `GET /temperatures/?city_id={city_id}`: Get the temperature records for a specific city.
