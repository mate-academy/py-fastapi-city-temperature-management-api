from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from api.deps import get_db
from crud import cities as crud
from schemas.city import CityCreate, CityRead, CityUpdate

router = APIRouter(prefix="/cities", tags=["cities"])

@router.post("", response_model=CityRead, status_code=201)
def create_city(city_in: CityCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_city(db, city_in)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400,
                            detail="City with this name already exists")

@router.get("", response_model=list[CityRead])
def get_cities(db: Session = Depends(get_db)):
    return crud.list_cities(db)

@router.get("/{city_id}", response_model=CityRead)
def get_city(city_id: int, db: Session = Depends(get_db)):
    city = crud.get_city(db, city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city

@router.put("/{city_id}", response_model=CityRead)
def update_city(city_id: int, city_in: CityUpdate,
                db: Session = Depends(get_db)):
    city = crud.get_city(db, city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    try:
        return crud.update_city(db, city, city_in)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400,
                            detail="City with this name already exists")

@router.delete("/{city_id}", status_code=204)
def delete_city(city_id: int, db: Session = Depends(get_db)):
    city = crud.get_city(db, city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    crud.delete_city(db, city)
