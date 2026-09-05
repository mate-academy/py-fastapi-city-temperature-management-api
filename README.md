# 🌡️ City Temperature Management API

A fully asynchronous REST API built with **FastAPI** for managing cities and collecting their current temperature history.

The application allows you to:

* 🏙️ Create, read, update and delete cities
* 🌡️ Fetch current temperatures for all stored cities
* 💾 Store temperature measurements in SQLite
* 📊 Retrieve temperature history
* 🔎 Filter temperature history by city
* ⚡ Perform external weather API requests asynchronously and concurrently

---

## 🛠️ Technologies

* **Python**
* **FastAPI** — web framework
* **SQLAlchemy 2.0** — ORM and database interaction
* **SQLite** — database
* **aiosqlite** — asynchronous SQLite driver
* **Pydantic** — data validation and serialization
* **pydantic-settings** — environment configuration
* **HTTPX** — asynchronous HTTP client
* **Uvicorn** — ASGI server
* **Open-Meteo API** — external weather data provider

---

## 📁 Project Structure

```text
app/
├── api/
│   ├── endpoints/
│   │   ├── cities.py
│   │   └── temperatures.py
│   └── router.py
│
├── core/
│   └── config.py
│
├── db/
│   ├── database.py
│   └── models.py
│
├── dependencies/
│   └── database.py
│
├── schemas/
│   ├── city.py
│   └── temperature.py
│
├── services/
│   └── weather.py
│
└── main.py
```

### 🧩 Architecture

The project is divided into several logical layers:

| Directory       | Responsibility                                |
| --------------- | --------------------------------------------- |
| `api/`          | API routers and endpoint handlers             |
| `schemas/`      | Pydantic request and response schemas         |
| `db/`           | SQLAlchemy models and database configuration  |
| `dependencies/` | FastAPI dependencies                          |
| `services/`     | External weather API integration              |
| `core/`         | Application configuration                     |
| `main.py`       | FastAPI application and startup configuration |

The application uses an **asynchronous architecture** for both database operations and external HTTP requests.

---

## 🗄️ Database

The application uses **SQLite** with asynchronous SQLAlchemy.

The database connection is configured through the `.env` file:

```env
DATABASE_URL=sqlite+aiosqlite:///./city_temperature.db
```

Two database tables are used:

### 🏙️ `cities`

Stores information about cities:

* `id`
* `name`
* `additional_info`

### 🌡️ `temperatures`

Stores temperature measurements:

* `id`
* `city_id`
* `date_time`
* `temperature`

Each city can have multiple temperature records, which allows the application to maintain a **temperature history**.

When a city is deleted, its related temperature records are also deleted.

---

## ⚙️ Installation

### 1️⃣ Clone the repository

```powershell
git clone <repository-url>
cd py-fastapi-city-temperature-management-api
```

### 2️⃣ Create a virtual environment

```powershell
python -m venv .venv
```

### 3️⃣ Activate the virtual environment

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4️⃣ Install dependencies

```powershell
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file in the project root:

```env
DATABASE_URL=sqlite+aiosqlite:///./city_temperature.db
```

A `.env.sample` file is also included as a template.

The actual `.env` file should **not be committed to Git**.

---

## 🚀 Running the Application

Start the development server:

```powershell
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

### 📚 Interactive API Documentation

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

---

# 🏙️ City API

## ➕ Create a City

```http
POST /cities
```

Example request:

```json
{
  "name": "Kyiv",
  "additional_info": "Capital of Ukraine"
}
```

Returns the created city with its generated `id`.

---

## 📋 Get All Cities

```http
GET /cities
```

Returns a list of all cities stored in the database.

---

## 🔎 Get a City

```http
GET /cities/{city_id}
```

Returns information about a specific city.

If the city does not exist, the API returns:

```json
{
  "detail": "City not found"
}
```

with HTTP status `404`.

---

## ✏️ Update a City

```http
PUT /cities/{city_id}
```

Example request:

```json
{
  "name": "Dnipro",
  "additional_info": "City in central Ukraine"
}
```

---

## 🗑️ Delete a City

```http
DELETE /cities/{city_id}
```

Deletes the city and its related temperature records.

Returns HTTP status `204 No Content` on success.

---

# 🌡️ Temperature API

## 🔄 Update Temperatures

```http
POST /temperatures/update
```

This endpoint:

