# Weather in Cities API

A FastAPI service designed to fetch, store, and manage weather data for multiple cities. This application utilizes modern Python practices to ensure high performance and data integrity.

## Key Features
- **Async API Integration**: Uses `httpx` and `asyncio` to fetch weather data for multiple cities concurrently.
- **ORM & Database**: Implements SQLAlchemy 2.0 with SQLite.
- **Migration Management**: Alembic is used for version-controlled database migrations.
- **Modular Design**: Structured for scalability and maintainability.

## Tech Stack
- **Framework**: FastAPI
- **Database**: SQLite
- **ORM**: SQLAlchemy 2.0
- **Migrations**: Alembic
- **Validation**: Pydantic
- **HTTP Client**: httpx

## How to setup

Follow these steps to configure and run the project locally.

```bash
# 1. Create a .env file in the root directory and add:
DATABASE_URL=sqlite+aiosqlite:///./project.db
PI_PREFIX=/api/v1
WEATHER_API_KEY=your_weather_api_key_here

2. Install dependencies
pip install -r requirements.txt

3. Apply database migrations to create the required tables
alembic upgrade head

# 4. Start the FastAPI development server
python run.py
```


## Project Structure
```text
api/
├── alembic/                # Database migrations
├── app/
│   ├── database/           # Configuration and database setup     
│   ├── models/             # SQLAlchemy database models
│   ├── routers/            # API route handlers
│   ├── schemas/            # Pydantic schemas
│   ├── services/           # Business logic and external API calls
│   └── main.py             # Main router
├── .gitignore
├── requirements.txt        # Dependencies
├── alembic.ini             # Alembic configuration
├── run.py                  # Entry point
└── README.md
