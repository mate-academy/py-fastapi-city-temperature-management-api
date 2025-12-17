from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List

from settings import SessionLocal
from . import schemas, crud


router = APIRouter(
    prefix="/temperatures",
    tags=["Temperature"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[schemas.Temperature])
def read_temperatures(
    city_id: int | None = Query(default=None),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    if city_id is not None:
        temps = crud.get_temperature_in_city(db, city_id=city_id, skip=skip, limit=limit)
    else:
        temps = crud.get_temperatures(db, skip=skip, limit=limit)

    return temps
