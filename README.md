# FastAPI City Temperature Management API

This project consists of two main parts:

* A CRUD API for managing cities
* A system for fetching and storing temperature data for each city

The application uses FastAPI, SQLAlchemy, SQLite, and asynchronous HTTP requests to retrieve real-time temperature data from an online source.

___

## 🚀 Functionality
### **_1) City API_**

A city consists of:

* id — a unique identifier
* name — the name of the city
* additional_info — additional information about the city

Available endpoints:

`POST /cities` – Create a city

`GET /cities ` – Get a list of all cities

`GET /cities/{city_id}` – Get a specific city

`PUT /cities/{city_id}` – Update a city

`DELETE /cities/{city_id}` – Delete a city

### **_2) Temperature API_**

A temperature record contains:

* id — unique ID
* city_id — ID of the city (ForeignKey)
* date_time — date and time of the measurement
* temperature — recorded temperature

Endpoints:

`POST /temperatures/update` – Fetch the current temperature for all cities from an online source and store it in the database

`GET /temperatures` – Get all temperature records or filter by city_id

_**Parameters:**_

* `GET /temperatures?city_id=2` – Returns temperature records for the city with ID 2
* Supports skip and limit for pagination

___

## 🌐 Temperature Source

Temperature data is retrieved from the online service: https://wttr.in/{city}?format=j1

This service returns weather information in JSON format.

___

## 📦 Technologies

* FastAPI
* SQLAlchemy
* SQLite
* Pydantic v2
* httpx (async)
* Uvicorn

___

## 📁 Project Structure

app/

    crud/
        city.py
        temperature.py
    models/
        city.py
        temperature.py
    routers/
        city.py
        temperature.py
    schemas/
        city.py
        temperature.py
    database.py
    dependencies.py
    main.py

___

## ▶️ How to Run the Project

1. Clone the repository:

    `git clone <repo-url>`
    
    `cd py-fastapi-city-temperature-management-api`


2. Create a virtual environment:

    `python -m venv .venv`


3. Activate the environment:

    **Windows:** `.venv\Scripts\activate`
    
    **Linux / Mac:** `source .venv/bin/activate`


4. Install dependencies:

    `pip install -r requirements.txt`

    Or manually:

    `pip install fastapi uvicorn sqlalchemy pydantic httpx`


5. Start the server:

    `uvicorn app.main:app --reload`

___

## 📘 API Documentation

_After launching:_

Swagger UI: http://127.0.0.1:8000/docs

ReDoc: http://127.0.0.1:8000/redoc


#### Example Response (GET /temperatures)

```json
{
  "id": 5,
  "date_time": "2025-11-17T18:29:32.912753",
  "temperature": 6,
  "city": {
    "id": 2,
    "name": "London",
    "additional_info": "Foggy and rainy city"
  }
}
```

___

## 🧠 Design Decisions

The wttr.in service was chosen for weather data because it is:

* free
* does not require an API key
* fast
* supports JSON output

Temperature data is stored as history to:

* track changes
* allow analysis
* match the task requirements

The Pydantic models use `from_attributes = True`, enabling serialization of SQLAlchemy ORM objects.

The temperature update feature uses asynchronous HTTP calls via `httpx.AsyncClient.`
This ensures that the application remains fast and responsive even when fetching temperature data for multiple cities at once.

___

## 📝 Limitations & Assumptions

The online source returns temperatures in Celsius, which is sufficient for this task.

The city is considered unique by name, so `DBCity.name` has `unique=True`.

Additional validation (e.g., checking if the city name is valid) was not required by the task.