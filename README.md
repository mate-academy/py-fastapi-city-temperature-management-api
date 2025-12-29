# City Temperature Management API

A learning-oriented FastAPI project for managing cities and storing their current temperatures.
The project demonstrates **FastAPI**, **async SQLAlchemy (2.0)**, **Pydantic v2**, external API integration, and basic backend architecture.

---

## ✨ Features

- CRUD operations for cities
- Fetching current temperature for all cities from an external weather API
- Storing temperature history in the database with timestamps
- Retrieving:
  - all temperature records
  - the latest temperature for a specific city

---

## 🧱 Tech Stack

- Python 3.10+
- FastAPI
- SQLAlchemy 2.0 (async)
- Pydantic v2
- Alembic
- httpx
- OpenWeather API
- PostgreSQL (or any SQL database supported by SQLAlchemy)

## how to run
1. Clone & enter the project folder: 
- git clone <your-repo-url>
- cd py-fastapi-city-temperature-management-api
2. Create & activate a virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1       # Windows PowerShell
3. Install dependencies
pip install -r requirements.txt
4. Configure environment variables
5. Run database migrations
6. Start the API server
uvicorn app.main:app --reload





---

## 📁 Project Structure

```text
app/
├── main.py
├── api/
│   ├── dependencies.py
│   └── routers/
│       ├── city.py
│       └── temperature.py
├── crud/
│   ├── city.py
│   └── temperature.py
├── models/
│   ├── city.py
│   └── temperature.py
├── schemas/
│   ├── city.py
│   └── temperature.py
├── services/
│   └── weather.py
├── database.py
└── migrations/
