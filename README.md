# City Temperature Management API

An async REST API for managing cities and tracking their temperature history. Built with FastAPI, SQLAlchemy 2.0, and SQLite.

## Key Features

*   Full CRUD for city management
*   Automatic temperature fetching from WeatherAPI for all tracked cities
*   Temperature history with filtering by city
---
## Tech Stack

*   **Backend:** Python 3.14, FastAPI
*   **Database:** SQLite (async via aiosqlite)
*   **ORM:** SQLAlchemy 2.0 (async)
*   **Migrations:** Alembic
*   **External API:** WeatherAPI (weatherapi.com)
---

## Running Locally

This project uses `uv` as its package manager.

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd py-fastapi-city-temperature-management-api
    ```

2.  **Install dependencies:**
    ```bash
    uv sync
    ```

3.  **Create and configure the environment file:**
    Copy the provided `.env.example` to `.env` and set your WeatherAPI key. A free key can be obtained at [weatherapi.com](https://www.weatherapi.com/).
    ```bash
    cp .env.example .env
    ```

4.  **Apply database migrations:**
    ```bash
    uv run alembic upgrade head
    ```

5.  **Start the development server:**
    ```bash
    uv run fastapi dev main.py
    ```

6.  **Accessing the application:**
    *   **Interactive Docs:** `http://127.0.0.1:8000/docs`
---

## Design Choices & Assumptions

*   Settings are lazily initialized with `@lru_cache` but validated at startup via `lifespan` — the server won't start without a valid `.env`.
*   `POST /temperatures/update` uses partial success: if some cities fail to fetch, the rest are still saved. An error is raised only if all requests fail.
