# City Temperature API

A FastAPI app that stores cities and saves their current temperature from [WeatherAPI](https://www.weatherapi.com/).

## How to run

You need Python 3.13+ and [uv](https://docs.astral.sh/uv/).

1. Install the dependencies:

   ```bash
   uv sync
   ```

2. Create a `.env` file in the project root and add your WeatherAPI key:

   ```
   YOUR_API_KEY=your_key_here
   ```

3. Create the database tables:

   ```bash
   uv run alembic upgrade head
   ```

4. Start the server:

   ```bash
   uv run uvicorn main:app --reload
   ```

5. Open http://127.0.0.1:8000/docs to try the API.

## Endpoints

| Method | URL | What it does |
|---|---|---|
| GET | `/cities/` | List all cities |
| GET | `/cities/{city_id}` | Get one city |
| POST | `/cities/` | Create a city |
| DELETE | `/cities/{city_id}` | Delete a city |
| GET | `/temperatures/` | List all temperature records |
| GET | `/temperatures/{city_id}` | List temperature records for one city |
| POST | `/temperatures/update/` | Fetch and save the current temperature for all cities |

## Design choices

- `city` and `temperature` are separate modules, each with its own routers, CRUD functions and schemas.
- Database models are in `models`, and Alembic manages the tables.
- SQLite keeps the setup simple.
- The update endpoint is async and uses `httpx`, because it waits for an external API.
- Other endpoints stay sync, because they only use the sync database session.
- The API key is kept in `.env`, so it is not stored in the code.

## Assumptions and simplifications

- City names must be ones WeatherAPI can find.
- If WeatherAPI can't return a city's temperature, that city is skipped and no error is returned.
- Cities are updated one at a time, not in parallel.
