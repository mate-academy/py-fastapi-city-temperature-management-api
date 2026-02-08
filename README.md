# City & Temperature Service (FastAPI)

A FastAPI application with two main areas:

- **City CRUD API**: create/list/update/delete cities stored in SQLite.
- **Temperature API**: fetch current temperatures for all stored cities, persist them, and expose history endpoints.

---

## Requirements

- **Python 3.13.5**
- `virtualenv` (recommended)
- Dependencies installed from `requirements.txt`

---

## How to run

### 1) Create and activate a virtual environment (virtualenv)

Activate it:

- macOS / Linux:
  ```bash
  source .venv/bin/activate
  ```
- Windows (PowerShell):
  ```powershell
  .\.venv\Scripts\Activate.ps1
  ```

### 2) Install dependencies

### 3) Database setup

This project uses **SQLite**. A local database file may already exist in the repo (e.g. `city_temperature.db`).

If migrations are not required/used in your environment, the app may create tables at startup (depending on implementation).

### 4) Start the API server

Most commonly with Uvicorn:

Then open:

- API docs (Swagger UI): `http://127.0.0.1:8000/docs`
- Alternative docs (ReDoc): `http://127.0.0.1:8000/redoc`

---

## API overview

### City endpoints (CRUD)

- `POST /cities` — Create a new city
- `GET /cities` — List all cities
- `GET /cities/{city_id}` — Get a specific city (optional)
- `PUT /cities/{city_id}` — Update a city (optional)
- `DELETE /cities/{city_id}` — Delete a city

Example payload for create:

### Temperature endpoints

- `POST /temperatures/update` — Fetch current temperature for **all cities** and store the results  
  (implemented using async I/O for external calls)
- `GET /temperatures` — List all temperature records
- `GET /temperatures?city_id={city_id}` — Temperature history for a single city

---


## Design choices (brief)

- **FastAPI routers split by domain**: the project is organized into separate modules (e.g., `city/` and `temperature/`) to keep concerns isolated and make it easier to extend.
- **SQLAlchemy + SQLite**: lightweight local persistence suitable for take-home tasks and easy local runs.
- **Pydantic schemas**: request/response validation is handled explicitly via schemas (separating API contracts from DB models).
- **Dependency injection**: DB session and other cross-cutting concerns are provided via FastAPI dependencies to keep handlers testable and avoid global state.
- **Async temperature fetching**: the temperature refresh endpoint is designed to use async calls to avoid blocking the server while calling external resources.

---

## Assumptions / simplifications

- **Temperature provider**: an external “current temperature” source is used; for simplicity, it may rely on a single provider and a minimal set of fields.
- **City identity / lookup**: cities are assumed to be uniquely identifiable in a way that the chosen temperature provider can resolve (e.g., by name or a stored external identifier if implemented).
- **History storage**: each update stores a new row per city per fetch run (no deduplication unless explicitly implemented).
- **Auth & rate limiting omitted**: endpoints are unauthenticated; rate limiting and API key management (if required by the temperature provider) are kept minimal for the scope of the task.
- **SQLite in-process**: suitable for local/dev; not intended as-is for high concurrency production workloads.

---

## Common troubleshooting

- **`uvicorn` not found**: install dependencies via `pip install -r requirements.txt`. If needed:
  ```bash
  pip install uvicorn
  ```
- **Database/migrations issues**: ensure you’re in the activated virtualenv and try:
  ```bash
  alembic upgrade head
  ```

---

## Project structure (high-level)

- `main.py` — FastAPI app entrypoint
- `database.py` — DB engine/session setup
- `city/` — city models/schemas/router/crud
- `temperature/` — temperature models/schemas/router/crud
- `alembic/` + `alembic.ini` — migrations (if used)
- `requirements.txt` — Python dependencies
