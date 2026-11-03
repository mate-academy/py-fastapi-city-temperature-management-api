City Temperature API

A FastAPI application that manages cities and stores the history of their current temperatures.

It consists of two parts (apps):

cities: CRUD API for city data.
temperatures: fetches the current temperature for every city in the database from an online service, stores it, and exposes the history.
Tech stack
Python 3.10+
FastAPI
SQLAlchemy 2.0 + SQLite
httpx (async HTTP client)
Open-Meteo as the weather source (free, no API key)
Project structure
city_temperature/
├── app/
│   ├── main.py            # app creation, routers, table creation on startup
│   ├── database.py        # engine, SessionLocal, Base
│   ├── dependencies.py    # get_db dependency
│   ├── cities/
│   │   ├── models.py      # SQLAlchemy City model
│   │   ├── schemas.py     # Pydantic schemas
│   │   ├── crud.py        # database operations
│   │   └── router.py      # /cities endpoints
│   └── temperatures/
│       ├── models.py      # SQLAlchemy Temperature model
│       ├── schemas.py     # Pydantic schemas
│       ├── crud.py        # database operations
│       ├── service.py     # async fetching from Open-Meteo
│       └── router.py      # /temperatures endpoints
├── requirements.txt
└── README.md
How to run
bash
# 1. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start the server
uvicorn app.main:app --reload

The API is available at http://127.0.0.1:8000 and the interactive documentation (Swagger UI) at http://127.0.0.1:8000/docs.

The SQLite database file app.db and all tables are created automatically on the first start.

Endpoints
Cities
Method	Path	Description
POST	/cities	Create a city
GET	/cities	List all cities
GET	/cities/{city_id}	Get a city
PUT	/cities/{city_id}	Update a city (partial update)
DELETE	/cities/{city_id}	Delete a city
Temperatures
Method	Path	Description
POST	/temperatures/update	Fetch current temperatures for all cities and store
GET	/temperatures	List all temperature records
GET	/temperatures/?city_id={id}	List temperature records for one city
Example
bash
curl -X POST http://127.0.0.1:8000/cities \
  -H "Content-Type: application/json" \
  -d '{"name": "Kyiv", "additional_info": "Capital of Ukraine"}'

curl -X POST http://127.0.0.1:8000/temperatures/update
curl http://127.0.0.1:8000/temperatures/?city_id=1
Design choices
Two separate apps (cities, temperatures), each with its own models, schemas, CRUD layer and router, following the FastAPI "bigger applications" structure. Routers contain only HTTP logic, database operations live in crud.py, and external API calls live in service.py.
Dependency injection is used for the database session (get_db) and for loading a city or returning 404 (get_city_or_404), so route handlers stay short and the logic is not duplicated.
Separate SQLAlchemy models and Pydantic schemas, so the API contract is independent from the database layout. Update uses a separate schema with all optional fields and exclude_unset=True for partial updates.
Async temperature fetching: httpx.AsyncClient with asyncio.gather requests all cities concurrently, so the update time does not grow linearly with the number of cities.
Graceful error handling:
404 for unknown cities, 409 for duplicate city names;
if the weather service fails for some cities, the remaining cities are still saved and the failed city names are returned in the failed field;
if it fails for all cities, the API returns 502.
Cascade delete: deleting a city also deletes its temperature history.
Assumptions and simplifications
City names are unique.
Open-Meteo has no lookup by city name for forecasts, so each city is first resolved to coordinates through its geocoding API (the first match is used). For ambiguous names (e.g. "Springfield") the result may not be the city you expect.
Temperatures are stored in °C, and date_time is the time of recording in UTC.
SQLAlchemy is used synchronously with SQLite, since the database is local and fast. Only network I/O (the weather requests) is asynchronous.
No migrations (Alembic) and no authentication; tables are created on startup with Base.metadata.create_all.
Every call to POST /temperatures/update adds new records, so the table works as a history and old records are never overwritten.
No pagination on GET /temperatures; GET /cities supports skip/limit.