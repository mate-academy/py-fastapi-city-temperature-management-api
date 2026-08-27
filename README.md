# City Temperature Management API

A FastAPI application for managing cities and recording their current temperatures. It uses SQLite and SQLAlchemy for persistence and the free, keyless [Open-Meteo](https://open-meteo.com/) APIs.

## Setup and run

Python 3.10 or newer is required.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API is available at `http://127.0.0.1:8000`, with interactive documentation at `/docs`. The `city_temperatures.db` SQLite file is created automatically.

## API

| Method | Path | Description |
| --- | --- | --- |
| `POST` | `/cities` | Create a city |
| `GET` | `/cities` | List cities |
| `GET` | `/cities/{city_id}` | Get one city |
| `PUT` | `/cities/{city_id}` | Replace one city |
| `DELETE` | `/cities/{city_id}` | Delete a city and its history |
| `POST` | `/temperatures/update` | Fetch and store weather for every city |
| `GET` | `/temperatures` | List all temperature history |
| `GET` | `/temperatures?city_id=1` | Filter history by city |
| `GET` | `/health` | Health check |

```bash
curl -X POST http://127.0.0.1:8000/cities \
  -H 'Content-Type: application/json' \
  -d '{"name":"Kyiv","additional_info":"Capital of Ukraine"}'
curl -X POST http://127.0.0.1:8000/temperatures/update
curl 'http://127.0.0.1:8000/temperatures?city_id=1'
```

The update endpoint fetches cities concurrently. A failure for one city does not discard successful readings for others; its response separates `created` records and `errors` keyed by city ID.

## Design choices and assumptions

- API schemas are separate from SQLAlchemy persistence models.
- Database sessions use FastAPI dependency injection.
- City names are unique because they are used for weather geocoding.
- Open-Meteo geocodes the city on each update; coordinates are not persisted because they are outside the requested model.
- Weather timestamps are requested in UTC and may be rounded to Open-Meteo's reporting interval.
- Deleting a city also deletes its temperature history.

## Tests

Tests use in-memory SQLite and mock the external weather service, so they require no internet connection.

```bash
pip install -r requirements-dev.txt
pytest
```
