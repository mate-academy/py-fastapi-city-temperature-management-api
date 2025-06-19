import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./city_temp.db")
