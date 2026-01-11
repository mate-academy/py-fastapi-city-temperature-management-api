import datetime
import httpx
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.engine import SessionLocal
from city import models as city_models
from . import crud, schemas
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENWEATHER_API_KEY")


router = APIRouter(prefix="/temperatures", tags=["temperatures"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.Temperature)
def create_temperature(
    temperature: schemas.TemperatureCreate, db: Session = Depends(get_db)
):
    return crud.create_temperature(db, temperature)


@router.get("/", response_model=list[schemas.Temperature])
def read_temperature(
    city_id: int | None = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    if city_id is not None:
        records = crud.get_temperatures_by_city(db, city_id, skip=skip, limit=limit)
        return records
    return crud.get_temperature(db, skip=skip, limit=limit)




@router.post("/update")
async def update_temperature(db: Session = Depends(get_db)):
    cities = db.query(city_models.City).all()
    if not cities:
        raise HTTPException(status_code=404, detail="No cities found in database")

    new_records = []

    async with httpx.AsyncClient() as client:
        for city in cities:
            if not api_key:
                raise HTTPException(status_code=500, detail="OpenWeather API key not configured")

            url = f"http://api.openweathermap.org/data/2.5/weather?q={city.name}&appid={api_key}&units=metric"

            response = await client.get(url)
            if response.status_code != 200:
                continue

            data = response.json()
            temp_value = data["main"]["temp"]

            new_records.append(
                crud.models.Temperature(
                    city_id=city.id,
                    date_time=datetime.datetime.utcnow(),
                    temperature=temp_value,
                )
            )

    # Добавляем все новые записи и коммитим один раз
    db.add_all(new_records)
    db.commit()

    return {"message": f"Temperature updated successfully for {len(new_records)} cities"}
