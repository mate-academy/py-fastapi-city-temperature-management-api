   # City Temperature Management API

FastAPI application for managing city data and fetching current temperature data from external weather API.

## Tech Stack

- **FastAPI** — web framework
- **SQLAlchemy** — ORM
- **SQLite** — database
- **Pydantic** — data validation
- **httpx** — async HTTP client
- **wttr.in** — weather data source (free, no API key required)

## Project Structure

```
├── main.py
├── database.py
├── dependies.py
├── settings.py
├── requirements.txt
├── README.md
├── alembic.ini
├── alembic/
│   └── versions/
└── temperature_management/
    ├── __init__.py
    ├── models.py
    ├── schemas.py
    ├── crud.py
    └── router.py
```

## Installation

1. Clone the repository:
```bash
    git clone https://github.com/your-username/py-fastapi-city-temperature-management-api.git
    cd py-fastapi-city-temperature-management-api
```

2. Create and activate virtual environment:
```bash
    python -m venv .venv
    source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
    pip install -r requirements.txt
```

## Running

```bash
    uvicorn main:app --reload
```

- API: `http://127.0.0.1:8000`
- Swagger docs: `http://127.0.0.1:8000/docs`

## API Endpoints

### Cities

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/cities/` | Get all cities |
| POST | `/cities/` | Create a new city |
| GET | `/cities/{city_id}/` | Get city by ID |
| PUT | `/cities/{city_id}/` | Full update of a city |
| PATCH | `/cities/{city_id}/` | Partial update of a city |
| DELETE | `/cities/{city_id}/` | Delete a city |

### Temperatures

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/temperatures/update/` | Fetch and store current temperatures for all cities |
| GET | `/temperatures/` | Get all temperature records |
| GET | `/temperatures/?city_id={id}` | Get temperature records for a specific city |

## Usage Examples

### Create a city
```bash
    curl -X POST http://127.0.0.1:8000/cities/ \
      -H "Content-Type: application/json" \
      -d '{"name": "Kyiv", "additional_info": "Capital of Ukraine"}'
```

### Fetch current temperatures for all cities
```bash
  curl -X POST http://127.0.0.1:8000/temperatures/update/
```

### Get all temperature records
```bash
  curl http://127.0.0.1:8000/temperatures/
```

### Get temperatures for a specific city
```bash
  curl http://127.0.0.1:8000/temperatures/?city_id=1
```

## Design Choices

- **wttr.in** used as weather data source — free, no registration or API key required
- Duplicate temperature records are prevented by checking `city_id` + `date_time` combination
- If a city name is not recognized by wttr.in, it is skipped and processing continues for other cities
- HTTP errors (`404`, `400`) are raised in CRUD functions for clean endpoint code
- `asyncio.run()` used to run async temperature fetch from a sync FastAPI endpoint

## Assumptions

- SQLite is used for simplicity; can be replaced with PostgreSQL by updating `DATABASE_URL` in `.env`
- Temperature is stored and returned in Celsius
- `date_time` is parsed from wttr.in `observation_time` field combined with the current date