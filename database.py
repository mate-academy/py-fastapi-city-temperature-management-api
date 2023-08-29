from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./city_temperature_catalog.db"
# SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./city_temperature_catalog.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
#
# engine = create_async_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )
# SessionLocal = sessionmaker(
#     autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
# )
#
# Base = declarative_base()
