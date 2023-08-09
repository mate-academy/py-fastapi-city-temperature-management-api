from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from city import crud, schemas
import models
from dependencies import get_db

router = APIRouter()


@router.post("/cities", response_model=schemas.CityList)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    db_city = crud.get_city_by_name(db, name=city.name)
    if db_city:
        raise HTTPException(status_code=400, detail="City already exists")
    return crud.create_city(db=db, city=city)


@router.get("/cities", response_model=list[schemas.CityList])
def read_cities(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    cities = crud.get_cities(db, skip=skip, limit=limit)
    return cities


@router.get("/cities/{city_id}", response_model=schemas.CityList)
def read_city(city_id: int, db: Session = Depends(get_db)):
    city = crud.get_city(db, city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@router.put("/cities/{city_id}", response_model=schemas.CityList)
def update_city(city_id: int, city: schemas.CityCreate, db: Session = Depends(get_db)):
    db_city = crud.get_city_by_id(city_id=city_id, db=db)
    if db_city is None:
        raise HTTPException(status_code=400, detail={"error": "City not found"})
    updated_city = crud.update_city(db=db, city_id=city_id, city=city)
    return updated_city


@router.delete("/cities/{city_id}")
def delete_city(city_id: int, db: Session = Depends(get_db)):
    db_city = crud.get_city_by_id(city_id=city_id, db=db)
    if db_city is None:
        raise HTTPException(status_code=400, detail={"error": "City not found"})
    return {"message": crud.delete_city(db=db, city_id=city_id)}
