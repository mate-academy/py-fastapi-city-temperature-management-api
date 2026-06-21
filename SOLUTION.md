# City Temperature Management API


## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Run

```bash
uvicorn app.main:app --reload
```

Open the API documentation:

```text
http://127.0.0.1:8000/docs
```

## Endpoints

- `POST /cities` - create a city.
- `GET /cities` - list all cities.
- `DELETE /cities/{city_id}` - delete a city.
- `POST /temperatures/update` - fetch current temperatures for all cities and save them.
- `GET /temperatures` - list all temperature records.
- `GET /temperatures?city_id=1` - list temperature records for one city.

## Design Choices

- SQLite is used as the database.
- SQLAlchemy is used for database models and sessions.
- FastAPI dependency injection is used for the database session.
- Open-Meteo is used for weather data because it does not require an API key.
