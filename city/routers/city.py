from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from city.crud import create_city_crud, get_all_cities, get_city_or_404, update_city_by_id, delete_city_crud
from city.schemas import CityResponse, CityCreate, CityUpdate
from dependencies import get_db

router = APIRouter()


@router.post("/cities", response_model=CityResponse)
def create_city(city_data: CityCreate, db: Session = Depends(get_db)):
    return create_city_crud(db, city_data)


@router.get("/cities", response_model=list[CityResponse])
def get_cities(db: Session = Depends(get_db)):
     return get_all_cities(db)


@router.get("/cities/{city_id}", response_model=CityResponse)
def get_city_by_id(city_id: int, db: Session = Depends(get_db)):
    return get_city_or_404(db, city_id)


@router.put("/cities/{city_id}", response_model=CityResponse)
def update_city(city_id: int, update_data: CityUpdate, db: Session = Depends(get_db)):
    return update_city_by_id(db, city_id, update_data)


@router.delete("/cities/{city_id}", status_code=200)
def delete_city(city_id: int, db: Session = Depends(get_db)):
    return delete_city_crud(db, city_id)
