# 🏙️ City Temperature Management API

An asynchronous REST API built with FastAPI to manage a list of cities and automatically track their current temperatures via integration with the XWeather (AerisWeather) API.#
## 🚀Key Features
* City CRUD: Create, Read, Update, and Delete cities.

* Automated Weather Updates: Fetch current temperatures for all stored cities with a single request.

* Temperature History: View history for all records or filter by a specific city_id.

* Asynchronous Architecture: Fully async database operations and external API calls.
```aiignore
AERIS_CLIENT_ID=example234
AERIS_CLIENT_SECRET=example11234$$$
```
## 🛠️ Tech Stack
* Python 3.13+

* FastAPI (Web Framework)

* SQLAlchemy 2.0 (Asynchronous ORM)

* Alembic (Database Migrations)

* Pydantic V2 (Data Validation & Settings Management)

* SQLite (Database)

* HTTPX (Async HTTP Client)

## 📦 Installation & Setup
### 1.Clone the repository:
```
https://github.com/Psychox1k/py-fastapi-city-temperature-management-api
cd py-fastapi-city-temperature-management-api
```
### 2.Set up the virtual environment:
```bash
python -m venv .venv
```
Activate (Windows):
```bash
.venv\Scripts\activate
```


Activate (macOS/Linux):

```bash
source .venv/bin/activate
```

### 3.Configuration:
- Create a .env file in the root directory and add your credentials:
```bash
AERIS_CLIENT_ID=your_id
AERIS_CLIENT_SECRET=your_secret 
```
### 4.Database Migrations:

```bash
  alembic revision --autogenerate -m "initial setup"  
  alembic upgrade head  
```
    
### 5.Run the Server:
```bash
uvicorn main:app --reload   
```
Access the API at: http://127.0.0.1:8000
Interactive API Documentation (Swagger): http://127.0.0.1:8000/docs

## 📝 Usage Tips

* Location Format: For best results with XWeather, use the City,CountryCode format when adding cities (e.g., London,uk or Paris,fr).

* Optional Filtering: The /temperatures/ endpoint supports an optional city_id query parameter to filter history for a specific location.