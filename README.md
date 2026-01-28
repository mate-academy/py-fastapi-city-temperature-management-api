# City Temperature API

FastAPI application for managing cities and storing historical temperature data fetched from an external weather API

---

## Features

* CRUD API for managing cities
* CRUD + list API for temperature records
* Async endpoint to fetch current temperature for all cities
* SQLite database with SQLAlchemy 2.0
* Pydantic v2 schemas
* Automatic API documentation via Swagger

---

## Tech Stack

* Python 3.10+
* FastAPI
* SQLAlchemy 2.0
* Pydantic v2
* SQLite
* httpx (async HTTP client)

---

## Project Structure

```
city_temperature_api/
│
├── app/
│   ├── main.py
│   ├── core/
│   │   └── database.py
│   ├── dependencies/
│   │   └── db.py
│   ├── models/
│   │   ├── city.py
│   │   └── temperature.py
│   ├── schemas/
│   │   ├── city.py
│   │   └── temperature.py
│   ├── routers/
│   │   ├── cities.py
│   │   └── temperatures.py
│   └── services/
│       └── weather.py
│
├── README.md
├── requirements.txt
└── app.db
```

---

## Installation & Run

### 1. Clone repository

```bash
git clone https://github.com/VYGAKOOL/py-fastapi-city-temperature-management-api
cd city_temperature_api
```

### 2. Create virtual environment

```bash
python -m venv venv
```

### 3. Activate virtual environment

**Windows:**

```bash
venv\Scripts\activate
```

**Linux / macOS:**

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run application

```bash
uvicorn app.main:app --reload
```

---

## API Documentation

After starting the server, open:

* Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## API Endpoints

### Cities

* `POST /cities` – create city
* `GET /cities` – list all cities
* `GET /cities/{id}` – get city by ID
* `PUT /cities/{id}` – update city (returns 400 if name already exists)
* `DELETE /cities/{id}` – delete city

### Temperatures

* `POST /temperatures` – create temperature record manually
* `GET /temperatures` – list all temperature records
* `GET /temperatures?city_id={id}` – list temperatures for a city
* `GET /temperatures/{id}` – get temperature record by ID
* `DELETE /temperatures/{id}` – delete temperature record

### Temperature Update

* `POST /temperatures/update` – fetch current temperature for all cities and store it in the database

---

## Design Choices

* **SQLAlchemy 2.0 style** (`Mapped`, `mapped_column`) is used for modern ORM patterns
* **Pydantic v2** with `ConfigDict(from_attributes=True)` for ORM compatibility
* **SQLite** chosen for simplicity and ease of setup
* **Open-Meteo API** used for weather data (no API key required)
* Temperature fetching implemented as **async** using `httpx`
* All city and temperature updates check for data integrity to avoid crashes

---

## Assumptions & Simplifications

* City temperature is fetched using the **city name** via Open-Meteo geocoding API
* No authentication or authorization implemented
* No database migrations (tables are created automatically on startup)
* Time is stored in **UTC**
* API responses are accessed safely using `.get()` to prevent KeyErrors
* Updating a city name checks for duplicates and returns a 400 error if the name exists

---

## Notes

This project is intended as a clean, minimal implementation focused on correctness, modern FastAPI practices, and readability.
