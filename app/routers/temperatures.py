from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from app import crud, schemas
from app.database import get_db
from app.weather_client import fetch_current_temperature

router = APIRouter(prefix="/temperatures", tags=["temperatures"])


@router.post("/update")
async def update_temperatures(db: Session = Depends(get_db)):
    cities = crud.get_cities(db)
    updated, failed = [], []
    for city in cities:
        temp = await fetch_current_temperature(city.name)
        if temp is None:
            failed.append(city.name)
            continue
        crud.create_temperature(db, city.id, temp, datetime.utcnow())
        updated.append(city.name)
    return {"updated": updated, "failed": failed}


@router.get("/", response_model=list[schemas.Temperature])
def read_temperatures(
        city_id: int | None = None,
        db: Session = Depends(get_db)
):
    return crud.get_temperatures(db, city_id)
