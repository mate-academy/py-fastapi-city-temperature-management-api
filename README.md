# Weather Monitor API

An asynchronous REST API built with FastAPI to track and monitor temperatures across different cities.
The system integrates with the Open-Meteo API to fetch real-time weather data and stores it in a local 
database for historical analysis.



## Features

- **City Management**: Full CRUD operations for cities.
- **Async Weather Fetching**: Real-time temperature updates using `httpx`.
- **Modern ORM**: Powered by SQLAlchemy 2.0 with type-safe `Mapped` models.
- **Automatic Migrations**: Database schema management with Alembic.
- **Validation**: Strict data validation using Pydantic V2.

---

## Tech Stack

- **Framework**: FastAPI
- **Database**: SQLite (via `aiosqlite`)
- **ORM**: SQLAlchemy 2.0 (Async)
- **Migrations**: Alembic
- **HTTP Client**: HTTPX (for async API requests)
- **Configuration**: Pydantic Settings (Environment variables)

---

## Prerequisites

- Python 3.9+
- Virtualenv (recommended)

---

## Installation & Setup

### 1. Clone the repository
```bash
git clone <your-repository-url>
cd weather-monitor-api
```

### 2. Activate venv
```bash
python -m venv venv
# Linux/macOS
source venv/bin/activate
# Windows
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a .env file in the root directory:

```bash
DATABASE_URL=sqlite+aiosqlite:///./weather.db
API_V1_PREFIX=/api/v1
```

### 5. Run Database Migrations
Initialize your database schema using Alembic:

```bash
alembic upgrade head
```

### Running the Application
Start the development server with auto-reload:


```bash
uvicorn main:app --reload
```

The API will be available at: http://127.0.0.1:8000

API Documentation
Once the server is running, you can access the interactive documentation:

Swagger UI: http://127.0.0.1:8000/docs