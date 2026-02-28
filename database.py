from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from settings import get_settings


settings = get_settings()

engine = create_engine(
    settings.database_url, 
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)

Base = declarative_base()
