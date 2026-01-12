# City Temperature Management System

FastAPI application for managing cities and their temperature data with real-time weather updates.

---

## Features

* **City Management** – Full CRUD operations for cities
* **Temperature Tracking** – Record and retrieve temperature data
* **Real-time Weather Updates** – Fetch current temperatures from OpenWeatherMap API
* **Database Migrations** – Using Alembic for schema management
* **Async Operations** – Non-blocking API calls for weather data
* **Performance Optimized** – Efficient queries (no N+1 problem)

---

## Installation

### Prerequisites

* Python 3.8+
* pip (Python package manager)

---

### Setup Instructions

#### 1. Clone repository

```bash
git clone <repository-url>
cd py-fastapi-city-temperature-management-api
```

#### 2. Create virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux / Mac
source .venv/bin/activate
```

#### 3. Install dependencies

```bash
pip install -r requirements.txt
```

#### 4. Configure environment variables

```bash
# Windows
copy .env.example .env

# Linux / Mac
cp .env.example .env
```

Edit `.env` and add your OpenWeatherMap API key (optional):

> Get a free API key: [https://openweathermap.org/api](https://openweathermap.org/api)

---

#### 5. Database migrations

```bash
# Initialize Alembic (if not done)
alembic init migrations

# Create migration
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head
```

---

#### 6. Run application

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

---

## Access

* **Swagger Docs:** [http://localhost:8080/docs](http://localhost:8080/docs)
* **ReDoc:** [http://localhost:8080/redoc](http://localhost:8080/redoc)
* **API Root:** [http://localhost:8080](http://localhost:8080)

---

## API Endpoints

### Cities API

| Method | Endpoint                   | Description                            |
| ------ | -------------------------- | -------------------------------------- |
| POST   | `/api/v1/cities/`          | Create new city                        |
| GET    | `/api/v1/cities/`          | Get all cities with temperature counts |
| GET    | `/api/v1/cities/{city_id}` | Get specific city                      |
| PUT    | `/api/v1/cities/{city_id}` | Update city                            |
| DELETE | `/api/v1/cities/{city_id}` | Delete city                            |

---

### Temperatures API

| Method | Endpoint                                  | Description                          |
| ------ | ----------------------------------------- | ------------------------------------ |
| POST   | `/api/v1/temperatures/update`             | Fetch and store current temperatures |
| GET    | `/api/v1/temperatures/`                   | Get all temperature records          |


---

## Design Choices

* **FastAPI** chosen for high performance, async support, and automatic OpenAPI docs.
* **Async HTTP client** is used to fetch weather data without blocking the event loop.
* **SQLAlchemy ORM** provides database abstraction and safe query building.
* **Single-query aggregation** (JOIN + COUNT) is used to avoid N+1 problems and improve scalability.
* **Alembic migrations** ensure controlled schema evolution.
* **Layered architecture** (routers → services → repositories) improves testability and maintainability.
* **Environment-based configuration** via `.env` for secrets and deployment flexibility.

---

## Assumptions & Simplifications

* Authentication & authorization are **not implemented** (demo scope).
* Only **OpenWeatherMap** is supported as a weather provider.
* No **caching** layer for weather data (direct API calls).
* No **rate limiting** or retry logic for external API.
* All timestamps are stored in **UTC**.
* Default DB can be **SQLite** for local dev.
* Error handling is **basic** (no custom error classes).
* No background scheduler – updates are triggered manually via endpoint.

---

## Technologies

* FastAPI
* SQLAlchemy
* Alembic
* PostgreSQL / SQLite
* OpenWeatherMap API
* Uvicorn

---

## Author

Art Sh.

---

## License

MIT License
