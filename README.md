# 🌡 City Temperature API

##  Overview
A FastAPI application that:
- Manages cities (CRUD).
- Fetches current temperatures from OpenWeatherMap.
- Stores temperature history in SQLite.
- Provides endpoints to view all records or filter by city.

---

##  Quick Start

### 1. Clone and enter project
```bash
git clone <repo_url>
cd city-temperature-api
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment
Create .env file:
DATABASE_URL=sqlite+aiosqlite:///./cities.db
OPENWEATHER_API_KEY=your_api_key_here

### 5. Run server
```bash
uvicorn main:app --reload
```

### Notes
Uses FastAPI, SQLAlchemy async, httpx.
Tables auto‑created at startup (no Alembic migrations).
Database file cities.db should be added to .gitignore.
Temperatures stored in Celsius (units=metric).

### Run Docs
Swagger UI → http://localhost:8000/docs
ReDoc → http://localhost:8000/redoc