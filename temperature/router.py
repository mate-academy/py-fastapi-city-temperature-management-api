from fastapi import APIRouter, Depends

from database import SessionLocal
from dependencies import get_db, CommonsDependencies

from temperature import crud
from temperature import schemas

router = APIRouter()

@router.get('/temperature/update/')
async def update_temperature(db: SessionLocal = Depends(get_db)):
    return await crud.sync_temperature(db)


@router.get('/temperature/', response_model=list[schemas.TemperatureRead])
def get_temperature_list(commons: CommonsDependencies, city_id: int = None, db: SessionLocal = Depends(get_db)):
    return crud.get_temperature_list(db, city_id, commons)
