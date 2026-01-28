# City & Temperature API

A RESTful API service for managing city data and monitoring temperatures. This project is built using **FastAPI** with a fully asynchronous architecture.

## 🛠 Tech Stack

* **Python 3.10+**
* **FastAPI** — High-performance web framework.
* **SQLAlchemy (Async)** — ORM for database interactions using `aiosqlite`.
* **Alembic** — Database migration tool.
* **Pydantic v2** — Data validation and settings management.
* **HTTPX** — Asynchronous HTTP client for external API requests.
* **SQLite** — Lightweight database (using `aiosqlite` driver).

---

## 🚀 How to Run

### 1. Clone and Setup Environment

Create a virtual environment and activate it:

```bash
# Create venv
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 2. Environment Configuration

Create a `.env` file in the root directory and add the database URL:

```env
DATABASE_URL=sqlite+aiosqlite:///./city.db
```

### 3. Database Migrations

Apply migrations to create the necessary tables in the database:

```bash
alembic upgrade head
```

*(Note: If this is the first run and no revision exists, create one first: `alembic revision --autogenerate -m "Initial"`)*

### 4. Start the Server

Run the development server using Uvicorn:

```bash
uvicorn src.main:app --reload
```

The API documentation (Swagger UI) will be available at:
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🏗 Design Choices

### 1. Project Structure (Feature-based)
The project is organized by business features (`city`, `temperature`) rather than by technical layers (controllers, models).
* **Reasoning:** This structure makes the codebase more scalable. Each feature module contains its own `router`, `schemas`, `models`, and `crud` logic, keeping related code together.

### 2. Asynchronous Architecture
The application uses `async/await` throughout the entire stack (Database I/O, HTTP requests, API Endpoints).
* **Reasoning:** I/O operations (like querying the database or fetching weather data) are blocking. Asynchronous programming allows the server to handle other incoming requests while waiting for these operations to complete, significantly improving performance.

### 3. Service Layer Pattern
The logic for interacting with the external weather API is isolated in `service.py`.
* **Reasoning:** Separation of concerns. The `router` handles HTTP requests, `crud` handles database operations, and `service` handles complex business logic and external integrations.

### 4. External API Strategy
I used **Open-Meteo** for fetching weather data.
* **Reasoning:** It is a reliable, free API that does not require an API key, making it ideal for testing and educational purposes.

---

## 📝 Assumptions & Simplifications

1.  **Geocoding Strategy:**
    When fetching coordinates for a city name, the application uses the first result returned by the Geocoding API. It assumes the user provides a specific enough city name (e.g., relying on "London" returning the capital of the UK).
2.  **Database:**
    SQLite is used for ease of setup. In a production environment, PostgreSQL would be the preferred choice.
3.  **Historical Data:**
    Every time the update endpoint is called, new temperature records are inserted into the database. No cleanup mechanism for old data is implemented in this scope.
4.  **Error Handling:**
    If the external API fails for a specific city during the batch update, the error is logged to the console, and the process continues for the remaining cities to ensure partial success.