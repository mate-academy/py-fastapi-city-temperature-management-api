from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session


from database import get_db
from schemas.city import CityCreate, CityRead, CityUpdate
import crud.city as crud_city

router = APIRouter()

@router.post("/", response_model=CityRead)
def create_city(city: CityCreate, db: Session=Depends(get_db)):
    return crud_city.create_city(db, city)

@router.get("/", response_model=list[CityRead])
def read_cities(db: Session = Depends(get_db)):
    return crud_city.get_cities(db)

@router.get("/{city_id}", response_model=CityRead)
def read_single_city(city_id: int, db: Session = Depends(get_db)):
    return crud_city.get_city(db, city_id)

@router.put("/{city_id}", response_model=CityRead)
def update_city(city_id: int, city: CityUpdate, db: Session = Depends(get_db)):
    return crud_city.update_city(db, city_id, city)

@router.delete("/{city_id}")
def delete_city(city_id: int, db: Session = Depends(get_db)):
    return crud_city.delete_city(db, city_id)
