from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, schemas
from .deps import get_db

router = APIRouter(prefix="/cities", tags=["Cities"])

@router.post("/", response_model=schemas.CityRead)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    return crud.create_city(db, city)

@router.get("/", response_model=list[schemas.CityRead])
def read_cities(db: Session = Depends(get_db)):
    return crud.get_cities(db)

@router.delete("/{city_id}")
def delete_city(city_id: int, db: Session = Depends(get_db)):
    if not crud.delete_city(db, city_id):
        raise HTTPException(status_code=404, detail="City not found")
    return {"detail": "City deleted"}
