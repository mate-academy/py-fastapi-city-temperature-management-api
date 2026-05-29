# City Weather Tracking Application

An application built using Python, FastAPI, and SQLAlchemy to manage city metadata and asynchronously retrieve cron-style temperature records.

## Design Architecture Choices

1. **Layered Structure**: Separation was applied across files (`models.py`, `schemas.py`, `crud.py`, `main.py`) and packages(`app`, `routers`).
2. **Asynchronous HTTP Client**: Used `httpx.AsyncClient()` inside the update loops instead of standard `requests` for async operations while retrieving real-time data from external APIs.
3. **External Free Data API**: Utilized Open-Meteo's geocoding and current weather APIs because they are fast and do not require rate-limiting API keys.

## Assumptions & Simplifications
* **Timezones**: Weather sync dates are normalized to Coordinated Universal Time (`UTC`) inside the DB.
* **Geocoding**: If a user submits a city name that cannot be matched to coordinates, the `/temperatures/update` background worker skips it silently rather than crashing.
* **Database Setup**: Database migrations are handled via built-in `create_all()`.

---

## Instructions on How to Run

### 1. Setup Virtual Environment & Install Dependencies
Ensure you are inside the root folder (`py-fastapi-city-temperature-management-api/`):
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Start the FastAPI Web Server
uvicorn app.main:app --reload

### 3. Accessing Interactive API Docs
http://127.0.0.1:8000/docs