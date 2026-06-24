# City Temperature API

A small FastAPI application for storing cities and their temperature history.

## Run the application

Create and activate a virtual environment, then install the dependencies:

```bash
python -m venv .venv
pip install -r requirements.txt
```

Run the API:

```bash
uvicorn app.main:app --reload
```

The interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

The SQLite database is created automatically as `weather.db`.

## Endpoints

- `POST /cities` - create a city
- `GET /cities` - list cities
- `DELETE /cities/{city_id}` - delete a city
- `POST /temperatures/update` - fetch and store current temperatures
- `GET /temperatures` - list all temperature records
- `GET /temperatures?city_id={city_id}` - list records for one city

Example city request:

```json
{
  "name": "Kyiv",
  "additional_info": "Capital of Ukraine"
}
```

## Design choices

The project uses async SQLAlchemy with SQLite and FastAPI dependency injection
for database sessions.

Current temperatures are fetched asynchronously from `wttr.in`, which does not
require an API key.

## Assumptions and simplifications

- City names are unique.
- Temperatures are stored in Celsius.
- If temperature fetching fails for any city, no new records are stored.
- Deleting a city also deletes its temperature history.
- Optional city detail and update endpoints are not included.
