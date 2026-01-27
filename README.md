# City Temperature Management API

A FastAPI-based application designed to manage city data and track their current temperatures using an external weather service.

## Features
- **City CRUD:** Create, Read, Update, and Delete city records.
- **Automatic Temperature Tracking:** Fetches real-time weather data for all registered cities.
- **Temperature History:** Stores and retrieves historical temperature records.
- **Asynchronous Operations:** Non-blocking API calls for weather updates.

## Requirements
- Python 3.8+
- FastAPI
- SQLAlchemy
- Uvicorn
- HTTPX (for async API requests)

## Installation & Setup
1. **Install dependencies:**
   pip install fastapi uvicorn sqlalchemy httpx
2. **Run the application:**
   uvicorn main:app --reload
3. **Access the API Documentation:**
   Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Design Choices & Assumptions
- **Database:** SQLite with SQLAlchemy.
- **Weather API:** Uses Open-Meteo (No API Key required).
- **Asynchronous:** Used httpx for parallel weather updates.
