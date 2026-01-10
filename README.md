# City Temperature Management API

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.68.0-009688.svg?logo=fastapi)](https://fastapi.tiangolo.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-1.4.0-red.svg)](https://www.sqlalchemy.org/)

A FastAPI application for managing city data and their temperature records. The application provides a REST API for CRUD operations with cities and stores temperature history data.

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- SQLite (included in Python)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Vasyl-Ch/py-fastapi-city-temperature-management-api.git
   cd py-fastapi-city-temperature-management-api
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Environment Setup

Create a `.env` file in the project root based on the example:

```bash
cp .env.example .env
```

### Running the Application

1. Apply database migrations:
   ```bash
   alembic upgrade head
   ```

2. Start the development server:
   ```bash
   uvicorn main:app --reload
   ```

3. Open API documentation in your browser:
   - Swagger UI: http://127.0.0.1:8000/docs
   - ReDoc: http://127.0.0.1:8000/redoc

## 🛠️ API Endpoints

### Cities

- `GET /cities` - Get a list of all cities
- `POST /cities` - Create a new city
- `GET /cities/{city_id}` - Get city details
- `PUT /cities/{city_id}` - Update city information
- `DELETE /cities/{city_id}` - Delete a city

### Temperatures

- `GET /temperatures` - Get all temperature records
- `GET /temperatures?city_id={city_id}` - Get temperature for a specific city
- `POST /temperatures/update` - Update temperatures for all cities

## 🏗️ Project Structure

```
.
├── alembic/              # Database migrations
├── city/                 # Cities module
│   ├── __init__.py
│   ├── crud.py          # CRUD operations for cities
│   ├── models.py        # SQLAlchemy models
│   ├── router.py        # FastAPI routers
│   └── schemas.py       # Pydantic schemas
├── services/            # External services
│   ├── __init__.py
│   └── get_weather.py   # Weather data service
├── temperature/         # Temperatures module
│   ├── __init__.py
│   ├── crud.py         # CRUD operations for temperatures
│   ├── models.py       # SQLAlchemy models
│   ├── router.py       # FastAPI routers
│   └── schemas.py      # Pydantic schemas
├── .env.example        # Configuration example
├── alembic.ini         # Alembic configuration
├── database.py         # Database setup
├── dependencies.py     # FastAPI dependencies
├── main.py            # Application entry point
├── requirements.txt   # Project dependencies
└── settings.py        # Application settings
```

## 🔍 Features

- Complete REST API for managing cities and temperature data
- Asynchronous weather data fetching from external API
- Data validation using Pydantic
- Automatic API documentation (Swagger UI and ReDoc)
- Database migrations with Alembic
- Configuration via environment variables

## 📝 Design Decisions and Assumptions

1. **Temperature Storage**: Temperatures are stored in the database with city reference and timestamp.
2. **External API**: OpenWeatherMap API is used to fetch current temperature data.
3. **Asynchronous Operations**: All I/O operations are performed asynchronously for better performance.
4. **Data Validation**: All input data is validated using Pydantic.
5. **Error Handling**: Centralized error handling with clear error messages.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
