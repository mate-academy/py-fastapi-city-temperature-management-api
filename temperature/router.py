import os

from dotenv import load_dotenv
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependencies import get_db
from temperature import schemas, crud
from temperature.temperature_update import fetch_temperatures

WEATHER_API = os.environ["WEATHER_API"]

router = APIRouter()


@router.get(
    "/temperatures/",
    response_model=list[schemas.TemperatureList]
)
def read_temperatures(
    city_id: int | None = None,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
):
    return crud.get_temperatures(
        city_id=city_id, skip=skip, limit=limit, db=db
    )


load_dotenv()


@router.post("/temperatures/update/", response_model=dict)
async def update_temperatures(db: Session = Depends(get_db)):
    await fetch_temperatures(db)
