# City Temperature Management API

FastAPI application that manages city data and temperature records
using OpenWeatherMap API.

## Technologies

- FastAPI
- SQLAlchemy + SQLite
- OpenWeatherMap API
- httpx (async HTTP client)
- python-dotenv

## Project Structure
```
├── main.py
├── database.py
├── city/
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   └── router.py
├── temperature/
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   └── router.py
└── .env
```

## Setup

1. Clone the repository:
```
   git clone <repo-url>
   cd py-fastapi-city-temperature-management-api
```

2. Create virtual environment:
```
   python3 -m venv venv
   source venv/bin/activate
```

3. Install dependencies:
```
   pip install fastapi uvicorn sqlalchemy httpx python-dotenv
```

4. Create `.env` file:
```
   WEATHER_API_KEY=your_openweathermap_api_key
```

5. Run the application:
```
   uvicorn main:app --reload
```

6. Open Swagger UI:
```
   http://127.0.0.1:8000/docs
```

## API Endpoints

### Cities
- `POST /cities/` - Create a new city
- `GET /cities/` - Get all cities
- `GET /cities/{city_id}` - Get city by ID
- `PUT /cities/{city_id}` - Update city
- `DELETE /cities/{city_id}` - Delete city

### Temperatures
- `POST /temperatures/update` - Fetch current temperatures for all cities
- `GET /temperatures/` - Get all temperature records
- `GET /temperatures/?city_id={id}` - Get temperatures for specific city

## Design Choices

- SQLite for simplicity
- Single `db.commit()` after processing all cities for efficiency
- `HTTPException` with 400 status for duplicate city names
- Async `httpx` client for fetching temperature data
- Dependency injection for database sessions

## Assumptions

- OpenWeatherMap free tier API is used
- Temperature is stored in Celsius
- City names must be unique
