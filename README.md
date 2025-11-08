# City Temperature Management API

REST API for managing cities and their temperature records with automatic data fetching from online sources.

## 📋 Table of Contents

- [Description](#description)
- [Technologies](#technologies)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Project Structure](#project-structure)
- [Usage Examples](#usage-examples)

## 📝 Description

The API allows you to:
- Manage cities (CRUD operations)
- Automatically fetch current temperature for all cities
- Store temperature history records
- Filter temperature data by city

## 🛠 Technologies

- **FastAPI** - modern web framework for building APIs
- **SQLAlchemy** (async) - ORM for database operations
- **Pydantic** - data validation
- **SQLite** (aiosqlite) - database
- **Alembic** - database migrations
- **httpx** - asynchronous HTTP requests
- **wttr.in API** - weather data source

## 📦 Installation

### Requirements

- Python 3.10+
- pip

### Installation Steps

1. Clone the repository:
```bash
git clone <repository-url>
cd py-fastapi-city-temperature-management-api
```

2. Create a virtual environment:
```bash
python -m venv .venv
```

3. Activate the virtual environment:

**Windows:**
```bash
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
source .venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

### requirements.txt
```
fastapi
uvicorn[standard]
sqlalchemy
aiosqlite
alembic
pydantic
httpx
```

5. Run database migrations:
```bash
alembic upgrade head
```

## 🚀 Running the Application

Start the development server:
```bash
uvicorn main:app --reload
```

The API will be available at: `http://localhost:8000`

Interactive documentation (Swagger UI): `http://localhost:8000/docs`

Alternative documentation (ReDoc): `http://localhost:8000/redoc`

## 🌐 API Endpoints

### Cities

#### Create a City
```http
POST /cities/
Content-Type: application/json

{
  "name": "Kyiv",
  "additional_info": "Capital of Ukraine"
}
```

**Response (201):**
```json
{
  "id": 1,
  "name": "Kyiv",
  "additional_info": "Capital of Ukraine"
}
```

#### Get All Cities
```http
GET /cities/
```

**Response (200):**
```json
[
  {
    "id": 1,
    "name": "Kyiv",
    "additional_info": "Capital of Ukraine"
  },
  {
    "id": 2,
    "name": "Lviv",
    "additional_info": "Western Ukraine"
  }
]
```

#### Get City by ID
```http
GET /cities/{id}
```

**Response (200):**
```json
{
  "id": 1,
  "name": "Kyiv",
  "additional_info": "Capital of Ukraine"
}
```

#### Update City
```http
PUT /cities/{id}
Content-Type: application/json

{
  "name": "Kyiv",
  "additional_info": "Capital and largest city of Ukraine"
}
```

**Response (200):**
```json
{
  "id": 1,
  "name": "Kyiv",
  "additional_info": "Capital and largest city of Ukraine"
}
```

#### Delete City
```http
DELETE /cities/{id}
```

**Response (204):** No Content

### Temperatures

#### Update Temperatures for All Cities
```http
POST /temperatures/update
```

Automatically fetches current temperature for all cities from wttr.in API and stores in database.

**Response (200):**
```json
{
  "message": "Successfully updated temperatures for 3 cities",
  "updated_cities": 3,
  "temperatures_added": 3
}
```

#### Get All Temperature Records
```http
GET /temperatures/
```

**Response (200):**
```json
[
  {
    "id": 1,
    "city_id": 1,
    "date_time": "2025-11-08T14:30:00",
    "temperature": 5.2
  },
  {
    "id": 2,
    "city_id": 2,
    "date_time": "2025-11-08T14:30:00",
    "temperature": 3.8
  }
]
```

#### Get Temperatures for Specific City
```http
GET /temperatures/?city_id=1
```

**Response (200):**
```json
[
  {
    "id": 1,
    "city_id": 1,
    "date_time": "2025-11-08T14:30:00",
    "temperature": 5.2
  },
  {
    "id": 5,
    "city_id": 1,
    "date_time": "2025-11-08T16:00:00",
    "temperature": 6.1
  }
]
```

## 📁 Project Structure

```
py-fastapi-city-temperature-management-api/
├── alembic/                    # Database migrations
│   ├── versions/
│   └── env.py
├── config/                     # Configuration
│   └── dependencies.py         # Dependency injection
├── crud/                       # CRUD operations
│   ├── city.py
│   └── temperature.py
├── database/                   # Database setup
│   └── engine.py
├── models/                     # SQLAlchemy models
│   └── entities.py
├── routes/                     # API routes
│   ├── city.py
│   └── temperature.py
├── schemas/                    # Pydantic schemas
│   ├── city.py
│   └── temperature.py
├── .gitignore
├── alembic.ini                 # Alembic configuration
├── main.py                     # Entry point
├── README.md
├── requirements.txt
└── weather.db                  # SQLite database
```

## 💡 Usage Examples

### Python (httpx)

```python
import httpx
import asyncio

async def main():
    async with httpx.AsyncClient() as client:
        # Create a city
        response = await client.post(
            "http://localhost:8000/cities/",
            json={"name": "Vinnytsia", "additional_info": "Central Ukraine"}
        )
        city = response.json()
        print(f"Created city: {city}")
        
        # Update temperatures
        response = await client.post("http://localhost:8000/temperatures/update")
        result = response.json()
        print(f"Updated temperatures: {result}")
        
        # Get temperatures for city
        response = await client.get(
            f"http://localhost:8000/temperatures/?city_id={city['id']}"
        )
        temperatures = response.json()
        print(f"Temperatures: {temperatures}")

asyncio.run(main())
```

### cURL

```bash
# Create a city
curl -X POST "http://localhost:8000/cities/" \
  -H "Content-Type: application/json" \
  -d '{"name": "Odesa", "additional_info": "Southern Ukraine"}'

# Update temperatures
curl -X POST "http://localhost:8000/temperatures/update"

# Get all temperatures
curl "http://localhost:8000/temperatures/"

# Get temperatures for city with ID=1
curl "http://localhost:8000/temperatures/?city_id=1"
```

### JavaScript (fetch)

```javascript
// Create a city
const createCity = async () => {
  const response = await fetch('http://localhost:8000/cities/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      name: 'Kharkiv',
      additional_info: 'Eastern Ukraine'
    })
  });
  const city = await response.json();
  console.log('Created city:', city);
};

// Update temperatures
const updateTemperatures = async () => {
  const response = await fetch('http://localhost:8000/temperatures/update', {
    method: 'POST'
  });
  const result = await response.json();
  console.log('Update result:', result);
};

// Get temperatures
const getTemperatures = async (cityId) => {
  const url = cityId 
    ? `http://localhost:8000/temperatures/?city_id=${cityId}`
    : 'http://localhost:8000/temperatures/';
  const response = await fetch(url);
  const temperatures = await response.json();
  console.log('Temperatures:', temperatures);
};
```

## 🔧 Configuration

### Database

SQLite is used by default. To change the database, edit `database/engine.py`:

```python
# PostgreSQL
SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://user:password@localhost/dbname"

# MySQL
SQLALCHEMY_DATABASE_URL = "mysql+aiomysql://user:password@localhost/dbname"
```

### Weather API

The project uses the free wttr.in API. To use other services (OpenWeatherMap, WeatherAPI), edit the `fetch_temperature_for_city` function in `crud/temperature.py`.

## 📊 Data Models

### City
```python
{
  "id": int,                    # Unique identifier
  "name": str,                  # City name (unique)
  "additional_info": str | None # Additional information
}
```

### Temperature
```python
{
  "id": int,           # Unique identifier
  "city_id": int,      # City ID
  "date_time": str,    # Date and time of record (ISO format)
  "temperature": float # Temperature in degrees Celsius
}
```

## 🐛 Error Handling

The API returns standard HTTP status codes:

- **200** - Successful request
- **201** - Resource created
- **204** - Successfully deleted (no content)
- **400** - Validation error or duplicate
- **404** - Resource not found
- **422** - Pydantic validation error
- **500** - Internal server error

Error example:
```json
{
  "detail": "City not found."
}
```
