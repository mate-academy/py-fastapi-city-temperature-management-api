## City Temperature Management API

FastAPI service that manages cities and their temperature history. It exposes CRUD operations for cities and an endpoint that fetches current temperatures for every city and stores the readings in SQLite.

### Requirements
- Python 3.10+
- pip / venv

### How to run
#### Setup
```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

#### Start the API
```bash
uvicorn app.main:app --reload
```
SQLite database `app.db` is created automatically on first start. Interactive docs live at `http://127.0.0.1:8000/docs`.

### Endpoints
- `POST /cities` - create a city. Body: `{ "name": "Paris", "additional_info": "Capital" }`
- `GET /cities` - list cities.
- `GET /cities/{city_id}` - retrieve one city.
- `PUT /cities/{city_id}` - update name or additional_info.
- `DELETE /cities/{city_id}` - remove a city (cascades temperatures).
- `POST /temperatures/update` - async fetch current temperature for every city and store it.
- `GET /temperatures` - list all temperature records; optional `?city_id=` filter. Returns `{ "records": [...], "total": n }`.

### Design choices
- Temperature fetcher uses `wttr.in` via `httpx` with async concurrency and times out quickly to keep the endpoint responsive.
- If network access fails or the provider errors, a deterministic synthetic temperature is generated per city so the endpoint still responds and history remains usable in restricted environments.
- SQLAlchemy ORM with SQLite; `SessionLocal` provided via FastAPI dependency.
- Pydantic schemas keep request/response contracts clear.
- Routers split into `cities` and `temperatures` to mirror domains.
- Table relationships enforce referential integrity; deleting a city deletes its temperature history.

### Assumptions & simplifications
- City names are unique.
- No authentication/authorization or rate limiting.
- Temperature provider is best-effort; results may be synthetic when offline.

### Quick manual flow
```bash
# add cities
curl -X POST http://127.0.0.1:8000/cities -H "Content-Type: application/json" -d "{\"name\": \"Paris\"}"
curl -X POST http://127.0.0.1:8000/cities -H "Content-Type: application/json" -d "{\"name\": \"Tokyo\"}"

# fetch and store temperatures
curl -X POST http://127.0.0.1:8000/temperatures/update

# list history (optionally filter)
curl "http://127.0.0.1:8000/temperatures?city_id=1"
```
