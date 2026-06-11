# City Temperature Management API

## How to Run

1. Clone the repository and navigate to the project folder:
   ```bash
   git clone <repo-url>
   cd py-fastapi-city-temperature-management-api
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

5. Open API docs at: http://127.0.0.1:8000/docs

## Design Choices

- **Async SQLAlchemy** with `aiosqlite` driver for fully async database operations.
- **Two separate packages** (`city` and `temperature`) each with its own `models`, `schemas`, `crud`, and `router` — keeps concerns separated and code easy to navigate.
- **wttr.in** was chosen as the weather data source — it is free, requires no API key, and supports city name queries directly.
- **Lifespan** is used to create database tables on startup instead of the deprecated `on_event("startup")`.

## Assumptions and Simplifications

- No authentication is implemented — all endpoints are public.
- Temperature update fetches data for all cities sequentially, not in parallel.
- `wttr.in` availability is assumed — no fallback if the service is down.
