from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import SessionLocal
from .. import crud, schemas

router = APIRouter(prefix="/cities", tags=["cities"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("", response_model=schemas.CityRead, status_code=201)
def create_city(city_in: schemas.CityCreate, db: Session = Depends(get_db)):
    if crud.get_city_by_name(db, city_in.name):
        raise HTTPException(status_code=400, detail="City with this name already exists.")
    return crud.create_city(db, city_in)


@router.get("", response_model=list[schemas.CityRead])
def list_cities(db: Session = Depends(get_db)):
    return crud.list_cities(db)


@router.get("/{city_id}", response_model=schemas.CityRead)
def get_city(city_id: int, db: Session = Depends(get_db)):
    city = crud.get_city(db, city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found.")
    return city


@router.put("/{city_id}", response_model=schemas.CityRead)
def update_city(city_id: int, city_in: schemas.CityUpdate, db: Session = Depends(get_db)):
    city = crud.get_city(db, city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found.")

    if city_in.name and city_in.name != city.name:
        if crud.get_city_by_name(db, city_in.name):
            raise HTTPException(status_code=400, detail="City with this name already exists.")

    return crud.update_city(db, city, city_in)


@router.delete("/{city_id}", status_code=204)
def delete_city(city_id: int, db: Session = Depends(get_db)):
    city = crud.get_city(db, city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found.")
    crud.delete_city(db, city)
    return None
