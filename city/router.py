from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated

from city.crud import get_city_by_name, create_new_city, get_list_of_cities, get_city_by_id, update_city_by_id, \
    delete_city_by_id
from city.schemas import City, CityCreate
from dependencies import get_db, common_parameters

router = APIRouter()
CommonDeps = Annotated[dict, Depends(common_parameters)]

@router.post("/cities", response_model=City, tags=["City CRUD"])
async def create_city(city: CityCreate, db: Session = Depends(get_db)):
    db_city = get_city_by_name(db, city.name)
    if db_city:
        raise HTTPException(status_code=404, detail="City already exists")
    return create_new_city(db, city)


@router.get("/cities", response_model=list[City], tags=["City CRUD"])
async def get_cities(commons: CommonDeps):
    return get_list_of_cities(commons["db"], commons["skip"], commons["limit"])

@router.get("/cities/{city_id}", response_model=City, tags=["City CRUD"])
async def get_city(city_id: int, db: Session = Depends(get_db)):
    city_from_db = get_city_by_id(db, city_id)
    if city_from_db is None:
        raise HTTPException(status_code=404, detail="City not found")
    return city_from_db

@router.put("/cities/{city_id}", response_model=City, tags=["City CRUD"])
async def update_city(city_id: int, city: CityCreate, db: Session = Depends(get_db)):
    db_city = get_city_by_id(db, city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return update_city_by_id(db, city_id, city)

@router.delete("/cities/{city_id}", response_model=City, tags=["City CRUD"])
def delete_city(city_id: int, db: Session = Depends(get_db)):
    db_city = get_city_by_id(db, city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return delete_city_by_id(db, city_id)