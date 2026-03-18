from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..deps import get_db
from .. import crud, models
from ..services.weather import fetch_temperature

router = APIRouter(prefix="/temperatures", tags=["Temperatures"])


@router.post("/update")
async def update_temperatures(db: Session = Depends(get_db)):
    cities = db.query(models.City).all()

    records = []

    for city in cities:
        temp = await fetch_temperature(city.latitude, city.longitude)
        record = crud.create_temperature_record(city.id, temp)
        records.append(record)

    # SINGLE COMMIT (FIX)
    db.add_all(records)
    db.commit()

    return records


@router.get("/")
def get_all(city_id: int | None = None, db: Session = Depends(get_db)):
    return crud.get_temperatures(db, city_id)
