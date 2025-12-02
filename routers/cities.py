from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from session_db import db_session
import crud.cities
import schemas.cities


router = APIRouter()


@router.get("/cities", response_model=list[schemas.cities.GetCity])
def get_cities_all(db: Session = Depends(db_session)):
    return crud.cities.get_all_cities(db)


@router.get("/cities/{city_id}", response_model=schemas.cities.GetCity)
def get_cities_id(city_id: int, db: Session = Depends(db_session)):
    db_city_by_id =  crud.cities.get_city_by_id(db, city_id)
    if not db_city_by_id:
        raise HTTPException(
            status_code=404,
            detail= f"City is {city_id} not found!"
        )
    return db_city_by_id


@router.post("/cities", response_model=schemas.cities.GetCity)
def create_city(create_cities: schemas.cities.CreateCity ,db: Session = Depends(db_session)):
    db_city_name = crud.cities.get_name_city(db, create_cities.name)
    if db_city_name:
        raise HTTPException(
            status_code=400,
            detail="City exists"
        )
    return crud.cities.create_city(db, create_cities)


@router.delete("/cities/{city_id}", response_model=schemas.cities.StatusMessage)
def delete_city(city_id: int, db: Session = Depends(db_session)):
    db_delete_city = crud.cities.get_city_by_id(db, city_id)
    if not db_delete_city:
        raise HTTPException(
            status_code=404,
            detail= f"City is {city_id} not found!"
        )
    db.delete(db_delete_city)
    db.commit()
    return {"message": f"Item {city_id} deleted successfully"}



@router.put("/cities/{city_id}", response_model=schemas.cities.GetCity)
def update_city(city_id: int, update_cities: schemas.cities.CityUpdate, db: Session = Depends(db_session)):
    db_city = crud.cities.get_city_by_id(db, city_id)
    if not db_city:
        raise HTTPException(
            status_code=404,
            detail=f"City is {city_id} not found!"
        )
    update_cities = update_cities.model_dump(exclude_unset=True)
    for key, value in update_cities.items():
        setattr(db_city, key, value)

    db.commit()
    db.refresh(db_city)
    return db_city