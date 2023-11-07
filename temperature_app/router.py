from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from temperature_app import schemas, crud
from dependencies import get_db

router = APIRouter()


@router.post("/temperatures/update/", response_model=list[schemas.Temperature])
def update_temperature(db: Session = Depends(get_db)):
    return crud.update_temperatures(db=db)


@router.get("/temperatures/", response_model=list[schemas.Temperature])
def read_temperatures(city_id: int = None, db: Session = Depends(get_db)):
    return crud.get_temperatures(db=db, city_id=city_id)
