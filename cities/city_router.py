from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from cities import schemas, crud
import models
from dependencies import get_db

router = APIRouter()


@router.get("/cities/")
def read_cities(db: Session = Depends(get_db)):
    return crud.get_cities(db=db)


@router.post("/cities/", response_model=schemas.City)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    return crud.create_city(db=db, city=city)


@router.delete("/cities/{city_id}")
def delete_city(city_id: int, db: Session = Depends(get_db)):
    db_city = db.query(models.City).filter(models.City.id == city_id).first()
    if db_city is None:
        raise HTTPException(status_code=400, detail={"error": f"No such city with id {city_id}"})
    return crud.delete_city(db=db, city_id=city_id)
