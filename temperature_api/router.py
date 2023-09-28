import os

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from httpx import AsyncClient
from sqlalchemy.orm import Session

import database
from dependencies import get_db
from settings import settings
from temperature_api import crud, schemas

database.Base.metadata.create_all(bind=database.engine)

router = APIRouter()

load_dotenv()
WEATHER_API = os.environ["WEATHER_KEY"]


@router.post("/temperatures/update", response_model=dict)
async def update_temperatures(
        city: str,
        db: Session = Depends(get_db)
):
    async with AsyncClient() as client:
        response = await client.get(
            settings.WEATHER_KEY, params={"key": WEATHER_API, "q": city}
        )
        if response.status_code == 200:
            temperature_data = response.json()
            for data_point in temperature_data:
                temperature_create = schemas.TemperatureCreate(**data_point)
                crud.create_temperature(db, temperature_create)
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail="Failed to fetch temperature data"
            )


@router.get("/temperatures/", response_model=list[schemas.Temperature])
def get_all_temperatures(
        db: Session = Depends(get_db)
):
    return crud.get_all_temperatures(db=db)


@router.get(
    "/temperatures/?city_id={city_id}",
    response_model=schemas.Temperature
)
def get_temperature_to_city(
        city_id: int,
        db: Session = Depends(get_db)
):
    db_tem = crud.get_temperature(db=db, city_id=city_id)
    if db_tem is None:
        raise HTTPException(status_code=404, detail="Temperature not found")
    return db_tem
