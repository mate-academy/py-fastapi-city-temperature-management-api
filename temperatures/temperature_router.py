from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
from dependencies import get_db
from temperatures import crud

router = APIRouter()


@router.get("/temperatures/")
def read_temperatures(db: Session = Depends(get_db)):
    return crud.get_temperatures(db)


@router.get("/temperatures/{city_id}/")
def read_temperature_for_city(city_id: int, db: Session = Depends(get_db)):
    db_temperature = crud.get_temperatures(db, city_id=city_id)
    return db_temperature


@router.post("/temperatures/update/")
async def update_temperature(db: Session = Depends(get_db)):
    for city in db.query(models.City).all():
        try:
            await crud.update_temperatures(db=db, city=city)
        except KeyError:  # If city does not exist
            continue
    return {"message": "Temperatures were updated"}
