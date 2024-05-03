from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from city import crud
from city.crud import update_city_by_id, delete_city_by_id, get_all_cities
from city.models import CityModel
from city.schemas import CitySchema

from dependencies import get_db

router = APIRouter()


@router.post("/cities/", response_model=CityModel)
def create_city_endpoint(city: CitySchema, db: Session = Depends(get_db)):
    db_city = crud.get_city_by_id(db=db, city_id=city.id)

    if db_city:
        raise HTTPException(
            status_code=400, detail="City already exists"
        )

    return crud.create_city(db=db, city=city)


@router.get("/cities/", response_model=list[CityModel])
def get_cities_endpoint(db: Session = Depends(get_db)):
    return get_all_cities(db=db)


@router.get("/cities/{city_id}/", response_model=CityModel)
def get_city_by_id(city_id: int, db: Session = Depends(get_db)):
    city_db = get_city_by_id(city_id=city_id, db=db)

    if city_db is None:
        raise HTTPException(status_code=404, detail="City not found")

    return city_db


@router.put("/cities/{city_id}/", response_model=CityModel)
def update_city_endpoint(city_id: int, city: CitySchema, db: Session = Depends(get_db)):
    return update_city_by_id(city_id=city_id, city=city, db=db)


@router.delete("/cities/{city_id}/", response_model=CityModel)
def delete_city_by_id_endpoint(city_id: int, db: Session = Depends(get_db)):
    return delete_city_by_id(db=db, city_id=city_id)