1. 📋 Retrieves all cities from the database.
2. 🌍 Resolves each city name to geographic coordinates using Open-Meteo.
3. 🌡️ Fetches the current temperature for each city.
4. ⚡ Performs the external requests concurrently.
5. 💾 Stores the results as new temperature records.
6. 📤 Returns the newly created records.

The external API requests use `httpx.AsyncClient` and `asyncio.gather()`.

For example, if the database contains:

```text
Kyiv
Lviv
Odesa
```

the application fetches their temperatures concurrently rather than waiting for one request to finish before starting the next one.

Each update creates **new temperature records**, preserving the historical data.

---

## 📋 Get Temperature History

```http
GET /temperatures
```

Returns all stored temperature records.

Example:

```json
[
  {
    "id": 10,
    "city_id": 1,
    "date_time": "2026-09-03T17:00:00",
    "temperature": 18.9
  },
  {
    "id": 11,
    "city_id": 2,
    "date_time": "2026-09-03T17:00:00",
    "temperature": 21.2
  }
]
```

---

## 🔎 Filter Temperature History by City

```http
GET /temperatures?city_id={city_id}
```

Example:

```http
GET /temperatures?city_id=1
```

Returns only temperature records belonging to the specified city.

---

# 🌍 External Weather API

Current temperature data is provided by **Open-Meteo**.

The application uses two Open-Meteo endpoints:

* Geocoding API — converts a city name into latitude and longitude.
* Weather API — retrieves the current temperature for those coordinates.

If the external weather service is unavailable or returns invalid data, the API responds with `502 Bad Gateway` instead of storing incomplete temperature data.

A **10-second HTTP timeout** is configured for external requests.

---

# ⚡ Asynchronous Architecture

The application is fully asynchronous.

### Database

SQLAlchemy uses:

```text
AsyncEngine
AsyncSession
aiosqlite
```

### HTTP

Weather requests use:

```text
httpx.AsyncClient
asyncio.gather()
```

Multiple city temperature requests can therefore be processed concurrently:

```text
             /temperatures/update
                      │
                Get all cities
                      │
               AsyncClient
                      │
          ┌───────────┼───────────┐
          ↓           ↓           ↓
        Kyiv        Lviv        Odesa
          │           │           │
          └───────────┼───────────┘
                      ↓
               asyncio.gather()
                      │
                      ↓
                Database commit
```

This approach is especially useful when the application needs to communicate with multiple external services.

---

# 💉 Dependency Injection

FastAPI dependency injection is used for database sessions.

The `get_db` dependency creates an asynchronous SQLAlchemy session for each request and automatically closes it after the request is completed.

This keeps database session management separate from endpoint logic.

---

# 🛡️ Error Handling

The application handles common errors, including:

* ❌ City not found
* ❌ City cannot be resolved by the geocoding service
* ❌ Temperature data is unavailable
* ❌ External weather API HTTP errors
* ⏱️ External API timeout

The application returns appropriate HTTP error responses instead of exposing unhandled exceptions.

---

# 🧠 Design Decisions

### Why SQLAlchemy?

SQLAlchemy provides a clean ORM layer and supports asynchronous database operations.

### Why SQLite?

SQLite was explicitly required by the task and is sufficient for this application.

### Why HTTPX?

HTTPX provides an asynchronous HTTP client that integrates naturally with FastAPI's async architecture.

### Why a separate `services/` layer?

The weather API integration contains external communication logic that does not belong directly in the endpoint handler.

Keeping it in `services/weather.py` makes the endpoint easier to read and keeps external API logic isolated.

### Why `asyncio.gather()`?

Temperature requests for different cities are independent, so they can be executed concurrently. This avoids unnecessary waiting between external HTTP requests.

---

# 📝 Assumptions & Simplifications

* SQLite is used because it is required by the task.
* City names are used for geocoding.
* The first matching geocoding result is used.
* Temperature updates create new records instead of replacing previous measurements.
* No authentication or authorization is implemented because it is outside the task requirements.
* No automated tests are included because tests were not required for this task.
* Database tables are created automatically when the application starts.
* For a larger production system, database migrations such as Alembic would be preferable.

---

# 📦 Requirements

All required Python packages are listed in `requirements.txt`.

Install them with:

```powershell
pip install -r requirements.txt
```

---

## 👩‍💻 Author

**HamsterKate** — [GitHub](https://github.com/HamsterKate)

Developed as a **FastAPI asynchronous programming project**.
