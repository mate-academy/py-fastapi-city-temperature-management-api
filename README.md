# City Temperature Management API

An asynchronous REST API service built with **FastAPI** designed to manage a list of cities and monitor their weather conditions (temperature) by fetching data from an external API.

## 🛠 Tech Stack

* **Python 3.10+**
* **FastAPI** — High-performance web framework.
* **SQLAlchemy 2.0 (AsyncIO)** — ORM for database interactions.
* **aiosqlite** — Driver for asynchronous SQLite support.
* **Pydantic V2** — Data validation and serialization.
* **Httpx** — Asynchronous HTTP client for making requests to the external Weather API.

---

## 🚀 Setup & Installation

### 0. Set up the Virtual Environment

`python -m venv venv`

# Windows
`venv\Scripts\activate`

# Linux/macOS
`source venv/bin/activate`

### 1. Install Dependencies
`pip install -r requirements.txt`

### 2. Configure Environment Variables
# Database Configuration (SQLite)
DATABASE_URL=sqlite+aiosqlite:///./sql_app.db

# Weather API Configuration (e.g., weatherapi.com)
API_KEY=your_api_key_here


API_BASE_URL=[http://api.weatherapi.com/v1/current.json](http://api.weatherapi.com/v1/current.json)

### 3. Run the Server

`uvicorn main:app --reload`


## 🏛 Design Choices

### 1. Full Asynchrony (Async/Await)
Since the project involves significant I/O operations (database queries and external API requests), the application was designed to be fully asynchronous.

AsyncSession is used in SQLAlchemy for non-blocking database access.

Httpx is used instead of requests. This allows the server to handle other incoming requests while waiting for the external weather service to respond, significantly improving performance under load.

### 2. Project Structure

The project is modularized into distinct apps (City, Temperature) to ensure scalability and maintainability. Each module contains its own:

router.py (Endpoints)

schemas.py (Pydantic models)

crud.py (Database logic)

models.py (SQLAlchemy models)

This adheres to the Separation of Concerns principle.

## 📝 Assumptions

### External API: 

The code assumes an API structure similar to WeatherAPI.com (using key and q parameters). If a different provider is used, the parameter logic in Temperature/router.py may need adaptation.

### Error Handling: 

If the external API fails to find a specific city or returns an error, the system logs the issue to the console but continues processing the remaining cities to ensure the batch update process is not halted.