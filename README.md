# 📌 City Temperature API

## 📖 Description

This project is a FastAPI application that provides:

- CRUD operations for cities
- Temperature tracking for cities
- Integration with external weather API

## ⚙️ Tech Stack
- FastAPI
- SQLAlchemy 2.0
- Alembic
- SQLite
- httpx (async requests)

## 🚀 How to run
- pip install -r requirements.txt

Run migrations
- alembic upgrade head

Start server
- uvicorn main:app --reload

## 📌 Endpoints
Cities
- POST /cities
- GET /cities
- GET /cities/{id}
- PUT /cities/{id}
- DELETE /cities/{id}
- Temperatures
- GET /temperatures
- GET /temperatures?city_id=1
- POST /temperatures/update

## 🧠 Design choices
Separation into layers:
- API (routes)
- CRUD (DB logic)
- Services (external API)
- SQLAlchemy 2.0 style (select, scalars)
- Dependency Injection via Depends

## ⚠️ Assumptions
- Weather data is fetched from OpenWeather API
- Temperatures are stored in Celsius
