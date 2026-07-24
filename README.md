# City Temperature Management API

A FastAPI service for maintaining a list of cities and recording their current
temperatures. Temperature readings are fetched from
[WeatherAPI](https://www.weatherapi.com/) and persisted in SQLite.

## Run the application

### Prerequisites

- Python 3.10 or newer
- A WeatherAPI API key

### Setup

1. Create and activate a virtual environment (optional, but recommended):

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate
   ```

2. Install the dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

3. Create a local environment file from the example and add a real WeatherAPI
   key:

   ```powershell
   Copy-Item .env.sample .env
   ```

   ```dotenv
   DB_URI=sqlite+aiosqlite:///db.sqlite3
   WEATHERAPI_KEY=your-weatherapi-key
   ```

4. Create or update the database schema:

   ```powershell
   alembic upgrade head
   ```

5. Start the application:

   ```powershell
   python main.py
   ```

   The server listens on `http://localhost:8000`. Interactive API
   documentation is available at `http://localhost:8000/docs`.

## API overview

When running locally, use the following paths (the trailing slash is part of
the implemented routes):

| Method   | Path                               | Purpose                                     |
|----------|------------------------------------|---------------------------------------------|
| `POST`   | `/cities/`                         | Create a city                               |
| `GET`    | `/cities/`                         | List cities                                 |
| `GET`    | `/cities/{city_id}/`               | Retrieve one city                           |
| `DELETE` | `/cities/{city_id}/`               | Delete a city                               |
| `POST`   | `/temperatures/update/`            | Fetch and save one current reading per city |
| `GET`    | `/temperatures/`                   | List recorded temperatures                  |
| `GET`    | `/temperatures/?city_id={city_id}` | List readings for a city                    |

Example city request:

```json
{
  "name": "Budapest",
  "additional_info": "Hungary"
}
```

The app is configured with `root_path="/api/v1"` for deployment behind a
reverse proxy. If such a proxy is configured, expose the API under `/api/v1`;
the local development server itself serves the routes listed above directly.

## Design choices

- **Feature-based modules:** `cities` and `temperatures` each contain their
  router, schema, model, and data-access code, keeping HTTP concerns separate
  from persistence logic.
- **Async I/O:** SQLAlchemy's async session and `httpx.AsyncClient` avoid
  blocking the event loop. The temperature-update endpoint fetches all city
  readings concurrently with `asyncio.gather`.
- **SQLite with Alembic migrations:** SQLite makes the project simple to run
  locally, while Alembic supplies repeatable schema creation and upgrades.
- **Dependency injection:** database sessions are provided through FastAPI's
  `Depends`, centralizing transaction commit and rollback behavior.
- **Partial update results:** a failed request for one city is returned as an
  error for that city without discarding successful readings for other cities.

## Assumptions and simplifications

- City names are submitted in a form understood by WeatherAPI; no geographic
  coordinates, duplicate-name prevention, or city-name normalization is
  implemented.
- Each update stores the temperature in Celsius (`current.temp_c`) with a
  single UTC timestamp shared by the batch.
- Temperature history is retained indefinitely; there is no pagination,
  ordering option, retention policy, or aggregation endpoint.
- The API has no authentication, authorization, rate limiting, or automated
  tests. These should be added before a production deployment.
- Deleting a city does not explicitly delete its historical temperature rows;
  foreign-key cascade behavior is intentionally not configured.
