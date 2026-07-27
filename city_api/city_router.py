from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from dependencies import get_db
from city_api import city_schemas, city_crud

router = APIRouter()

@router.post("/cities/", response_model=city_schemas.CityCreate)
def create_new_city(
    new_city: city_schemas.CityCreate,
    db: Session = Depends(get_db)
):
    db_new_city = city_crud.get_city_by_name(db=db, name=new_city.name)
    if db_new_city:
        raise HTTPException(
            status_code=404,
            detail="City already exist!"
        )
    return city_crud.city_create(db=db, city=new_city)


@router.get("/cities/", response_model=list[city_schemas.City])
def get_city_list(
    limit: int | None = None,
    skip: int | None = None,
    db: Session = Depends(get_db)
):
    return city_crud.get_city_list(db=db, skip=skip, limit=limit)


@router.get("/cities/{city_id}", response_model=city_schemas.City)
def get_city_by_id(
    city_id: int,
    db: Session = Depends(get_db)
):
    db_city = city_crud.get_city_by_id(db=db, id=city_id)
    if db_city is None:
        raise HTTPException(
            status_code=404,
            detail="City not found!"
        )
    return db_city


@router.put("/cities/{city_id}", response_model=city_schemas.City)
def update_city_by_id(
    city_id: int,
    new_values: city_schemas.CityUpdate,
    db: Session = Depends(get_db)
):
    db_city = city_crud.get_city_by_id(db=db, id=city_id)
    if db_city is None:
        raise HTTPException(
            status_code=404,
            detail="City not found!"
        )
    return city_crud.update_city_details(db=db, city=db_city, new_values=new_values)


@router.delete("/cities/{city_id}", response_model=city_schemas.CityDeleteMessage)
def delete_city_by_id(
    city_id: int,
    db: Session = Depends(get_db)
):
    db_city = city_crud.get_city_by_id(db=db, id=city_id)
    if db_city is None:
        raise HTTPException(
            status_code=404,
            detail="City not found!"
        )
    return city_crud.delete_city(db=db, city=db_city)
