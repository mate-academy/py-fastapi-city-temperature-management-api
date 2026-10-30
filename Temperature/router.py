from fastapi import APIRouter, Depends
from httpx import AsyncClient
from sqlalchemy.orm import Session

from Temperature import schemas
from Temperature.crud import create_temperature, retrieve_temp
from dependencies import get_db

router = APIRouter()


@router.post("/temperatures/update/", response_model=list[schemas.TemperatureList])
async def create_all_temperature_for_cities(db: Session = Depends(get_db)):
    async with AsyncClient() as client:
        return await create_temperature(db, client)


@router.get("/temperatures/", response_model=list[schemas.TemperatureList])
def get_temp_with_city_id(city_id: int | None = None, db: Session = Depends(get_db)):
    return retrieve_temp(db, city_id)