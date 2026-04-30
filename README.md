## FastAPI City Temperature Management API

The application consists of two main components (apps):

1. A CRUD (Create, Read, Update, Delete) API for managing city data.
2. An API that fetches current temperature data for all cities in the database and stores this data in the database.

## What apps do

### City CRUD API
- `POST /cities`: Create a new city.
- `GET /cities`: Get a list of all cities.
- `GET /cities/{city_id}`: Get the details of a specific city.
- `PUT /cities/{city_id}`: Update the details of a specific city.
- `DELETE /cities/{city_id}`: Delete a specific city.

### Temperature API
- `POST /temperatures/update` fetch current temperature for all cities in the database. 
- Store temperature history.
- `GET /temperatures`: Get a list of all temperature records.
- `GET /temperatures/?city_id={city_id}`: Get the temperature records for a specific city.

## Tech Stack
- FastApi
- SQLAlchemy
- Alembic
- Pydantic
- httpx

## How to run application

### 1. Clone repository
```
git clone https://github.com/B0hdanR/py-fastapi-city-temperature-management-api.git
cd py-fastapi-city-temperature-management-api
```
### 2. Create virtual environment and install dependencies
```
python -m venv venv
venv\Scripts\activate (on Windows)
source venv/bin/activate (on macOS)
pip install -r requirements.txt
```
### 3. Run migrations
```
alembic upgrade head
```
### 4. Run application
```
uvicorn app.main:app --reload
```
### 5. Open in browser
http://127.0.0.1:8000/docs

## External APIs
In this project, two external APIs are used together to fetch temperature data.
- Nominatim (https://nominatim.org/)

The weather API requires **latitude and longitude**, but users provide only **city names**.

So Nominatim API was used to convert a city name into coordinates.

Example of use: (https://nominatim.openstreetmap.org/search?q=Germany&format=json)

- Open-Meteo (https://api.open-meteo.com/v1/forecast)

After receiving the coordinates, the Open-Meteo API was used to obtain the temperature.

### Optimization

- Temperature updates use: `asyncio.gather()`

This allows fetching data for multiple cities simultaneously instead of one by one.

- Coordinates are fetched once and stored

There is no need to find the country coordinates again every time the temperature is updated, which speeds up the application.
