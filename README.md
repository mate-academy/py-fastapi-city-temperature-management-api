# City Temperature Management API

A FastAPI service for managing cities and their latest temperatures, with weather data fetched from OpenWeather.

## How to Run the Application

### 1) Clone and open the project

```bash
git clone <your-repository-url>
cd py-fastapi-city-temperature-management-api
```

### 2) Create and activate virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3) Install dependencies

```bash
pip install -r requirements.txt
```

### 4) Configure environment variables

Create a `.env` file in the project root:

```env
API_KEY=your_openweather_api_key
DATABASE_URL=your_database_url
```

> Use your real OpenWeather key in `API_KEY`.

### 5) Run database migrations

```bash
alembic upgrade head
```

### 6) Start the API

```bash
fastapi dev main.py
```

The API will be available at:

- App: `http://127.0.0.1:8000`
- Swagger UI: `http://127.0.0.1:8000/docs`

---

## Design Choices

- **FastAPI** was selected for fast development, built-in validation, and async support.
- **OpenWeather API** is used as an external source for current weather data.
- **HTTP requests are async** to fetch temperatures for multiple cities concurrently and reduce total waiting time.
- **SQLAlchemy ORM** is used for data modeling and persistence.
- **Alembic** is used for schema versioning and repeatable DB changes.

---

## Assumptions and Simplifications

- Only the **latest temperature** per city is stored (not full historical series).
- City names are treated as unique entries.
- If external weather fetch fails for a city, the update process continues for other cities.
- Temperature values are requested in **metric** units.
- Error handling is kept straightforward to keep the project structure simple.

---

## Notes

- Ensure your database is running before applying migrations or starting the app.
- If you change models, create a new Alembic migration before deploying.