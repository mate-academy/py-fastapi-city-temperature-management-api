# City Temperature Management API

This is a FastAPI-based backend application for managing cities and their temperature data.
The application allows creating cities with geographic coordinates and fetching current
temperature data using an external weather service.

---

## 🚀 Features

- CRUD operations for cities
- Store latitude and longitude for each city
- Fetch current temperature for cities
- Store temperature records
- Async SQLAlchemy with SQLite
- FastAPI automatic API documentation

---

## 🛠 Tech Stack

- Python 3.12+
- FastAPI
- SQLAlchemy (async)
- SQLite
- HTTPX
- Uvicorn

---

## 📁 Project Structure

app/
├── main.py
├── db/
│ ├── base.py
│ ├── session.py
│ └── init_db.py
├── cities/
│ ├── models.py
│ ├── schemas.py
│ ├── crud.py
│ └── router.py
├── temperatures/
│ ├── models.py
│ ├── schemas.py
│ ├── crud.py
│ ├── router.py
│ └── services/
│ └── weather.py


---

## ▶️ How to Run the Application


1 Install dependencies
pip install -r requirements.txt

2 Run migrations
alembic upgrade head

3 Run the application
uvicorn app.main:app --reload

4 Open API documentation
http://127.0.0.1:8000/docs

📌 API Endpoints
Cities

POST /cities/ — create a city

GET /cities/ - get a list of all cities

GET /cities/{id} — get city by ID

PUT /cities/{id} — update city

DELETE /cities/{id} — delete city

Temperatures

GET /temperatures/ — get all temperature records

GET /temperatures/?city_id={id} — get temperatures for a specific city

POST /temperatures/update — fetch and store current temperatures for all cities

🧠 Design Choices

FastAPI was chosen for its performance, async support, and built-in API documentation.

Async SQLAlchemy is used to avoid blocking database operations.

The application is split into logical domains (cities, temperatures).

External weather API logic is isolated in the services layer.

⚠️ Assumptions & Simplifications

SQLite is used for simplicity and local development.

No authentication or authorization is implemented.

Temperature updates are triggered manually via an API endpoint.

External API error handling is minimal.