from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependencies import get_db
from . import schemas, crud

router = APIRouter()


@router.get("/temperature/", response_model=list[schemas.TemperatureBase])
def get_all_temperature(db: Session = Depends(get_db)):
    return crud.all_temperature(db=db)


@router.get("/temperatures/?city_id={city_id}", response_model=list[schemas.TemperatureBase])
def get_all_temperature_by_city_id(city_id: int, db: Session = Depends(get_db)):
    return crud.all_temperature_by_city_id(db=db, city_id=city_id)
