from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.city import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/cities", tags=["cities"])


@router.post("", response_model=schemas.City, status_code=status.HTTP_201_CREATED)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    if crud.get_city_by_name(db, name=city.name):
        raise HTTPException(status_code=400, detail="City with this name already exists")
    return crud.create_city(db, city)


@router.get("", response_model=list[schemas.City])
def read_cities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_cities(db, skip=skip, limit=limit)


@router.get("/{city_id}", response_model=schemas.City)
def read_city(city_id: int, db: Session = Depends(get_db)):
    db_city = crud.get_city(db, city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


@router.put("/{city_id}", response_model=schemas.City)
def update_city(city_id: int, city: schemas.CityCreate, db: Session = Depends(get_db)):
    db_city = crud.get_city(db, city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    existing = crud.get_city_by_name(db, name=city.name)
    if existing and existing.id != city_id:
        raise HTTPException(status_code=400, detail="City with this name already exists")
    return crud.update_city(db, db_city, city)


@router.delete("/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_city(city_id: int, db: Session = Depends(get_db)):
    db_city = crud.get_city(db, city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    crud.delete_city(db, db_city)
