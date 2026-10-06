# Temperature Catalog API

A FastAPI REST API for storing a list of cities and their temperature history. The current temperature is fetched from the free [Open-Meteo](https://open-meteo.com/) API (no API key required).
 
### How to run
 
1. Create and activate a virtual environment:
```bash
   python -m venv venv
   # Linux / macOS
   source venv/bin/activate
   # Windows
   venv\Scripts\activate
```
 
2. Install dependencies:
```bash
   pip install -r requirements.txt
```
 
3. Apply database migrations (from the project root, where `alembic.ini` is located):
```bash
   alembic upgrade head
```
 
   This command creates the `temperature_catalog.db` file (SQLite) in the project root along with all tables (`city`, `temperature`).
 
4. Start the application (from the project root, where `main.py` is located):
```bash
   uvicorn main:app --reload
```
 
5. Open in your browser:
   - API: http://127.0.0.1:8000
   - Swagger UI (interactive documentation): http://127.0.0.1:8000/docs
An internet connection is required to update temperatures.
 
### Migrations (Alembic)
 
If you change `db/models.py`, generate a new migration and apply it:
 
```bash
alembic revision --autogenerate -m "describe your changes"
alembic upgrade head
```
 
Review the generated file in `alembic/versions/` before applying it — autogenerate does not always detect every change correctly (for example, column renames in SQLite).
 
### Usage example
 
```bash
# add a city
curl -X POST http://127.0.0.1:8000/cities/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Kyiv", "additional_info": "Capital of Ukraine"}'
 
# fetch the current temperature for all cities and save it to the DB
curl -X POST http://127.0.0.1:8000/temperatures/update/
 
# list cities
curl http://127.0.0.1:8000/cities/
```
 
### Endpoints
 
| Method | Path | Description |
|--------|------|-------------|
| GET | `/cities/` | List all cities |
| POST | `/cities/` | Create a city (`name`, `additional_info`) |
| DELETE | `/cities/{city_id}` | Delete a city together with all its temperature records |
| POST | `/temperatures/update/` | Fetch the current temperature for all cities from Open-Meteo and save it to the DB |
| GET | `/temperatures` | All temperature records for all cities |
| GET | `/temperatures/?city_id=1` | All temperature records for a specific city |
 
### Design choices
 
- **FastAPI + Pydantic** — automatic data validation and ready-made Swagger documentation.
- **SQLAlchemy 2.0 + SQLite** — an ORM with minimal boilerplate, and SQLite needs no separate server. The DB path is built with `pathlib`, so the project behaves the same on any OS. The `check_same_thread=False` option is needed because FastAPI may handle a request in a different thread.
- **Alembic for migrations** — versioning of the DB schema: table structure can be changed without losing data, and changes can be rolled back.
- **Layered structure**: `db/` (connection and models), `schemas.py` (Pydantic schemas for the API), `crud.py` (database and external API access), `main.py` (routes). This keeps business logic separate from HTTP handlers.
- **Separate models and schemas**: SQLAlchemy models (`DBCity`, `DBTemperature`) are separate from Pydantic schemas (`City`, `Temperature`), and `from_attributes = True` converts one into the other automatically.
- **The `get_db` dependency** opens a session per request and guarantees it is closed after the response.
- **Asynchronous temperature updates**: the `/temperatures/update/` endpoint uses `httpx.AsyncClient` and `asyncio.gather`, so requests for all cities run in parallel rather than one by one.
- **Two-step Open-Meteo lookup**: first geocoding (city name → coordinates), then a current-weather request by coordinates.
- **Error tolerance**: if the external API fails or a city is not found, that city is skipped while the rest are updated normally. The response contains the number of updated cities and the total count.
- **Cascade deletion**: when a city is deleted, its temperature records are removed first so the foreign key is not violated.
- **A single timestamp** (`datetime.now(timezone.utc)`) for all records created in one update.
### Assumptions and simplifications
 
- A city name is unique and is used as the geocoding search query. The first Open-Meteo result is used, so for ambiguous names (e.g. cities with the same name in different countries) the wrong city may be selected.
- Temperature is in °C (the Open-Meteo default); only the current value at the time of the update is stored.
- Temperature updates are triggered manually via `POST /temperatures/update/`. There is no automatic scheduler (cron, background tasks).
- The DB schema is managed by Alembic: every model change is recorded as a new migration. Batch mode (`render_as_batch`) is used for SQLite because it has limited `ALTER TABLE` support.
- No authentication, pagination, or caching, so the `/temperatures` endpoints return all records at once; with a large amount of data, pagination should be added.
- There are no tests; verification is done manually via Swagger UI.
