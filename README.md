# City & Temperature API (FastAPI)

FastAPI application that:
- manages **cities** (CRUD)
- fetches and stores **current temperatures** for all cities

## Tech Stack
- FastAPI  
- SQLAlchemy  
- SQLite  
- httpx  
- Uvicorn  

## Project Structure
```
app/
  main.py
  database.py
  models.py
  schemas.py
  crud.py
  routers/
    cities.py
    temperatures.py
  services/
    weather.py
```

## Setup & Run

### 1. Create virtual environment and install dependencies
```bash
python -m venv .venv
source .venv/bin/activate    # macOS/Linux
# .venv\Scripts\activate    # Windows

pip install fastapi uvicorn sqlalchemy httpx
```

### 2. Run the server
```bash
uvicorn app.main:app --reload
```

API will be available at:
- Swagger UI: http://127.0.0.1:8000/docs  
- OpenAPI: http://127.0.0.1:8000/openapi.json  

### Database
The project uses SQLite database:
```
sqlite:///./app.db
```
Tables are created automatically on startup.

## API Endpoints

### Cities
- `POST /cities` — create city  
- `GET /cities` — list all cities  
- `GET /cities/{city_id}` — get one city  
- `PUT /cities/{city_id}` — update city  
- `DELETE /cities/{city_id}` — delete city  

Example:
```bash
curl -X POST "http://127.0.0.1:8000/cities" \
-H "Content-Type: application/json" \
-d '{"name":"London","additional_info":"UK"}'
```

### Temperatures
- `POST /temperatures/update` — fetch temperature for all cities and save to DB  
- `GET /temperatures` — list all temperature records  
- `GET /temperatures?city_id={city_id}` — list records for one city  

Example:
```bash
curl -X POST "http://127.0.0.1:8000/temperatures/update"
```

## Design Notes

### Weather Provider
The application uses **Open-Meteo API**:
1. City name is converted to latitude and longitude  
2. Current temperature is requested using coordinates  

No API key is required.

### Concurrency Safety
Temperature fetching is done asynchronously using `asyncio.gather`.  
Database writes are performed **after all async tasks finish**, inside a single transaction.

This avoids sharing a SQLAlchemy `Session` between concurrent tasks and prevents race conditions.

## Assumptions
- City names are unique  
- Temperature is stored in Celsius  
- If one city fails to fetch temperature, other cities are still processed  
- SQLite is used for simplicity  
