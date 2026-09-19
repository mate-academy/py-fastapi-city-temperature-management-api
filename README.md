# City Weather Management API

A FastAPI application designed to manage city data and automatically track, record, and serve historical temperature data using asynchronous external API integration.

---

## 🛠️ Features

* **City Management (CRUD):** Complete RESTful endpoints to create, read, update, and delete city records.
* **Asynchronous Weather Sync:** Fetches current temperatures concurrently for all cities stored in the database using `httpx` and `asyncio`.
* **Temperature History Tracking:** Persists historical temperature data with timestamps and offers filtered retrieval by city.
* **Database Management:** Built with SQLAlchemy ORM and SQLite, including cascade deletions for related temperature records.
* **Data Validation:** Strict schema validation powered by Pydantic v2.

---

## 🏗️ Project Structure

The project follows standard FastAPI guidelines for multi-file/bigger applications:

```text
city_weather_app/
├── app/
│   ├── __init__.py
│   ├── main.py          # Application entry point & router inclusion
│   ├── database.py      # SQLAlchemy database engine & session setup
│   ├── models.py        # SQLAlchemy ORM models (City, Temperature)
│   ├── schemas.py       # Pydantic data schemas
│   ├── dependencies.py  # Dependency injection (e.g., DB session)
│   └── routers/
│       ├── __init__.py
│       ├── cities.py    # Endpoints for City CRUD operations
│       └── temperatures.py # Endpoints for temperature updates & history
├── requirements.txt
└── README.md