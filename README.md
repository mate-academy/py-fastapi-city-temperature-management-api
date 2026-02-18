# City & Temperature Management API

## Overview
This project is a FastAPI application designed to manage city data and track temperature history for each city.  
The system consists of two main components:

1. **City CRUD API** — allows creating, reading, updating, and deleting city records.  
2. **Temperature API** — fetches current temperature data for all cities from an online source and stores it in the database, providing full access to temperature history.

The application uses **SQLite**, **SQLAlchemy**, **Pydantic**, and **asynchronous HTTP requests** to retrieve temperature data.

---

## Features

### City Management
- Add new cities  
- Retrieve all cities  
- Retrieve a specific city (optional requirement — implemented)  
- Update city information (optional requirement — implemented)  
- Delete a city  

### Temperature Tracking
- Fetch current temperature for all cities from an external API  
- Store temperature records in the database  
- Retrieve full temperature history  
- Filter temperature history by city  

---

## Technologies Used
- **FastAPI** — main web framework  
- **SQLAlchemy** — ORM for database models  
- **SQLite** — lightweight database  
- **Pydantic** — data validation  
- **HTTPX** — async temperature fetching  
- **Dependency Injection** — for DB session management  
- **Modular FastAPI project structure**  

---

## How to Run the Application

### 1. Clone the repository
```bash
git clone https://github.com/mtotsevych/py-fastapi-city-temperature-management-api.git
cd project
```
### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows
```
### 3. Install dependencies
```bash
pip install -r requirements.txt
```
### 4. Run the application
```bash
uvicorn app.main:app --reload
```

---

## Open API documentation
FastAPI automatically generates interactive docs:

### 1. Swagger UI
```bash
http://127.0.0.1:8000/docs
```
### 2. ReDoc
```bash
http://127.0.0.1:8000/redoc
```

---

### Design Choices

### 1. Modular Structure
The project is split into routers, CRUD modules, schemas, and utilities to keep the code clean and maintainable.
### 2. Dependency Injection
Database sessions are injected using FastAPI’s Depends, ensuring proper session lifecycle management.
### 3. Asynchronous Temperature Fetching
Temperature updates use async HTTP requests to avoid blocking the event loop and improve performance.
### 4. Separate CRUD Logic
CRUD operations are isolated from route handlers to keep endpoints clean and focused.
