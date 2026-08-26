from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import httpx
from datetime import datetime

from .. import models, schemas
from ..database import SessionLocal

router = APIRouter(prefix="/temperatures", tags=["Temperatures"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/update")
async def update_temperatures(db: Session = Depends(get_db)):
    cities = db.query(models.City).all()
    if not cities:
        return {"message": "No cities found to update."}

    async with httpx.AsyncClient() as client:
        for city in cities:
            url = f"https://wttr.in/{city.name}?format=j1"
            try:
                response = await client.get(url)

                if response.status_code == 200:
                    data = response.json()
                    current_temp = float(data["current_condition"][0]["temp_C"])

                    new_temp = models.Temperature(
                        city_id=city.id,
                        temperature=current_temp,
                        date_time=datetime.now(datetime.UTC)
                    )
                    db.add(new_temp)
            except Exception as e:
                print(f"Failed to fetch data for {city.name}: {e}")

    db.commit()
    return {"message": "Temperatures updated successfully"}


@router.get("/", response_model=List[schemas.Temperature])
def read_temperatures(city_id: int = None, db: Session = Depends(get_db)):
    if city_id:
        return db.query(models.Temperature).filter(models.Temperature.city_id == city_id).all()
    return db.query(models.Temperature).all()