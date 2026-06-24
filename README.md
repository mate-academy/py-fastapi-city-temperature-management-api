# City Temperature API

A FastAPI application that manages city data and tracks their current temperatures,
sourced from the free [Open-Meteo](https://open-meteo.com/) weather API (no API key required).

---

## Requirements

- Python 3.11+
- An internet connection (to fetch live temperature data)

---

## Running the Application

```bash
# 1. Clone / unzip the project
cd city-temperature-api

# 2. Create and activate a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start the server
uvicorn main:app --reload
```

The API will be available at **http://127.0.0.1:8000**.

Interactive docs (Swagger UI): **http://127.0.0.1:8000/docs**

---

## API Reference

### Cities

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/cities/` | Create a new city |
| `GET` | `/cities/` | List all cities (supports `skip` & `limit`) |
| `GET` | `/cities/{city_id}` | Get a specific city |
| `PUT` | `/cities/{city_id}` | Update a city's fields |
| `DELETE` | `/cities/{city_id}` | Delete a city (cascades to temperatures) |

**Create city body**
```json
{ "name": "Kyiv", "additional_info": "Capital of Ukraine" }
```

### Temperatures

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/temperatures/update` | Fetch & store current temperatures for all cities |
| `GET` | `/temperatures/` | List all temperature records |
| `GET` | `/temperatures/?city_id=1` | Temperature history for a specific city |

**Typical workflow**
```bash
# Add some cities
curl -X POST http://localhost:8000/cities/ \
     -H "Content-Type: application/json" \
     -d '{"name": "Kyiv", "additional_info": "Capital of Ukraine"}'

curl -X POST http://localhost:8000/cities/ \
     -H "Content-Type: application/json" \
     -d '{"name": "Lviv"}'

# Trigger a temperature fetch for all cities
curl -X POST http://localhost:8000/temperatures/update

# View temperature history
curl http://localhost:8000/temperatures/
curl "http://localhost:8000/temperatures/?city_id=1"
```

---

## Design Choices

### Framework & Database
- **FastAPI** for async-first routing and automatic OpenAPI documentation.
- **SQLAlchemy 2.0** with the modern `Mapped`/`mapped_column` API for type-safe ORM models.
- **SQLite** for zero-setup local development. Swapping to PostgreSQL requires only changing `DATABASE_URL` in `database.py`.

### Two-step weather lookup
Temperature fetching uses the Open-Meteo API in two steps:
1. **Geocoding** (`geocoding-api.open-meteo.com`) — city name → (lat, lon)
2. **Current weather** (`api.open-meteo.com`) — (lat, lon) → temperature (°C)

Both are fully free and require no registration or API key.

All cities are queried **concurrently** via `asyncio.gather`, so fetching 100 cities takes about the same time as fetching one.

### Dependency Injection
`get_db` is a FastAPI dependency that yields a per-request SQLAlchemy session and guarantees cleanup via a `finally` block. This pattern is consistent across all routers.

### Error Handling
- Duplicate city names return **409 Conflict**.
- Missing resources return **404 Not Found**.
- Failed temperature lookups (network errors, unknown city name) are collected and returned in the `failed` list of `POST /temperatures/update` rather than crashing the entire batch.
- Cascade `delete-orphan` on the `City → Temperature` relationship ensures referential integrity on city deletion.

### Cascade deletion
Deleting a city also removes all of its temperature records via SQLAlchemy's `cascade="all, delete-orphan"` relationship option.

