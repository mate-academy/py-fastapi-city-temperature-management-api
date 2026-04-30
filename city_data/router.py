from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from city_data import crud, schemas, models
from dependencies import get_db

router = APIRouter()

@router.get("/cities/")
def get_cities(db: Session = Depends(get_db)):
    return crud.get_city_list(db=db)

@router.post("/cities/")
def create_city(city_data: schemas.CityCreate, db: Session = Depends(get_db)):
    return crud.create_city(db=db, city_data=city_data)

@router.delete("/cities/{city_id}/")
def delete_city(city_id: int, db: Session = Depends(get_db)):
    return crud.delete_city(db=db, city_id=city_id)

@router.post("/temperatures/update")
async def create_temperature(db: Session = Depends(get_db)):
    cities = db.scalars(select(models.City)).all()
    for city in cities:
        lat, lon = await crud.geocode_city(city.name)
        temperature = await crud.fetch_temperature(lat, lon)
        crud.save_temperature(db=db, temperature_data=temperature, city_id=city.id)

@router.get("/temperatures/")
def get_temperature(city_id, db: Session = Depends(get_db)):
    if city_id is None:
        return crud.get_temperature_list(db=db)
    return crud.get_temperature_for_city(db=db, city_id=city_id)