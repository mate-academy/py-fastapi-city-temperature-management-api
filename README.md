# City Temperature API

FastAPI application for managing cities and storing temperature history.

## Features

- Create, list, read, update and delete cities.
- Fetch current temperature for every city asynchronously.
- Save temperature records in SQLite.
- Filter temperature history by `city_id`.
- Automatic Swagger documentation.

## Technologies

- FastAPI
- SQLAlchemy 2
- SQLite
- Pydantic 2
- HTTPX
- Open-Meteo API

## Project structure

```text
app/
├── crud/
├── models/
├── routers/
├── schemas/
├── services/
├── database.py
└── main.py
```

## Installation

```bash
git clone <repository-url>
cd fastapi-city-temperature

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

For Windows:

```bash
.venv\Scripts\activate
```

## Run

```bash
uvicorn app.main:app --reload
```

Open:

- API: `http://127.0.0.1:8000`
- Swagger: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Endpoints

### Cities

- `POST /cities`
- `GET /cities`
- `GET /cities/{city_id}`
- `PUT /cities/{city_id}`
- `DELETE /cities/{city_id}`

Example request:

```json
{
  "name": "London",
  "additional_info": "Capital of the United Kingdom"
}
```

### Temperatures

- `POST /temperatures/update`
- `GET /temperatures`
- `GET /temperatures?city_id=1`

The update endpoint first converts every city name to coordinates using the
Open-Meteo geocoding endpoint. It then requests current temperature data for
all cities concurrently with `asyncio.gather` and `httpx.AsyncClient`.

## Design choices

- SQLAlchemy models and Pydantic schemas are kept in separate modules.
- Database sessions are provided through FastAPI dependency injection.
- Deleting a city also deletes its temperature history.
- A failed request for one city does not prevent successful cities from being
  stored.
- City names are unique to avoid duplicate weather requests.

## Assumptions

- City names can be resolved by the Open-Meteo geocoding service.
- Temperature is stored in degrees Celsius.
- SQLite is sufficient for this educational project.
