from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException

from . import schemas, crud
from dependencies import get_db


router = APIRouter()


@router.get("/temperatures", response_model=list[schemas.TemperatureDefault])
def get_all_temperatures(db: Session = Depends(get_db)):
    return crud.get_all_temperatures(db)


@router.get("/city/temperatures", response_model=list[schemas.TemperatureDefault])
def get_temperatures_by_city_id(city_id: int, db: Session = Depends(get_db)):
    db_city_id = crud.get_city_id(db, city_id)
    if not db_city_id:
        raise HTTPException(
            status_code=400,
            detail=f"city_id={city_id} was not found"
        )
    else:
        return crud.get_temperature_by_city_id(db, city_id)


@router.post("/temperature/", response_model=schemas.TemperatureDefault,
             status_code=201,
             response_description="Successful Response. Record of temperature was created")
def create_temperature(new_temperature_record: schemas.TemperatureCreate, db: Session = Depends(get_db)):
    db_temperature = crud.get_temperature_by_city_id(db, new_temperature_record.city_id)
    if not db_temperature:
        raise HTTPException(
            status_code=400,
            detail=f"city_id={new_temperature_record.city_id} was not found"
        )
    else:
        return crud.create_temperature(db, new_temperature_record)
