from fastapi import APIRouter, Depends, HTTPException
from database import SessionLocal

from city import schemas
from city import crud
from city.utils import get_city_by_name

from dependencies import get_db, CommonsDependencies


router = APIRouter()

@router.get("/cities/", response_model=list[schemas.CityRead])
def get_city_list(commons: CommonsDependencies, db: SessionLocal = Depends(get_db)):
    return crud.get_city_list(db, commons)


@router.post("/cities/", response_model=schemas.CityRead)
def create_city(city: schemas.CityCreate, db: SessionLocal = Depends(get_db)):
    if get_city_by_name(db, city.name):
        raise HTTPException(
            status_code=400,
            detail=f"City with name {city.name} already exists"
        )

    return crud.create_city(db, city)


@router.delete("/city/{city_id}/", response_model=schemas.CityRead)
def delete_city(city_id: int, db: SessionLocal = Depends(get_db)):
    city_to_delete = crud.delete_city(db, city_id)

    if not city_to_delete:
        raise HTTPException(
            status_code=404,
            detail=f"City with id {city_id} not found"
        )

    return city_to_delete


@router.get("/city/{city_id}/", response_model=schemas.CityRead)
def get_city_detail(city_id: int, db: SessionLocal = Depends(get_db)):
    city = crud.get_city_detail(db, city_id)

    if not city:
        raise HTTPException(status_code=404, detail=f"City with id {city_id} not found")

    return city


@router.put("/city/{city_id}/", response_model=schemas.CityRead)
def update_city(city_id: int, city: schemas.CityUpdate, db: SessionLocal = Depends(get_db)):
    updated_city = crud.update_city(db, city_id, city)

    if not updated_city:
        raise HTTPException(status_code=404, detail=f"City with id {city_id} not found")

    return updated_city
