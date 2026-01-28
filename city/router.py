from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from city.crud import get_all_cities, update_city, delete_city, get_city_by_id, \
    create_city
from city.exceptions import InvalidCityIdException
from db.session import get_db
from city.schema import City, CityCreate

router = APIRouter()


@router.get("/cities/", response_model=List[City])
def get_cities(db: Annotated[Session, Depends(get_db)]):
    return get_all_cities(db)


@router.post("/cities/", response_model=City)
def add_new_city(db: Annotated[Session, Depends(get_db)], city_data: CityCreate):
    return create_city(db=db, city_data=city_data)


@router.get("/cities/{city_id}", response_model=City)
def get_city(city_id: int, db: Annotated[Session, Depends(get_db)]):
    city = get_city_by_id(db, city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@router.put("/cities/{city_id}", response_model=City)
def update_city(city_id: int,
             db: Annotated[Session, Depends(get_db)],
             city_data: CityCreate):
    try:
        return update_city(db=db, city_id=city_id,
                                     city_data=city_data)
    except InvalidCityIdException as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/cities/{city_id}", response_model=City)
def delete_city_by_id(city_id: int, db: Annotated[Session, Depends(get_db)]):
    try:
        return delete_city(db=db, city_id=city_id)
    except InvalidCityIdException as e:
        raise HTTPException(status_code=404, detail=str(e))
