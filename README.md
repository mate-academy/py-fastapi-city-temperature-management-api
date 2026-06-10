# FastAPI City & Temperature API

## Overview

This project is a FastAPI application for managing city data and storing temperature history for those cities.

The application includes two main parts:

- **City CRUD API**
  - Create a city
  - Get all cities
  - Get a single city
  - Update a city
  - Delete a city

- **Temperature API**
  - Fetch current temperature for all cities from an external online service
  - Save temperature records into the database
  - Get all saved temperature records
  - Filter temperature history by `city_id`

The project uses:

- **FastAPI** for the web API
- **SQLAlchemy** for database interaction
- **SQLite** as the default database
- **Pydantic** for data validation
- **Async HTTP requests** for fetching temperature data from an external API
- **OpenWeater** for fetching API data
### Cities

- `POST /cities` — create a new city
- `GET /cities` — get all cities
- `GET /cities/{city_id}` — get city by ID
- `PUT /cities/{city_id}` — update city by ID
- `DELETE /cities/{city_id}` — delete city by ID

### Temperatures

- `POST /temperatures/update` — fetch and save current temperature for all cities
- `GET /temperatures` — get all temperature records
- `GET /temperatures?city_id={city_id}` — get temperature records for one city

---

## Requirements

Before running the project, make sure you have:

- **Python 3.10+**
- **pip**
- Internet access for temperature API requests

---

## Setup Instructions

### 1. Create a virtual environment

#### On Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### On macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 2. Install dependencies

Install all required packages from `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

### 3. Create environment variables

Create a `.env` file inside the `app/db` directory:

```bash
app/db/.env
```

Add the following variables:

```env
API_KEY=your_temperature_api_key
DATABASE_URL=sqlite:///./weather.db
```

### Environment variables description

- `API_KEY` — API key for the external weather/temperature service
- `DATABASE_URL` — database connection string

Example for SQLite:

```env
DATABASE_URL=sqlite:///./weather.db
```



## Run the Application

Run the project using `main.py`:

```bash
python app/main.py
```

## API Documentation

After starting the server, open:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`


## Example `.env`

```env
API_KEY=1234567890abcdef
DATABASE_URL=sqlite:///./weather.db
```

## Notes

- Make sure the `.env` file exists before running the application.
- Make sure your `API_KEY` is valid.
- If you use SQLite, the database file will be created automatically if it does not exist.

## Summary

This project provides a clean FastAPI application with:

- city CRUD operations
- temperature history storage
- async temperature updates from an external service
- SQLite database support
- environment-based configuration
- auto-generated API documentation