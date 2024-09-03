from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.core.database import get_db


def get_service(session: AsyncSession = Depends(get_db)) -> crud.Service:
    return crud.Service(session)
