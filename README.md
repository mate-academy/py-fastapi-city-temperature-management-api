# City Temperature Management API

## How to Run

### 1. Create and activate virtual environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Start the server

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

Interactive documentation (Swagger UI): `http://127.0.0.1:8000/docs`

---

## API Endpoints

### Cities

| Method     | URL                   | Description       |
| ---------- | --------------------- | ----------------- |
| `POST`   | `/cities/`          | Create a new city |
| `GET`    | `/cities/`          | Get all cities    |
| `GET`    | `/cities/{city_id}` | Get a city by ID  |
| `PUT`    | `/cities/{city_id}` | Update a city     |
| `DELETE` | `/cities/{city_id}` | Delete a city     |

### Temperatures

| Method   | URL                             | Description                                         |
| -------- | ------------------------------- | --------------------------------------------------- |
| `POST` | `/temperatures/update`        | Fetch and store current temperatures for all cities |
| `GET`  | `/temperatures/`              | Get all temperature records                         |
| `GET`  | `/temperatures/?city_id={id}` | Get temperature records for a specific city         |

---

## Design Choices

- **SQLite + SQLAlchemy ORM** — lightweight database suitable for this task, with SQLAlchemy providing clean model definitions and query building.
- **Pydantic v2 schemas** — separate `Base`, `Create`, and `Response` models for clean data validation and serialization.
- **Dependency injection** — `get_db()` generator ensures database sessions are always properly closed.
- **`httpx.AsyncClient`** — used for async HTTP requests to the weather API, allowing concurrent fetching without blocking the event loop.
- **wttr.in API** — free, no-auth-required weather service used to fetch current temperature by city name (`https://wttr.in/{city}?format=j1`).
- **Error handling** — each city fetch is wrapped in `try/except` so a failure for one city does not abort the entire update.

---

## Assumptions and Simplifications

- City names passed to the weather API must be recognizable by wttr.in (e.g. "Kyiv", "London"). Unrecognized names will return an error entry in the response but won't crash the endpoint.
- No authentication or rate limiting is implemented.
- The SQLite database file (`database.db`) is created automatically on first run
