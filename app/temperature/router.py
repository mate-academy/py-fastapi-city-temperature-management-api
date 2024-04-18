from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from . import schemas, crud


router = APIRouter()


@router.post("/temperatures/update")
async def update_temperatures(db: Session = Depends(get_db)):
    return await crud.update_temperature(db=db)


@router.get("/temperatures/", response_model=list[schemas.Temperature])
def read_temperatures(db: Session = Depends(get_db)):
    return crud.get_temperatures(db=db)


@router.get("/temperatures/{city_id}", response_model=list[schemas.Temperature])
def read_temperatures(city_id: int, db: Session = Depends(get_db)):
    return crud.get_temperature_by_city_id(db=db, city_id=city_id)
