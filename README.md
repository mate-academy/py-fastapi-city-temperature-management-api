# Weather API

A FastAPI application for managing city data and their corresponding temperature records with clean architecture and dependency injection.

## Features

- **City Management**: Full CRUD operations for cities
- **Temperature Tracking**: Automated temperature fetching and historical data storage
- **Clean Architecture**: Separated concerns with models, schemas, repositories, and routers
- **Dependency Injection**: Proper DI pattern for repositories
- **Async Operations**: Efficient async temperature fetching from external API
- **SQLite Database**: Local database storage with SQLAlchemy ORM
- **API Documentation**: Auto-generated interactive API docs with Swagger UI

## Project Structure

```
weather-api/
├── README.md
├── requirements.txt
└── src/
    ├── main.py            # FastAPI application entry point
    ├── dependencies.py    # Dependency injection configuration
    ├── db/
    │   ├── __init__.py
    │   ├── base.py        # SQLAlchemy base
    │   └── session.py     # Database session management
    ├── models/
    │   ├── __init__.py
    │   ├── city.py        # City SQLAlchemy model
    │   └── temperature.py # Temperature SQLAlchemy model
    ├── schemas/
    │   ├── __init__.py
    │   ├── city.py        # City Pydantic schemas
    │   └── temperature.py # Temperature Pydantic schemas
    ├── repositories/
    │   ├── __init__.py
    │   ├── city.py        # City CRUD operations
    │   └── temperature.py # Temperature CRUD operations
    └── routers/
        ├── __init__.py
        ├── city.py        # City API endpoints
        └── temperature.py # Temperature API endpoints
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup Instructions

1. **Navigate to the project directory**

```bash
cd weather-api
```

2. **Create a virtual environment (recommended)**

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

## Running the Application

### Start the server

```bash
# From the root directory
python -m uvicorn src.main:app --reload
```

Or from within src:

```bash
cd src
python main.py
```

The API will be available at:
- **Application**: http://localhost:8000
- **Interactive API docs (Swagger)**: http://localhost:8000/docs
- **Alternative API docs (ReDoc)**: http://localhost:8000/redoc

## API Endpoints

### City Endpoints

#### Create a City
```http
POST /cities
Content-Type: application/json

{
  "name": "New York",
  "additional_info": "The largest city in the USA"
}
```

#### Get All Cities
```http
GET /cities?skip=0&limit=100
```

#### Get a Specific City
```http
GET /cities/{city_id}
```

#### Update a City
```http
PUT /cities/{city_id}
Content-Type: application/json

{
  "name": "New York City",
  "additional_info": "Updated information"
}
```

#### Delete a City
```http
DELETE /cities/{city_id}
```

### Temperature Endpoints

#### Fetch and Store Current Temperatures
```http
POST /temperatures/update
```

This endpoint:
1. Retrieves all cities from the database
2. Fetches current temperature for each city from Open-Meteo API
3. Stores the temperature data with timestamp
4. Returns a summary of successful and failed updates

#### Get All Temperature Records
```http
GET /temperatures?skip=0&limit=100
```

#### Get Temperature Records for a Specific City
```http
GET /temperatures?city_id=1&skip=0&limit=100
```

## Architecture

### Clean Architecture Layers

1. **Models Layer** (`src/models/`)
   - SQLAlchemy ORM models
   - Database table definitions
   - Database-only concerns

2. **Schemas Layer** (`src/schemas/`)
   - Pydantic models for API validation
   - Request/Response schemas
   - Data transfer objects (DTOs)

3. **Repositories Layer** (`src/repositories/`)
   - Data access logic
   - CRUD operations
   - Database query encapsulation

4. **Routers Layer** (`src/routers/`)
   - HTTP endpoint definitions
   - Request handling
   - Response formatting

5. **Dependencies Layer** (`src/dependencies.py`)
   - Dependency injection configuration
   - Service locator pattern

### Design Patterns

#### Dependency Injection
- Repositories are injected via FastAPI's `Depends`
- Database sessions managed through context managers
- Promotes testability and loose coupling

```python
# Example of DI in action
@router.get("/cities")
def get_cities(repo: CityRepository = Depends(get_city_repository)):
    return repo.get_all()
