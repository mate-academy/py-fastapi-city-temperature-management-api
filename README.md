# City Temperature Management API

A FastAPI application for maintaining a list of cities and recording their current
temperatures. Data is stored in SQLite through SQLAlchemy. Current weather is loaded
asynchronously from the keyless [Open-Meteo API](https://open-meteo.com/).

## Running the application

Python 3.11 or newer is recommended.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API is then available at `http://127.0.0.1:8000`. Interactive OpenAPI
documentation is available at `http://127.0.0.1:8000/docs`.

By default, the application creates `city_temperatures.db` in the project directory.
Set `DATABASE_URL` to use another SQLAlchemy database URL:

```bash
DATABASE_URL=sqlite:///./another.db uvicorn app.main:app
```

## API

| Method | Path | Description |
|---|---|---|
| `POST` | `/cities` | Create a city |
| `GET` | `/cities` | List cities |
| `GET` | `/cities/{city_id}` | Get one city |
| `PUT` | `/cities/{city_id}` | Update supplied city fields |
| `DELETE` | `/cities/{city_id}` | Delete a city and its temperature history |
| `POST` | `/temperatures/update` | Fetch and save current temperatures for all cities |
| `GET` | `/temperatures` | List all recorded temperatures |
| `GET` | `/temperatures?city_id=1` | Filter temperature history by city |
| `GET` | `/health` | Health check |

Example:

```bash
curl -X POST http://127.0.0.1:8000/cities \
  -H 'Content-Type: application/json' \
  -d '{"name":"Dublin","additional_info":"Ireland"}'

curl -X POST http://127.0.0.1:8000/temperatures/update
curl 'http://127.0.0.1:8000/temperatures?city_id=1'
```

## Design choices

- Routers, persistence models, validation schemas, and the external weather client
  are separated so each part can be tested or replaced independently.
- A database session and the weather service are injected as FastAPI dependencies.
- Weather requests for all cities run concurrently using `asyncio.gather`. Records
  are committed only after every request succeeds; an upstream failure returns
  `502 Bad Gateway` without saving a partial update.
- SQLAlchemy provides the persistence layer, while SQLite keeps local setup simple.
- The application creates its database tables automatically during startup.

## Assumptions and simplifications

- Open-Meteo geocoding can return several places with the same name. This project
  intentionally uses the first result because the required city model has no country
  or coordinates.
- Deleting a city cascades to its temperature history.
- Every call to `/temperatures/update` creates a new history record for each city,
  even if Open-Meteo returns the same observation time as an earlier call.
- Database migrations and authentication are outside the scope of this assignment.

## Tests

```bash
pip install -r requirements-dev.txt
pytest
```

Tests use an isolated in-memory SQLite database and a fake weather service, so they
do not require internet access.
