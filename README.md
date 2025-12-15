# City Temperature Management API

FastAPI application for managing cities and storing temperature history.

---

## Task Overview

This project implements a REST API with two main parts:

1. City CRUD API to manage city data.
2. Temperature API to fetch current temperature data for all cities and store temperature history.

---

## Technology Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite
- httpx
- Uvicorn

---

## Assumptions and Simplifications

- Temperature data is fetched from the Open-Meteo public API.
- No API key is required.
- City coordinates are stored in the `additional_info` field.
- Coordinate format must be:

"lat,lon"

Example:

"51.0447,-114.0719"

- Cities without valid coordinates are skipped during temperature updates.

---

## API Endpoints

### Cities

POST /cities  
Create a new city.

GET /cities  
Get a list of all cities.

DELETE /cities/{city_id}  
Delete a city by ID.

---

### Temperatures

POST /temperatures/update  
Fetch current temperatures for all cities and store them in the database.

GET /temperatures  
Get all stored temperature records.

GET /temperatures?city_id={city_id}  
Get temperature records for a specific city.

---

## Project Structure

app/main.py  
app/database.py  
app/models.py  
app/schemas.py  
app/crud.py  
app/api/cities.py  
app/api/temperatures.py  
app/services/weather_client.py  
requirements.txt  
README.md  

---

## How to Run the Project

1. Create a virtual environment

Windows PowerShell:

py -m venv .venv  
.venv\Scripts\Activate.ps1  

Linux or macOS:

python3 -m venv .venv  
source .venv/bin/activate  

2. Install dependencies

pip install -r requirements.txt  

3. Run the application

uvicorn app.main:app --reload  

---

## API Documentation

Swagger UI is available at:

http://127.0.0.1:8000/docs

---

## Example Usage

1. Create a city

POST /cities

Request body:

{
  "name": "Calgary",
  "additional_info": "51.0447,-114.0719"
}

2. Update temperatures

POST /temperatures/update

3. Get temperature history

GET /temperatures

or

GET /temperatures?city_id=1

---

## Notes

- Temperature fetching is implemented using asynchronous HTTP requests.
- Each temperature update creates a new record, allowing temperature history tracking.

## Design choices
- Project is split into layers: API routers, CRUD/database logic, and external service client.
- SQLite is used for simplicity and fast local setup.
- SQLAlchemy ORM models represent database tables; Pydantic schemas represent request/response shapes.
- Dependency injection (`Depends(get_db)`) is used to provide one DB session per request.

## Assumptions
- External temperature data is fetched from Open-Meteo (no API key required).
- `City.additional_info` stores coordinates in the format "lat,lon" (example: "51.0447,-114.0719").
- Cities with missing/invalid coordinates are skipped during `/temperatures/update`.
