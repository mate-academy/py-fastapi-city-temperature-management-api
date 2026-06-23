# City & Temperature Management API

## Running the Application

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
fastapi dev app/main.py
```

API documentation will be available at:

```text
http://127.0.0.1:8000/docs
```

---

## Design Choices

* **FastAPI** for a simple, modern, and high-performance REST API.
* **SQLAlchemy ORM** for database access and model management.
* **Dependency Injection** (`Depends`) for clean resource management and easier testing.
* **httpx.AsyncClient** for non-blocking weather API requests.
* **Project structure** follows FastAPI recommendations by keeping application code inside the `app/` package.

---

## Assumptions & Simplifications

* **SQLite** is used for simplicity and easy local setup.
* **wttr.in** is used as the weather provider because it requires no API key.
* Database operations are synchronous since SQLite I/O overhead is minimal for this use case.
* Temperature updates are committed in a single transaction to reduce database writes.
