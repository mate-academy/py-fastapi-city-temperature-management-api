from datetime import datetime
from typing import Optional

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from app import schemas, crud
from app.database import SessionLocal

from app.models import DBCity, DBTemperature
from app.services.weather import get_temperature_by_city_name


router = APIRouter()

def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.post("/temperatures/update/")
async def update_temperatures(db: Session = Depends(get_db)):
    cities = db.query(DBCity).all()

    for city in cities:
        try:
            temp = await get_temperature_by_city_name(city.name)
        except ValueError:
            continue

        record = DBTemperature(
            city_id=city.id, temperature=temp, date_time=datetime.utcnow()
        )
        db.add(record)

    db.commit()
    return {"status": "ok"}


@router.get("/temperatures/", response_model=list[schemas.Temperature])
def get_temperatures(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_temperature_list(db=db, skip=skip, limit=limit)


@router.get(
    "/temperatures/",
    response_model=list[schemas.Temperature],
)
def get_temperatures(skip: int = 0,
                     limit: int = 100,
                     db: Session = Depends(get_db)):
    return crud.get_temperature_list(skip=skip, limit=limit, db=db)


@router.get("/temperatures/{city_id}",
            response_model=list[schemas.Temperature])
def get_temperatures(city_id: Optional[int] = None,
                     skip: int = 0,
                     limit: int = 100,
                     db: Session = Depends(get_db)):

    if city_id is not None:
        return crud.get_temperature_by_city(db=db, city_id=city_id, skip=skip, limit=limit)
    return crud.get_temperature_list(db=db, skip=skip, limit=limit)