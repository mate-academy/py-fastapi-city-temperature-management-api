# City Temperature Management API
 
A **FastAPI** application for managing cities and storing current temperature data retrieved from the **Open-Meteo API**.
 
---
 
##  Technologies
 
- Python 3.13
- FastAPI
- SQLAlchemy 2.x
- Pydantic
- Alembic
- SQLite
- httpx
- Open-Meteo API
---
 
##  Installation
 
### 1. Clone the repository
 
```bash
git clone <repository-url>
cd py-fastapi-city-temperature-management-api
```
 
### 2. Create a virtual environment
 
**macOS / Linux:**
```bash
python3 -m venv venv
```
 
**Windows:**
```bash
python -m venv venv
```
 
### 3. Activate the virtual environment
 
**macOS / Linux:**
```bash
source venv/bin/activate
```
 
**Windows:**
```bash
venv\Scripts\activate
```
 
### 4. Install dependencies
 
```bash
pip install -r requirements.txt
```
 
---
 
##  Run the Application
 
Start the FastAPI development server with:
 
```bash
uvicorn app.main:app --reload
```
 
The API will be available at:
 
```
http://127.0.0.1:8000
```
 
---
 
## API Documentation
 
FastAPI automatically provides interactive API documentation:
 
| Documentation | URL |
|---|---|
| Swagger UI | [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) |
| ReDoc | [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) |
 
---
 
## 🗄️ Database Migrations
 
The project uses **Alembic** for database migrations.
 
Run existing migrations with:
 
```bash
alembic upgrade head
```
 
To create a new migration after changing the database models:
 
```bash
alembic revision --autogenerate -m "describe your changes"
```
 
Then apply it:
 
```bash
alembic upgrade head
```
 
---
 
## Project Overview
 
The API allows users to:
 
- ✅ Create and manage cities
- ✅ Retrieve city information
- ✅ Fetch current temperature data
- ✅ Store temperature data in the database
- ✅ Update and delete cities
- ✅ Retrieve cities by name
> Temperature data is retrieved from **Open-Meteo** using the city's geographical coordinates.