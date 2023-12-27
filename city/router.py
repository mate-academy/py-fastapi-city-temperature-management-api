from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from dependencies import get_db
from city import schemas, crud

router = APIRouter()


@router.get("/cities/", response_model=list[schemas.City])
def get_cities(skip: int = 0, limit: int = 5, db: Session = Depends(get_db)):
    return crud.get_all_cities(db, skip=skip, limit=limit)


@router.get("/cities/{city_id}", response_model=schemas.City)
def get_city(city_id: int, db: Session = Depends(get_db)):
    db_city = crud.get_city_by_id(db, city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


@router.post("/cities/", response_model=schemas.City)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    db_city = crud.get_city_by_name(db=db, name=city.name)
    if db_city:
        raise HTTPException(
            status_code=400, detail="Such name for City already exists"
        )
    return crud.create_city(db=db, city=city)


@router.put("/cities/{city_id}", response_model=schemas.City)
def update_city(city_id: int, city: schemas.CityCreate, db: Session = Depends(get_db)):
    db_city = crud.update_city(db, city_id, city)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


@router.delete("/cities/{city_id}", response_model=schemas.City)
def delete_city(city_id: int, db: Session = Depends(get_db)):
    db_city = crud.delete_city(db, city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city
