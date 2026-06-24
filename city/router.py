from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from city import crud, schemas
from dependencies import get_db

router = APIRouter(prefix="/cities", tags=["cities"])


@router.post("/", response_model=schemas.City)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    return crud.create_city(db, city)


@router.get("/", response_model=list[schemas.City])
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
    db_city = crud.update_city(db, city_id, city)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


@router.delete("/{city_id}")
def delete_city(city_id: int, db: Session = Depends(get_db)):
    db_city = crud.delete_city(db, city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return {"ok": True}
