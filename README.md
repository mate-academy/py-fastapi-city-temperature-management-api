# 🌤️ City Temperature Management API

This is a **FastAPI** project for managing cities and their corresponding temperature records. The application fetches live temperature data from an external weather API and stores it in a database.

---

## 📁 Project Structure
```
fastapi-project
├── alembic/
├── src
│   └── weatherapi 
│   │   ├── crud
│   │   │   ├── city.py
│   │   │   ├── temperature.py
│   │   ├── models
│   │   │   ├── base.py
│   │   │   ├── city.py
│   │   │   ├── temperature.py
│   │   ├── routers
│   │   │   ├── city.py
│   │   │   ├── temperature.py
│   │   ├── schemas
│   │   │   ├── city.py
│   │   │   ├── temperature.py
│   │   ├── dependencies.py
│   │   ├── service.py
│   │   └── utils.py
│   ├── config.py  # global configs
│   ├── database.py  # db connection related stuff
│   └── main.py
├── requirements.txt
├── .gitignore
├── README.md
└── alembic.ini
```
---

## 🚀 Features

- Add/read/delete cities
- Update/read temperatures
- Fetch current temperature from weather API
- Record temperatures in DB using an async workflow
- Paginated and filterable temperature endpoint
- Alembic-based database migrations
- Typed, modular CRUD with SQLAlchemy 2.x (async)
- Pydantic v2 schema management

---

## 📦 Technologies Used

- FastAPI
- SQLAlchemy (async + 2.0 style)
- Pydantic v2
- Alembic
- SQLite + aiosqlite
- External weather API (e.g. WeatherAPI or OpenWeatherMap)

---

## ⚙️ Setup

1. **Install dependencies**

```bash
pip install -r requirements.txt
# Make migrate via alembic
alembic upgrade head
# and run via uvicorn
uvicorn src.main:app --reload --port 5000
```

## 📘 Example Endpoints
- GET /cities/ – list all cities
- POST /cities/ – create a new city
- DELETE /cities/city_id - destroy city by id
- GET /temperatures/ - list all temperatures
- GET /temperatures/?city_id=1 - temperatures by city ID
- POST /temperatures/update - fetch & store current temperatures for all cities
