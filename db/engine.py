from sqlalchemy import event
from sqlite3 import Connection as Sqlite3Conn
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
)

from config import settings

engine = create_async_engine(
    settings.DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = async_sessionmaker(
    bind=engine, autoflush=False, autocommit=False
)

@event.listens_for(engine.sync_engine, "connect")
def enforce_sqlite_fk(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, Sqlite3Conn):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
