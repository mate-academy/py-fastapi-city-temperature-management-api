from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from database import SyncSessionLocal, AsyncSessionLocal, async_engine


#sync_version_session
def get_db() -> Session:
    db = SyncSessionLocal()

    try:
        yield db
    finally:
        db.close()


#async_version_session
async def get_async_db() -> AsyncSession:
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()


#annotates
def db_async_param(db_async: AsyncSession = Depends(get_async_db)):
    return db_async

DbAsyncDep = Annotated[AsyncSession, Depends(db_async_param)]


def db_sync_param(db_sync: Session = Depends(get_db)):
    return db_sync

DbSyncDep = Annotated[Session, Depends(db_sync_param)]


def city_id_query_param(city_id: int | None = None):
    return city_id

CityIdQuery = Annotated[int | None, Depends(city_id_query_param)]