```

#### Repository Pattern
- Separates business logic from data access
- Provides clean interface for database operations
- Makes testing easier with mock repositories

#### Separation of Concerns
- **Models**: Database structure (SQLAlchemy)
- **Schemas**: API contracts (Pydantic)
- **Repositories**: Data operations
- **Routers**: HTTP handling

### Technology Choices

1. **SQLite Database**
   - Lightweight and requires no separate server
   - Perfect for development and small-scale deployments
   - File-based storage (`weather.db`)

2. **Open-Meteo API**
   - Free weather API with no authentication required
   - Reliable and well-documented
   - Provides current weather data globally

3. **Async Temperature Fetching**
   - Uses `asyncio.gather()` for concurrent API calls
   - Significantly faster when fetching data for multiple cities
   - Non-blocking operations

### Data Models

#### City (Database Model)
- `id`: Auto-incrementing primary key
- `name`: Unique city name
- `additional_info`: Optional text field

#### Temperature (Database Model)
- `id`: Auto-incrementing primary key
- `city_id`: Foreign key to cities table
- `date_time`: Timestamp of when temperature was recorded
- `temperature`: Temperature value in Celsius

#### Schemas (API Models)
- `CityCreate`: For creating cities
- `CityUpdate`: For updating cities
- `CityResponse`: For returning city data
- `TemperatureCreate`: For creating temperature records
- `TemperatureResponse`: For returning temperature data

## Error Handling

The API implements proper error handling:

- **400 Bad Request**: Duplicate city names, invalid input
- **404 Not Found**: City or resource not found
- **422 Unprocessable Entity**: Validation errors
- **500 Internal Server Error**: Server-side errors

## Testing the API

### Using the Interactive Docs

1. Navigate to http://localhost:8000/docs
2. Click on any endpoint to expand it
3. Click "Try it out" button
4. Fill in the required parameters
5. Click "Execute" to make the request

### Using curl

```bash
# Create a city
curl -X POST "http://localhost:8000/cities" \
  -H "Content-Type: application/json" \
  -d '{"name":"London","additional_info":"Capital of UK"}'

# Get all cities
curl "http://localhost:8000/cities"

# Update temperatures for all cities
curl -X POST "http://localhost:8000/temperatures/update"

# Get temperature records
curl "http://localhost:8000/temperatures"

# Get temperatures for a specific city
curl "http://localhost:8000/temperatures?city_id=1"
```

## Development

### Project Guidelines

1. **Models vs Schemas**
   - Use `models/` for SQLAlchemy database models
   - Use `schemas/` for Pydantic API validation models
   - Keep them separate for clean architecture

2. **Repository Pattern**
   - All database operations go through repositories
   - Routers should never directly access the database
   - Use dependency injection for repositories

3. **Async Operations**
   - Use async/await for I/O operations
   - Keep sync operations in separate functions
   - Use `asyncio.gather()` for concurrent operations

## Assumptions and Simplifications

1. **Temperature API**
   - Uses Open-Meteo free API (no authentication needed)
   - Temperature is in Celsius
   - City names must match geocoding database for successful lookups

2. **Database**
   - SQLite is used for simplicity
   - Database file is created automatically on first run
   - No migrations system (using SQLAlchemy's `create_all`)

3. **Concurrency**
   - No rate limiting implemented for temperature API calls
   - Assumes reasonable number of cities (<100)

4. **Validation**
   - City names must be unique
   - Basic validation via Pydantic models
   - No sophisticated address parsing

5. **Security**
   - No authentication/authorization implemented
   - Suitable for development/internal use
   - Production deployment would need additional security measures

## Future Enhancements

- Add authentication and authorization
- Implement rate limiting
- Add caching for temperature data
- Store city coordinates in database to avoid repeated geocoding
- Add database migrations (Alembic)
- Add comprehensive unit and integration tests
- Add support for multiple temperature units (Fahrenheit, Kelvin)
- Implement background tasks for automatic temperature updates
- Add data visualization endpoints
- Support batch city creation
- Add logging and monitoring
- Docker containerization

## License

This project is created as a technical assessment and is free to use and modify.

## Support

For issues or questions, please refer to the API documentation at http://localhost:8000/docs
