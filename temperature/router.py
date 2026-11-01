from fastapi import APIRouter, Depends

from database import SessionLocal
from dependencies import get_db

from temperature import crud

router = APIRouter()

@router.get('/temperature/update/')
async def update_temperature(db: SessionLocal = Depends(get_db)):
    return await crud.sync_temperature(db)
