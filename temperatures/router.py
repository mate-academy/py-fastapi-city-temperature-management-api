from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import SessionLocal
from cities.models import City
from temperatures import models
from temperatures import schemas
from temperatures.crud import create_or_update_temperature
from temperatures.services import get_temp

router = APIRouter()

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.post("/temperatures/update/")
async def update_temperatures(db: Session = Depends(get_db)):
    cities = db.scalars(select(City)).all()
    if not cities:
        raise HTTPException(status_code=404, detail="No cities in database")

    for city in cities:
        temp_value = await get_temp(city.name)
        if temp_value is not None:
            create_or_update_temperature(db=db, city_id=city.id, temp_val=temp_value)

    return "Temperatures updated successfully"


@router.get("/temperatures/", response_model=list[schemas.Temperature])
def get_temperatures(city_id: Optional[int] = None, db: Session = Depends(get_db)):
    stmt = select(models.Temperature)
    if city_id is not None:
        stmt = stmt.where(models.Temperature.city_id == city_id)
    return db.scalars(stmt).all()
