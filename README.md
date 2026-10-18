Markdown
# Weather & Cities Management API

A modular **FastAPI** web service for managing cities and performing bulk asynchronous temperature updates using the **Open-Meteo API**

## 🛠 Tech Stack

* **Python 3.10+**
* **FastAPI** — Web framework
* **SQLAlchemy** — ORM for SQLite database interactions
* **Pydantic v2** — Data validation and serialization
* **HTTPX** — Async HTTP client for external API requests
* **Uvicorn** — ASGI server

---

## 🏗 Design Decisions

* **Feature-Based Architecture:** The application is split into independent feature modules (`cities/` and `temperatures/`), providing a clean structure that is easy to scale and maintain
* **External Weather Integration:** Uses the free **Open-Meteo API** (Geocoding API to resolve city coordinates and Forecast API to fetch current temperature metrics). No API keys required
* **Cascade Deletion:** Database models configured with `cascade="all, delete-orphan"`. Deleting a city automatically cleans up all associated temperature history records
* **Bulk Temperature Processing:** The `POST /temperatures/update` endpoint queries all existing cities from the database, asynchronously fetches their latest temperature readings, and saves the new entries in bulk

---

## 📁 Project Structure

```text
.
├── database.py         # SQLite connection setup & SessionLocal configuration
├── models.py           # SQLAlchemy models (City, Temperature)
├── main.py             # Application entrypoint & router initialization
├── cities/             # City management module
│   ├── crud.py
│   ├── router.py
│   └── schemas.py
├── temperatures/       # Temperature management module
│   ├── crud.py
│   ├── router.py
│   ├── schemas.py
│   └── service.py      # Async HTTP service (httpx -> Open-Meteo API)
└── requirements.txt
🚀 Getting Started
1. Clone & Set Up Virtual Environment

python -m venv venv

# On Windows:
venv\Scripts\activate

# On Linux/macOS:
source venv/bin/activate
2. Install Dependencies

pip install -r requirements.txt
3. Run the Uvicorn Server

uvicorn main:app --reload
The application will be running at http://127.0.0.1:8000.

📖 API Documentation
Interactive API documentation is generated automatically:

Swagger UI: http://127.0.0.1:8000/docs

ReDoc: http://127.0.0.1:8000/redoc

📌 Main Endpoints
Cities (/cities)
POST /cities/ — Create a new city

GET /cities/ — Retrieve all cities

GET /cities/{city_id} — Get specific city details

PUT /cities/{city_id} — Update a city's information

DELETE /cities/{city_id} — Delete a city (cascades to related temperature logs)

Temperatures (/temperatures)
POST /temperatures/update — Fetch and save current weather for all registered cities via Open-Meteo

GET /temperatures/ or GET /temperatures/?city_id={id} — Retrieve temperature history (filterable by city_id)