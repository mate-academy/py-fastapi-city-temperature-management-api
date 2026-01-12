from datetime import datetime

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas, crud
from app.database import SessionLocal
from app.routers.cities import router
from app.models import DBCity, DBTemperature
from app.services.weather import get_temperature_by_city_name


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


@router.get("/", response_model=list[schemas.Temperature])
def get_temperatures(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_temperature_list(db=db, skip=skip, limit=limit)


@router.get(
    "/temperatures/",
    response_model=list[schemas.Temperature],
)
def get_temperatures(skip: int = 0, limit: int = 100):
    return crud.get_temperature_list(skip=skip, limit=limit)


@router.get("/temperatures/{city_id}",
            response_model=list[schemas.Temperature])
def get_city_temperature(city_id: int, db: Session = Depends(get_db)):
    temperature = crud.get_temperature(db=db, city_id=city_id)
    if not temperature:
        raise HTTPException(status_code=404, detail="City not found")
    return temperature
