Окей! Я виправив форматування, прибрав зайві проблеми з відступами, додав Markdown-структуру для списків і таблиці, щоб README виглядав **чисто та професійно**. Ось відредагована версія:

---

````markdown
# Weather API Service

This is a FastAPI-based asynchronous application for managing cities and their temperatures. The application fetches geocoding data and temperature from external APIs and stores them in a local SQLite database.

---

## 🚀 Features

- CRUD operations for cities
- Fetch and store temperatures asynchronously
- Uses FastAPI with async SQLAlchemy (`AsyncSession`)
- Handles external API calls concurrently
- Compatible with high-load requests (limited by SQLite)

---

## 📦 Requirements

- Python 3.11+
- SQLite
- Dependencies:

```bash
pip install fastapi uvicorn sqlalchemy aiosqlite httpx python-dotenv
````

---

## ⚡ Running the Application

1. Clone the repository:

```bash
git clone <your-repo-url>
cd <repo-folder>
```

2. Create a `.env` file in the root directory with the following:

```env
DATABASE_URL=sqlite+aiosqlite:///./api_city_tempr.db
GEOCODE_ENDPOINT=<your_geocode_api_endpoint>
WEATHER_ENDPOINT=<your_weather_api_endpoint>
WEATHER_API=<your_api_key>
```

3. Run the FastAPI server:

```bash
uvicorn main:app --reload
```

4. Access the interactive docs at:

```
http://127.0.0.1:8000/docs
```

---

## 🏗 Design Choices

1. **Async HTTP calls**

   * Used `httpx.AsyncClient` to fetch geocoding and weather data asynchronously.
   * Enables concurrent API requests to external services for faster updates.

2. **Async SQLAlchemy (`AsyncSession`)**

   * Database operations are fully asynchronous for scalability and performance.

3. **Single commit after loop**

   * All temperature records are added to the session and committed once, reducing SQLite write locks.

4. **Separate schemas for request/response**

   * Pydantic models are used for input validation and response serialization.

5. **Environment variables**

   * API keys and endpoints are loaded from `.env` for security and flexibility.

---

## 🔹 Assumptions and Simplifications

* **SQLite as the database**

  * Chosen for simplicity. Not suitable for extreme high-load or production-grade concurrency.
  * Can be easily switched to PostgreSQL or MySQL.

* **Single endpoint for updating temperatures**

  * Triggered manually via `/temperatures/update`. In production, should be scheduled as a background task or cron job.

* **No authentication**

  * For simplicity. Can be added with FastAPI Security utilities (OAuth2, JWT).

* **Error handling for external APIs**

  * Failures are logged, but the process continues for other cities.

* **Temperature precision**

  * Assumes temperature is returned in metric units (Celsius).

* **Limited concurrency**

  * For high-load safety, a semaphore can be added, but currently sequential for simplicity.

---

## 📖 Endpoints

| Method | URL                       | Description                                       |
| ------ | ------------------------- | ------------------------------------------------- |
| POST   | `/temperatures/update`    | Update temperatures for all cities asynchronously |
| GET    | `/temperatures`           | List all temperature records                      |
| GET    | `/temperatures/{city_id}` | Get temperature for a specific city               |
| POST   | `/cities`                 | Create a new city                                 |
| GET    | `/cities`                 | List all cities                                   |
| GET    | `/cities/{city_id}`       | Get a city by ID                                  |
| PATCH  | `/cities/{city_id}`       | Update a city                                     |
| DELETE | `/cities/{city_id}`       | Delete a city                                     |

---

## ✅ Notes

* Interactive API docs available at `/docs` (Swagger UI).
* Async operations ensure scalability for multiple concurrent requests.
* For real high-load testing, consider switching to PostgreSQL and running temperature updates as background tasks.

