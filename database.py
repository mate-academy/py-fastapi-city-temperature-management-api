from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker, declarative_base

#sync_version
SQLALCHEMY_SYNC_DATABASE_URL = 'sqlite:///./city_temperature.db'

sync_engine = create_engine(
    SQLALCHEMY_SYNC_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
SyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)




#async_version
SQLALCHEMY_ASYNC_DATABASE_URL = 'sqlite+aiosqlite:///./city_temperature.db'

async_engine = create_async_engine(
    SQLALCHEMY_ASYNC_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
AsyncSessionLocal = async_sessionmaker(async_engine, autocommit=False, autoflush=False)





Base = declarative_base()
