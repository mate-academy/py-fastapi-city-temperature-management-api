# City Temperature Management API

FastAPI application that manages city data and their corresponding temperature data.

## Features

- CRUD operations for managing cities
- Temperature updates from WeatherAPI.com
- Temperature history tracking
- OpenAPI documentation

## Requirements

- Python 3.12+
- Poetry for dependency management
- WeatherAPI.com API key

## Installation

1. Clone the repository
```bash
git clone https://github.com/vladyslav-tmf/py-fastapi-city-temperature-management-api.git
cd py-fastapi-city-temperature-management-api
```
2. Install dependencies using Poetry:
```bash
poetry install
```
3. Create `.env` file with your WeatherAPI.com API key:
```bash
WEATHER_API_KEY=your_api_key_here
WEATHER_API_BASE_URL=your_weather_api_base_url # Optional
```

## Running the Application

1. Activate Poetry environment:
```bash
poetry shell
```

2. Run the application:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`
OpenAPI documentation will be available at `http://localhost:8000/docs`

## API Endpoints

### Cities

- `POST /cities/` - Create a new city
  ```json
  {
    "name": "London",
    "additional_info": "Capital of UK"
  }
  ```

- `GET /cities/` - Get list of cities
- `GET /cities/{city_id}` - Get city details
- `PUT /cities/{city_id}` - Update city
- `DELETE /cities/{city_id}` - Delete city

### Temperatures

- `GET /temperatures/` - Get temperature history
- `GET /temperatures/?city_id={city_id}` - Get temperature history for specific city
- `POST /temperatures/update/` - Update temperatures for all cities

## Project Structure

```
py-fastapi-city-temperature-management-api/
│
├── app/
│   ├── __init__.py
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py
│   ├── database/
│   │   ├── __init__.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── city.py
│   │   │   └── temperature.py
│   │   ├── session.py
│   │   └── __init__.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── city.py
│   │   └── temperature.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── city.py
│   │   └── temperature.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── weather.py
│   └── main.py
│
├── .gitignore
├── pyproject.toml
└── README.md
```

## Design Choices

1. **SQLite Database**: Simple and portable, perfect for demonstration
2. **Modular Structure**: Separation of concerns between models, schemas, and business logic
3. **Error Handling**: Comprehensive error handling for API requests and database operations
4. **Type Safety**: Full type hints coverage for better code quality

## Assumptions and Simplifications

1. Using SQLite instead of a production-grade database
2. No authentication/authorization implemented
3. Simple error logging (print statements)
4. All temperatures are in Celsius
5. WeatherAPI.com as the only weather data provider
6. The controller and CRUD logic are not separated intentionally for simplicity.
