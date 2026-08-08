from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from db.engine import get_db
from temperature_api import schemas, crud

router = APIRouter(
    prefix="/temperature",
    tags=["Temperature"],
)

@router.get("/", response_model=list[schemas.Temperature], status_code=200)
def get_temperatures(db: Session = Depends(get_db)):
    return crud.get_all_temperatures(db=db)

@router.get("/", response_model=list[schemas.Temperature], status_code=200)
def get_temperatures(db: Session = Depends(get_db), city_id: int = 0):
    return crud.get_temperature_for_city(db=db, city_id=city_id)
