## City Temperature Management API

A FastAPI application for managing city data and their corresponding temperature records using a weather API (OpenWeatherMap).

### Features

- ✅ **CRUD API for Cities** — Add, view, update, and delete cities.
- 🌡️ **Temperature History API** — Fetch and store current temperatures for all cities.
- 🔍 **Filtering** — Get temperature history per city.
- ⚡ **Async Data Fetching** — Non-blocking temperature updates using `httpx`.
- 🧩 **Modular Structure** — Clear separation of routers, schemas, models, CRUD logic, and dependencies.

### 🏗️ Project Structure
```
├── main.py # FastAPI app entry point
├── models.py # SQLAlchemy models
├── schemas.py # Pydantic schemas
├── crud/
│ ├── city.py # City database logic
│ └── temperature.py # Temperature database logic
├── routers/
│ ├── cities.py # /cities endpoints
│ └── temperatures.py # /temperatures endpoints
├── database.py # DB engine and session config
├── dependencies.py # DB dependency for injection
├── .env # API key configuration
└── README.md # Documentation
```

## 🚀 Getting Started

### ✅ Prerequisites

- Python 3.10+
- OpenWeatherMap API key — [Get your key here](https://openweathermap.org/api)

### 📥 Installation

1. **Clone the repo**

```bash
  git clone https://github.com/VladimirDolhyi/py-fastapi-city-temperature-management-api.git
  cd py-fastapi-city-temperature-management-api
```

2. **Create a virtual environment and activate it**

```bash
  python -m venv venv
  source venv/bin/activate      On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
  pip install -r requirements.txt
```

4. **Set up your .env file**

```bash
  WEATHER_API_KEY=your_openweathermap_api_key_here
```

5. **Run the application**

```bash
  uvicorn main:app --reload
```

6. **Open API Docs**

```bash
  Visit: http://localhost:8000/docs
```
### 🔧 API Endpoints
```
🏙️ Cities
Method	Endpoint	Description
POST	/cities/	Create a new city
GET	/cities/	Get all cities
GET	/cities/{city_id}	Get a specific city (optional)
PUT	/cities/{city_id}	Update a city (optional)
DELETE	/cities/{city_id}	Delete a city
🌡️ Temperatures
Method	Endpoint	Description
POST	/temperatures/update	Fetch and store current temps for cities
GET	/temperatures/	Get all temperature records
GET	/temperatures/?city_id={id}	Filter temperature records by city
```

### 🧪 Example Usage

#### Create a city
```
POST /cities/
{
  "name": "Kyiv",
  "additional_info": "Hero city"
}
```

#### Update temperatures
```
POST /temperatures/update
```

#### Get temperature history for a city
```
GET /temperatures/?city_id=1
```