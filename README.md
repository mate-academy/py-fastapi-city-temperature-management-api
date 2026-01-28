## City Temperature Management API

FastAPI service for managing cities and storing current temperature snapshots for each city.

### Requirements

- Python 3.12+
- SQLite (local file)

### Configuration

Create `.env` in the project root (optional). Default is SQLite:

```
DATABASE_URL=sqlite+aiosqlite:///./test.db
ECHO=False
```

### Database

Run migrations:

```
alembic upgrade head
```

### Run the API

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn api_v1.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

### API Usage

Cities:

- `POST /cities`
- `GET /cities`
- `GET /cities/{city_id}`
- `PUT /cities/{city_id}`
- `PATCH /cities/{city_id}`
- `DELETE /cities/{city_id}`

Example:

```
curl -X POST http://127.0.0.1:8000/cities \
  -H "Content-Type: application/json" \
  -d '{"name":"Kyiv","additional_info":"UA"}'
```

Query params for list endpoints:

- `skip` (default `0`)
- `limit` (default `100`, max `100`)

Temperatures:

- `POST /temperatures/update` fetches current temperature for all cities and stores results.
- `GET /temperatures` returns temperature history.
- `GET /temperatures?city_id={city_id}` returns history for a single city.

Example:

```
curl -X POST http://127.0.0.1:8000/temperatures/update
```

```
curl "http://127.0.0.1:8000/temperatures?city_id=1&limit=20"
```

### External API

Temperature data is fetched from Open-Meteo (no API key required):

- Geocoding: `https://geocoding-api.open-meteo.com/v1/search`
- Current weather: `https://api.open-meteo.com/v1/forecast`

### Design choices and assumptions

- SQLite is used for local development.
- Temperature updates append new history records (duplicates are possible if data does not change).
- Uniqueness of city names is enforced at the database level and converted to `409 Conflict` in the API.
