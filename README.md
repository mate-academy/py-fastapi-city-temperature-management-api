# 🌡️ City Temperature Management API

An async web application built with **FastAPI** for managing a list of cities and automatically collecting current temperature data for each of them.

---

## 🛠 Tech Stack

| Technology | Description |
|---|---|
| **Python 3.11+** | Core language |
| **FastAPI** | Modern async web framework |
| **SQLAlchemy (Async)** | ORM for database access |
| **Aiosqlite** | Async SQLite driver |
| **Alembic** | Database migration management |
| **HTTPX** | Async HTTP client for weather API requests |
| **Pydantic** | Data validation |

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/irina957/py-fastapi-city-temperature-management-api.git
cd py-fastapi-city-temperature-management-api
```

### 2. Set up a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate        # Linux / macOS
# .venv\Scripts\activate         # Windows

pip install -r requirements.txt
```

### 3. Apply migrations

```bash
alembic upgrade head
```

### 4. Run the server

```bash
uvicorn main:app --reload
```

### 5. Open the docs

Navigate to **http://127.0.0.1:8000/docs** to access the interactive Swagger UI.

---

## 📌 API Endpoints

### 🏙 Cities (CRUD)

| Method | Path | Description |
|---|---|---|
| `POST` | `/cities` | Create a new city |
| `GET` | `/cities` | Get a list of all cities |
| `GET` | `/cities/{city_id}` | Get detailed info about a specific city |
| `PUT` | `/cities/{city_id}` | Update city data (name or additional info) |
| `DELETE` | `/cities/{city_id}` | Delete a city and all its associated data |


### 🌤 Temperature

| Method | Path | Description |
|---|---|---|
| `POST` | `/temperatures/update` | Fetch and update temperatures for all cities |
| `GET` | `/temperatures` | Get the full temperature history |
| `GET` | `/temperatures/?city_id={id}` | Get temperature history for a specific city |

---


## 💡 Design Decisions

**Separation of concerns.** The project is split into independent `city` and `temperature` modules, each containing its own `router`, `crud`, and `schemas` — making the codebase easy to maintain and extend.

**Async parallelism.** Temperature fetching uses `asyncio.gather` to query the external weather API for all cities simultaneously, rather than sequentially. This significantly speeds up the `/temperatures/update` endpoint.

**No API key required.** Weather data is sourced from [Open-Meteo API](https://open-meteo.com/), which is free and requires no registration or API key, keeping the project simple to run.

**Geocoding step.** Since the city model does not store coordinates, the service automatically resolves `lat/lon` from the city name via the Geocoding API before fetching weather data.
