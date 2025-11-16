from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import get_db
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/cities", tags=["cities"])

@router.post("/", response_model=schemas.City, status_code=201)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    existing = crud.get_city_by_name(db, city.name)
    if existing:
        raise HTTPException(status_code=409, detail="City with this name already exists")
    try:
        return crud.create_city(db, city)
    except IntegrityError:
        raise HTTPException(status_code=409, detail="City with this name already exists")

@router.get("/", response_model=list[schemas.City])
def list_cities(db: Session = Depends(get_db)):
    return crud.get_cities(db)

@router.get("/{city_id}", response_model=schemas.City)
def get_city(city_id: int, db: Session = Depends(get_db)):
    city = crud.get_city(db, city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city

@router.put("/{city_id}", response_model=schemas.City)
def put_city(city_id: int, city_update: schemas.CityCreate, db: Session = Depends(get_db)):
    updated = crud.update_city(db, city_id, city_update.dict(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="City not found")
    return updated

@router.delete("/{city_id}", response_model=schemas.City)
def delete_city(city_id: int, db: Session = Depends(get_db)):
    city = crud.delete_city(db, city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city
