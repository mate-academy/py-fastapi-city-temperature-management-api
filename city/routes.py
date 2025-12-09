from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from city.crud import create_city, get_cities, get_city_by_id, update_city, delete_city_from_db
from city.schemas import CityCreateSchema, CitySchema, CityUpdateSchema
from dependencies import get_db

router = APIRouter()


@router.post("/", response_model=CitySchema)
def add_city(data: CityCreateSchema, db: Session = Depends(get_db)):
    result = create_city(data, db)
    return result


@router.get("/", response_model=list[CitySchema])
def list_cities(db: Session = Depends(get_db)):
    result = get_cities(db)
    return result


@router.get("/{city_id}", response_model=CitySchema)
def get_city(city_id: int, db: Session = Depends(get_db)):
    result = get_city_by_id(city_id, db)
    return result


@router.put("/{city_id}", response_model=CitySchema)
def edit_city(data: CityUpdateSchema, db: Session = Depends(get_db)):
    result = update_city(data, db)
    return result


@router.delete("/{city_id}", response_model=CitySchema)
def delete_city(city_id: int, db: Session = Depends(get_db)):
    result = delete_city_from_db(city_id, db)
    return result
