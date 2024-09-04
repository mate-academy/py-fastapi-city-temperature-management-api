from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from city import crud
from city.schemas import City, CityList
from dependencies import get_db

router = APIRouter()


@router.get("/cities/", response_model=list[CityList])
def get_cities(db: Session = Depends(get_db)):
    return crud.get_all_cities(db=db)


@router.post("/cities/", response_model=CityList)
def create_city(city: City, db: Session = Depends(get_db)):
    return crud.create_city(db=db, city=city)


@router.get("/cities/{city_id}/", response_model=CityList)
def retrieve_city(city_id: int, db: Session = Depends(get_db)):
    return crud.retrieve_city(db=db, city_id=city_id)


@router.put("/cities/{city_id}/", response_model=CityList)
def update_city(city: City, city_id: int, db: Session = Depends(get_db)):
    return crud.update_city(db=db, city_id=city_id, city=city)


@router.delete("/cities/{city_id}/")
def delete_city(city_id: int, db: Session = Depends(get_db)):
    crud.delete_city(db=db, city_id=city_id)
